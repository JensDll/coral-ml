import zmq from 'zeromq'
import { Listener } from '../types'

type RequestData = {
  topK: number
  threshold: number
}

export const updateVideoSettings = (client: zmq.Request) => {
  let queued: RequestData | null = null
  let numSend = 0

  return async (data: RequestData, callback: Listener<void>) => {
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
        await client.receive()
        numSend--
      } while (queued)
    } catch (e) {
      queued = data
      console.log(`Error updating model parameters ${e}`)
    } finally {
      callback()
    }
  }
}
