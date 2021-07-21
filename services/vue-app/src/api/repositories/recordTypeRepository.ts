import { useFetch } from '~/composable'
import { useRecordTypeStore } from '~/store/recordTypeStore'
import { EnumerableEnvelope } from './common'

export type RecordType = {
  id: number
  recordType: RecordType
  total: number
  loaded: boolean
}

export const recordTypeRepository = {
  async loadAll() {
    const { data, responseOk } = await useFetch<EnumerableEnvelope<RecordType>>(
      '/recordType'
    )
      .get()
      .json(false).promise

    if (responseOk && data) {
      const store = useRecordTypeStore()
      store.recordTypes = data.data
    }
  }
}
