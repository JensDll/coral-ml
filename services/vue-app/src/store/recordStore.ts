import { defineStore } from 'pinia'
import { ApiRecord } from '~/api'

type State = {
  records: ApiRecord[]
  pageNumber: number
  pageSize: number
  total: number
  loadedRecord?: ApiRecord
  loadingRecord: boolean
}

export const useRecordStore = defineStore({
  id: 'recordStore',
  state(): State {
    return {
      records: [],
      pageNumber: 1,
      pageSize: 200,
      total: 0,
      loadingRecord: false
    }
  },
  getters: {
    loadedType(): 'image' | 'video' | '' {
      switch (this.loadedRecord?.recordType) {
        case 'Image Classification':
          return 'image'
        case 'Object Detection':
          return 'video'
        default:
          return ''
      }
    },
    loadedModelFileName(): string | undefined {
      return this.loadedRecord?.modelFileName.replace('.tflite', '')
    }
  }
})
