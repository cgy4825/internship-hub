import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss()],
  // 相对路径 base，便于部署到 GitHub Pages 子路径
  base: './',
  // 固定开发/预览端口，避免与其它软件冲突（开发用 5300）
  server: {
    port: 5300,
    host: true, // 允许局域网访问，便于手机/其它设备调试
  },
  preview: {
    port: 4173,
  },
  build: {
    outDir: 'dist',
  },
})
