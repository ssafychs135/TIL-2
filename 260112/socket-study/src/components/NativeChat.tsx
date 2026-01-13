import React, { Component } from 'react';

interface State {
  messages: string[];
  input: string;
}

class NativeChat extends Component<{}, State> {
  private ws: WebSocket | null = null;

  constructor(props: {}) {
    super(props);
    this.state = {
      messages: [],
      input: '',
    };
  }

  componentDidMount() {
    // WebSocket 연결 (포트 8080)
    this.ws = new WebSocket('ws://localhost:8080');

    this.ws.onopen = () => {
      this.setState(prevState => ({
        messages: [...prevState.messages, 'System: Connected to Server']
      }));
    };

    this.ws.onmessage = (event) => {
      this.setState(prevState => ({
        messages: [...prevState.messages, event.data]
      }));
    };

    this.ws.onclose = () => {
      this.setState(prevState => ({
        messages: [...prevState.messages, 'System: Disconnected']
      }));
    };
  }

  componentWillUnmount() {
    if (this.ws) {
      this.ws.close();
    }
  }

  sendMessage = () => {
    const { input } = this.state;
    if (this.ws && input.trim()) {
      this.ws.send(input);
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
      <div style={{ border: '2px solid #333', borderRadius: '8px', padding: '20px', width: '300px', backgroundColor: '#f9f9f9', color: '#333' }}>
        <h3>Native WebSocket</h3>
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
          <button onClick={this.sendMessage} style={{ padding: '8px 12px', cursor: 'pointer' }}>Send</button>
        </div>
      </div>
    );
  }
}

export default NativeChat;