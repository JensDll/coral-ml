import { EventEmitter } from 'ws'
import http from 'http'
import https from 'https'

declare module 'ws' {
  type Options = {
    backlog: number
    clientTracking: true
    handleProtocols: () => any
    host: string
    noServer: boolean
    path: string
    perMessageDeflate: boolean
    port: number
    server: http.Server | https.Server
    verifyClient: () => any
  }

  class WebSocketServer extends EventEmitter {
    constructor(options: Partial<Options>, callback?: () => any)

    clients: Set<any>
  }
}
