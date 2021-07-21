import { defineStore } from 'pinia'

export const useNavStore = defineStore({
  id: 'navStore',
  state() {
    return {
      navHidden: false
    }
  },
  actions: {
    toggleNav() {
      this.navHidden = !this.navHidden
    }
  }
})
