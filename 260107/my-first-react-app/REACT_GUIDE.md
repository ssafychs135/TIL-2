# ⚛️ Vue 개발자를 위한 React 입문 가이드

이 가이드는 **Vue 3 Composition API (`<script setup>`)** 개발 방식에 익숙한 분들이 React의 핵심 개념을 빠르게 이해할 수 있도록 비교 중심으로 작성되었습니다.

## 🚀 1. 시작하기 (Setup)
React도 Vite를 사용하여 빠르고 간편하게 프로젝트를 생성할 수 있습니다.

```bash
# 1. Vite 프로젝트 생성 (React + SWC 추천)
npm create vite@latest my-react-app

# 2. 폴더 이동 및 패키지 설치
cd my-react-app
npm install

# 3. 개발 서버 실행
npm run dev
```

---

## 🆚 2. 핵심 개념 비교 (Vue vs React)

### ① 컴포넌트 구조 (Structure)
Vue는 `<template>`, `<script>`, `<style>`이 분리되어 있지만, React는 **JSX**를 사용하여 JavaScript 함수 하나에 논리와 뷰를 모두 담습니다.

| Vue 3 (`<script setup>`) | React (Function Component) |
| :--- | :--- |
| **Template + Script** 분리 | **JSX** (JS가 HTML을 포함) |
| `.vue` 파일 | `.jsx` 또는 `.tsx` 파일 |
| `v-bind`, `v-model` 등의 디렉티브 사용 | 순수 **JavaScript 문법** 사용 (`map`, `&&` 등) |

**React 예시:**
```tsx
// App.tsx
function App() {
  // Logic (Script)
  const title: string = "Hello React";

  // View (Template) -> JSX 리턴
  return <h1>{title}</h1>;
}
```

### ② 반응형 상태 (State) ⭐️
Vue의 `ref`와 유사하지만, React는 **Setter 함수**를 통해서만 값을 변경해야 합니다.

| 기능 | Vue 3 | React |
| :--- | :--- | :--- |
| 선언 | `const count = ref<number>(0)` | `const [count, setCount] = useState<number>(0)` |
| 값 읽기 | `count.value` (스크립트), `count` (템플릿) | `count` (어디서나) |
| 값 변경 | `count.value++` | `setCount(count + 1)` (불변성 유지 필수) |

**💡 중요: [count, setCount]의 비밀**
`useState`는 `[값, 함수]` 형태의 **배열**을 반환합니다. 우리는 **자바스크립트 구조 분해 할당**을 통해 이 배열의 요소에 이름을 붙여서 사용하는 것입니다.
*   **첫 번째 자리**: 현재 상태 값 (이름은 마음대로 지을 수 있음)
*   **두 번째 자리**: 상태를 변경하는 함수 (이름은 마음대로 지을 수 있음)
*   **규칙(Convention)**: 자동으로 생성되는 것이 아니라 개발자가 직접 짓는 이름입니다. 하지만 관례상 **`set + 변수명`** (예: `setCount`) 형식을 사용하여 코드를 읽기 쉽게 만듭니다.

**React 예시:**
```tsx
import { useState } from 'react';

function Counter() {
  // 제네릭으로 타입 지정 가능: useState<number>(0)
  const [count, setCount] = useState<number>(0); 

  return (
    <button onClick={() => setCount(count + 1)}>
      Count: {count}
    </button>
  );
}
```

### ③ Props (데이터 전달)
Vue의 `defineProps`와 달리, React는 **함수의 매개변수**로 props를 받습니다. TypeScript에서는 **Interface**를 사용하여 Props의 타입을 정의합니다.

| 기능 | Vue 3 | React |
| :--- | :--- | :--- |
| 선언 | `defineProps<{ title: string }>()` | `function MyComp({ title }: { title: string }) { ... }` |
| 전달 | `<MyComp :title="msg" />` | `<MyComp title={msg} />` |

**React 예시:**
```tsx
interface WelcomeProps {
  name: string;
}

// 자식 컴포넌트: Props 타입 지정
function Welcome({ name }: WelcomeProps) {
  return <h2>Hello, {name}</h2>;
}

// 부모 컴포넌트
function App() {
  return <Welcome name="SSAFY" />;
}
```

### ④ 이벤트 처리 (Event Handling)
Vue의 `@click` 대신 `onClick` (카멜 케이스)을 사용합니다. `emit`은 없으며, **함수를 props로 전달**하여 자식에서 실행하는 방식을 사용합니다.

