// src/lib/socket.ts
import { io } from "socket.io-client";

// Connect to Flask backend
export const socket = io("http://localhost:5000", {
    transports: ["websocket"], // prefer WS
});
