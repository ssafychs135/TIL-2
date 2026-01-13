import { Component } from 'react';
import NativeChat from './components/NativeChat';
import SocketIOChat from './components/SocketIOChat';
import './App.css';

class App extends Component {
  render() {
    return (
      <div className="App">
        <h1>Real-time Chat Study (Class Components)</h1>
        <p>Compare Native WebSocket vs Socket.IO</p>
        <div style={{ display: 'flex', justifyContent: 'center', gap: '50px', flexWrap: 'wrap' }}>
          <NativeChat />
          <SocketIOChat />
        </div>
      </div>
    );
  }
}

export default App;
