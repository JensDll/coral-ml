import { Id, Listener } from './types'
import { toBool } from '../converters/index'
import zmq from 'zeromq'

let busy = false

export const loadModel =
  (client: zmq.Request) => async (id: string, callback: Listener<boolean>) => {
    try {
      console.log(`Loading model with id (${id})`)
      busy = true
      await client.send(id)
      const [success] = await client.receive()
      const status = toBool(success)
      console.log(`Loaded model, success (${status})`)
      callback(status)
    } catch (e) {
      console.log(`Error loading model ${e}`)
      callback(false)
    }
  }
