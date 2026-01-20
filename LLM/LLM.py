import os
import sys

# 1. 환경 변수 로드 (최우선 순위)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# 2. LangSmith 설정을 코드 레벨에서 강제 (환경 변수가 없으면 기본값 사용)
# 이 코드는 다른 어떤 LangChain 모듈이 임포트되기 전에 실행되어야 함
if os.environ.get("LANGCHAIN_API_KEY"):
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_PROJECT"] = os.environ.get("LANGCHAIN_PROJECT", "Graph-Test")
    print(f"✅ LangSmith Tracing Enabled. Project: {os.environ['LANGCHAIN_PROJECT']}")
else:
    print("⚠️ LangSmith API Key not found. Tracing disabled.")

import subprocess
import time
import random
import logging
import json
import asyncio
from typing import TypedDict, Annotated, List, Literal, Optional, Dict, Any
from contextlib import AsyncExitStack

# LangChain 관련 임포트는 환경 변수 설정 후에
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, AIMessage, ToolMessage
from langchain_core.tools import tool
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver 
from langchain_google_genai import ChatGoogleGenerativeAI
from google.api_core.exceptions import ResourceExhausted

# --- [설정] ---
class Config:
    MODEL_NAME = "gemini-2.5-flash-lite"
    MAX_RETRIES = 5
    LOG_LEVEL = logging.INFO
    MCP_CONFIG_PATH = "config/mcp.json"

class SchemaWarningFilter(logging.Filter):
    def filter(self, record):
        msg = record.getMessage()
        if "additionalProperties" in msg or "$schema" in msg:
            return False
        return True

logging.basicConfig(level=Config.LOG_LEVEL, format="%(asctime)s - %(levelname)s - %(message)s")
for handler in logging.getLogger().handlers:
    handler.addFilter(SchemaWarningFilter())
logger = logging.getLogger(__name__)

try:
    import google.genai._extra_utils
    google.genai._extra_utils._DEFAULT_MAX_REMOTE_CALLS_AFC = 100
except ImportError:
    pass

# --- [상태 정의] ---
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    plan: List[str]
    current_step_index: int
    final_report: Optional[dict]

# --- [구조화된 출력] ---
class PlanSchema(BaseModel):
    steps: List[str] = Field(description="실행할 구체적인 단계별 계획 목록 (코드 작성 시 함수/클래스 단위로 세분화 필수)")

class ReviewReport(BaseModel):
    status: Literal["SUCCESS", "FAILED"]
    summary: str

# --- [도구 정의] ---
@tool
def log_reasoning(reasoning: str) -> str:
    """[도구] 현재 상태에 대한 분석, 생각, 또는 검토 내용을 기록합니다."""
    return f"분석 내용이 기록되었습니다: {reasoning[:100]}..."

@tool
def generate_code_draft(code_snippet: str, description: str) -> str:
    """[도구] 파일에 저장하기 전에 코드 초안을 생성하여 검토합니다.
    실제 파일 저장 도구가 아니며, 생성된 코드를 메모리에 잠시 보관하는 용도입니다.
    이 도구를 호출한 후, 반드시 write_code_to_file이나 append_to_file을 사용하여 파일에 저장해야 합니다."""
    return f"코드 초안 생성됨 ({len(code_snippet)} chars). 내용을 확인하고 이상 없으면 파일에 저장하세요."

@tool
def list_project_structure(root_path: str = ".", max_depth: int = 3) -> Dict[str, Any]:
    """[도구] 프로젝트 파일 구조 조회"""
    ignore_dirs = {".git", ".venv", "__pycache__", "node_modules", ".DS_Store", ".pytest_cache"}
    items = []
    try:
        abs_root = os.path.abspath(root_path)
        for root, dirs, files in os.walk(abs_root):
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            rel_path = os.path.relpath(root, abs_root)
            level = 0 if rel_path == "." else rel_path.count(os.sep) + 1
            if level > max_depth: continue
            items.append({"path": rel_path, "type": "directory", "name": os.path.basename(root) or root})
            if level < max_depth:
                for f in files:
                    if not f.startswith("."):
                        items.append({"path": os.path.join(rel_path, f), "type": "file", "name": f})
        return {"status": "success", "items": items}
    except Exception as e: return {"status": "error", "message": str(e)}

@tool
def read_file(file_path: str) -> Dict[str, Any]:
    """[도구] 파일 내용 읽기 (최대 10,000자)"""
    try:
        if not os.path.exists(file_path): return {"status": "error", "message": f"File not found: {file_path}"}
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return {"status": "success", "content": content[:10000] + ("...truncated" if len(content) > 10000 else "")}
    except Exception as e: return {"status": "error", "message": str(e)}

