import zmq from 'zeromq'
import { Repository } from '../types'
import { MessageEnvelope, IOListener, CONFIG } from '~/domain'

export const modelRepository: Repository<'model'> = {
  loadModel() {
    const client = new zmq.Request()
    client.connect(CONFIG.URI.MODEL_MANAGER)

    const close = () => {
      client.close()
    }

    const listener: IOListener<string, any> = async (id, respond) => {
      try {
        console.log(`Loading model with id ${id}`)
        await client.send(id)
        console.log(`Loading model message queued`)
        const [result] = await client.receive()
        const response: MessageEnvelope = JSON.parse(result.toString())
        console.log(`Loaded model with response ${result.toString()}`)
        respond(response)
      } catch {}
    }

    return ['model:load', close, listener]
  }
}
