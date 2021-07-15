import { createServer } from 'http'
import zmq from 'zeromq'
import { Server } from 'socket.io'
import { loadModel, classify } from './endpoints'

export function apiStart() {
  const MODL_MANAGER_PORT = 5600
  const CLASSIFY_PORT = 5700

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

    const reqModelManger = new zmq.Request()
    reqModelManger.connect(`tcp://localhost:${MODL_MANAGER_PORT}`)
    socket.on('load model', loadModel(reqModelManger))

    const reqClassify = new zmq.Request()
    reqClassify.connect(`tcp://localhost:${CLASSIFY_PORT}`)
    socket.on('classify', classify(reqClassify))

    socket.on('disconnect', () => {
      reqModelManger.close()
      reqClassify.close()
      console.log(`A user disconnected (${socket.id})`)
    })
  })

  httpServer.listen(LISTEN)
  console.log(`API listening on http://127.0.0.1:${LISTEN}`)
}
