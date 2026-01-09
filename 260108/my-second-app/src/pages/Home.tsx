import { useState, useCallback } from 'react';
// CSS는 App.css를 공유하거나 별도로 만들 수 있지만, 일단 상위 App.css 스타일을 따릅니다.
import TodoItem, { type Todo } from '../components/TodoItem';
import { useLocalStorage } from '../hooks/useLocalStorage';

function Home() {
  const [inputValue, setInputValue] = useState<string>('');
  const [todos, setTodos] = useLocalStorage<Todo[]>('todos', []);

  const addTodo = () => {
    if (!inputValue.trim()) return; 

    const newTodo: Todo = {
      id: Date.now(), 
      text: inputValue
    };

    setTodos([...todos, newTodo]);
    setInputValue('');
  };

  const deleteTodo = useCallback((id: number) => {
    setTodos(todos.filter(todo => todo.id !== id));
  }, [todos, setTodos]);

  return (
    <div>
      <h1>My Todo List</h1>
      
      <div className="input-group">
        <input 
          type="text" 
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && addTodo()}
          placeholder="할 일을 입력하세요"
        />
        <button onClick={addTodo}>추가</button>
      </div>

      <ul>
        {todos.length === 0 ? (
           <p className="empty-msg">할 일이 없습니다! 작업을 추가해보세요.</p>
        ) : (
          todos.map((todo) => (
            <TodoItem 
              key={todo.id} 
              todo={todo} 
              onDelete={deleteTodo} 
            />
          ))
        )}
      </ul>
    </div>
  );
}

export default Home;
