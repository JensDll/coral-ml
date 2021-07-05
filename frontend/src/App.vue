<template>
  <h1>Streamer</h1>
  <img src="" alt="stream" ref="imgRef" v-show="connected" />
  <div v-if="connected">
    <button @click="stream.disconnect()">Disconnect</button>
  </div>
  <button @click="connect()" v-else :disabled="connecting">Connect</button>
</template>

<script setup lang="ts">
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
    const socket = io("http://localhost:5000")
    const img = imgRef.value

    connecting.value = true

    socket.on("connect", () => {
      connected.value = true
      connecting.value = false
    })

    let url = ''
    socket.on("video:stream", (frame) => {
      const uint8Array = new Uint8Array(frame)
      const blob = new Blob([uint8Array], { type: 'image/jpeg' })
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
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
