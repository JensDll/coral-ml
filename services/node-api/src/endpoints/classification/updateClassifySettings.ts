import zmq from 'zeromq'
import { Listener, MessageEnvelope } from '../types'

type RequestData = {
  topK: number
  threshold: number
}

type Response = {
  probabilities: number[]
  classes: string[]
  inferenceTime: number
}

export const updateClassifySettings = (client: zmq.Request) => {
  let queued: RequestData | null = null
  let numSend = 0

  let response: MessageEnvelope<Response> = {
    success: false,
    errors: []
  }

  return async (
    data: RequestData,
    callback: Listener<MessageEnvelope<Response>>
  ) => {
    try {
      do {
        if (numSend === 1) {
          throw 'HMW Reached'
        }
        if (queued) {
          await client.send(JSON.stringify(queued))
        } else {
          await client.send(JSON.stringify(data))
        }
        numSend++
        queued = null
        const [result] = await client.receive()
        response = JSON.parse(result.toString())
        numSend--
      } while (queued)
    } catch (e) {
      queued = data
      console.log(`Error updating model parameters ${e}`)
    } finally {
      callback(response)
    }
  }
}
