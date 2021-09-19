import zmq from 'zeromq'
import { IOListener, CONFIG, queueLast } from '~/domain'
import { Repository } from '../types'

type ClassifyRequest = {
  image: Buffer
  format: string
}

type ClassifyResponse = {
  probabilities: number[]
  classes: string[]
  inferenceTime: number
}

type Settings = {
  topK: number
  scoreThreshold: number
}

export const imageRepository: Repository<'image'> = {
  classify() {
    const client = new zmq.Request()
    client.connect(CONFIG.URI.IMAGE_CLASSIFICATION)

    const close = () => {
      client.close()
    }

    const listener: IOListener<ClassifyRequest, ClassifyResponse> = async (
      { image, format },
      respond
    ) => {
      try {
        await client.send([image, format])
        const [buffer] = await client.receive()
        respond(JSON.parse(buffer.toString()))
      } catch {}
    }

    return ['image:classify', close, listener]
  },
  updateSettings() {
    const client = new zmq.Request()
    client.connect(CONFIG.URI.IMAGE_UPDATE_SETTINGS)
    const send = queueLast(client)

    const close = () => {
      client.close()
    }

    const listener: IOListener<Settings, void> = async (settings, respond) => {
      const buffers = await send(settings)
      if (buffers.length) {
        const response = JSON.parse(buffers[0].toString())
        respond(response)
      }
    }

    return ['image:update:settings', close, listener]
  }
}
