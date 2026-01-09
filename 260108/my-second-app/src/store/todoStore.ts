import { create } from 'zustand';
import { persist } from 'zustand/middleware'; // 로컬 스토리지 저장을 쉽게 해주는 미들웨어
import { type Todo } from '../components/TodoItem';

interface TodoStore {
  todos: Todo[];
  addTodo: (text: string) => void;
  deleteTodo: (id: number) => void;
}

// create 함수로 스토어 생성
export const useTodoStore = create<TodoStore>()(
  persist(
    (set) => ({
      todos: [],
      addTodo: (text) =>
        set((state) => ({
          todos: [...state.todos, { id: Date.now(), text }],
        })),
      deleteTodo: (id) =>
        set((state) => ({
          todos: state.todos.filter((todo) => todo.id !== id),
        })),
    }),
    {
      name: 'todos-zustand', // 로컬 스토리지 키 이름
    }
  )
);
