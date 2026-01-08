// 타입을 별도로 관리하면 좋지만, 간단히 여기서 정의하거나 공유할 수 있습니다.
// (실무에서는 types.ts 등으로 분리하기도 합니다)
export interface Todo {
  id: number;
  text: string;
}

interface TodoItemProps {
  todo: Todo;
  onDelete: (id: number) => void; // id를 받아서 void를 반환하는 함수 타입
}

function TodoItem({ todo, onDelete }: TodoItemProps) {
  return (
    <li className="todo-item">
      <span>{todo.text}</span>
      <button 
        className="delete-btn"
        // 부모에게 받은 함수 실행
        onClick={() => onDelete(todo.id)}
      >
        삭제
      </button>
    </li>
  );
}

export default TodoItem;
