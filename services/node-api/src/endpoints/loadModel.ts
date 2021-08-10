import { Listener } from './types'
import zmq from 'zeromq'

type Response = {
  success: boolean
  error: string
}

export const loadModel =
  (client: zmq.Request) => async (id: string, callback: Listener<Response>) => {
    try {
      console.log(`Loading model with id (${id})`)
      await client.send(id)
      console.log(`Loading model message queued`)
      const [result] = await client.receive()
      const response: Response = JSON.parse(result.toString())
      console.log(`Loaded model with response (${result.toString()})`)
      callback(response)
    } catch (e) {
      console.log(`Error loading model (${e})`)
      callback({
        success: false,
        error: e.toString()
      })
    }
  }