@tool
def write_code_to_file(file_path: str, content: str) -> Dict[str, Any]:
    """[도구] 파일 작성/덮어쓰기 (새 파일 생성 시 사용)"""
    try:
        abs_path = os.path.abspath(file_path)
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)
        with open(abs_path, "w", encoding="utf-8") as f:
            f.write(content)
        return {"status": "success", "message": f"Successfully wrote to {file_path}"}
    except Exception as e: return {"status": "error", "message": str(e)}

@tool
def append_to_file(file_path: str, content: str) -> Dict[str, Any]:
    """[도구] 기존 파일 끝에 내용 추가 (긴 코드를 나누어 작성할 때 사용)"""
    try:
        if not os.path.exists(file_path): return {"status": "error", "message": f"File not found: {file_path}. Use write_code_to_file to create it first."}
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(content)
        return {"status": "success", "message": f"Successfully appended to {file_path}"}
    except Exception as e: return {"status": "error", "message": str(e)}

@tool
def execute_command(command: str) -> Dict[str, Any]:
    """[도구] 쉘 명령어 실행"""
    try:
        res = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=60)
        return {"status": "success" if res.returncode == 0 else "failed", "stdout": res.stdout, "stderr": res.stderr}
    except Exception as e: return {"status": "error", "message": str(e)}

base_tools = [log_reasoning, generate_code_draft, list_project_structure, read_file, write_code_to_file, append_to_file, execute_command]

# --- [매니저 클래스] ---
class MCPManager:
    def __init__(self):
        self.exit_stack = AsyncExitStack()
        self.mcp_tools = []

    async def initialize(self):
        try:
            from mcp import ClientSession, StdioServerParameters
            from mcp.client.stdio import stdio_client
            from langchain_mcp_adapters.tools import load_mcp_tools
        except ImportError: return

        if not os.path.exists(Config.MCP_CONFIG_PATH): return
        try:
            with open(Config.MCP_CONFIG_PATH, "r") as f: config = json.load(f)
            for name, server_config in config.get("mcpServers", {}).items():
                if not server_config.get("command"): continue
                logger.info(f"Connecting to MCP: {name}")
                args = [os.path.expandvars(arg) for arg in server_config.get("args", [])]
                params = StdioServerParameters(command=server_config["command"], args=args, env=server_config.get("env"))
                transport = await self.exit_stack.enter_async_context(stdio_client(params))
                client = await self.exit_stack.enter_async_context(ClientSession(transport[0], transport[1]))
                await client.initialize()
                tools = await load_mcp_tools(client)
                self.mcp_tools.extend(tools)
        except Exception as e: logger.error(f"MCP Error: {e}")

    async def cleanup(self): await self.exit_stack.aclose()

class LLMManager:
    def __init__(self):
        self.llm = None
        self.llm_with_tools = None

    def initialize(self, extra_tools: List[Any] = None):
        if "GOOGLE_API_KEY" not in os.environ:
            logger.error("GOOGLE_API_KEY가 설정되지 않았습니다.")
            return
        self.llm = ChatGoogleGenerativeAI(model=Config.MODEL_NAME, temperature=0)
        all_tools = base_tools + (extra_tools if extra_tools else [])
        self.llm_with_tools = self.llm.bind_tools(all_tools)

    async def invoke(self, mode: str, messages: List[BaseMessage], schema=None, **kwargs):
        model = self.llm_with_tools if mode == "tools" else self.llm
        if mode == "structured": model = self.llm.with_structured_output(schema)
        return await model.ainvoke(messages, **kwargs)

mcp_manager = MCPManager()
llm_manager = LLMManager()

# --- [노드 정의] ---

async def planner_node(state: AgentState):
    logger.info("📅 [Planner] 계획 수립...")
    prompt = """당신은 수석 엔지니어입니다. 사용자의 요청을 해결하기 위한 체계적인 실행 계획을 수립하십시오.

[계획 수립 원칙]
1. **상황 파악:** 작업 환경(파일 구조 등)을 먼저 확인하는 단계를 포함하십시오.
2. **정보 수집:** 필요한 정보가 있다면 검색이나 파일 읽기를 통해 확보하는 단계를 포함하십시오.
3. **실행 및 결과물 생성:** 사용자의 요청이 구체적인 결과물(코드, 문서, 파일 등)을 요구한다면, 이를 실제로 생성하고 저장하는 단계를 반드시 포함하십시오.
4. **단계적 접근:** 복잡한 작업은 한 번에 처리하려 하지 말고, 논리적인 순서에 따라 여러 단계로 나누십시오. (예: 뼈대 작성 -> 세부 내용 추가 -> 검증)
"""
    messages = [SystemMessage(content=prompt)] + state["messages"]
    plan_data = await llm_manager.invoke("structured", messages, PlanSchema)
    plan_summary = "\n".join([f"{i+1}. {s}" for i, s in enumerate(plan_data.steps)])
    logger.info(f"📋 수립된 계획:\n{plan_summary}")
    
    return {
        "plan": plan_data.steps,
        "current_step_index": 0,
        "messages": [AIMessage(content=f"작업 계획을 수립했습니다:\n{plan_summary}")]
    }

