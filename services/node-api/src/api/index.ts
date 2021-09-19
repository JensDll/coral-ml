import io from 'socket.io'
import { modelRepository } from './repositories/modelRepository'
import { imageRepository } from './repositories/imageRepository'
import { videoRepository } from './repositories/videoRepository'
import { registerRepositories as _registerRepositories } from './repositories/register'

export const registerRepositories = (socket: io.Socket) => {
  _registerRepositories(socket, [
    modelRepository,
    imageRepository,
    videoRepository
  ])
}
