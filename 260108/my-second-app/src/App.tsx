import { useState } from 'react';
import './App.css';
import TodoItem, { type Todo } from './components/TodoItem';
import { useLocalStorage } from './hooks/useLocalStorage'; // Custom Hook 임포트

function App() {
  const [inputValue, setInputValue] = useState<string>('');
  
  // ⭐️ useState 대신 useLocalStorage 사용
  // 'todos'라는 키로 로컬 스토리지에 저장됩니다.
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

  const deleteTodo = (id: number) => {
    setTodos(todos.filter(todo => todo.id !== id));
  };

  return (
    <div className="app">
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

export default App;