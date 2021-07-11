import zmq from "zeromq"
import { Server, Socket as IOSocket } from "socket.io"
import { createServer } from "http"

const subscriberPort = 5500
const modelManagerPort = 5600

const listen = 6100

const httpServer = createServer()
const io = new Server(httpServer, {
  maxHttpBufferSize: 1e8,
  cors: {
    origin: "*"
  }
})

async function readVideo(socket: IOSocket, subscriber: zmq.Subscriber) {
  for await (const [frame] of subscriber) {
    socket.emit("video stream", frame)
  }
}

io.on("connection", socket => {
  console.log(`A users connected (${socket.id})`)

  const subscriber = new zmq.Subscriber()
  subscriber.connect(`tcp://localhost:${subscriberPort}`)
  subscriber.subscribe("")

  const request = new zmq.Request()
  request.connect(`tcp://localhost:${modelManagerPort}`)

  readVideo(socket, subscriber)

  socket.on("load model", async (id, callback) => {
    console.log(id)

    await request.send(id)
    await request.receive()

    callback({
      id
    })
  })

  socket.on("image classification", async (image, callback) => {
    console.log(image)
  })

  socket.on("disconnect", () => {
    subscriber.close()
    console.log(`A user disconnected (${socket.id})`)
  })
})

httpServer.listen(listen)
console.log(`Server listening on port ${listen}`)
