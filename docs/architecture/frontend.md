# 前端架构与设计规范

> 描述 `web/` 前端工程的结构、设计原则与页面规划。

## 1. 技术栈

- **框架**：React + TypeScript + Vite
- **样式**：Tailwind CSS
- **路由**（MVP 单页可先不引入，或引入轻量路由）；默认做单页聚合视图
- **工具**：ESLint + Prettier（保持代码一致）

## 2. 目录结构

```
web/src/
├── main.tsx                # 入口
├── App.tsx                 # 根组件
├── components/             # 通用可复用组件（原子/复合）
│   ├── InternCard.tsx      # 实习信息卡片
│   ├── FilterBar.tsx       # 搜索/筛选栏
│   ├── FavoriteButton.tsx  # 收藏按钮
│   └── ...
├── features/               # 业务功能模块
│   └── internships/        # 实习列表相关
├── hooks/                  # 自定义 Hook
│   ├── useInternships.ts   # 加载/过滤数据
│   └── useFavorites.ts     # 收藏（localStorage）
├── lib/                    # 纯工具
├── types/                  # TypeScript 类型（对应 docs/data/schema.md）
└── styles/
    └── index.css           # 全局样式（Tailwind）
```

## 3. 设计原则

1. **组件颗粒度**：尽量小而单一职责；逻辑放 `hooks/`，展示放 `components/`。
2. **类型先行**：先定义类型（`types/`），再写组件，保证与后端 schema 一致。
3. **纯函数**：过滤/统计逻辑放 `lib/`，便于测试与复用。
4. **视觉一致性**：颜色、间距、圆角、阴影统一用 Tailwind 主题令牌（tokens）管理，不散落魔法值。

## 4. 视觉与 UX 目标

- **现代、干净、有质感**：浅色调背景 + 白色卡片 + 柔和阴影 + 圆角。
- **品牌色**：用一个主色（如科技感的蓝/紫）+ 中性灰阶。
- **卡片信息层级**：公司名 > 岗位名 > 标签 > 城市/类型/日期，一目了然。
- **交互反馈**：hover 提升、点击深链新标签打开、收藏即时反馈。
- **响应式**：桌面多列栅格、移动端单列。

## 5. 页面规划

- **首页（聚合列表）**：顶部标题 + 搜索框 + 筛选项 + 排序；下方为实习信息卡片流。
- **「今日新增」区**：高亮当天/近 24h 新增岗位，满足「每天更新」感知。
- **收藏区**：查看已收藏（可后续做独立视图）。
- 后续可扩展：公司详情页、按公司聚合、订阅/RSS。

## 6. 数据接入

- 前端以 `import` 或运行时 `fetch` 引入 `data/internships.json`。
- MVP 采用构建期引入（`/data/internships.json` 作为静态资产），保证 Vercel/GitHub Pages 直接可用。
