import { Socket } from 'socket.io-client'

export type VideoSettings = {
  topK: number
  scoreThreshold: number
}

export class VideoRepository {
  socket: Socket

  constructor(socket: Socket) {
    this.socket = socket
  }

  updateSettings(settings: VideoSettings): Promise<void> {
    return new Promise((resolve, reject) => {
      this.socket.emit('video:update:settings', settings, () => {
        resolve()
      })
    })
  }
}
