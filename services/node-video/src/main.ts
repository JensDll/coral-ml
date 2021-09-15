import { createServer } from 'http'
import WebSocket, { WebSocketServer } from 'ws'

if (process.env.MODE !== 'PROD') {
  const dotenv = await import('dotenv')
  dotenv.config()
}

var wss = new WebSocketServer({
  port: +process.env.PORT_STREAM_OUT,
  host: process.env.APP_HOST,
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

const server = createServer((req, resp) => {
  req.on('data', data => {
    broadcastData(data)
  })
})

server.headersTimeout = 0
server.listen(+process.env.PORT_STREAM_IN, process.env.APP_HOST)

console.log(
  `Listening for incoming MPEG-TS Stream on http://${process.env.APP_HOST}:${process.env.PORT_STREAM_IN}`
)
console.log(
  `Awaiting WebSocket connections on ws://${process.env.APP_HOST}:${process.env.PORT_STREAM_OUT}`
)
