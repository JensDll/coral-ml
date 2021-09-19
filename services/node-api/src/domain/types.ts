export type MessageEnvelope<T = any> = {
  success: boolean
  errors: string[]
  data?: T
}

export type ResponseCallback<TResponse = any> = (
  data: MessageEnvelope<TResponse>
) => void

export type IOListener<TRequest, TResponse> = (
  request: TRequest,
  respond: TResponse extends never ? never : ResponseCallback<TResponse>
) => void
