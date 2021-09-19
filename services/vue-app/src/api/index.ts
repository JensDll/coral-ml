export type {
  PaginationEnvelope,
  PaginationRequest,
  EnumerableEnvelope,
  RecordType,
  Id
} from './types'

import { RecordRepository } from './repositories/recordRepository'
import { RecordTypeRepository } from './repositories/recordTypeRepository'

export type { ApiRecord } from './repositories/recordRepository'
export type { ApiRecordType } from './repositories/recordTypeRepository'

export const recordRepository = new RecordRepository()
export const recordTypeRepository = new RecordTypeRepository()

import { io } from 'socket.io-client'
import { ModelRepository } from './repositories/modelRepository'
import { ImageRepository } from './repositories/imageRepository'
import { VideoRepository } from './repositories/videoRepository'

export type {} from './repositories/modelRepository'
export type { ImageSettings } from './repositories/imageRepository'
export type { VideoSettings } from './repositories/videoRepository'

const socket = io(import.meta.env.VITE_URI_NODE_API, {
  transports: ['websocket'],
  path: import.meta.env.MODE !== 'development' ? '/node-api/' : undefined
})
socket.on('connect', () => {
  console.log(`[Socket] Connected ${socket.id}`)
})
export const modelRepository = new ModelRepository(socket)
export const imageRepository = new ImageRepository(socket)
export const videoRepository = new VideoRepository(socket)
