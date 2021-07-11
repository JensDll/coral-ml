export type EnumerableEnvelope<T> = {
  data: T[]
  pageNumber: number
  pageSize: number
  total: number
}

export type PaginationRequest = {
  pageNumber: number
  pageSize: number
}

export type Id = number | string
