import os
import subprocess
import time
import random
import logging
import json
import asyncio
from typing import TypedDict, Annotated, List, Literal, Optional, Dict, Any
from contextlib import AsyncExitStack

from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, AIMessage, ToolMessage
from langchain_core.tools import tool
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langchain_google_genai import ChatGoogleGenerativeAI
from google.api_core.exceptions import ResourceExhausted

# google.genai 패키지의 AFC 제한을 해제 (Monkey Patch)
try:
    import google.genai._extra_utils
    # 기본값을 충분히 크게 설정하여 제한에 걸리지 않게 함
    google.genai._extra_utils._DEFAULT_MAX_REMOTE_CALLS_AFC = 10000
except ImportError:
    pass
except Exception as e:
    logging.warning(f"google.genai AFC 제한 수정 실패: {e}")

# MCP 관련 임포트
try:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    # langchain-mcp-adapters가 설치되어 있다고 가정하고 도구 변환 기능 사용
    # 만약 직접적인 load 함수가 없다면 아래와 같이 수동으로 변환할 수도 있음
    from langchain_mcp_adapters.tools import load_mcp_tools
except ImportError:
    # MCP 패키지가 없는 경우를 대비
    ClientSession = None
    StdioServerParameters = None
    stdio_client = None
    load_mcp_tools = None


# --- 설정 (Configuration) ---
class Config:
    # 사용할 LLM 모델 이름 (Gemini 모델 유지)
    MODEL_NAME = "gemini-2.5-flash-lite"
    # 최대 재시도 횟수
    MAX_RETRIES = 5
    # 기본 대기 시간 (초)
    RATE_LIMIT_DELAY = 2.0
    # 로그 레벨 설정
    LOG_LEVEL = logging.INFO

    # 모델 호출 횟수 제한 (사실상 해제)
    MAX_REMOTE_CALLS = 999999

    # 도구 호출 무한 루프 방지
    RECURSION_LIMIT = 50
    
    # MCP 설정 파일 경로
    MCP_CONFIG_PATH = "config/mcp.json"

    # 시스템 프롬프트
    SYSTEM_PROMPT = """당신은 숙련된 파이썬 개발자이자 QA 전문가입니다.
당신의 목표는 코드 베이스를 분석하고, 문제를 식별하며, **적극적으로 코드를 수정하여 개선하는 것**입니다.
또한 사용자가 특정 작업(번역, 리팩토링, 기능 추가 등)을 지시하면, 현재 코드에 문제가 없더라도 **반드시 지시사항을 이행**해야 합니다.

지침:
1. **도구 사용 필수 (Mandatory)**: 코드를 작성하거나 수정할 때는 **절대로** 대화창(Text Response)에 코드를 출력하지 마세요. **반드시** `write_code_to_file`, `replace_code_in_file` 등의 도구를 호출하여 파일 시스템에 직접 반영해야 합니다. 도구를 호출하지 않으면 작업은 실패한 것입니다.
2. **지시 이행 우선**: 사용자가 "새 파일에 작성하라", "번역하라" 등의 구체적인 지시를 내리면, 자신의 판단보다 이를 우선시하여 수행하세요.
3. **단계별 추론 (CoT)**: 행동하기 전에 단계별로 생각하세요. (계획 -> 분석 -> 수정 -> 검증)
4. **분석 우선**: 수정하기 전에 항상 프로젝트 구조를 확인하고 관련 파일을 읽으세요.
5. **안전성**: 코드를 변경하기 전에는 `request_user_approval` 도구를 사용하여 사용자의 승인을 요청하세요.
6. **언어**: 모든 분석, 설명, 리포트는 **한국어**로 작성하세요.
"""


