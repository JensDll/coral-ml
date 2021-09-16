import './loadEnv'
import { createServer } from 'http'
import { Server } from 'socket.io'
import { ModelRepository, ImageRepository, VideoRepository } from './api'

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

  const modelRepository = new ModelRepository()
  const videoRepository = new VideoRepository()
  const imageRepository = new ImageRepository()

  socket.on('model:load', modelRepository.loadModel.bind(modelRepository))

  socket.on('image:classify', imageRepository.classify.bind(imageRepository))
  socket.on(
    'image:update:settings',
    imageRepository.updateSettings.bind(imageRepository)
  )

  socket.on(
    'video:update:settings',
    videoRepository.updateSettings.bind(videoRepository)
  )

  socket.on('disconnect', () => {
    console.log(`A user disconnected (${socket.id})`)
    modelRepository.close()
    videoRepository.close()
    imageRepository.close()
  })
})

httpServer.listen(+process.env.APP_LISTEN, process.env.APP_HOST)
console.log(
  `API listening on http://${process.env.APP_HOST}:${process.env.APP_LISTEN}`
)
