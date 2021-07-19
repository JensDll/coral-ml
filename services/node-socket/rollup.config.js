import { defineConfig } from 'rollup'
import typescript from '@rollup/plugin-typescript'
import { terser } from 'rollup-plugin-terser'
import replace from '@rollup/plugin-replace'

const watchConfig = defineConfig({
  input: 'src/main.ts',
  output: {
    file: 'bundle.js',
    format: 'esm'
  },
  plugins: [
    typescript(),
    replace({
      'process.env.HOST': JSON.stringify('localhost'),
      'process.env.CORAL_APP': JSON.stringify('localhost'),
      preventAssignment: true
    })
  ]
})

const buildConfig = defineConfig({
  input: 'src/main.ts',
  output: {
    file: 'dist/bundle.min.js',
    format: 'esm'
  },
  plugins: [
    typescript(),
    terser(),
    replace({
      'process.env.HOST': JSON.stringify('node-socket'),
      'process.env.CORAL_APP': JSON.stringify('coral-app'),
      preventAssignment: true
    })
  ]
})

export default args => {
  if (args.watch) {
    return watchConfig
  } else if (args.build) {
    delete args.build
    return buildConfig
  }
}
