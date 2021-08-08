import { createServer } from "http";
import WebSocket, { WebSocketServer } from "ws";

const SOCKET_PORT = 8080;
const LISTEN = 5060;
const HOST = process.env.HOST;

var wss = new WebSocketServer({
  port: SOCKET_PORT,
  host: HOST,
  perMessageDeflate: false,
});

wss.on("connection", (ws, req) => {
  console.log(`Client connected ${req.socket.remoteAddress}`);
  ws.on("close", () => {
    console.log(`Client disconnected ${req.socket.remoteAddress}`);
  });
});

function broadcastData(data: any) {
  wss.clients.forEach((client) => {
    if (client.readyState === WebSocket.OPEN) {
      client.send(data);
    }
  });
}

const server = createServer((request, response) => {
  request.on("data", (data) => {
    broadcastData(data);
  });
});

server.headersTimeout = 0;
server.listen(LISTEN, HOST);

console.log(
  `Listening for incomming MPEG-TS Stream on http://${HOST}:${LISTEN}`
);
console.log(`Awaiting WebSocket connections on ws://${HOST}:${SOCKET_PORT}`);
