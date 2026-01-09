import { useParams, useNavigate } from 'react-router-dom';

function TodoDetail() {
  const { id } = useParams<{ id: string }>(); // URL 파라미터 읽기
  const navigate = useNavigate(); // 페이지 이동 훅

  return (
    <div style={{ padding: '20px', textAlign: 'center' }}>
      <h2>할 일 상세 정보</h2>
      <p>현재 할 일의 ID는 <strong>{id}</strong> 입니다.</p>
      
      <div style={{ marginTop: '20px' }}>
        <button 
          onClick={() => navigate(-1)} // 뒤로 가기
          style={{
            padding: '10px 20px',
            backgroundColor: '#666',
            color: 'white',
            border: 'none',
            borderRadius: '5px',
            cursor: 'pointer'
          }}
        >
          뒤로 가기
        </button>
      </div>
    </div>
  );
}

export default TodoDetail;
