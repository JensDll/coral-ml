export type EnumerableEnvelope<T> = {
  data: T[]
  total: number
}

export type PaginationEnvelope<T> = {
  data: T[]
  pageNumber: number
  pageSize: number
  total: number
}

export type PaginationRequest = {
  pageNumber: number
  pageSize: number
}

export type RecordType = 'Image Classification' | 'Object Detection'

export type Id = number | string

export type MessageEnvelope<T = any> = {
  success: boolean
  errors: string[]
  data: T
}
