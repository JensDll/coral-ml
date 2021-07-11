import { inject, InjectionKey } from "vue"
import { SocketService } from "~/api"

export const socketService = new SocketService("http://localhost:6100")

export const socketServiceKey: InjectionKey<SocketService> = Symbol()

export const useSocketService = () => inject(socketServiceKey) as SocketService
