import zmq from 'zeromq'
import { createServer } from 'http'
import { Server } from 'socket.io'
import {
  loadModel,
  classify,
  updateVideoSettings,
  updateClassifySettings
} from './endpoints'

if (process.env.MODE !== 'PROD') {
  const dotenv = await import('dotenv')
  dotenv.config()
}

const httpServer = createServer()
const io = new Server(httpServer, {
  maxHttpBufferSize: 1e9,
  cors: {
    origin: '*',
    preflightContinue: true
  }
})

const baseAddress = `tcp://${process.env.CORAL_HOST}`

io.on('connection', socket => {
  console.log(`A user connected (${socket.id})`)

  const modelManagerClient = new zmq.Request({
    receiveTimeout: 20000,
    sendTimeout: 20000
  })
  modelManagerClient.connect(
    `${baseAddress}:${process.env.CORAL_PORT_MODEL_MANAGER}`
  )
  socket.on('load model', loadModel(modelManagerClient))

  const classifyClient = new zmq.Request({
    receiveTimeout: 20000,
    sendTimeout: 20000
  })
  classifyClient.connect(
    `${baseAddress}:${process.env.CORAL_PORT_IMAGE_CLASSIFICATION}`
  )
  socket.on('classify', classify(classifyClient))

  const updateClassify = new zmq.Request()
  updateClassify.connect(
    `${baseAddress}:${process.env.CORAL_PORT_IMAGE_SETTINGS}`
  )
  socket.on('update classify', updateClassifySettings(updateClassify))

  const updateVideo = new zmq.Request()
  updateVideo.connect(`${baseAddress}:${process.env.CORAL_PORT_VIDEO_SETTINGS}`)
  socket.on('update video', updateVideoSettings(updateVideo))

  socket.on('disconnect', () => {
    classifyClient.close()
    classifyClient.close()
    console.log(`A user disconnected (${socket.id})`)
  })
})

httpServer.listen(+process.env.APP_LISTEN, process.env.APP_HOST)
console.log(
  `API listening on http://${process.env.APP_HOST}:${process.env.APP_LISTEN}`
)
