export type Id = string | number

export type Listener<T> = (resp: T) => void
