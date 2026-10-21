import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// The dev server forwards /api calls to Django, so no CORS setup is needed.
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': 'http://127.0.0.1:8000',
    },
  },
})
