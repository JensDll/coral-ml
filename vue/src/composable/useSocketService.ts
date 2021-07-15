import { inject, InjectionKey } from 'vue'
import { SocketService } from '~/api'

export const socketService = new SocketService(
  import.meta.env.VITE_IO_SOCKET_URI
)

export const socketServiceKey: InjectionKey<SocketService> = Symbol()

export const useSocketService = () => inject(socketServiceKey) as SocketService
