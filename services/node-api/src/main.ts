import { createServer } from 'http'
import zmq from 'zeromq'
import { Server } from 'socket.io'
import { loadModel, classify, updateVideo } from './endpoints'

const MODL_MANAGER_PORT = 7000
const CLASSIFY_PORT = 7100
const VIDEO_PORT = 7200
const LISTEN = 5050
const HOST = process.env.HOST

const httpServer = createServer()
const io = new Server(httpServer, {
  maxHttpBufferSize: 1e9,
  cors: {
    origin: '*',
    preflightContinue: true
  }
})

io.on('connection', socket => {
  console.log(`A user connected (${socket.id})`)

  const modelManagerClient = new zmq.Request({
    receiveTimeout: 20000,
    sendTimeout: 20000
  })
  modelManagerClient.connect(
    `tcp://${process.env.CORAL_APP}:${MODL_MANAGER_PORT}`
  )
  socket.on('load model', loadModel(modelManagerClient))

  const classifyClient = new zmq.Request()
  classifyClient.connect(`tcp://${process.env.CORAL_APP}:${CLASSIFY_PORT}`)
  socket.on('classify', classify(classifyClient))

  const videoClient = new zmq.Request({
    sendTimeout: 0
  })
  videoClient.connect(`tcp://${process.env.CORAL_APP}:${VIDEO_PORT}`)
  socket.on('update video', updateVideo(videoClient))

  socket.on('disconnect', () => {
    classifyClient.close()
    classifyClient.close()
    console.log(`A user disconnected (${socket.id})`)
  })
})

httpServer.listen(LISTEN, HOST)
console.log(`API listening on http://${HOST}:${LISTEN}`)
