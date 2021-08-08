import { defineStore } from 'pinia'
import { RecordType } from '~/api'

type State = {
  recordTypes: RecordType[]
}

export const useRecordTypeStore = defineStore({
  id: 'recordTypeStore',
  state(): State {
    return {
      recordTypes: []
    }
  }
})
