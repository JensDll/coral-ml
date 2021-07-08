export type EnumerableEnvelope<T> = {
  data: T[]
  pageNumber: number
  pageSize: number
  total: number
}

export type TFLiteModel = {
  id: number
  modelName: string
}

import { io } from "socket.io-client"
import { ref } from "vue"
import type { Ref } from "vue"

const connected = ref(false)
const connecting = ref(false)
const stream = ref() as Ref<Stream>
const imgRef = ref() as Ref<HTMLImageElement>

class Stream {
  socket

  constructor() {
    const socket = io("http://localhost:5500")
    const img = imgRef.value

    connecting.value = true

    socket.on("connect", () => {
      connected.value = true
      connecting.value = false
    })

    let url = ""
    socket.on("video:stream", frame => {
      const uint8Array = new Uint8Array(frame)
      const blob = new Blob([uint8Array], { type: "image/jpeg" })
      URL.revokeObjectURL(url)
      url = URL.createObjectURL(blob)
      img.src = url
    })

    this.socket = socket
  }

  disconnect() {
    connected.value = false
    this.socket.disconnect()
  }
}

function connect() {
  stream.value = new Stream()
}
