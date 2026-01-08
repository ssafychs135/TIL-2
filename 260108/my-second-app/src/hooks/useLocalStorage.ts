import { useState, useEffect } from 'react';

// 제네릭(<T>)을 사용하여 어떤 타입의 데이터든 저장할 수 있게 만듭니다.
export function useLocalStorage<T>(key: string, initialValue: T) {
  // 1. 초기값 설정 (Lazy Initialization)
  // 컴포넌트가 처음 렌더링될 때 한 번만 실행됩니다.
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key);
      // 저장된 값이 있으면 파싱해서 반환, 없으면 초기값 반환
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      console.error(error);
      return initialValue;
    }
  });

  // 2. 값이 변경될 때마다 로컬 스토리지 업데이트
  useEffect(() => {
    try {
      window.localStorage.setItem(key, JSON.stringify(storedValue));
    } catch (error) {
      console.error(error);
    }
  }, [key, storedValue]); // key나 storedValue가 바뀔 때 실행

  // useState처럼 [값, 설정함수]를 반환
  return [storedValue, setStoredValue] as const;
}
