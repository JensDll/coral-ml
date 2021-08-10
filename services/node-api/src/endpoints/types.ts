export type Id = string | number

export type Listener<T> = (resp: T) => void

export type MessageEnvelope<T> = {
  success: boolean
  errors: string[]
  data?: T
}
