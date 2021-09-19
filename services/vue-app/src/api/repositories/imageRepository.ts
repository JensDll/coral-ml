import { Socket } from 'socket.io-client'
import { useImage } from '~/composition'
import { MessageEnvelope } from '../types'

export type ClassificationResult = {
  probabilities: number[]
  classes: string[]
  inferenceTime: number
}
export type ImageSettings = {
  topK: number
  scoreThreshold: number
}

export class ImageRepository {
  socket: Socket

  constructor(socket: Socket) {
    this.socket = socket
  }

  classify(image: File): Promise<MessageEnvelope<ClassificationResult>> {
    const format = useImage(image).getFormat()
    return new Promise((resolve, reject) => {
      this.socket.emit(
        'image:classify',
        { image, format },
        (response: MessageEnvelope<ClassificationResult>) => {
          resolve(response)
        }
      )
    })
  }

  updateSettings(
    settings: ImageSettings
  ): Promise<MessageEnvelope<ClassificationResult>> {
    return new Promise((resolve, reject) => {
      this.socket.emit(
        'image:update:settings',
        settings,
        (response: MessageEnvelope<ClassificationResult>) => {
          resolve(response)
        }
      )
    })
  }
}