# 로깅 설정
logging.basicConfig(
    level=Config.LOG_LEVEL, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# --- 상태 정의 (State Definition) ---
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    retry_count: int
    verification_count: int  # 검증 실패 횟수
    final_report: Optional[dict]


# --- 구조화된 출력 정의 (Structured Output) ---
class ReviewReport(BaseModel):
    status: Literal["SUCCESS", "FAILED", "PENDING_APPROVAL"]
    summary: str = Field(description="분석 및 변경 사항에 대한 전체 요약")
    changed_files: List[str] = Field(description="수정된 파일 목록")
    test_results: str = Field(description="테스트 실행 결과")


# --- 기존 도구 구현 (Tools) ---

@tool
def list_project_structure(root_path: str = ".", max_depth: int = 3) -> Dict[str, Any]:
    """
    [도구] 프로젝트의 파일 구조를 트리 형태로 반환합니다.
    어떤 파일들이 있는지 파악할 때 가장 먼저 사용해야 합니다.
    """
    ignore_dirs = {
        ".git",
        ".venv",
        "__pycache__",
        "node_modules",
        ".DS_Store",
        ".pytest_cache",
    }
    items = []
    try:
        abs_root = os.path.abspath(root_path)
        for root, dirs, files in os.walk(abs_root):
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            rel_path = os.path.relpath(root, abs_root)
            level = 0 if rel_path == "." else rel_path.count(os.sep) + 1

            if level > max_depth:
                continue

            items.append(
                {
                    "path": rel_path,
                    "type": "directory",
                    "name": os.path.basename(root) or root,
                }
            )

            if level < max_depth:
                for f in files:
                    if not f.startswith("."):
                        items.append(
                            {
                                "path": os.path.join(rel_path, f),
                                "type": "file",
                                "name": f,
                            }
                        )
        return {"status": "success", "items": items}
    except Exception as e:
        logger.error(f"구조 조회 중 에러 발생: {e}")
        return {"status": "error", "message": str(e)}


@tool
def search_codebase(query: str, root_path: str = ".") -> Dict[str, Any]:
    """
    [도구] 코드베이스 전체에서 특정 문자열이나 패턴(grep)을 검색합니다.
    """
    try:
        command = [
            "grep",
            "-rnI",
            "--exclude-dir=.git",
            "--exclude-dir=.venv",
            query,
            root_path,
        ]
        res = subprocess.run(command, capture_output=True, text=True)

        matches = []
        if res.returncode == 0 and res.stdout:
            for line in res.stdout.strip().split("\n"):
                if len(matches) >= 50:
                    break
                parts = line.split(":", 2)
                if len(parts) >= 3:
                    matches.append(
                        {
                            "file": parts[0],
                            "line": parts[1],
                            "content": parts[2].strip(),
                        }
                    )
            return {"status": "success", "matches": matches, "count": len(matches)}
        return {"status": "success", "matches": [], "message": "검색 결과가 없습니다."}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@tool
def read_file(file_path: str) -> Dict[str, Any]:
    """
    [도구] 파일의 전체 내용을 읽어서 반환합니다.
    """
    try:
        if not os.path.exists(file_path):
            return {
                "status": "error",
                "message": f"파일을 찾을 수 없습니다: {file_path}",
            }
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return {"status": "success", "file_path": file_path, "content": content}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@tool
def write_code_to_file(file_path: str, content: str) -> Dict[str, Any]:
    """
    [도구] 파일에 코드를 작성합니다. (새 파일 생성 또는 전체 덮어쓰기)
    """
    try:
        abs_path = os.path.abspath(file_path)
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)
        with open(abs_path, "w", encoding="utf-8") as f:
            f.write(content)
        logger.info(f"파일 작성 완료: {abs_path}")
        return {
            "status": "success",
            "file_path": abs_path,
            "message": "파일이 성공적으로 작성되었습니다.",
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


@tool
def apply_code_patch(
    file_path: str,
    start_line: int,
    end_line: int,
    new_code: str
) -> Dict[str, Any]:
    """
    [도구] 파일의 특정 라인 범위(start_line ~ end_line)를 새로운 코드로 교체합니다.
    """
    try:
        if not os.path.exists(file_path):
            return {
                "status": "error",
                "message": f"파일을 찾을 수 없습니다: {file_path}",
            }

        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        if start_line < 1 or end_line > len(lines) or start_line > end_line:
            return {
                "status": "error",
                "message": f"유효하지 않은 라인 범위입니다: {start_line}-{end_line}",
            }

        if not new_code.endswith("\n"):
            new_code += "\n"

        lines[start_line - 1 : end_line] = [new_code]

        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(lines)

        return {
            "status": "success",
            "message": f"{start_line}-{end_line}번 라인을 수정했습니다.",
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


@tool
def run_linter(file_path: str) -> Dict[str, Any]:
    """
    [도구] 파이썬 파일의 문법 오류를 검사합니다. (Syntax Check)
    """
    try:
        result = subprocess.run(
            ["python3", "-m", "py_compile", file_path],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            return {
                "status": "success",
                "message": "문법 검사 통과 (Syntax check passed).",
            }
        return {"status": "failed", "errors": result.stderr}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@tool
def execute_command(command: str) -> Dict[str, Any]:
    """
    [도구] 쉘 명령어를 실행하고 결과를 반환합니다.
    """
    try:
        res = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=60,
        )
        return {
            "status": "success" if res.returncode == 0 else "failed",
            "stdout": res.stdout,
            "stderr": res.stderr,
            "exit_code": res.returncode,
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


@tool
def request_user_approval(action_description: str) -> Dict[str, Any]:
    """
    [도구] 위험한 작업(파일 수정/삭제 등) 전에 사용자의 승인을 요청합니다.
    """
    return {"status": "APPROVAL_REQUIRED", "action": action_description}


# 기본 도구 리스트
base_tools = [
    list_project_structure,
    search_codebase,
    read_file,
    write_code_to_file,
    apply_code_patch,
    run_linter,
    execute_command,
    request_user_approval,
]


# --- MCP 관리자 (MCP Manager) ---
class MCPManager:
    def __init__(self):
        self.exit_stack = AsyncExitStack()
        self.mcp_tools = []

    async def initialize(self):
        """config/mcp.json을 읽어 MCP 서버들에 연결하고 도구를 로드합니다."""
        if not load_mcp_tools:
            logger.warning("langchain-mcp-adapters 또는 mcp가 설치되지 않아 MCP를 사용할 수 없습니다.")
            return

        if not os.path.exists(Config.MCP_CONFIG_PATH):
            logger.info(f"MCP 설정 파일이 없습니다: {Config.MCP_CONFIG_PATH}")
            return

        try:
            with open(Config.MCP_CONFIG_PATH, "r") as f:
                config = json.load(f)
            
            mcp_servers = config.get("mcpServers", {})
            for name, server_config in mcp_servers.items():
                logger.info(f"MCP 서버 연결 시도: {name}")
                command = server_config.get("command")
                args = server_config.get("args", [])
                env = server_config.get("env", None)
                
                if not command:
                    continue

                server_params = StdioServerParameters(
                    command=command,
                    args=args,
                    env=env
                )
                
                # stdio_client 컨텍스트 매니저 실행
                stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
                client = await self.exit_stack.enter_async_context(ClientSession(stdio_transport[0], stdio_transport[1]))
                await client.initialize()
                
                # 도구 로드
                tools = await load_mcp_tools(client)
                self.mcp_tools.extend(tools)
                logger.info(f"MCP 서버 '{name}'에서 {len(tools)}개의 도구를 로드했습니다.")
                
        except Exception as e:
            logger.error(f"MCP 초기화 중 오류 발생: {e}")

    async def cleanup(self):
        await self.exit_stack.aclose()


# --- LLM 관리자 (LLM Manager) ---
class LLMManager:
    def __init__(self):
        self.llm = None
        self.llm_with_tools = None

    def initialize(self, api_key: Optional[str] = None, extra_tools: List[Any] = None):
        if api_key:
            os.environ["GOOGLE_API_KEY"] = api_key

        if "GOOGLE_API_KEY" not in os.environ:
            logger.warning("GOOGLE_API_KEY가 환경 변수에 없습니다.")
            return

        try:
            # Gemini 모델 유지
            self.llm = ChatGoogleGenerativeAI(model=Config.MODEL_NAME, temperature=0)
            
            # 기본 도구 + MCP 도구
            all_tools = base_tools + (extra_tools if extra_tools else [])
            self.llm_with_tools = self.llm.bind_tools(all_tools)
            logger.info(f"LLM 초기화 완료: {Config.MODEL_NAME} (총 도구 수: {len(all_tools)})")
        except Exception as e:
            logger.error(f"LLM 초기화 실패: {e}")

    async def safe_invoke(
        self,
        model_type: Literal["base", "tools", "structured"],
        messages: List[BaseMessage],
        output_schema: Any = None,
    ):
        if not self.llm:
            raise Exception("LLM이 초기화되지 않았습니다. API Key를 확인해주세요.")

        model = self.llm
        if model_type == "tools":
            model = self.llm_with_tools
        elif model_type == "structured" and output_schema:
            model = self.llm.with_structured_output(output_schema)

        retry_delay = Config.RATE_LIMIT_DELAY
        for attempt in range(Config.MAX_RETRIES):
            try:
                # 비동기 invoke 사용
                return await model.ainvoke(messages)
            except ResourceExhausted:
                wait = retry_delay * (2**attempt) + random.uniform(0, 1)
                logger.warning(f"사용량 초과. {wait:.2f}초 후 재시도...")
                await asyncio.sleep(wait)
            except Exception as e:
                if "429" in str(e):
                    wait = retry_delay * (2**attempt)
                    logger.warning(f"속도 제한. {wait:.2f}초 후 재시도...")
                    await asyncio.sleep(wait)
                else:
                    raise e
        raise Exception("최대 재시도 횟수를 초과했습니다.")

mcp_manager = MCPManager()
llm_manager = LLMManager()


# --- 그래프 노드 정의 (Graph Nodes) ---
async def analyzer_node(state: AgentState):
    logger.info("분석가(Analyzer) 작동 중...")
    messages = state["messages"]
    if not any(isinstance(m, SystemMessage) for m in messages):
        messages = [SystemMessage(content=Config.SYSTEM_PROMPT)] + messages

    response = await llm_manager.safe_invoke("tools", messages)
    return {"messages": [response], "retry_count": state.get("retry_count", 0) + 1}


async def verifier_node(state: AgentState):
    """
    [검증 노드] 사용자의 요청이 파일 변경을 포함하는데도
    실제로 파일 변경 도구가 사용되지 않았는지 검사합니다.
    """
    logger.info("검증가(Verifier) 작동 중...")
    messages = state["messages"]
    
    # 1. 사용자의 마지막 요청 찾기
    user_requests = [m for m in messages if isinstance(m, HumanMessage) and "[시스템 경고]" not in m.content]
    if not user_requests:
        return {"messages": []}
    
    last_user_msg = user_requests[-1].content.lower()
    
    # 2. 파일 변경 의도 키워드 검사
    modification_keywords = [
        "파일", "작성", "생성", "만들", "수정", "변경", "저장", "추가", 
        "file", "create", "write", "make", "modify", "save", "add", "gen"
    ]
    has_modification_intent = any(k in last_user_msg for k in modification_keywords)
    
    if not has_modification_intent:
        return {"messages": []}

    # 3. 실제 파일 변경 도구 사용 여부 검사
    write_tools = ["write_code_to_file", "replace_code_in_file", "apply_code_patch"]
    tool_msgs = [m for m in messages if isinstance(m, ToolMessage)]
    
    has_write_action = any(tm.name in write_tools for tm in tool_msgs)
    
    # 4. 검증 실패 처리
    if has_modification_intent and not has_write_action:
        current_verification = state.get("verification_count", 0)
        
        if current_verification < 3:
            logger.warning(f"검증 실패: 파일 변경 요청이 있었으나 수행되지 않음 ({current_verification + 1}/3)")
            feedback = (
                "[시스템 경고] 사용자가 파일 생성/수정을 요청했지만, 당신은 아직 파일을 작성하는 도구(write_code_to_file 등)를 사용하지 않았습니다. "
                "텍스트로만 답변하지 말고 **반드시 도구를 호출**하여 파일을 실제로 저장하세요. 이미 작성했다면 도구 호출 기록이 있는지 확인하세요."
            )
            return {
                "messages": [HumanMessage(content=feedback)],
                "verification_count": current_verification + 1
            }
            
    return {"messages": []}


async def reporter_node(state: AgentState):
    logger.info("리포터(Reporter) 작동 중...")
    messages = state["messages"] + [
        HumanMessage(content="지금까지의 모든 작업을 바탕으로 최종 리포트를 한국어로 작성해줘.")
    ]
    report = await llm_manager.safe_invoke("structured", messages, ReviewReport)
    return {"final_report": report.model_dump()}


def should_continue(state: AgentState):
    last_message = state["messages"][-1]
    if state.get("retry_count", 0) >= Config.MAX_REMOTE_CALLS:
        return "verifier"
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    return "verifier"


def check_verification(state: AgentState):
    """
    검증 결과에 따라 분석가로 돌아갈지 리포터로 갈지 결정합니다.
    """
    last_message = state["messages"][-1]
    if isinstance(last_message, HumanMessage) and "[시스템 경고]" in last_message.content:
        return "analyzer"
    return "reporter"


# --- 메인 실행부 (Main Execution) ---
# ... imports ...
try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

# ... (existing imports) ...

# ... (existing code) ...

# --- 메인 실행부 (Main Execution) ---
async def async_main():
    # .env 파일 로드 (.env 파일이 있으면 환경변수로 로드)
    if load_dotenv:
        load_dotenv()
        if "GOOGLE_API_KEY" in os.environ:
            logger.info(".env 파일에서 환경 변수를 로드했습니다.")
    else:
        logger.warning("python-dotenv 패키지가 설치되지 않아 .env 파일을 로드하지 못했습니다.")

    if "GOOGLE_API_KEY" not in os.environ:
        key = input("🔑 Google API Key를 입력하세요: ").strip()
        if key:
            os.environ["GOOGLE_API_KEY"] = key
        else:
            print("API Key가 필요합니다.")
            return

    print("\n💬 에이전트 준비 (MCP 통합됨).")
    
    # MCP 초기화
    await mcp_manager.initialize()
    
    # LLM 초기화 (MCP 도구 포함)
    llm_manager.initialize(extra_tools=mcp_manager.mcp_tools)

    # 그래프 구성 (도구 리스트가 동적이므로 여기서 구성)
    workflow = StateGraph(AgentState)
    
    # 모든 도구 (기본 + MCP)에 에러 처리 설정 추가
    all_tools = base_tools + mcp_manager.mcp_tools
    for t in all_tools:
        t.handle_tool_error = True
    
    workflow.add_node("analyzer", analyzer_node)
    workflow.add_node("tools", ToolNode(all_tools))
    workflow.add_node("verifier", verifier_node)
    workflow.add_node("reporter", reporter_node)

    workflow.set_entry_point("analyzer")
    workflow.add_conditional_edges(
        "analyzer", should_continue, {"tools": "tools", "verifier": "verifier"}
    )
    workflow.add_edge("tools", "analyzer")
    workflow.add_conditional_edges(
        "verifier", check_verification, {"analyzer": "analyzer", "reporter": "reporter"}
    )
    workflow.add_edge("reporter", END)

    app = workflow.compile()

    user_request = input("\n📝 작업 입력:\n>>> ").strip()
    if not user_request:
        user_request = "프로젝트 구조를 분석해줘."

    current_messages = [HumanMessage(content=user_request)]

    try:
        # 비동기 스트리밍 실행 (중간 과정 출력)
        print("\n🚀 에이전트 작업 로그:")
        final_report = {}
        
        async for event in app.astream(
            {"messages": current_messages, "retry_count": 0, "verification_count": 0},
            config={"recursion_limit": Config.RECURSION_LIMIT},
        ):
            for key, value in event.items():
                if key == "reporter":
                    final_report = value.get("final_report", {})
                    continue

                if key == "verifier" and value.get("messages"):
                    for msg in value["messages"]:
                        if "[시스템 경고]" in msg.content:
                            print(f"\n[🚨 검증 실패]: {msg.content}")
                    continue

                if "messages" in value:
                    new_messages = value["messages"]
                    for msg in new_messages:
                        if isinstance(msg, AIMessage):
                            # AI의 생각이나 답변 출력
                            if msg.content:
                                print(f"\n[🤖 AI]: {msg.content}")
                            
                            # 도구 호출 정보 출력
                            if msg.tool_calls:
                                print("\n[🛠️ 도구 요청]:")
                                for tool_call in msg.tool_calls:
                                    print(f"  - 함수: {tool_call['name']}")
                                    print(f"  - 인자: {tool_call['args']}")

                        elif isinstance(msg, ToolMessage):
                            # 도구 실행 결과 출력
                            print(f"\n[⚡ 도구 결과 ({msg.name})]:")
                            content = str(msg.content)
                            if len(content) > 300:
                                print(f"{content[:300]}... (내용 생략됨)")
                            else:
                                print(f"{content}")

        # 최종 리포트 출력
        if final_report:
            print("\n=== 📋 최종 리포트 ===")
            print(f"상태: {final_report.get('status')}")
            print(f"요약: {final_report.get('summary')}")
            print(f"변경 파일: {final_report.get('changed_files')}")
            print("========================")
        else:
            print("\n⚠️ 최종 리포트가 생성되지 않았습니다.")
        
    except Exception as e:
        logger.error(f"실행 중 에러: {e}")
    finally:
        await mcp_manager.cleanup()

def main():
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
