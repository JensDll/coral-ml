import io from 'socket.io'
import { OnClose, Repository } from '../types'

export function registerRepositories(
  socket: io.Socket,
  repositories: Repository<any>[]
) {
  const onCloseCallbacks: OnClose[] = []

  for (const repository of repositories) {
    for (const func of Object.values(repository)) {
      const [event, close, listener] = func()
      onCloseCallbacks.push(close)
      socket.on(event, listener)
    }
  }

  socket.on('disconnect', () => {
    console.log(`A user disconnected (${socket.id})`)
    onCloseCallbacks.forEach(close => close())
  })
}
