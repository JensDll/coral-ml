import zmq from 'zeromq'
import { Listener } from './types'

type RequestData = {
  topK: number
  threshold: number
}

export const updateVideo =
  (client: zmq.Request) =>
  async (data: RequestData, callback: Listener<void>) => {
    console.log(data)
    await client.send(JSON.stringify(data))
    await client.receive()
    callback()
  }
