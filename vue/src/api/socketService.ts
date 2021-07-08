import { io, Socket } from "socket.io-client"
import { ref, onBeforeUnmount, reactive, markRaw, onMounted, Ref } from "vue"

class SocketService {
  connected = ref(false)
  connecting = ref(true)
  socket: Socket

  constructor(address: string) {
    this.socket = markRaw(io(address))

    this.socket.on("connect", () => {
      this.connecting.value = false
      this.connected.value = true
    })

    onBeforeUnmount(() => {
      console.log(`[Socket] Disconnect (${this.socket.id})`)
      this.socket.disconnect()
    })
  }

  disconnect() {
    this.connected.value = false
    this.socket.disconnect()
  }

  readVideo(imgRef: Ref<HTMLImageElement>) {
    onMounted(() => {
      const img = imgRef.value

      let url = ""
      this.socket.on("video:stream", frame => {
        const uint8Array = new Uint8Array(frame)
        const blob = new Blob([uint8Array], { type: "image/jpeg" })
        URL.revokeObjectURL(url)
        url = URL.createObjectURL(blob)
        img.src = url
      })
    })
  }

  loadModel(model: any) {
    this.socket.emit("model:load", model)
  }
}

export const useSockerService = () =>
  reactive(new SocketService("http://localhost:6100"))
