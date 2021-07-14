import { SocketService } from '~/api'

export const useSocketService = () => new SocketService('http://localhost:6100')
