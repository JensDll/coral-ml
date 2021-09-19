import { createFetch } from './createFetch'

export const useFetch = createFetch(import.meta.env.VITE_URI_RECORD_API)
