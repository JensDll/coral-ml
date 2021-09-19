import { defineConfig } from 'rollup'
import typescript from '@rollup/plugin-typescript'
import alias from '@rollup/plugin-alias'
import path from 'path'

export default args => {
  const plugins = [
    alias({
      entries: [
        {
          find: '~',
          replacement: path.resolve(__dirname, 'src')
        }
      ]
    }),
    typescript()
  ]

  const config = defineConfig({
    input: 'src/main.ts',
    output: {
      file: 'dist/bundle.js',
      format: 'esm'
    },
    plugins
  })

  delete args.build

  return config
}
