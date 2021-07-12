import { Id, Listener } from './types'
import { toBool } from '../converters/index'
import zmq from 'zeromq'

export const loadModel =
  (req: zmq.Request) => async (id: string, callback: Listener<boolean>) => {
    console.log(`Load model with id (${id})`)

    await req.send(id)
    const [success] = await req.receive()

    callback(toBool(success))
  }
