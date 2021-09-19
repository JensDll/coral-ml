declare global {
  namespace NodeJS {
    interface ProcessEnv {
      MODE: string

      APP_HOST: string
      APP_LISTEN: string

      CORAL_HOST: string
      CORAL_PORT_MODEL_MANAGER: string
      CORAL_PORT_IMAGE_CLASSIFICATION: string
      CORAL_PORT_IMAGE_SETTINGS: string
      CORAL_PORT_VIDEO_SETTINGS: string
    }
  }
}

export {}
