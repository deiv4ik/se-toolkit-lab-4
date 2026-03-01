import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/items': {
        target: 'http://10.93.26.27:42002',
        changeOrigin: true,
        rewrite: (path) => `${path}/`,
      },
    },
  },
})
