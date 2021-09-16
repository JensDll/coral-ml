import { Request } from 'zeromq'
import { ReplyCallback, Repository } from './types'
import { URI } from './uri'
import { makeMessageEnvelope } from '~/common/factory'

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

export class ImageRepository implements Repository {
  classifyClient: Request
  settingsClient: Request

  constructor() {
    this.classifyClient = new Request()
    this.classifyClient.connect(URI.IMAGE_CLASSIFICATION)
    this.settingsClient = new Request()
    this.settingsClient.connect(URI.IMAGE_UPDATE_SETTINGS)
  }

  close() {
    this.classifyClient.close()
    this.settingsClient.close()
  }

  async classify(
    { image, format }: ClassifyRequest,
    reply: ReplyCallback<ClassifyResponse>
  ) {
    try {
      await this.classifyClient.send([image, format])
      const [buffer] = await this.classifyClient.receive()
      reply(JSON.parse(buffer.toString()))
    } catch {}
  }

  async updateSettings(settings: Settings, reply: ReplyCallback) {
    console.log(settings)
  }
}
