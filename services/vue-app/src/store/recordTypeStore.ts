import { defineStore } from 'pinia'
import { ApiRecordType } from '~/api'

type State = {
  recordTypes: ApiRecordType[]
}

export const useRecordTypeStore = defineStore({
  id: 'recordTypeStore',
  state(): State {
    return {
      recordTypes: []
    }
  }
})
