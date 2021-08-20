import { defineStore } from 'pinia'

export const useNavStore = defineStore({
  id: 'navStore',
  state() {
    return {
      navHidden: true
    }
  },
  actions: {
    toggleNav() {
      this.navHidden = !this.navHidden
    }
  }
})