| 기능 | Vue 3 | React |
| :--- | :--- | :--- |
| 이벤트 | `@click="handler"` | `onClick={handler}` |
| 부모 통신 | `emit('update')` | 부모가 준 함수 실행: `props.onUpdate()` |

**React 예시:**
```tsx
interface ButtonProps {
  onSmash: () => void; // 반환값이 없는 함수 타입
}

function Button({ onSmash }: ButtonProps) {
  return <button onClick={onSmash}>Click Me</button>;
}

function App() {
  const handleClick = () => alert('Clicked!');
  // 함수 자체를 prop으로 전달
  return <Button onSmash={handleClick} />;
}
```

### ⑤ 라이프사이클 & 감시 (Lifecycle & Watch)
Vue의 `onMounted`, `watch`, `unmounted` 등을 **`useEffect`** 하나로 통합해서 처리합니다.

| 기능 | Vue 3 | React |
| :--- | :--- | :--- |
| 마운트 시 | `onMounted(() => ...)` | `useEffect(() => ..., [])` (빈 배열) |
| 값 변경 감지 | `watch(val, () => ...)` | `useEffect(() => ..., [val])` (의존성 배열) |

**React 예시:**
```tsx
import { useEffect, useState } from 'react';

function Timer() {
  const [count, setCount] = useState<number>(0);

  useEffect(() => {
    console.log("마운트 됨 (or count 변경 됨)");
  }, [count]); // count가 변할 때마다 실행

  return <div>{count}</div>;
}
```

### ⑥ 반복문과 조건문 (Loop & Condition)
별도의 디렉티브(`v-for`, `v-if`)가 없고 **JavaScript 문법**을 그대로 씁니다.

| 기능 | Vue 3 | React |
| :--- | :--- | :--- |
| 반복문 | `v-for="item in list"` | `list.map(item => <div key={item.id}>...</div>)` |
| 조건문 | `v-if="isShow"` | `{ isShow && <div>...</div> }` (AND 연산자) |
| if-else | `v-if`, `v-else` | `{ isShow ? <A/> : <B/> }` (삼항 연산자) |

#### 🔍 조건부 렌더링 상세 패턴

1.  **논리 AND 연산자 (`&&`)** - "조건이 맞을 때만 보여주기" (`v-if`)
    *   가장 많이 쓰이는 패턴입니다. 왼쪽 조건이 `true`이면 오른쪽 JSX를 반환합니다.
    *   **주의**: 숫자의 경우 `0`은 거짓이지만 React가 화면에 `0`을 출력해버립니다. 
        *   `{ count && <p>Count exists</p> }` (count가 0이면 화면에 0이 나옴)
        *   `{ count > 0 && <p>Count exists</p> }` (명확한 비교식 권장)

2.  **삼항 연산자 (`? :`)** - "이거 아니면 저거 보여주기" (`v-if / v-else`)
    *   조건에 따라 서로 다른 컴포넌트를 보여줄 때 사용합니다.
    *   너무 길어지면 가독성이 떨어지므로, 복잡할 경우 별도의 변수로 빼거나 컴포넌트를 분리하는 것이 좋습니다.

3.  **Early Return** - "특정 조건에서 렌더링 차단"
    *   함수형 컴포넌트 내부에서 `if`문을 사용하여 일찍 `return null`을 하면 아무것도 그리지 않습니다. Vue의 `v-if`를 컴포넌트 최상단에 거는 것과 비슷합니다.

```tsx
interface Data {
  name: string;
  isNew: boolean;
  isVip: boolean;
}

interface AppProps {
  isLoading: boolean;
  data: Data | null; // 데이터가 없으면 null일 수 있음
}

function App({ isLoading, data }: AppProps) {
  // 1. Early Return 패턴 (로딩 중일 때)
  if (isLoading) return <div>로딩 중...</div>;

  // 2. 데이터가 없을 때
  if (!data) return null;

  return (
    <div>
      <h1>데이터: {data.name}</h1>
      {/* 3. AND 연산자 패턴 */}
      {data.isNew && <span className="badge">신규</span>}
      
      {/* 4. 삼항 연산자 패턴 */}
      {data.isVip ? <VipCard /> : <NormalCard />}
    </div>
  );
}
```

#### 💡 참고: 왜 if문을 직접 못 쓰나요?
JSX의 `{ }` 중괄호 안에는 **값(Expression)**으로 평가되는 코드만 들어갈 수 있습니다. `if`문이나 `for`문은 **문장(Statement)**이기 때문에 `{ }` 안에 직접 넣으면 에러가 납니다. 대신 값을 반환하는 논리 연산자나 삼항 연산자를 활용하는 것입니다.

