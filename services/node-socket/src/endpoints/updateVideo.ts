import zmq from 'zeromq'
import { Listener } from './types'

type RequestData = {
  topK: number
  threshold: number
}

export const updateVideo =
  (client: zmq.Request) =>
  async (data: RequestData, callback: Listener<void>) => {
    await client.send(JSON.stringify(data))
    await client.receive()
    callback()
  }
