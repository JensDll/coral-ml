import { ref, Ref } from "vue"

type AsyncFunction = (...args: any[]) => Promise<any>

export function useLoading<Fs extends readonly AsyncFunction[]>(
  ...fs: [...Fs]
): {
  [K in keyof Fs]: [Ref<boolean>, Fs[K]]
} {
  function wrapper(f: AsyncFunction) {
    const loading = ref(false)
    const callback = async (...args: any[]) => {
      loading.value = true
      try {
        return await f(...args)
      } finally {
        loading.value = false
      }
    }

    return [loading, callback]
  }

  return fs.map(wrapper) as any
}
