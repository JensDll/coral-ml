import zmq from 'zeromq'
import { IOListener, CONFIG, queueLast } from '~/domain'
import { Repository } from '../types'

type Settings = {
  topK: number
  scoreThreshold: number
}

export const videoRepository: Repository<'video'> = {
  updateSettings() {
    const client = new zmq.Request()
    client.connect(CONFIG.URI.VIDEO_UPDATE_SETTINGS)
    const send = queueLast(client)

    const close = () => {
      client.close()
    }

    const listener: IOListener<Settings, never> = settings => {
      send(settings)
    }

    return ['video:update:settings', close, listener]
  }
}
