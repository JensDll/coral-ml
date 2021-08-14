declare global {
  namespace NodeJS {
    interface ProcessEnv {
      HOST: string
      LISTEN: string
      CORAL_APP: string
    }
  }
}

export {}
