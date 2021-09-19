if (process.env.MODE !== 'PROD') {
  const dotenv = await import('dotenv')
  dotenv.config()
}

export {}
