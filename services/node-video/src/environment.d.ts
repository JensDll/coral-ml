declare global {
  namespace NodeJS {
    interface ProcessEnv {
      HOST: string
      STREAM_IN_PORT: string
      STREAM_OUT_PORT: string
      CORAL_APP: string
    }
  }
}

export {}
