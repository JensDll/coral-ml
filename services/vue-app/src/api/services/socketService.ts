import { io, Socket } from 'socket.io-client'
import { ref } from 'vue'
import { useImage } from '~/composable'

export type MessageEnvelope<T = []> = {
  success: boolean
  errors: string[]
  data: T
}

type ClassificationResult = MessageEnvelope<{
  probabilities: number[]
  classes: string[]
  inferenceTime: number
}>

type LoadModelResult = MessageEnvelope

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
      import.meta.env.MODE !== 'development'
        ? { path: '/node-api/' }
        : undefined
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

  loadModel(id: number) {
    return new Promise<LoadModelResult>((resolve, reject) => {
      this.socket.emit('load model', id, (response: LoadModelResult) => {
        resolve(response)
      })
    })
  }

  async classify(image: File) {
    const format = useImage.getFormat(image)

    return new Promise<ClassificationResult>((resolve, reject) => {
      this.socket.emit(
        'classify',
        { image, format },
        (response: ClassificationResult) => {
          resolve(response)
        }
      )
    })
  }

  async updateVideo(request: UpdateVideoRequest) {
    return new Promise<void>((resolve, reject) => {
      this.socket.emit('update video', request, () => {
        resolve()
      })
    })
  }
}

export const socketService = new SocketService(import.meta.env.VITE_NODE_API)
