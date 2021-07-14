import zmq from 'zeromq'
import { Server } from 'socket.io'
import { createServer } from 'http'
import { loadModel, classify } from './endpoints'

const modelManagerPort = 5600
const classifyPort = 5700

const listen = 6100

const httpServer = createServer()
const io = new Server(httpServer, {
  maxHttpBufferSize: 1e9,
  cors: {
    origin: '*'
  }
})

io.on('connection', socket => {
  console.log(`A user connected (${socket.id})`)

  const reqModelManger = new zmq.Request()
  reqModelManger.connect(`tcp://localhost:${modelManagerPort}`)
  socket.on('load model', loadModel(reqModelManger))

  const reqClassify = new zmq.Request()
  reqClassify.connect(`tcp://localhost:${classifyPort}`)
  socket.on('image classification', classify(reqClassify))

  socket.on('disconnect', () => {
    reqModelManger.close()
    reqClassify.close()
    console.log(`A user disconnected (${socket.id})`)
  })
})

httpServer.listen(listen)
console.log(`Server listening on port ${listen}`)
