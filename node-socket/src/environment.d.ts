declare global {
  namespace NodeJS {
    interface ProcessEnv {
      HOST: string
    }
  }
}

export {}
