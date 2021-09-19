import { IOListener } from '~/domain'

export type OnClose = () => void

export type Repository<TEvent extends string> = {
  [key: string]: () => [`${TEvent}:${string}`, OnClose, IOListener<any, any>]
}
