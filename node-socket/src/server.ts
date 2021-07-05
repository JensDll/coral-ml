import zmq from "zeromq"
import { Server, Socket as IOSocket } from "socket.io"
import { createServer } from "http"

const port = 5555
const listen = 5000

const sock = new zmq.Subscriber()
sock.connect(`tcp://localhost:${port}`)
sock.subscribe("")

console.log(`Subscriber connected to port ${port}`)

const httpServer = createServer()
const io = new Server(httpServer, {
  cors: {
    origin: "*",
  },
})

async function startReading(socket: IOSocket, subscriber: zmq.Subscriber) {
  for await (const [frame] of subscriber) {
    socket.emit("video:stream", frame)
  }
}

io.on("connection", socket => {
  console.log(`A user connected (${socket.id})`)

  const subscriber = new zmq.Subscriber()
  subscriber.connect(`tcp://localhost:${port}`)
  subscriber.subscribe("")

  startReading(socket, subscriber)

  socket.on("disconnect", () => {
    subscriber.close()
    console.log(`A user disconnected (${socket.id})`)
  })
})

httpServer.listen(listen)
console.log(`Server listening on port ${listen}`)
