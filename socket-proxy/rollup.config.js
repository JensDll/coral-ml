import { defineConfig } from 'rollup'
import typescript from '@rollup/plugin-typescript'
import { terser } from 'rollup-plugin-terser'
import { nodeResolve } from '@rollup/plugin-node-resolve'
import commonjs from '@rollup/plugin-commonjs'
import json from '@rollup/plugin-json'

const watchConfig = defineConfig({
  input: 'src/main.ts',
  output: {
    file: 'bundle.js',
    format: 'esm'
  },
  plugins: [typescript()]
})

const buildConfig = defineConfig({
  input: 'src/main.ts',
  output: {
    file: 'dist/bundle.min.js',
    format: 'esm'
  },
  plugins: [
    typescript(),
    // nodeResolve(),
    // commonjs({
    //   dynamicRequireTargets: ['node_modules/socket.io/dist/*.js']
    // }),
    // json(),
    terser()
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
