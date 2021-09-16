export type MessageEnvelope<T = any> = {
  success: boolean
  errors: string[]
  data?: T
}
export type ReplyCallback<T = any> = (data: MessageEnvelope<T>) => void
export interface Repository {
  close(): void
}
