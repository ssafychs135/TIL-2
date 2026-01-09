import { createContext, useContext, useState, ReactNode, useEffect } from 'react';
import { type Todo } from '../components/TodoItem';

// 1. Context에서 관리할 데이터 타입 정의
interface TodoContextType {
  todos: Todo[];
  addTodo: (text: string) => void;
  deleteTodo: (id: number) => void;
}

// 2. Context 생성
const TodoContext = createContext<TodoContextType | null>(null);

// 3. Provider 컴포넌트 생성
export function TodoProvider({ children }: { children: ReactNode }) {
  // 기존 useLocalStorage 로직을 여기서 사용하거나, 간단히 useState로 구현
  // (여기서는 이해를 돕기 위해 useState와 useEffect로 직접 구현)
  const [todos, setTodos] = useState<Todo[]>(() => {
    const item = window.localStorage.getItem('todos-context');
    return item ? JSON.parse(item) : [];
  });

  useEffect(() => {
    window.localStorage.setItem('todos-context', JSON.stringify(todos));
  }, [todos]);

  const addTodo = (text: string) => {
    const newTodo = { id: Date.now(), text };
    setTodos((prev) => [...prev, newTodo]);
  };

  const deleteTodo = (id: number) => {
    setTodos((prev) => prev.filter((todo) => todo.id !== id));
  };

  return (
    <TodoContext.Provider value={{ todos, addTodo, deleteTodo }}>
      {children}
    </TodoContext.Provider>
  );
}

// 4. Custom Hook 생성 (사용하기 쉽게)
export function useTodoContext() {
  const context = useContext(TodoContext);
  if (!context) {
    throw new Error('useTodoContext must be used within a TodoProvider');
  }
  return context;
}
