import { useFetch } from '~/composable'
import { EnumerableEnvelope } from './common'

export type RecordType = {
  id: number
  recordType: string
  total: number
}

export const recordTypeRepository = {
  getAll<T extends boolean>(immediate: T) {
    return useFetch<EnumerableEnvelope<RecordType>>('/recordType')
      .get()
      .json(immediate)
  }
}
