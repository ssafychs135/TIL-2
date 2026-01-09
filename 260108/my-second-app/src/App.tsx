import { Routes, Route, Link } from 'react-router-dom';
import './App.css';
import Home from './pages/Home';
import About from './pages/About';
import TodoDetail from './pages/TodoDetail';

function App() {
  return (
    <div className="app">
      {/* 네비게이션 바 */}
      <nav className="nav-bar">
        <Link to="/" className="nav-link">Home</Link> | 
        <Link to="/about" className="nav-link">About</Link>
      </nav>

      {/* 라우팅 설정 */}
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="/todo/:id" element={<TodoDetail />} />
      </Routes>
    </div>
  );
}

export default App;