async def executor_node(state: AgentState):
    idx = state["current_step_index"]
    plan = state["plan"]
    if idx >= len(plan): return {"messages": []}

    current_task = plan[idx]
    logger.info(f"⚙️ [Executor] 단계 {idx+1}/{len(plan)}: {current_task}")

    system_prompt = f"""당신은 실행가(Executor)입니다.
현재 단계: {current_task}

[행동 지침]
1. **도구 사용 필수:** 텍스트로 대답하는 대신, 현재 단계를 완수하기 위해 가장 적절한 도구를 호출하십시오.
2. **결과물 중심:** 사용자가 원하는 결과가 있다면, 단순한 계획이나 생각(`log_reasoning`)에 그치지 말고, `write_code_to_file` 등의 도구를 사용하여 실제 결과물을 만들어내십시오.
3. **문제 해결:** 도구 실행 중 오류(예: 파일 없음)가 발생하면, 즉시 멈추지 말고 상황을 파악(`list_project_structure` 등)하여 스스로 문제를 해결하십시오.
4. **미완성 금지:** 코드나 문서를 작성할 때는 `TODO`나 빈칸으로 남겨두지 말고, 문맥에 맞는 내용을 충실히 채워 넣으십시오.
"""
    messages = [SystemMessage(content=system_prompt)] + state["messages"]
    response = await llm_manager.invoke("tools", messages, tool_choice="any")
    return {"messages": [response]}

async def update_step_node(state: AgentState):
    return {"current_step_index": state["current_step_index"] + 1}

async def reporter_node(state: AgentState):
    logger.info("📝 [Reporter] 결과 보고...")
    messages = state["messages"] + [HumanMessage(content="작업 결과를 요약하여 보고해줘.")]
    report = await llm_manager.invoke("structured", messages, ReviewReport)
    return {"final_report": report.model_dump()}

# --- [그래프 구성] ---

async def async_main():
    if "GOOGLE_API_KEY" not in os.environ:
        os.environ["GOOGLE_API_KEY"] = input("🔑 Google API Key: ").strip()

    await mcp_manager.initialize()
    llm_manager.initialize(extra_tools=mcp_manager.mcp_tools)

    if not llm_manager.llm: return

    # 체크포인터 초기화
    memory = MemorySaver()

    workflow = StateGraph(AgentState)
    workflow.add_node("planner", planner_node)
    workflow.add_node("executor", executor_node)
    workflow.add_node("tools", ToolNode(base_tools + mcp_manager.mcp_tools))
    workflow.add_node("update_step", update_step_node)
    workflow.add_node("reporter", reporter_node)

    workflow.set_entry_point("planner")
    workflow.add_edge("planner", "executor")
    
    def route_executor(state):
        if state["messages"][-1].tool_calls: return "tools"
        return "update_step"

    workflow.add_conditional_edges("executor", route_executor, {"tools": "tools", "update_step": "update_step"})
    workflow.add_edge("tools", "update_step")
    workflow.add_conditional_edges("update_step", lambda x: "executor" if x["current_step_index"] < len(x["plan"]) else "reporter", {"executor": "executor", "reporter": "reporter"})
    workflow.add_edge("reporter", END)

    # 체크포인터를 포함하여 그래프 컴파일
    app = workflow.compile(checkpointer=memory)
    
    user_input = input(">>> 작업 지시: ") or "프로젝트를 분석해줘."
    
    # 현재 시간을 기반으로 동적 thread_id 생성 (식별 가능하게)
    current_time = time.strftime("%Y%m%d_%H%M%S")
    thread_id = f"session_{current_time}"
    logger.info(f"🚀 새로운 세션 시작 - Thread ID: {thread_id}")
    
    # 스레드 설정
    config = {"configurable": {"thread_id": thread_id}}

    async for event in app.astream({"messages": [HumanMessage(content=user_input)], "plan": [], "current_step_index": 0}, config=config):
        for key, value in event.items():
            if "messages" in value:
                m = value["messages"][-1]
                if isinstance(m, AIMessage):
                    if m.tool_calls:
                        for tc in m.tool_calls: print(f"🛠️ [Tool]: {tc['name']}")
                    elif m.content: print(f"🤖 [AI]: {m.content[:100]}...")
                elif isinstance(m, ToolMessage): print(f"⚡ [Result]: {str(m.content)[:50]}...")
            if "final_report" in value: print(f"\n✅ [완료]: {value['final_report']['summary']}")

    await mcp_manager.cleanup()

if __name__ == "__main__":
    asyncio.run(async_main())
