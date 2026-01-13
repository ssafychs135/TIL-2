import express from 'express';
import { createServer } from 'http';
import { Server } from 'socket.io';
import cors from 'cors';

const app = express();
app.use(cors());

const httpServer = createServer(app);
const io = new Server(httpServer, {
    cors: {
        origin: "*", // Allow all origins for simplicity in dev
        methods: ["GET", "POST"]
    }
});

io.on('connection', (socket) => {
    console.log(`User connected (Socket.IO): ${socket.id}`);

    socket.on('chat message', (msg) => {
        console.log(`Message: ${msg}`);
        // Broadcast to all
        io.emit('chat message', `[Socket.IO] ${msg}`);
    });

    socket.on('disconnect', () => {
        console.log(`User disconnected (Socket.IO): ${socket.id}`);
    });
});

const PORT = 3000;
httpServer.listen(PORT, () => {
    console.log(`Socket.IO Server running on http://localhost:${PORT}`);
});
