import { createServer } from 'http'
import zmq from 'zeromq'
import { Server } from 'socket.io'
import { loadModel, classify, updateVideo } from './endpoints'

export function apiStart() {
  const MODL_MANAGER_PORT = 7100
  const CLASSIFY_PORT = 7200
  const VIDEO_PORT = 7300

  const LISTEN = 5050

  const httpServer = createServer()
  const io = new Server(httpServer, {
    maxHttpBufferSize: 1e9,
    cors: {
      origin: '*'
    }
  })

  io.on('connection', socket => {
    console.log(`A user connected (${socket.id})`)

    const modelManagerClient = new zmq.Request()
    modelManagerClient.connect(`tcp://localhost:${MODL_MANAGER_PORT}`)
    socket.on('load model', loadModel(modelManagerClient))

    const classifyClient = new zmq.Request()
    classifyClient.connect(`tcp://localhost:${CLASSIFY_PORT}`)
    socket.on('classify', classify(classifyClient))

    const videoClient = new zmq.Request()
    videoClient.connect(`tcp://localhost:${VIDEO_PORT}`)
    socket.on('update video', updateVideo(videoClient))

    socket.on('disconnect', () => {
      classifyClient.close()
      classifyClient.close()
      console.log(`A user disconnected (${socket.id})`)
    })
  })

  httpServer.listen(LISTEN)
  console.log(`API listening on http://127.0.0.1:${LISTEN}`)
}
