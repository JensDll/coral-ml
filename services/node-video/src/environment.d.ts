declare global {
  namespace NodeJS {
    interface ProcessEnv {
      APP_HOST: string
      STREAM_IN_PORT: string
      STREAM_OUT_PORT: string
    }
  }
}

export {}
