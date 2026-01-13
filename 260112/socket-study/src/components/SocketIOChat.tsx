import React, { Component } from 'react';
import { io, Socket } from 'socket.io-client';

interface State {
  messages: string[];
  input: string;
}

class SocketIOChat extends Component<{}, State> {
  private socket: Socket | null = null;

  constructor(props: {}) {
    super(props);
    this.state = {
      messages: [],
      input: '',
    };
  }

  componentDidMount() {
    // Socket.IO 연결 (포트 3000)
    this.socket = io('http://localhost:3000');

    this.socket.on('connect', () => {
      this.setState(prevState => ({
        messages: [...prevState.messages, `System: Connected (ID: ${this.socket?.id})`]
      }));
    });

    this.socket.on('chat message', (msg: string) => {
      this.setState(prevState => ({
        messages: [...prevState.messages, msg]
      }));
    });
  }

  componentWillUnmount() {
    if (this.socket) {
      this.socket.disconnect();
    }
  }

  sendMessage = () => {
    const { input } = this.state;
    if (this.socket && input.trim()) {
      this.socket.emit('chat message', input);
      this.setState({ input: '' });
    }
  };

  handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    this.setState({ input: e.target.value });
  };

  handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      this.sendMessage();
    }
  };

  render() {
    const { messages, input } = this.state;

    return (
      <div style={{ border: '2px solid #007bff', borderRadius: '8px', padding: '20px', width: '300px', backgroundColor: '#f0f8ff', color: '#333' }}>
        <h3>Socket.IO</h3>
        <div style={{ height: '300px', overflowY: 'auto', border: '1px solid #ccc', borderRadius: '4px', marginBottom: '10px', padding: '10px', backgroundColor: '#fff' }}>
          {messages.map((msg, idx) => (
            <div key={idx} style={{ marginBottom: '5px', fontSize: '14px' }}>{msg}</div>
          ))}
        </div>
        <div style={{ display: 'flex', gap: '5px' }}>
          <input 
            style={{ flex: 1, padding: '8px', borderRadius: '4px', border: '1px solid #ccc' }}
            value={input} 
            placeholder="Type a message..."
            onChange={this.handleInputChange} 
            onKeyPress={this.handleKeyPress}
          />
          <button 
            onClick={this.sendMessage} 
            style={{ padding: '8px 12px', cursor: 'pointer', backgroundColor: '#007bff', color: 'white', border: 'none', borderRadius: '4px' }}
          >
            Send
          </button>
        </div>
      </div>
    );
  }
}

export default SocketIOChat;