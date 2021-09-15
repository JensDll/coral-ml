declare global {
  namespace NodeJS {
    interface ProcessEnv {
      APP_HOST: string
      PORT_STREAM_IN: string
      PORT_STREAM_OUT: string
    }
  }
}

export {}
