import { Id, Listener } from './types'
import { toBool } from '../converters/index'
import zmq from 'zeromq'

let busy = false

export const loadModel =
  (client: zmq.Request) => async (id: string, callback: Listener<boolean>) => {
    if (busy) {
      callback(false)
    } else {
      console.log(`Load model with ids (${id})`)
      busy = true
      await client.send(id)
      const [success] = await client.receive()
      const status = toBool(success)
      console.log(`Loaded model with status (${status})`)
      callback(status)
      busy = false
    }
  }
