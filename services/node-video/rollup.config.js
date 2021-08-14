import { defineConfig } from 'rollup'
import typescript from '@rollup/plugin-typescript'
import { terser } from 'rollup-plugin-terser'
import replace from '@rollup/plugin-replace'

const watchConfig = defineConfig({
  input: 'src/main.ts',
  output: {
    file: 'dist/watch.js',
    format: 'esm'
  },
  plugins: [
    typescript(),
    replace({
      'process.env.HOST': JSON.stringify('localhost'),
      'process.env.STREAM_IN_PORT': JSON.stringify('5060'),
      'process.env.STREAM_OUT_PORT': JSON.stringify('8080'),
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
      'process.env.HOST': JSON.stringify('node-video'),
      'process.env.STREAM_IN_PORT': JSON.stringify('8080'),
      'process.env.STREAM_OUT_PORT': JSON.stringify('80'),
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
