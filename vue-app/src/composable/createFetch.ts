import { reactive } from 'vue'
import { useUri } from './useUri'

interface FetchOptions extends RequestInit {
  uri: string
}

type State<TData> = {
  loading: boolean
  responseOk: boolean
  data?: TData
  response?: Response
  error?: unknown
}

type StateWithPromise<T> = { state: State<T>; promise: Promise<State<T>> }

export type ParsingOptions<T> = {
  json<TImmediate extends boolean>(
    immediate: TImmediate
  ): TImmediate extends true ? State<T> : StateWithPromise<T>
  json(): State<T>
  blob<TImmediate extends boolean>(
    immediate: TImmediate
  ): TImmediate extends true ? State<T> : StateWithPromise<T>
  blob(): State<T>
  text<TImmediate extends boolean>(
    immediate: TImmediate
  ): TImmediate extends true ? State<string> : StateWithPromise<string>
  text(): State<string>
}

const makeRequest = async <T>(state: State<T>, options: FetchOptions) => {
  try {
    console.log(`[FETCH] Fetching ...`)
    state.loading = true
    state.response = await fetch(options.uri, options)
    state.responseOk = state.response.ok
  } catch (e) {
    state.error = e
  } finally {
    console.log(`[FETCH] ${options.uri} ${state.response?.status}`)
    state.loading = false
  }
}

const parseRequest = async <T>(
  state: State<T>,
  options: FetchOptions,
  type: 'json' | 'blob' | 'text'
) => {
  await makeRequest(state, options)
  if (state.response && state.responseOk) {
    state.data = await state.response[type]()
  }
  return state
}

const parsingOptions = <T>(
  state: State<T>,
  options: FetchOptions
): ParsingOptions<T> => ({
  json(immediate = false): any {
    const promise = parseRequest(state, options, 'json')
    if (immediate) {
      promise.then()
      return state
    }
    return { state, promise }
  },
  text(immediate = false): any {
    const promise = parseRequest(state, options, 'text')
    if (immediate) {
      promise.then()
      return state
    }
    return { state, promise }
  },
  blob(immediate = false): any {
    const promise = parseRequest(state, options, 'blob')
    if (immediate) {
      promise.then()
      return state
    }
    return { state, promise }
  }
})

const fetchMethods = <T>(state: State<T>, fetchOptions: FetchOptions) => ({
  get(options: RequestInit = {}) {
    fetchOptions = Object.assign(fetchOptions, options)
    fetchOptions.method = 'GET'
    return parsingOptions(state, fetchOptions)
  },
  post(options: RequestInit = {}) {
    fetchOptions = Object.assign(fetchOptions, options)
    fetchOptions.method = 'POST'
    return parsingOptions(state, fetchOptions)
  },
  put(options: RequestInit = {}) {
    fetchOptions = Object.assign(fetchOptions, options)
    fetchOptions.method = 'PUT'
    return parsingOptions(state, fetchOptions)
  },
  delete(options: RequestInit = {}) {
    fetchOptions = Object.assign(fetchOptions, options)
    fetchOptions.method = 'DELETE'
    return parsingOptions(state, fetchOptions)
  }
})

const useFetch =
  (baseUri: string) =>
  <TData>(uri: string, params: Record<string | number, unknown> = {}) => {
    const fetchOptions: FetchOptions = {
      uri: baseUri + uri
    }

    if (Object.keys(params).length > 0) {
      fetchOptions.uri += `?${useUri.toUrlParams(params)}`
    }

    const state = reactive<State<TData>>({
      loading: false,
      responseOk: false
    })

    return fetchMethods(state, fetchOptions)
  }

export const createFetch = (baseUri: string) => useFetch(baseUri)
