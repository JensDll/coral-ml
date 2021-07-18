import { io, Socket } from 'socket.io-client'
import { ref } from 'vue'
import { useImage } from '~/composable'

type MessageEnvelope<T> = {
  success: boolean
  errors: string[]
  data: T
}

type ClassificationResult = {
  classes: string[]
  probabilities: number[]
  inferenceTime: number
}

export type UpdateVideoRequest = {
  topK: number
  threshold: number
}

export class SocketService {
  connected = ref(false)
  socket: Socket

  constructor(address: string) {
    this.socket = io(
      address,
      import.meta.env.PROD ? { path: '/socket-api/' } : undefined
    )

    this.socket.on('connect', () => {
      console.log(`[Socket] Connected (${this.socket.id})`)
      this.connected.value = true
    })
  }

  disconnect() {
    this.connected.value = false
    this.socket.disconnect()
  }

  async loadModel(id: string | number) {
    return new Promise<boolean>((resolve, reject) => {
      this.socket.emit('load model', id, (success: boolean) => {
        resolve(success)
      })
    })
  }

  async classify(image: File) {
    const format = useImage.getFormat(image)

    return new Promise<MessageEnvelope<ClassificationResult>>(
      (resolve, reject) => {
        this.socket.emit('classify', { image, format }, (resp: any) => {
          resolve(resp)
        })
      }
    )
  }

  async updateVideo(request: UpdateVideoRequest) {
    return new Promise<void>((resolve, reject) => {
      this.socket.emit('update video', request, () => {
        resolve()
      })
    })
  }
}

export const socketService = new SocketService(
  import.meta.env.VITE_IO_SOCKET_URI
)
