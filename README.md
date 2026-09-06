# 大厂实习信息聚合站

> 面向在校生的**大厂实习信息聚合 + 一键跳转官方投递渠道**的轻量网站。

## 这是什么

把分散在牛客网、各大公司官方校招网站的实习机会集中展示，支持搜索、筛选、收藏，每天更新，**点击卡片直达官方投递页面**。

## 技术栈

- **前端**：React + TypeScript + Vite + Tailwind CSS
- **数据采集**：Python
- **数据**：标准 JSON（进 git，静态托管直接读取）
- **部署**：Vercel / GitHub Pages（免费）

## 目录结构

```
internship-hub/
├── docs/                  # 全部文档（markdown）
│   ├── standards/         # 开发规范
│   ├── architecture/      # 系统架构
│   ├── data/              # 数据结构/schema
│   └── decisions/         # ADR 决策记录
├── web/                   # 前端工程
├── collector/             # 数据采集器（Python）
├── data/                  # 采集产物 JSON
└── README.md
```

## 快速启动（前端本地预览）

```bash
cd web
npm install
npm run dev        # 开发服务器：http://localhost:5300
```

> 开发端口已在 `web/vite.config.ts` 中固定为 5300，并开启局域网访问（`host: true`），
> 同一 WiFi 下可用 `http://<电脑IP>:5300` 在手机上进行调试。

## 数据采集

```bash
python collector/run.py
```

采集产物会写入 `data/internships.json`（单一事实来源）并同步到 `web/public/data/`，
同时生成 RSS 订阅源 `data/feed.xml`。见 [`docs/architecture/collector.md`](docs/architecture/collector.md)。

## 生产构建与部署

```bash
cd web
npm run build      # 产物输出到 web/dist
npm run preview    # 预览产物：http://localhost:4173
```

- **Vercel**：仓库根配置见 `web/vercel.json`（静态托管，近零成本）。
- **GitHub Pages**：`.github/workflows/deploy-pages.yml` 在推送到 `main` 时自动构建发布。

## 文档

- [文档中心](docs/README.md)
- [开发规范](docs/standards/development-standards.md)
- [系统架构](docs/architecture/overview.md)
- [数据结构](docs/data/schema.md)

## 设计原则

- **索引层，不搬运**：只展示结构化元信息，点击深链到官方投递渠道，降低版权/合规风险。
- **近零成本**：静态托管 + 定时采集，无需常驻服务器/数据库。
- **可插拔数据源**：采集器模块化，坏一个不影响其他。
