import { io, Socket } from 'socket.io-client'
import { ref, onMounted, Ref } from 'vue'
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
  }

  disconnect() {
    this.connected.value = false
    this.socket.disconnect()
  }

  readVideo(imgRef: Ref<HTMLImageElement>) {
    onMounted(() => {
      const img = imgRef.value

      let url = ''
      this.socket.on('video stream', frame => {
        const uint8Array = new Uint8Array(frame)
        const blob = new Blob([uint8Array], { type: 'image/jpeg' })
        URL.revokeObjectURL(url)
        url = URL.createObjectURL(blob)
        img.src = url
      })
    })
  }

  async loadModel(id: string | number) {
    return new Promise<boolean>((resolve, reject) => {
      this.socket.emit('load model', id, (success: boolean) => {
        resolve(success)
      })
    })
  }

  async imageClassification(image: File) {
    const format = useImage.getFormat(image)

    return new Promise<MessageEnvelope<ClassificationResult>>(
      (resolve, reject) => {
        this.socket.emit(
          'image classification',
          { image, format },
          (resp: any) => {
            resolve(resp)
          }
        )
      }
    )
  }
}
