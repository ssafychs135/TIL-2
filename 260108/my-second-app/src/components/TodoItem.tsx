import { memo } from 'react';
import { Link } from 'react-router-dom';

export interface Todo {
  id: number;
  text: string;
}

interface TodoItemProps {
  todo: Todo;
  onDelete: (id: number) => void;
}

// React.memo로 감싸서 props가 변경되지 않으면 리렌더링을 방지합니다.
const TodoItem = memo(function TodoItem({ todo, onDelete }: TodoItemProps) {
  console.log(`TodoItem 렌더링: ${todo.text}`);

  return (
    <li className="todo-item">
      {/* 텍스트를 클릭하면 상세 페이지로 이동 */}
      <Link to={`/todo/${todo.id}`} style={{ textDecoration: 'none', color: 'inherit', flex: 1 }}>
        <span>{todo.text}</span>
      </Link>
      
      <button 
        className="delete-btn"
        onClick={() => onDelete(todo.id)}
      >
        삭제
      </button>
    </li>
  );
});

export default TodoItem;
