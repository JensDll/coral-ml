import { Listener } from './types'
import zmq from 'zeromq'

type Response = any

type RequestData = {
  image: Buffer
  format: string
}

export const imageClassification =
  (request: zmq.Request) =>
  async ({ image, format }: RequestData, callback: Listener<Response>) => {
    await request.send([image, format])
    const resp = await request.receive()
    console.log(resp)
    callback(resp)
  }
