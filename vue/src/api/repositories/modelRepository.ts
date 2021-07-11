import { useFetch } from '../../composable'
import { EnumerableEnvelope, Id, PaginationRequest } from './common'

export type TFLiteModelRecord = {
  id: number
  modelName: string
}

export const modelRepository = {
  getAll<T extends boolean>(
    immediate: T,
    pagination: PaginationRequest = { pageNumber: 1, pageSize: 100 }
  ) {
    return useFetch<EnumerableEnvelope<TFLiteModelRecord>>(
      '/model',
      {},
      pagination
    )
      .get()
      .json(immediate)
  },
  uploadModel<T extends boolean>(model: File, label: File, immediate: T) {
    const formData = new FormData()
    formData.append('model', model)
    formData.append('label', label)

    return useFetch<void>('/model').post(formData).text(immediate)
  },
  download<T extends boolean>(id: Id, immediate: T) {
    return useFetch<Blob>(`/model/${id}`).get().blob(immediate)
  }
}
