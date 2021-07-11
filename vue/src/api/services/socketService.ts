import { io, Socket } from 'socket.io-client'
import { ref, onMounted, Ref } from 'vue'

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
    return new Promise((resolve, reject) => {
      this.socket.emit('load model', id, (resp: { id: string }) => {
        resolve(resp)
      })
    })
  }

  async imageClassification(image: File) {
    const buffer = await image.arrayBuffer()
    return new Promise((resolve, reject) => {
      this.socket.emit('image classification', buffer, (resp: any) => {
        resolve(resp)
      })
    })
  }
}
