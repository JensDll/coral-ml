import { createServer } from 'http'
import WebSocket from 'ws'

export function videoStart(host: string) {
  const SOCKET_PORT = 8080
  const LISTEN = 5060

  var wss = new WebSocket.Server({
    port: SOCKET_PORT,
    host,
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
  server.listen(LISTEN, host)

  console.log(
    `Listening for incomming MPEG-TS Stream on http://${host}:${LISTEN}`
  )
  console.log(`Awaiting WebSocket connections on ws://${host}:${SOCKET_PORT}`)
}
