# ⚛️ React 실전 연습 로그 (260108)

이 문서는 `my-second-app` 프로젝트를 통해 학습한 React 실전 적용 과정을 기록합니다.

## 1. 프로젝트 초기화 (Cleanup)
Vite로 생성된 기본 코드를 정리하고 깨끗한 상태에서 시작합니다.

- **목표**: `src/App.tsx`와 `src/App.css`를 정리하여 나만의 앱을 만들 준비를 한다.
- **핵심**: 불필요한 import 제거, 기본 스타일 초기화.

## 2. 실습 계획 & Vue 비교

### Step 1: State 설계와 Two-way Binding
React에는 양방향 바인딩(`v-model`)이 없습니다. **단방향 데이터 흐름**을 지키기 위해 `value`(읽기)와 `onChange`(쓰기)를 수동으로 연결합니다.

**실제 코드:**
```tsx
const [inputValue, setInputValue] = useState<string>('');

<input 
  type="text" 
  value={inputValue}
  onChange={(e) => setInputValue(e.target.value)} 
/>
```

| 구분 | Vue (`v-model`) | React (`useState`) |
| :--- | :--- | :--- |
| **코드** | `<input v-model="text" />` | `<input value={text} onChange={e => setText(e.target.value)} />` |
| **특징** | 자동 동기화 | 명시적 제어 (함수가 실행되어야 값이 바뀜) |

---

### Step 2: 다중 Input 관리 (e.target.name)
입력 필드가 늘어날 때마다 `useState`를 계속 추가하는 것은 비효율적입니다. 객체 형태의 State 하나로 여러 입력을 관리하는 패턴을 사용합니다.

#### 1. 핵심 원리
- **HTML `name` 속성**: 각 input을 식별하는 키 역할을 합니다.
- **Computed Property Name (계산된 속성명)**: ES6 문법인 `[key]: value`를 사용하여 객체의 특정 키 값을 동적으로 업데이트합니다.
- **Spread Operator (`...`)**: 불변성을 지키기 위해 기존 객체를 먼저 복사합니다.

**실제 코드 패턴:**
```tsx
// 1. 객체로 상태 초기화
const [inputs, setInputs] = useState({
  username: '',
  email: '',
});

// 2. 비구조화 할당으로 값 추출 (편의성)
const { username, email } = inputs;

const onChange = (e: React.ChangeEvent<HTMLInputElement>) => {
  const { name, value } = e.target; // input의 name과 value 추출

  setInputs({
    ...inputs,       // 기존 객체 복사 (필수!)
    [name]: value,   // name 키에 해당하는 값만 덮어쓰기
  });
};

// 3. JSX 적용
return (
  <div>
    <input 
      name="username" 
      value={username} 
      onChange={onChange} 
      placeholder="이름"
    />
    <input 
      name="email" 
      value={email} 
      onChange={onChange} 
      placeholder="이메일"
    />
  </div>
);
```

| 구분 | 개별 관리 | 통합 관리 (Best Practice) |
| :--- | :--- | :--- |
| **State 개수** | 입력 필드 수만큼 (`useState` n개) | 1개 (객체) |
| **핸들러 함수** | 각각 따로 생성 | 1개로 재사용 가능 |
| **확장성** | 필드 추가 시 코드량 증가 | 필드만 추가하면 됨 |

---

### Step 3: 불변성(Immutability)과 리스트 렌더링
React는 상태의 **참조값**이 바뀌어야 업데이트를 감지합니다. 따라서 배열을 직접 수정(`push`)하지 않고 스프레드 연산자를 사용합니다.

**실제 코드:**
```tsx
const addTodo = () => {
  const newTodo = { id: Date.now(), text: inputValue };
  // 기존 배열을 복사하고 새 항목을 추가한 '새 배열'을 생성
  setTodos([...todos, newTodo]); 
};

// JSX에서의 반복문 (map)
<ul>
  {todos.map((todo) => (
    <li key={todo.id}>{todo.text}</li>
  ))}
</ul>
```

