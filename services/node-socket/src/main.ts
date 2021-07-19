import { apiStart } from './api'
import { videoStart } from './video'

apiStart(process.env.HOST)
videoStart(process.env.HOST)
