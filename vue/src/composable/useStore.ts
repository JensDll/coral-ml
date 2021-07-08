import { inject, InjectionKey, reactive, readonly } from "vue"

type State = {
  navHidden: boolean
}

export const createStore = () => {
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

export const storeKey: InjectionKey<ReturnType<typeof createStore>> = Symbol()

export const useStore = () => inject(storeKey, createStore())