| 구분 | Vue (Mutable) | React (Immutable) |
| :--- | :--- | :--- |
| **추가** | `todos.push(newTodo)` | `setTodos([...todos, newTodo])` |
| **반복** | `<li v-for="todo in todos">` | `todos.map(todo => <li key={todo.id}>)` |

---

### Step 4: 조건부 스타일링 (Template Literals & Class Toggling)
특정 상태(예: 완료 여부, 활성화 상태)에 따라 UI의 스타일을 동적으로 바꿔야 할 때 템플릿 리터럴을 활용합니다.

#### 1. 핵심 패턴
백틱(`` ` ``)을 사용하여 기본 클래스와 조건부 클래스를 하나의 문자열로 합칩니다.

**실제 코드:**
```tsx
// 1. 상태 정의
const [isDone, setIsDone] = useState(false);

// 2. 템플릿 리터럴을 활용한 클래스 결합
// isDone이 true면 'completed' 클래스가 추가됨
<li className={`todo-item ${isDone ? 'completed' : ''}`}>
  {text}
  <button onClick={() => setIsDone(!isDone)}>토글</button>
</li>
```

#### 2. Vue와 비교

| 구분 | Vue (`:class`) | React (Template Literals) |
| :--- | :--- | :--- |
| **문법** | `:class="{ active: isActive }"` | `className={`item ${isActive ? 'active' : ''}`}` |
| **특징** | 객체 기반의 직관적인 문법 | 순수 JS 문자열 연산 (유연함) |

#### 💡 팁: 더 깔끔한 관리를 원한다면?
클래스가 너무 많아져서 문자열 연산이 복잡해질 경우, `clsx`나 `classnames` 같은 외부 라이브러리를 사용하면 Vue와 유사한 객체 기반 문법을 쓸 수 있습니다.
- 예: `className={clsx('item', { active: isActive, hidden: isHidden })}`

---

### Step 5: 데이터 삭제 (Filter)
배열에서 요소를 삭제할 때도 원본을 건드리는 `splice` 대신, 특정 항목을 제외한 새로운 배열을 반환하는 **`filter`**를 사용합니다.

**실제 코드:**
```tsx
const deleteTodo = (id: number) => {
  // 조건에 맞는 요소만 남긴 '새 배열'로 교체
  setTodos(todos.filter(todo => todo.id !== id));
};
```

| 구분 | Vue | React |
| :--- | :--- | :--- |
| **삭제** | `todos.splice(index, 1)` | `setTodos(todos.filter(t => t.id !== id))` |

---

### Step 6: 컴포넌트 분리와 Props 전달
자식이 부모의 상태를 변경해야 할 때, 부모는 함수 자체를 Props로 전달합니다.

**실제 코드 (자식 컴포넌트):**
```tsx
interface TodoItemProps {
  todo: Todo;
  onDelete: (id: number) => void; // 부모로부터 받은 함수 타입
}

function TodoItem({ todo, onDelete }: TodoItemProps) {
  return (
    <li>
      {todo.text}
      <button onClick={() => onDelete(todo.id)}>삭제</button>
    </li>
  );
}
```

| 구분 | Vue | React |
| :--- | :--- | :--- |
| **부모** | `<Child @delete="onDel" />` | `<Child onDelete={onDel} />` |
| **자식** | `emit('delete', id)` | `props.onDelete(id)` |

---

### Step 7: 로컬 스토리지와 Custom Hook
`useEffect`를 사용해 상태 변경 시 로컬 스토리지에 저장하는 부수 효과를 처리하고, 이를 Custom Hook으로 분리하여 재사용합니다.

**실제 코드 (Custom Hook):**
```tsx
export function useLocalStorage<T>(key: string, initialValue: T) {
  const [storedValue, setStoredValue] = useState<T>(() => {
    const item = window.localStorage.getItem(key);
    return item ? JSON.parse(item) : initialValue;
  });

  useEffect(() => {
    window.localStorage.setItem(key, JSON.stringify(storedValue));
  }, [key, storedValue]);

  return [storedValue, setStoredValue] as const;
}
```

| 구분 | Vue (`watch`) | React (`useEffect`) |
| :--- | :--- | :--- |
| 감지 | `watch(todos, (newVal) => { ... })` | `useEffect(() => { ... }, [todos])` |
| 로직 분리 | Composables (`useTodo.js`) | Custom Hook (`useLocalStorage.ts`) |

---

### Step 8: useEffect의 생명주기와 부수 효과 (Side Effects)
`useEffect`는 컴포넌트의 렌더링 이후에 발생하는 '부수 효과'를 처리합니다. Vue의 생명주기 훅(Life Cycle Hooks)과 Watcher의 기능을 하나로 합친 것과 같습니다.

**실제 코드:**
```tsx
useEffect(() => {
  // 1. Mount 시점 (onMounted) 또는 의존성 변경 시 (watch)
  console.log('효과 발생!');

  return () => {
    // 2. Unmount 시점 (onUnmounted) 또는 다음 효과 발생 전 정리 (Cleanup)
    console.log('정리 작업 수행 (Cleanup)');
  };
}, [storedValue]); // 의존성 배열
```

#### 💡 핵심 포인트: 의존성 배열 (Dependency Array)
1. **`[]` (빈 배열)**: 컴포넌트가 처음 나타날 때(Mount) 딱 한 번만 실행됩니다. (Vue의 `onMounted`)
2. **`[value]` (값이 있는 배열)**: `value`가 변경될 때마다 실행됩니다. (Vue의 `watch`)
3. **배열 생략**: 모든 렌더링 시점마다 실행됩니다. (성능 주의)

#### 🔍 Q&A: 괄호(`[]`) 안에는 무엇을 넣나요?
네, 맞습니다! 이 배열은 **"감시할 상태 목록(Dependency List)"**입니다. React에게 **"이 안에 적힌 값(State, Props)이 변할 때만 효과를 실행해줘!"**라고 명령하는 것입니다.

- **작동 원리**: React는 렌더링 전후의 배열 내 값들을 비교(Diffing)합니다.
- **예시**: `[count, userId]`라고 적으면, `count` **또는** `userId` 중 하나라도 값이 바뀌면 `useEffect`가 다시 실행됩니다.
- **비유**: "경비원에게 `count`라는 값이 움직이면 보고해!"라고 지시하는 것과 같습니다. (빈 배열 `[]`은 "아무것도 감시하지 말고 처음에만 보고해"라는 뜻이 됩니다.)

#### 🔄 Vue와 비교 정리

| 구분 | Vue | React (`useEffect`) |
| :--- | :--- | :--- |
| **Mount** | `onMounted(() => ...)` | `useEffect(() => ..., [])` |
| **Update** | `watch(val, () => ...)` | `useEffect(() => ..., [val])` |
| **Unmount** | `onUnmounted(() => ...)` | `useEffect(() => { return () => ... }, [])` |
| **정리(Cleanup)** | N/A (명시적 훅 필요) | `return` 키워드로 함수 반환 |

#### ⚠️ 주의: Cleanup 함수(return)를 생략하면?
만약 `return` 함수를 작성하지 않거나 비워두면, 컴포넌트가 사라지거나(Unmount) 업데이트되기 전에 **기존 작업이 정리되지 않습니다.**

**발생할 수 있는 문제:**
1. **메모리 누수 (Memory Leak)**: `setInterval`이나 외부 라이브러리 인스턴스가 계속 메모리에 남아 성능을 저하시킵니다.
2. **이벤트 중복 등록**: `window.addEventListener`가 렌더링될 때마다 계속 쌓여, 클릭 한 번에 함수가 수십 번 실행될 수 있습니다.
3. **업데이트 에러**: 이미 사라진 컴포넌트의 상태를 변경하려고 시도하여 콘솔 경고나 에러가 발생합니다.

**❌ 나쁜 예시 (타이머 미해제):**
```tsx
useEffect(() => {
  const timer = setInterval(() => {
    console.log('타이머 작동 중...'); // 컴포넌트가 사라져도 영원히 실행됨 😱
  }, 1000);
  
  // return () => clearInterval(timer); // 이 정리가 꼭 필요합니다!
}, []);
```

#### ❓ 정리할 내용이 없는 경우 (Optional Return)
모든 `useEffect`가 `return`을 가질 필요는 없습니다. 정리(Cleanup)가 필요 없는 단순한 작업이라면 함수만 실행하고 아무것도 반환하지 않아도 됩니다. (이 경우 `undefined`를 반환하는 것과 같습니다.)

**1. return이 필요 없는 경우 (단순 Side Effect):**
- 콘솔 로그 출력 (`console.log`)
- 로컬 스토리지에 데이터 저장 (`localStorage.setItem`)
- API 데이터 가져오기 (단순 호출)
- 문서 제목 변경 (`document.title = ...`)

**2. return이 꼭 필요한 경우 (정리가 필요한 Side Effect):**
- 타이머 (`setTimeout`, `setInterval`) 해제
- 이벤트 리스너 (`addEventListener`) 제거
- 외부 라이브러리 인스턴스 파괴 (예: 차트, 지도 라이브러리)
- 소켓 연결 종료

---

### Step 9: React.memo와 컴포넌트 최적화
React는 부모 컴포넌트가 렌더링되면 자식 컴포넌트도 기본적으로 다시 렌더링됩니다. `React.memo`를 사용하면 Props가 변하지 않았을 때 자식의 재렌더링을 건너뛰어 성능을 최적화할 수 있습니다.

**실제 코드 (TodoItem.tsx):**
```tsx
import { memo } from 'react';

const TodoItem = memo(function TodoItem({ todo, onDelete }: TodoItemProps) {
  console.log(`TodoItem 렌더링: ${todo.text}`);
  return (
    <li>{todo.text}</li>
  );
});
```

#### 💡 최적화 원리
- **메모이제이션(Memoization)**: 이전에 계산된 결과를 메모리에 저장해두고, 같은 입력이 들어오면 다시 계산하지 않고 저장된 결과를 재사용하는 기법입니다.
- **얕은 비교(Shallow Comparison)**: `React.memo`는 기본적으로 props의 값을 얕은 비교를 통해 변경 여부를 판단합니다.

| 구분 | 일반 컴포넌트 | React.memo 적용 |
| :--- | :--- | :--- |
| **렌더링 조건** | 부모가 변하면 무조건 실행 | Props가 변할 때만 실행 |
| **장점** | 구조가 단순함 | 불필요한 연산/DOM 조작 방지 |

---

### Step 10: useCallback과 함수 메모이제이션
`React.memo`를 써도 여전히 `TodoItem`이 리렌더링되는 현상이 있었습니다. 이유는 **함수도 객체**이기 때문입니다. `App` 컴포넌트가 다시 실행될 때마다 `deleteTodo` 함수도 새로 만들어지고, 자식 입장에서는 "Props(onDelete)가 바뀌었다!"고 인식합니다.

이를 해결하기 위해 `useCallback`으로 함수 자체를 기억합니다.

**실제 코드:**
```tsx
const deleteTodo = useCallback((id: number) => {
  setTodos(todos.filter(todo => todo.id !== id));
}, [todos]); // todos가 바뀔 때만 함수를 새로 만듦
```

#### 💡 왜 필요한가요?
1. **참조 동일성 유지**: 함수 내용이 같아도 메모리 주소가 다르면 다른 값으로 취급됩니다. `useCallback`은 의존성이 변하지 않으면 **같은 메모리 주소**의 함수를 반환합니다.
2. **자식 컴포넌트 최적화**: `React.memo`로 감싸진 자식에게 함수를 props로 넘길 때 필수적입니다.

| 상황 | useCallback 미사용 | useCallback 사용 |
| :--- | :--- | :--- |
| **입력 타이핑 시** | `deleteTodo` 재생성됨 → 자식 리렌더링 | `deleteTodo` 유지됨 → 자식 렌더링 건너뜀 |
| **Todos 변경 시** | `deleteTodo` 재생성됨 | `deleteTodo` 재생성됨 (의도된 동작) |

---

### Step 11: 전역 상태 관리 (Context API vs Zustand)
앱의 규모가 커지면 부모에서 자식의 자식으로 계속 Props를 넘겨주는 **'Props Drilling'** 문제가 발생합니다. 이를 해결하기 위해 전역 상태 관리를 사용합니다.

#### 1. Context API (React 내장)
- **개념**: React 컴포넌트 트리 전체에 데이터를 공급하는 통로(Provider)를 만듭니다.
- **특징**: 별도 설치 없이 사용 가능하지만, 상태가 바뀌면 Provider 하위의 모든 소비 컴포넌트가 리렌더링될 수 있어 최적화가 까다롭습니다.
- **용도**: 테마(Dark Mode), 언어 설정, 로그인 사용자 정보 등 **자주 변하지 않는 정적 데이터**.

**코드 예시:**
```tsx
// 생성
const ThemeContext = createContext('light');

// 공급 (Provider)
<ThemeContext.Provider value="dark">
  <App />
</ThemeContext.Provider>

// 사용 (Consumer)
const theme = useContext(ThemeContext);
```

#### 2. Zustand (외부 라이브러리)
- **개념**: "독일어(상태)"에서 유래한, 훅(Hook) 기반의 아주 가볍고 직관적인 상태 관리 라이브러리입니다.
- **특징**: `Provider`로 감쌀 필요가 없고, 상태의 특정 부분만 구독(Selector)하여 불필요한 리렌더링을 자동으로 막아줍니다. Redux보다 훨씬 코드가 짧습니다.
- **용도**: Todo List, 장바구니, 복잡한 폼 등 **자주 변하고 업데이트가 빈번한 데이터**.

**코드 예시:**
```tsx
// 스토어 생성 (create)
import { create } from 'zustand';

const useStore = create((set) => ({
  count: 0,
  inc: () => set((state) => ({ count: state.count + 1 })),
}));

// 컴포넌트에서 사용
function Counter() {
  const { count, inc } = useStore();
  return <button onClick={inc}>{count}</button>;
}
```

#### 🆚 비교 요약

| 구분 | Context API | Zustand |
| :--- | :--- | :--- |
| **설치** | 불필요 (내장) | 필요 (`npm install zustand`) |
| **사용법** | `Provider` 래핑 필요 | `Hook`으로 즉시 사용 |
| **성능** | 최적화 수동 필요 (Memoization) | 상태 선택(Selector)으로 자동 최적화 |
| **적합 대상** | 전역 테마, 인증 정보 | 앱의 핵심 비즈니스 로직, 복잡한 상태 |

---

### Step 12: React Router를 이용한 페이지 이동
SPA(Single Page Application)는 페이지를 새로고침하지 않고 주소창의 경로(URL)만 변경하여 다른 화면을 보여줍니다. 이를 위해 `react-router-dom` 라이브러리를 사용합니다.

#### 1. 설치 및 설정
```bash
npm install react-router-dom
```

`main.tsx`에서 앱 전체를 `<BrowserRouter>`로 감싸줍니다.

```tsx
import { BrowserRouter } from 'react-router-dom';

<BrowserRouter>
  <App />
</BrowserRouter>
```

#### 2. 라우팅 정의 (App.tsx)
`Routes`와 `Route` 컴포넌트를 사용하여 경로와 보여줄 컴포넌트를 연결합니다.

```tsx
<Routes>
  <Route path="/" element={<Home />} />
  <Route path="/about" element={<About />} />
</Routes>
```

#### 3. 페이지 이동 (Link)
`<a>` 태그를 쓰면 페이지가 새로고침되므로, 대신 `<Link>` 컴포넌트를 사용합니다.

```tsx
import { Link } from 'react-router-dom';

<nav>
  <Link to="/">홈으로</Link>
  <Link to="/about">소개</Link>
</nav>
```

| 구분 | 일반 웹 (`<a>`) | React Router (`<Link>`) |
| :--- | :--- | :--- |
| **동작** | 페이지 전체 새로고침 (서버 요청) | JS로 화면만 교체 (클라이언트 라우팅) |
| **상태** | 모든 State 초기화됨 | State 유지 가능 (SPA) |
| **속도** | 상대적으로 느림 | 깜빡임 없이 즉시 전환 |

---

### Step 13: 동적 라우팅 (Dynamic Routing)
URL의 특정 부분을 변수처럼 사용하는 기능입니다. 예를 들어, 상세 페이지를 만들 때 ID 값에 따라 다른 내용을 보여줘야 할 때 사용합니다.

#### 1. 라우트 설정 (App.tsx)
콜론(`:`)을 사용하여 파라미터가 들어갈 자리를 지정합니다.
```tsx
<Route path="/todo/:id" element={<TodoDetail />} />
```

#### 2. 링크 생성 (TodoItem.tsx)
템플릿 리터럴을 사용하여 실제 ID 값을 경로에 넣습니다.
```tsx
<Link to={`/todo/${todo.id}`}>{todo.text}</Link>
```

#### 3. 파라미터 읽기 (TodoDetail.tsx)
`useParams` 훅을 사용하여 URL에 있는 값을 가져옵니다.
```tsx
import { useParams, useNavigate } from 'react-router-dom';

function TodoDetail() {
  const { id } = useParams(); // URL의 :id 부분을 가져옴
  const navigate = useNavigate(); // 페이지 이동을 위한 훅

  return (
    <div>
      <h2>ID: {id}</h2>
      <button onClick={() => navigate(-1)}>뒤로 가기</button>
    </div>
  );
}
```

#### 💡 useNavigate 훅

- **`navigate('/path')`**: 특정 경로로 이동

- **`navigate(-1)`**: 뒤로 가기 (히스토리 스택 이용)

- **`navigate(1)`**: 앞으로 가기



---



### Step 14: 전역 상태 관리 구현 패턴 비교

`TodoDetail` 페이지에서 할 일 내용을 보여주려면, `todos` 배열이 `Home` 컴포넌트 내부에 갇혀 있으면 안 됩니다. 이를 해결하기 위한 두 가지 방법을 비교합니다.



#### 1. Context API 방식 (React 내장)

보일러플레이트(준비 코드)가 다소 길지만, 외부 라이브러리 없이 구현 가능합니다.



**1) Context 생성 (TodoContext.tsx)**

```tsx

import { createContext, useContext, useState } from 'react';



// 데이터 타입 정의

interface TodoContextType {

  todos: Todo[];

  addTodo: (text: string) => void;

  deleteTodo: (id: number) => void;

}



// 1. 컨텍스트 생성

const TodoContext = createContext<TodoContextType | null>(null);



// 2. Provider 생성 (데이터 공급자)

export function TodoProvider({ children }: { children: React.ReactNode }) {

  const [todos, setTodos] = useState<Todo[]>([]);

  // ... addTodo, deleteTodo 로직 ...



  return (

    <TodoContext.Provider value={{ todos, addTodo, deleteTodo }}>

      {children}

    </TodoContext.Provider>

  );

}



// 3. Custom Hook (사용 편의성)

export function useTodo() {

  const context = useContext(TodoContext);

  if (!context) throw new Error('Provider 없음!');

  return context;

}

```



**2) 앱 감싸기 (main.tsx)**

```tsx

<TodoProvider>

  <App />

</TodoProvider>

```



**3) 사용하기 (Home.tsx / Detail.tsx)**

```tsx

const { todos, deleteTodo } = useTodo(); // 훅으로 바로 사용

```



---



#### 2. Zustand 방식 (라이브러리)

Redux DevTools 사용이 가능하고 코드가 압도적으로 간결합니다.



**1) 스토어 생성 (todoStore.ts)**

```tsx

import { create } from 'zustand';



interface TodoStore {

  todos: Todo[];

  addTodo: (text: string) => void;

  deleteTodo: (id: number) => void;

}



export const useTodoStore = create<TodoStore>((set) => ({

  todos: [],

  // 상태 변경 함수가 스토어 내부에 위치 (Action)

  addTodo: (text) => set((state) => ({

    todos: [...state.todos, { id: Date.now(), text }]

  })),

  deleteTodo: (id) => set((state) => ({

    todos: state.todos.filter(t => t.id !== id)

  })),

}));

```



**2) 사용하기 (어디서든)**

```tsx

// Provider 감싸기 필요 없음!

const todos = useTodoStore((state) => state.todos);

const addTodo = useTodoStore((state) => state.addTodo);

```



#### 🏆 결론 및 선택



- **Context API**: 설정이 복잡하고 렌더링 최적화가 어렵지만, 의존성이 없습니다.



- **Zustand**: 설치가 필요하지만 코드가 깔끔하고 성능 최적화가 자동입니다.



- **실습 선택**: 우리 프로젝트는 **Zustand**를 사용하여 리팩토링합니다.







---







### Step 15: 실제 코드 작성 및 적용 방법



두 가지 방식을 모두 코드로 작성해 보았습니다.







#### 1. Context API 적용 방법



**파일 경로**: `src/context/TodoContext.tsx`







**1) main.tsx 수정 (Provider 감싸기)**



```tsx



import { TodoProvider } from './context/TodoContext';







<BrowserRouter>



  <TodoProvider> {/* 앱 전체에 데이터 공급 */}



    <App />



  </TodoProvider>



</BrowserRouter>



```







**2) 컴포넌트에서 사용 (Home.tsx)**



```tsx



import { useTodoContext } from '../context/TodoContext';







function Home() {



  const { todos, addTodo, deleteTodo } = useTodoContext();



  // ... 나머지 로직 동일



}



```







#### 2. Zustand 적용 방법 (권장)



**파일 경로**: `src/store/todoStore.ts`







**1) main.tsx 수정 불필요**



Zustand는 Provider가 필요 없습니다.







**2) 컴포넌트에서 사용 (Home.tsx)**



```tsx



import { useTodoStore } from '../store/todoStore';







function Home() {



  // 필요한 상태와 함수만 쏙쏙 골라서 가져옴 (Selector)



  const todos = useTodoStore((state) => state.todos);



  const addTodo = useTodoStore((state) => state.addTodo);



  const deleteTodo = useTodoStore((state) => state.deleteTodo);



  // ... 나머지 로직 동일



}



```







---







### Step 16: 향후 학습 과제



- [x] React Router를 이용한 페이지 이동 (동적 라우팅 포함)



- [x] Context API와 Zustand 코드 작성 및 비교



- [ ] Zustand를 실제 프로젝트(Home.tsx)에 적용하여 리팩토링



- [ ] TodoDetail 페이지에 전역 상태 연결하여 내용 표시

---

## 3. 리액트 용어 정리 (Glossary)

이 문서에서 사용된 주요 리액트 및 웹 개발 용어에 대한 설명입니다.

### 핵심 개념 (Core Concepts)
- **Vite**: 빠르고 가벼운 최신 프론트엔드 빌드 도구입니다. 리액트 프로젝트를 생성하고 실행하는 데 사용됩니다.
- **State (상태)**: 컴포넌트 내부에서 관리되는 동적인 데이터입니다. 값이 변하면 리액트는 컴포넌트를 리렌더링하여 UI를 업데이트합니다.
- **Props (Properties)**: 부모 컴포넌트가 자식 컴포넌트에게 전달하는 읽기 전용 데이터입니다.
- **One-way Data Flow (단방향 데이터 흐름)**: 데이터가 부모에서 자식으로 한 방향(아래)으로만 흐르는 리액트의 특징입니다.
- **Immutability (불변성)**: 상태를 직접 수정하지 않고, 새로운 값을 만들어 교체하는 원칙입니다. 리액트가 변경 사항을 감지하기 위해 필요합니다.
- **Side Effects (부수 효과)**: 데이터 가져오기, 구독 설정, 수동 DOM 조작 등 컴포넌트 렌더링 외에 발생하는 모든 작업을 의미합니다.

### 훅 (Hooks)
- **useState**: 함수형 컴포넌트에서 상태를 관리할 수 있게 해주는 훅입니다.
- **useEffect**: 함수형 컴포넌트에서 부수 효과(Side Effects)를 수행할 수 있게 해주는 훅입니다. (생명주기 관리)
- **useCallback**: 함수를 메모이제이션(기억)하여 불필요한 재생성을 방지하는 훅입니다. 최적화에 사용됩니다.
- **Custom Hook**: 자주 사용되는 로직을 분리하여 재사용 가능하게 만든 사용자 정의 훅입니다. (`use`로 시작하는 함수)
- **Dependency Array (의존성 배열)**: `useEffect`나 `useCallback` 등이 언제 재실행될지 결정하는 배열입니다.
- **Cleanup Function (정리 함수)**: `useEffect`에서 반환하는 함수로, 컴포넌트가 사라지거나 업데이트되기 전에 실행되어 메모리 누수 등을 방지합니다.

### 라우팅 (Routing)
- **SPA (Single Page Application)**: 페이지 새로고침 없이 동적으로 콘텐츠를 갱신하는 웹 애플리케이션입니다.
- **React Router**: 리액트에서 SPA 라우팅을 구현하기 위한 표준 라이브러리입니다.
- **Dynamic Routing (동적 라우팅)**: URL의 특정 부분(파라미터)에 따라 다른 내용을 보여주는 라우팅 방식입니다. (예: `/todo/:id`)
- **useParams**: URL 경로에 포함된 파라미터 값(예: `:id`)을 가져오는 훅입니다.
- **useNavigate**: 코드로 페이지를 이동시킬 때 사용하는 훅입니다.

### 상태 관리 (State Management)
- **Context API**: 리액트 내장 기능으로, Props Drilling 없이 컴포넌트 트리 전체에 데이터를 공급할 수 있습니다.
- **Props Drilling**: 데이터를 깊은 곳에 있는 자식에게 전달하기 위해 중간 컴포넌트들을 거쳐 Props를 계속 내려주는 현상입니다.
- **Zustand**: 간결한 문법과 자동 최적화를 제공하는 인기 있는 외부 상태 관리 라이브러리입니다.
- **Selector (선택자)**: 상태 저장소(Store)에서 필요한 데이터만 골라내는 함수입니다. (Zustand 등에서 사용)

### 최적화 (Optimization)
- **Memoization (메모이제이션)**: 이전에 계산한 값을 메모리에 저장해두고 재사용하여 연산 속도를 높이는 기술입니다.
- **React.memo**: 컴포넌트의 Props가 바뀌지 않았다면 리렌더링을 건너뛰도록 설정하는 고차 컴포넌트(HOC)입니다.
