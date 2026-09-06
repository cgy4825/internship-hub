# 开发规范（总纲）

> 本文件是项目的**强制性开发标准**。任何开发行为（写代码、提交、建目录、写文档）都必须遵守。
> 修订本文件需新增 ADR 并在 `docs/decisions/` 记录缘由，禁止静默修改。

---

## 1. 命令行约定

- **包管理器统一为 `npm`**。当前环境未安装 `pnpm`，全项目（含前端）一律使用 `npm`。
- **禁止混用**包管理器：不得在 `web/` 用 `npm`、在别处用 `yarn`。锁定为 `npm`。
- 涉及依赖的命令优先采用 `npm install`、`npm run <script>`。
- 涉及 node 运行版本的配置固定声明在 `web/package.json` 的 `engines` 与 `.nvmrc`。

## 2. 仓库目录结构

```
internship-hub/
├── README.md                 # 项目简介、快速启动
├── docs/                     # 全部文档（markdown，权威）
│   ├── standards/            # 开发规范与代码风格
│   ├── architecture/         # 系统架构说明
│   ├── data/                 # 数据结构/schema
│   └── decisions/            # ADR 架构决策记录
├── web/                      # 前端工程（Vite + React + TS + Tailwind）
│   ├── src/                  # 源代码
│   │   ├── components/       # 可复用组件
│   │   ├── features/         # 业务功能模块
│   │   ├── hooks/            # 自定义 Hook
│   │   ├── lib/              # 纯工具/库函数
│   │   ├── data/             # 数据相关
│   │   └── styles/           # 全局样式
│   └── package.json
├── collector/                # 数据采集器（Python）
├── data/                     # 采集产物：生成的 JSON 数据（进 git 便于静态托管）
└── .gitignore
```

## 3. Git 提交规范

采用 **Conventional Commits**（[规范链接](https://www.conventionalcommits.org/)）：

```
<type>(<scope>): <subject>
```

- `type`：`feat` / `fix` / `docs` / `style` / `refactor` / `perf` / `test` / `build` / `ci` / `chore` / `revert`
- `scope`：受影响模块，如 `web`、`collector`、`docs`、`data`
- `subject`：一句话说清改动，首字母小写，结尾不加句号

**示例**

```
feat(web): 增加城市筛选器
docs(architecture): 补充采集器模块说明
chore(data): 更新今日采集数据
```

### 提交前置检查
- 不要提交 `node_modules/`、`__pycache__/`、`.pyc`、构建产物等（由 `.gitignore` 兜底，但提交前仍要确认）。
- 一次提交只做一件事；无关改动拆分提交。

## 4. 代码风格

### 通用
- 统一使用 UTF-8 编码；换行符 `LF`。
- 缩进：Python 用 4 空格；TypeScript/JS 用 2 空格。
- 命名：类型用 `PascalCase`，变量/函数用 `camelCase`，常量用 `UPPER_SNAKE_CASE`，CSS 类用 `kebab-case`。

### TypeScript / React
- 使用 **TypeScript 严格模式**（`strict: true`）。
- 组件文件用 `.tsx`，非组件逻辑用 `.ts`。
- 数据模型用 `interface` 定义，集中放在对应模块的 `types.ts`。
- 不依赖隐式 `any`，尽量避免 `@ts-ignore`。

### Python（采集器）
- 遵循 **PEP 8**。
- 新增采集器需继承统一的采集器基类/接口，保持可插拔。
- 采集器可单独运行，通过 Stdout/文件输出结构化 JSON。

## 5. 质量门禁

- 前端构建必须通过：`npm run build` 不得报错。
- 前端代码尽量满足 ESLint 通过；至少不允许明显未使用的变量/错误。
- 数据采集器输出必须符合 [`docs/data/schema.md`](../data/schema.md) 定义的 schema，否则视为失败。

## 6. 文档要求

- 所有文档一律用 **markdown**，存放于 `docs/`。
- 文档书写遵循 [`documentation-standards.md`](./documentation-standards.md)。
- **每个开发阶段都必须在进度文档中留痕**：前置条件、做了什么、产出、验证方式、遇到的问题。
- 重要决策必须新增 ADR 到 `docs/decisions/`。

## 7. 目录/文件命名

- 目录用 `kebab-case`（如 `internship-hub`、`docs/standards`）。
- 前端组件文件用 `PascalCase.tsx`（如 `InternCard.tsx`）。
- 采集器源文件用 `snake_case.py`（如 `nowcoder_collector.py`）。
