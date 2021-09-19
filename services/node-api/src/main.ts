import './loadEnv'
import { createServer } from 'http'
import { Server } from 'socket.io'
import { registerRepositories } from './api'

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
  registerRepositories(socket)
})

httpServer.listen(+process.env.APP_LISTEN, process.env.APP_HOST)
console.log(
  `API listening on http://${process.env.APP_HOST}:${process.env.APP_LISTEN}`
)
