import { io, Socket } from 'socket.io-client'
import { ref, onMounted, Ref, onBeforeUnmount } from 'vue'
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

export class SocketService {
  connected = ref(false)
  socket: Socket

  constructor(address: string) {
    this.socket = io(address)

    this.socket.on('connect', () => {
      console.log(`[Socket] Connected (${this.socket.id})`)
      this.connected.value = true
    })

    onBeforeUnmount(() => {
      this.disconnect()
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
}
