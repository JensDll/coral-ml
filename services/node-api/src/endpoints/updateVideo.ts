import zmq from 'zeromq'
import { Listener } from './types'

type RequestData = {
  topK: number
  threshold: number
}

export const updateVideo =
  (client: zmq.Request) =>
  async (data: RequestData, callback: Listener<void>) => {
    try {
      await client.send(JSON.stringify(data))
      await client.receive()
    } catch (e) {
      console.log(`Error updating video parameters ${e}`)
    } finally {
      callback()
    }
  }
