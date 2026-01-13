# React 클래스형 컴포넌트로 배우는 WebSocket vs Socket.IO

이 가이드는 React의 **클래스형 컴포넌트(Class Components)**를 사용하여 **Native WebSocket**과 **Socket.IO**를 구현하는 방법과 그 차이점을 설명합니다.

## 1. 프로젝트 구조 및 실행

### 구조
- **Server (`/server`)**: Node.js 백엔드
  - `src/native.ts`: 순수 WebSocket 서버 (Port 8080)
  - `src/socketio.ts`: Socket.IO 서버 (Port 3000)
- **Client (`/socket-study`)**: React 프론트엔드 (클래스형 컴포넌트)

### 실행 방법
3개의 터미널에서 각각 실행합니다:
1. **WebSocket 서버**: `cd server && npx ts-node src/native.ts`
2. **Socket.IO 서버**: `cd server && npx ts-node src/socketio.ts`
3. **React 앱**: `cd socket-study && npm run dev`

---

## 2. React 클래스형 컴포넌트의 생명주기 (Lifecycle)

실시간 통신에서 가장 중요한 것은 **"언제 연결하고, 언제 끊을 것인가?"**입니다. 클래스형 컴포넌트에서는 다음 두 메서드가 이 역할을 담당합니다.

### `componentDidMount()`
- **역할**: 컴포넌트가 화면에 나타난(마운트된) 직후 한 번 실행됩니다.
- **용도**: 외부 API 호출, 타이머 설정, **WebSocket/Socket.IO 연결 초기화**에 적합합니다.
- **코드 예시**:
  ```typescript
  componentDidMount() {
    this.socket = io('http://localhost:3000');
    // 이벤트 리스너 등록
    this.socket.on('connect', () => { ... });
  }
  ```

### `componentWillUnmount()`
- **역할**: 컴포넌트가 화면에서 사라지기(언마운트) 직전에 실행됩니다.
- **용도**: 메모리 누수를 방지하기 위해 **연결 종료**, 타이머 해제 등의 정리(Clean-up) 작업을 합니다.
- **코드 예시**:
  ```typescript
  componentWillUnmount() {
    if (this.socket) {
      this.socket.disconnect(); // 연결 해제
    }
  }
  ```

---

## 3. 구현 상세 비교

### A. Native WebSocket (`NativeChat.tsx`)

브라우저 내장 API인 `WebSocket`을 직접 사용합니다.

1. **연결 생성**:
   `new WebSocket('ws://localhost:8080')`을 통해 TCP 연결을 엽니다.
2. **이벤트 처리**:
   - `onopen`: 연결 성공 시 호출.
   - `onmessage`: 서버에서 메시지 도착 시 호출. `event.data`에 실제 데이터가 들어있습니다.
   - `onclose`: 연결 종료 시 호출.
3. **상태 업데이트 주의사항**:
   ```typescript
   // 기존 메시지 배열에 새 메시지를 추가할 때
   this.setState(prevState => ({
     messages: [...prevState.messages, event.data]
   }));
   ```
   *`this.state.messages`를 직접 참조하지 않고 `prevState`를 사용하는 것이 안전합니다.*

### B. Socket.IO (`SocketIOChat.tsx`)

`socket.io-client` 라이브러리를 사용합니다.

1. **연결 생성**:
   `io('http://localhost:3000')` 함수를 호출합니다. (프로토콜이 `ws://`가 아닌 `http://`임에 주의)
2. **이벤트 처리**:
   - WebSocket과 달리 **이벤트 이름('chat message')**을 직접 지정할 수 있어 직관적입니다.
   - 데이터 포맷팅(JSON 파싱 등)을 라이브러리가 자동으로 처리해줍니다.
   ```typescript
   this.socket.on('chat message', (msg) => {
     // msg는 이미 문자열 또는 객체로 변환되어 있음
     this.setState(prevState => ({
       messages: [...prevState.messages, msg]
     }));
   });
   ```

---

## 4. 핵심 차이점 요약

| 특징 | Native WebSocket | Socket.IO |
| :--- | :--- | :--- |
| **프로토콜** | 표준 WebSocket (ws://) | WebSocket + HTTP Long Polling (자체 프로토콜) |
| **연결 방식** | `new WebSocket()` | `io()` |
| **이벤트 명** | 오직 `message` | 사용자 정의 가능 (`chat`, `alert` 등) |
| **재접속** | 직접 구현 필요 | **자동 지원** |
| **룸(Room)** | 직접 구현 필요 | 기본 지원 (`join`, `to` 등) |

## 5. 학습 포인트
- **State 관리**: 배열(`messages`)을 업데이트할 때 불변성을 유지하며 `spread operator(...)`를 사용하는 패턴을 익히세요.
- **This Binding**: 클래스 메서드(`sendMessage` 등)를 화살표 함수(`sendMessage = () => { ... }`)로 정의하면, 별도의 `bind` 작업 없이 `this`에 접근할 수 있어 편리합니다.
- **Cleanup**: `componentWillUnmount`에서 연결을 닫지 않으면, 컴포넌트가 사라져도 백그라운드에서 연결이 유지되어 리소스가 낭비될 수 있습니다.
