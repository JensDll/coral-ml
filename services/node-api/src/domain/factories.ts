import { MessageEnvelope } from './types'

export const makeMessageEnvelope = <T>(
  data: T,
  errors: string[] = []
): MessageEnvelope => ({ success: errors.length == 0, errors, data })
