import { ref, Ref } from 'vue'
import { UnPromise } from '~/utils/types'

type AsyncFunction = (...args: any[]) => Promise<any>

type RefedAsyncFunction<T extends AsyncFunction> = (
  ...args: Parameters<T>
) => Promise<Ref<UnPromise<ReturnType<T>>>>

export function useLoading<Fs extends readonly AsyncFunction[]>(
  ...fs: [...Fs]
): {
  [K in keyof Fs]: [
    Ref<boolean>,
    // @ts-ignore
    Ref<UnPromise<ReturnType<Fs[K]>> | undefined>,
    Fs[K]
  ]
} {
  function wrapper(f: AsyncFunction) {
    const loading = ref(false)
    const result = ref()

    const callback = async (...args: any[]) => {
      loading.value = true
      try {
        result.value = await f(...args)
        return result.value
      } finally {
        loading.value = false
      }
    }

    return [loading, result, callback]
  }

  return fs.map(wrapper) as any
}
