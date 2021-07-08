import zmq from "zeromq"
import { Server, Socket as IOSocket } from "socket.io"
import { createServer } from "http"

const subscriberPort = 5500
const replyPort = 5600

const listen = 6100

const httpServer = createServer()
const io = new Server(httpServer, {
  cors: {
    origin: "*"
  }
})

async function readVideo(socket: IOSocket, subscriber: zmq.Subscriber) {
  for await (const [frame] of subscriber) {
    socket.emit("video:stream", frame)
  }
}

io.on("connection", socket => {
  console.log(`A users connected (${socket.id})`)

  const subscriber = new zmq.Subscriber()
  subscriber.connect(`tcp://localhost:${subscriberPort}`)
  subscriber.subscribe("")

  const reply = new zmq.Reply()
  reply.connect(`tcp://localhost:${replyPort}`)

  readVideo(socket, subscriber)

  socket.on("disconnect", () => {
    subscriber.close()
    console.log(`A user disconnected (${socket.id})`)
  })

  socket.on("model:load", model => {
    console.log(model)
  })
})

httpServer.listen(listen)
console.log(`Server listening on port ${listen}`)
