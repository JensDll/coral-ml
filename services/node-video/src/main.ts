import { createServer } from 'http'
import WebSocket, { WebSocketServer } from 'ws'

const HOST = process.env.HOST
const STREAM_OUT_PORT = +process.env.STREAM_OUT_PORT
const STREAM_IN_PORT = +process.env.STREAM_IN_PORT

var wss = new WebSocketServer({
  port: STREAM_OUT_PORT,
  host: HOST,
  perMessageDeflate: false
})

wss.on('connection', (ws, req) => {
  console.log(`Client connected ${req.socket.remoteAddress}`)
  ws.on('close', () => {
    console.log(`Client disconnected ${req.socket.remoteAddress}`)
  })
})

function broadcastData(data: any) {
  wss.clients.forEach(client => {
    if (client.readyState === WebSocket.OPEN) {
      client.send(data)
    }
  })
}

const server = createServer((request, response) => {
  request.on('data', data => {
    broadcastData(data)
  })
})

server.headersTimeout = 0
server.listen(STREAM_IN_PORT, HOST)

console.log(
  `Listening for incoming MPEG-TS Stream on http://${HOST}:${STREAM_IN_PORT}`
)
console.log(`Awaiting WebSocket connections on ws://${HOST}:${STREAM_OUT_PORT}`)
