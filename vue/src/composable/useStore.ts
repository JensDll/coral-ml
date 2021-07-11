import { inject, InjectionKey, reactive, readonly } from "vue"

type State = {
  navHidden: boolean
}

const createStore = () => {
  const state = reactive<State>({
    navHidden: false
  })

  return {
    actions: {
      toggleNav() {
        state.navHidden = !state.navHidden
      }
    },
    state: readonly(state)
  }
}

export const store = createStore()

export const storeKey: InjectionKey<ReturnType<typeof createStore>> = Symbol()

export const useStore = () => inject(storeKey) as typeof store
