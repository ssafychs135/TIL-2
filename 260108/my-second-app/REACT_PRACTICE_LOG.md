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

### Step 2: 불변성(Immutability)과 리스트 렌더링
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

### Step 3: 데이터 삭제 (Filter)
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

### Step 4: 컴포넌트 분리와 Props 전달
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

### Step 5: 로컬 스토리지와 Custom Hook
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
| **감지** | `watch(todos, (newVal) => { ... })` | `useEffect(() => { ... }, [todos])` |
| **로직 분리** | Composables (`useTodo.js`) | Custom Hook (`useLocalStorage.ts`) |