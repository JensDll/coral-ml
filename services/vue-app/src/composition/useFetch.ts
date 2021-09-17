import { createFetch } from './createFetch'

export const useFetch = createFetch(import.meta.env.VITE_RECORD_API)
