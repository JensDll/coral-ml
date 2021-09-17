export type {
  PaginationEnvelope,
  PaginationRequest,
  EnumerableEnvelope,
  RecordType,
  Id
} from './types'

import { RecordRepository } from './recordRepository'
import { RecordTypeRepository } from './recordTypeRepository'

export type { ApiRecord } from './recordRepository'
export type { ApiRecordType } from './recordTypeRepository'

export const recordRepository = new RecordRepository()
export const recordTypeRepository = new RecordTypeRepository()

import { io } from 'socket.io-client'
import { ModelRepository } from './modelRepository'
import { ImageRepository } from './imageRepository'
import { VideoRepository } from './videoRepository'

export type {} from './modelRepository'
export type { ImageSettings } from './imageRepository'
export type { VideoSettings } from './videoRepository'

const socket = io(import.meta.env.VITE_NODE_API, {
  transports: ['websocket'],
  path: import.meta.env.MODE !== 'development' ? '/node-api/' : undefined
})
socket.on('connect', () => {
  console.log(`[Socket] Connected ${socket.id}`)
})
export const modelRepository = new ModelRepository(socket)
export const imageRepository = new ImageRepository(socket)
export const videoRepository = new VideoRepository(socket)
