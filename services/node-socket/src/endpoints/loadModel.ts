import { Id, Listener } from './types'
import { toBool } from '../converters/index'
import zmq from 'zeromq'

let busy = false

export const loadModel =
  (client: zmq.Request) => async (id: string, callback: Listener<boolean>) => {
    if (busy) {
      callback(false)
    } else {
      console.log(`Load model with id (${id})`)
      busy = true
      await client.send(id)
      const [success] = await client.receive()
      callback(toBool(success))
      busy = false
    }
  }
