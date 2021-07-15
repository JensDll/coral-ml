import { defineConfig } from 'vite'
import path from 'path'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  assetsInclude: ['jsmpeg.min.js'],
  resolve: {
    alias: {
      '~': path.resolve(__dirname, 'src')
    }
  }
})
