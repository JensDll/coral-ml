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
  (client: zmq.Request) =>
  async ({ image, format }: RequestData, callback: Listener<Response>) => {
    console.log(image)
    // await client.send([image, format])
    // const [result] = await client.receive()
    // const data: Response = JSON.parse(result.toString())
    callback({ data: 'auiwzvd' } as any)
  }
