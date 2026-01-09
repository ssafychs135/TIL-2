function About() {
  return (
    <div style={{ textAlign: 'center', padding: '20px' }}>
      <h1>소개 페이지</h1>
      <p>이 프로젝트는 React 학습을 위한 Todo List 앱입니다.</p>
      <p>React Router를 사용하여 페이지 이동을 구현했습니다.</p>
      <ul style={{ listStyle: 'none', padding: 0, marginTop: '20px' }}>
        <li>✅ Vite + React</li>
        <li>✅ TypeScript</li>
        <li>✅ React Router</li>
      </ul>
    </div>
  );
}

export default About;
