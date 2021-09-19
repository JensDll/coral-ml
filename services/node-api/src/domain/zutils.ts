import zmq from 'zeromq'

export const queueLast = <TData>(socket: zmq.Request) => {
  let queued: TData | null = null
  let numQueued = 0
  let result: Buffer[] = []

  return async (data: TData | null): Promise<Buffer[]> => {
    try {
      do {
        if (numQueued === 1) {
          throw void 0
        }
        await socket.send(JSON.stringify(queued !== null ? queued : data))
        queued = null
        numQueued++
        result = await socket.receive()
        numQueued--
      } while (queued !== null)
    } catch (e) {
      queued = data
    } finally {
      return result
    }
  }
}
