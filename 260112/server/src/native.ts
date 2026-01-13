import { WebSocketServer, WebSocket } from 'ws';

const wss = new WebSocketServer({ port: 8080 });

console.log('Native WebSocket Server running on ws://localhost:8080');

wss.on('connection', (ws) => {
    console.log('Client connected (Native)');

    ws.on('message', (data) => {
        const message = data.toString();
        console.log(`Received: ${message}`);
        
        // Broadcast to all clients
        wss.clients.forEach((client) => {
            if (client.readyState === WebSocket.OPEN) {
                client.send(`[Native] ${message}`);
            }
        });
    });

    ws.on('close', () => console.log('Client disconnected (Native)'));
});
