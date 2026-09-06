import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss()],
  // 相对路径 base，便于部署到 GitHub Pages 子路径
  base: './',
  build: {
    outDir: 'dist',
  },
})
