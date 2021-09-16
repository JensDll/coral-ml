import { Request } from 'zeromq'
import { ReplyCallback, Repository } from './types'
import { URI } from './uri'

type Settings = {
  topK: number
  scoreThreshold: number
}

export class VideoRepository implements Repository {
  settingsClient: Request

  constructor() {
    this.settingsClient = new Request()
    this.settingsClient.connect(URI.VIDEO_UPDATE_SETTINGS)
  }

  close() {
    this.settingsClient.close()
  }

  async updateSettings(settings: Settings, reply: ReplyCallback) {}
}
