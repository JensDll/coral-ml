import { useFetch } from '~/composition'
import { useRecordTypeStore } from '~/store/recordTypeStore'
import { EnumerableEnvelope, RecordType } from './types'

export type ApiRecordType = {
  id: number
  recordType: RecordType
  total: number
  loaded: boolean
}

export class RecordTypeRepository {
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
