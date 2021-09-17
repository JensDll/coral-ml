import { Socket } from 'socket.io-client'
import { MessageEnvelope } from './types'

export class ModelRepository {
  socket: Socket

  constructor(socket: Socket) {
    this.socket = socket
  }

  loadModel(id: number) {
    return new Promise<MessageEnvelope>((resolve, reject) => {
      this.socket.emit('model:load', id, (response: MessageEnvelope) => {
        resolve(response)
      })
    })
  }
}
