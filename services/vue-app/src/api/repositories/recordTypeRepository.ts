import { useFetch } from '~/composable'
import { useRecordTypeStore } from '~/store/recordTypeStore'
import { EnumerableEnvelope, RecordType } from './common'

export type ApiRecordType = {
  id: number
  recordType: RecordType
  total: number
  loaded: boolean
}

export const recordTypeRepository = {
  async loadAll() {
    const { data, responseOk } = await useFetch<
      EnumerableEnvelope<ApiRecordType>
    >('/recordType')
      .get()
      .json(false).promise

    if (responseOk && data) {
      const store = useRecordTypeStore()
      store.recordTypes = data.data
    }
  }
}
