import { Request } from 'zeromq'
import { URI } from './uri'
import { ReplyCallback, MessageEnvelope, Repository } from './types'

export class ModelRepository implements Repository {
  client: Request

  constructor() {
    this.client = new Request()
    this.client.connect(URI.MODEL_MANAGER)
  }

  close() {
    this.client.close()
  }

  async loadModel(id: string, reply: ReplyCallback) {
    try {
      console.log(`Loading model with id ${id}`)
      await this.client.send(id)
      console.log(`Loading model message queued`)
      const [result] = await this.client.receive()
      const response: MessageEnvelope = JSON.parse(result.toString())
      console.log(`Loaded model with response ${result.toString()}`)
      reply(response)
    } catch {}
  }
}
