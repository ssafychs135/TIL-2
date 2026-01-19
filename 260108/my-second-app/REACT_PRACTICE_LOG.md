# ⚛️ React 실전 연습 로그 (260108)

이 문서는 `my-second-app` 프로젝트를 통해 학습한 React 실전 적용 과정을 기록합니다.

## 1. 프로젝트 초기화 (Cleanup)
- **목표**: `src/App.tsx`와 `src/App.css` 정리 및 초기화.
- **핵심**: 불필요한 import 제거, 기본 스타일 Reset.

---

## Part 1. State와 렌더링 기초 (Basics)

### 1-1. 단방향 데이터 흐름 (Input)
React는 양방향 바인딩(`v-model`)이 없습니다. `value`(읽기)와 `onChange`(쓰기)를 수동으로 연결합니다.

```tsx
const [inputValue, setInputValue] = useState<string>('');
<input value={inputValue} onChange={(e) => setInputValue(e.target.value)} />
```

| 구분 | Vue (`v-model`) | React (`useState`) |
| :--- | :--- | :--- |
| **특징** | 자동 동기화 | 명시적 제어 (함수가 실행되어야 값이 바뀜) |

### 1-2. 다중 Input 관리 (One State)
여러 개의 Input을 하나의 객체 State로 관리하여 코드를 간소화합니다.

- **핵심**: `e.target.name`과 계산된 속성명(`[name]: value`) 활용.

```tsx
const [inputs, setInputs] = useState({ name: '', email: '' });

const onChange = (e) => {
  const { name, value } = e.target;
  setInputs({ ...inputs, [name]: value }); // 기존 객체 복사 필수
};
```

### 1-3. 불변성과 리스트 렌더링
배열을 직접 수정(`push`)하지 않고, 스프레드 연산자(`...`)로 새로운 배열을 생성하여 업데이트합니다.

```tsx
// 추가 (Add)
setTodos([...todos, newTodo]); 

// 반복 (Map)
{todos.map((todo) => <li key={todo.id}>{todo.text}</li>)}
```

### 1-4. 조건부 스타일링 (Template Literals)
백틱(`` ` ``)과 삼항 연산자를 사용하여 클래스를 동적으로 조작합니다.

```tsx
<li className={`todo-item ${isDone ? 'completed' : ''}`}>...</li>
```

### 1-5. 데이터 삭제 (Filter)
`splice` 대신 `filter`를 사용하여 조건에 맞는 요소만 남긴 **새 배열**로 교체합니다.

```tsx
setTodos(todos.filter(todo => todo.id !== id));
```

---

## Part 2. 컴포넌트와 이펙트 (Structure & Effects)

### 2-1. Props 전달
부모가 자식에게 데이터나 함수를 전달할 때 Props 인터페이스를 정의하여 사용합니다.

```tsx
interface TodoItemProps {
  todo: Todo;
  onDelete: (id: number) => void;
}
// <Child onDelete={handleDelete} /> 형태로 전달
```

### 2-2. Custom Hook (로직 재사용)
`useEffect`를 포함한 복잡한 로직(예: 로컬 스토리지 동기화)을 별도 함수로 분리합니다.

```tsx
export function useLocalStorage<T>(key: string, initialValue: T) {
  // ... useState와 useEffect 로직
  return [storedValue, setStoredValue] as const;
}
```

### 2-3. useEffect 생명주기
컴포넌트의 Mount, Update, Unmount 시점을 `useEffect` 하나로 관리합니다.

- **`[]`**: Mount 시 1회 실행 (Vue `onMounted`)
- **`[dep]`**: 해당 값이 변할 때 실행 (Vue `watch`)
- **`return () => ...`**: Cleanup 함수 (Vue `onUnmounted`)

---

## Part 3. 성능 최적화 (Optimization)

### 3-1. React.memo (컴포넌트 캐싱)
부모가 렌더링되더라도 Props가 변하지 않았다면 자식의 재렌더링을 건너뜁니다.

```tsx
const TodoItem = memo(function TodoItem({ todo }: Props) { ... });
```

### 3-2. useCallback (함수 캐싱)
함수가 재생성되어 자식 컴포넌트가 불필요하게 렌더링되는 것을 방지합니다.

```tsx
const deleteTodo = useCallback((id) => {
  setTodos(prev => prev.filter(t => t.id !== id));
}, []); // 의존성 배열이 비어있으면 함수가 재생성되지 않음
```

---

## Part 4. 라우팅과 전역 상태 (Architecture)

### 4-1. 전역 상태 관리 비교
Props Drilling을 해결하기 위한 두 가지 방식을 비교합니다.

| 구분 | Context API (내장) | Zustand (라이브러리) |
| :--- | :--- | :--- |
| **특징** | `Provider` 래핑 필요, 보일러플레이트 많음 | Hook 기반, 코드가 매우 간결함 |
| **선택** | 정적 데이터(테마, 언어) | **빈번한 데이터(Todo, 장바구니)** |

### 4-2. React Router 설정
SPA 라우팅을 위해 `react-router-dom`을 사용합니다.

- **설정**: `main.tsx`에서 `<BrowserRouter>`로 감싸기.
- **이동**: `<Link to="...">` 사용 (새로고침 방지).
- **정의**: `<Route path="/" element={<Home />} />`

### 4-3. 동적 라우팅 (Dynamic Routing)
URL 파라미터를 통해 상세 페이지를 구현합니다.

```tsx
// 라우트 정의
<Route path="/todo/:id" element={<TodoDetail />} />

// 값 읽기
const { id } = useParams();
```

### 4-4. 코드 구현 (Zustand)
실제 프로젝트에는 **Zustand**를 적용하여 `Home.tsx`를 리팩토링합니다.

```tsx
// Store 생성
const useTodoStore = create((set) => ({
  todos: [],
  addTodo: (text) => set(state => ({ todos: [...state.todos, text] })),
}));

// 사용
const todos = useTodoStore(state => state.todos);
```

---

## 5. 향후 학습 과제
- [x] React Router 기본 및 동적 라우팅
- [x] Context API vs Zustand 비교 및 실습
- [ ] TodoDetail 페이지에 전역 상태 연결하여 데이터 표시
- [ ] UI 라이브러리(Tailwind CSS 또는 Styled Components) 도입 검토

---

## 6. 리액트 용어 정리 (Glossary)

### 핵심 개념
- **Immutability (불변성)**: 상태를 직접 변경하지 않고 복사본을 만들어 교체하는 원칙.
- **One-way Flow**: 데이터는 부모 → 자식으로만 흐름.

### 훅 (Hooks)
- **useState**: 상태 관리.
- **useEffect**: 부수 효과(Side Effect) 처리.
- **useCallback**: 함수 메모이제이션.
- **Custom Hook**: 로직의 재사용 가능한 분리.

### 라우팅 & 상태
- **SPA**: 페이지 새로고침 없는 단일 페이지 앱.
- **Params**: URL에 포함된 변수 (`:id`).
- **Props Drilling**: 깊은 계층으로 데이터를 전달하며 발생하는 비효율.
- **Selector**: Store에서 필요한 상태만 구독하여 성능 최적화.