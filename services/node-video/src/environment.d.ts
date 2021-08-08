declare global {
  namespace NodeJS {
    interface ProcessEnv {
      HOST: string
      CORAL_APP: string
    }
  }
}

export {}
