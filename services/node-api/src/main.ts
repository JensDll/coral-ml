import { createServer } from 'http'
import zmq from 'zeromq'
import { Server } from 'socket.io'
import {
  loadModel,
  classify,
  updateVideoSettings,
  updateClassifySettings
} from './endpoints'

const MODL_MANAGER_PORT = 7000

const UPDATE_VIDEO_ARGS_PORT = 7100

const CLASSIFY_PORT = 7300
const UPDATE_CLASSIFY_ARGS_PORT = 7301

const LISTEN = +process.env.LISTEN
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

  const classifyClient = new zmq.Request({
    receiveTimeout: 20000,
    sendTimeout: 20000
  })
  classifyClient.connect(`tcp://${process.env.CORAL_APP}:${CLASSIFY_PORT}`)
  socket.on('classify', classify(classifyClient))

  const updateVideo = new zmq.Request()
  updateVideo.connect(
    `tcp://${process.env.CORAL_APP}:${UPDATE_VIDEO_ARGS_PORT}`
  )
  socket.on('update video', updateVideoSettings(updateVideo))

  const updateClassify = new zmq.Request()
  updateClassify.connect(
    `tcp://${process.env.CORAL_APP}:${UPDATE_CLASSIFY_ARGS_PORT}`
  )
  socket.on('update classify', updateClassifySettings(updateClassify))

  socket.on('disconnect', () => {
    classifyClient.close()
    classifyClient.close()
    console.log(`A user disconnected (${socket.id})`)
  })
})

httpServer.listen(LISTEN, HOST)
console.log(`API listening on http://${HOST}:${LISTEN}`)
