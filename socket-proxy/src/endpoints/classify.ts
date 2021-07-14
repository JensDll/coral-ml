import { Listener } from './types'
import zmq from 'zeromq'

type Response = {
  success: boolean
  errors: string[]
  data: any
}

type RequestData = {
  image: Buffer
  format: string
}

export const classify =
  (request: zmq.Request) =>
  async ({ image, format }: RequestData, callback: Listener<Response>) => {
    await request.send([image, format])
    console.log(image)
    const [results] = await request.receive()
    const data: Response = JSON.parse(results.toString())
    callback(data)
  }
