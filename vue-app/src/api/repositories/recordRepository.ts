import { useDownload, useFetch } from '../../composable'
import { PaginationEnvelope, Id, PaginationRequest } from './common'

export type Record = {
  id: number
  modelFileName: string
  labelFileName: string
  loaded: boolean
  recordTypeId: number
  recordType: string
}

export const recordRepository = {
  getWidthRecordTypeId<T extends boolean>(
    immediate: T,
    recordTypeId: Id,
    pagination: PaginationRequest = { pageNumber: 1, pageSize: 100 }
  ) {
    return useFetch<PaginationEnvelope<Record>>(
      `/record/type/${recordTypeId}`,
      pagination
    )
      .get()
      .json(immediate)
  },
  getLoaded<T extends boolean>(immediate: T) {
    return useFetch<Record>('/record/loaded').get().json(immediate)
  },
  getById<T extends boolean>(immediate: T, id: Id) {
    return useFetch<Record>(`/record/${id}`).get().json(immediate)
  },
  async download(id: Id) {
    const { data } = await useFetch<Blob>(`/record/download/${id}`)
      .get()
      .blob(false).promise

    if (data) {
      useDownload(data, 'model.zip')
    }
  },
  upload<T extends boolean>(
    immediate: T,
    modelTypeId: Id,
    model: File,
    label: File
  ) {
    const formData = new FormData()
    formData.append('modelTypeId', modelTypeId.toString())
    formData.append('model', model)
    formData.append('label', label)

    return useFetch<void>('/record').post({ body: formData }).text(immediate)
  },
  setLoaded<T extends boolean>(immediate: T, id: Id) {
    return useFetch<void>(`/record/${id}`).put().text(immediate)
  },
  delete<T extends boolean>(immediate: T, id: Id) {
    return useFetch<void>(`/record/${id}`).delete().text(immediate)
  }
}