#### 🔍 반복문(map) 심화 학습
React에서 목록을 만들 때 왜 `map`을 쓸까요?
1.  **배열을 리턴**: `map()`은 기존 배열을 토대로 **JSX 엘리먼트로 구성된 새로운 배열**을 만들어 반환합니다. React는 배열 안에 담긴 JSX를 자동으로 펼쳐서 화면에 그려줍니다.
2.  **Key의 역할 (필수)**: 
    *   React는 어떤 항목이 바뀌었는지 식별하기 위해 `key`를 사용합니다.
    *   `key`가 없으면 목록이 변경될 때 모든 요소를 다시 그려서 성능이 떨어집니다.
    *   **주의**: 배열의 `index`를 key로 쓰는 것은 지양해야 합니다. (항목의 순서가 바뀌면 React가 엉뚱한 요소를 업데이트하는 버그가 생길 수 있습니다.) 가능하면 **데이터의 고유 ID**를 사용하세요.

#### 💡 참고: 일반 `for` 루프도 사용 가능한가요?
네, 가능합니다! 하지만 JSX 내부 `{ }` 안에는 `for` 문(문장)을 직접 넣을 수 없으므로, **`return` 문 밖에서 미리 배열을 만들어두는 방식**을 사용해야 합니다. 이 방식을 통해 "React는 결국 JSX가 담긴 배열을 화면에 그린다"는 원리를 이해할 수 있습니다.

```tsx
interface Fruit {
  id: string;
  name: string;
}

function App() {
  // 권장사항: 고유 ID를 포함한 객체 배열
  const fruits: Fruit[] = [
    { id: 'f1', name: '사과' },
    { id: 'f2', name: '바나나' }
  ];
  const result: JSX.Element[] = []; // 결과 배열 타입 명시

  for (let i = 0; i < fruits.length; i++) {
    const item = fruits[i];
    // index(i) 대신 고유 ID를 key로 사용
    result.push(<li key={item.id}>{item.name}</li>);
  }

  return <ul>{result}</ul>;
}
```
*(단, 실무에서는 코드가 훨씬 간결한 `map()`을 주로 사용합니다.)*

**React 예시:**
```tsx
interface User {
  id: number;
  name: string;
}

const users: User[] = [
  { id: 101, name: 'Alice' },
  { id: 102, name: 'Bob' }
];

function UserList() {
  return (
    <ul>
      {users.map((user) => (
        // 고유한 id를 key로 할당
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}
```

---

## 🛠️ 3. 실전 예제 (Todo App 변환)

Vue 코드와 React 코드를 비교해 보세요.

### React Version
```tsx
import { useState } from 'react';

function TodoApp() {
  // 타입 명시: 문자열 상태
  const [input, setInput] = useState<string>("");
  // 타입 명시: 문자열 배열 상태
  const [todos, setTodos] = useState<string[]>([]);

  const addTodo = () => {
    if (!input) return;
    // push 대신 새로운 배열을 만들어서 교체 (불변성)
    setTodos([...todos, input]);
    setInput("");
  };

  return (
    <div>
      {/* v-model 대신 value + onChange */}
      {/* onChange 이벤트 객체의 타입은 React.ChangeEvent<HTMLInputElement> */}
      <input 
        value={input} 
        onChange={(e: React.ChangeEvent<HTMLInputElement>) => setInput(e.target.value)} 
      />
      <button onClick={addTodo}>추가</button>

      <ul>
        {/* v-for 대신 map */}
        {todos.map((todo, index) => (
          <li key={index}>{todo}</li>
        ))}
      </ul>
    </div>
  );
}

export default TodoApp;
```

---

## 💡 4. Vue 개발자가 주의할 점 (Gotchas)

1.  **불변성 (Immutability)**:
    *   Vue: `list.push(newItem)` (가능)
    *   React: `setList([...list, newItem])` (반드시 새 배열/객체 생성)
2.  **className**:
    *   HTML `class` 속성 대신 `className`을 사용해야 합니다.
3.  **반환값**:
    *   JSX는 반드시 **하나의 부모 태그**로 감싸져야 합니다. (혹은 `<> ... </>` Fragment 사용)
4.  **반응형 객체**:
    *   Vue의 `reactive`처럼 깊은 감지는 지원하지 않으므로, 객체 상태 변경 시 `...spread` 연산자를 자주 사용하게 됩니다.