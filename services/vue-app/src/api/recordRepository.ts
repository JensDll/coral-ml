import { useRecordStore } from '~/store/recordStore'
import { useDownload, useFetch } from '../composition'
import { PaginationEnvelope, Id, PaginationRequest, RecordType } from './types'

export type ApiRecord = {
  id: number
  modelFileName: string
  loaded: boolean
  recordTypeId: number
  recordType: RecordType
}

export class RecordRepository {
  async loadWithRecordTypeId(
    recordTypeId: Id,
    pagination: PaginationRequest = { pageNumber: 1, pageSize: 200 }
  ) {
    const { data, responseOk } = await useFetch<PaginationEnvelope<ApiRecord>>(
      `/record/type/${recordTypeId}`,
      pagination
    )
      .get()
      .json(false).promise

    if (responseOk && data) {
      const recordStore = useRecordStore()
      recordStore.$patch({
        records: data.data,
        pageNumber: data.pageNumber,
        pageSize: data.pageSize,
        total: data.total
      })
    }
  }

  async loadLoaded() {
    const { data, responseOk } = await useFetch<ApiRecord>('/record/loaded')
      .get()
      .json(false).promise

    if (responseOk) {
      const recordStore = useRecordStore()
      recordStore.$patch({
        loadedRecord: data
      })
    }
  }

  getById<T extends boolean>(immediate: T, id: Id) {
    return useFetch<ApiRecord>(`/record/${id}`).get().json(immediate)
  }

  async download(id: Id) {
    const { data } = await useFetch<Blob>(`/record/download/${id}`)
      .get()
      .blob(false).promise

    if (data) {
      useDownload(data, 'model.zip')
    }
  }

  upload<T extends boolean>(
    immediate: T,
    recordTypeId: Id,
    model: File,
    label: File
  ) {
    const formData = new FormData()
    formData.append('recordTypeId', recordTypeId.toString())
    formData.append('model', model)
    formData.append('label', label)

    return useFetch<void>('/record').post({ body: formData }).text(immediate)
  }

  setLoaded<T extends boolean>(immediate: T, id: Id) {
    return useFetch<void>(`/record/${id}`).put().text(immediate)
  }

  delete<T extends boolean>(immediate: T, id: Id) {
    return useFetch<void>(`/record/${id}`).delete().text(immediate)
  }
}
