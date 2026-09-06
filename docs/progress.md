# 开发进度日志

> 本文件按阶段记录项目开发过程：前置条件、目标、产出、验证方式、遗留问题。
> 后续每完成一个阶段，在文末追加一条记录。

---

## 阶段 0：需求确认与方案定稿（2025-06-10）

### 前置条件
- 项目发起人（非专业程序员）提出「大厂实习信息聚合 + 一键投递 + 每日更新」的想法。
- 已确认约束：数据源采用**自动爬取**、范围锁定**大厂互联网/科技公司**、功能含**搜索/筛选/收藏/提醒**、**无技术背景 + 预算很低**。

### 目标
明确产品定位、架构方向、合规原则，并确立技术路线。

### 产出（决策记录）
- 定位：**索引层 + 深链**，只展示结构化元信息，点击跳官方投递渠道（降低版权/合规风险）。见 [`data/schema.md`](../data/schema.md)。
- 技术架构：静态站点 + 定时采集，近零成本。见 ADR-0001 / ADR-0002。
- 收藏：MVP 用 localStorage，不建用户系统。见 ADR-0003。

### 验证方式
- 与发起人确认数据源、功能（搜索/筛选/收藏/提醒）、账号策略（先不要）。
- 确认从零搭建、当前目录、精美前端、规范文档的要求。

### 遗留问题
- 「提醒」第一版以 RSS 为主，邮件/微信后续再评估。

---

## 阶段 1：工程骨架与文档体系（2025-06-10）

### 前置条件
- 工具链确认：Node 24 / npm 11 / git 2.49 / Python 3.13（pnpm 未装，统一用 npm）。

### 目标
建立规范的工程目录与权威文档体系。

### 产出
- 项目目录：`D:\ideaProject\internship-hub\`，git 已初始化。
- 文档中心 `docs/`：
  - [`standards/development-standards.md`](../standards/development-standards.md) —— 开发规范（命令、目录、Git 提交、风格、质量门禁）
  - [`standards/documentation-standards.md`](../standards/documentation-standards.md) —— 文档书写规范
  - [`architecture/overview.md`](../architecture/overview.md) —— 系统总体架构
  - [`architecture/frontend.md`](../architecture/frontend.md)、[`architecture/collector.md`](../architecture/collector.md)
  - [`data/schema.md`](../data/schema.md) —— 数据结构权威定义
  - [`decisions/`](../decisions/) —— ADR-0001 ~ 0003

### 验证方式
- 目录、文档齐备；schema 与前端类型、采集器三方一致。

### 遗留问题
- 无。

---

## 阶段 2：前端 MVP（2025-06-10）

### 前置条件
- 规范文档就绪；技术栈 Vite + React + TS + Tailwind v4。

### 目标
搭建精美、可运行的聚合列表页，完成搜索/筛选/收藏/今日新增交互。

### 产出
- `web/` 工程：`package.json`、Vite/TS 配置、Tailwind、入口与样式。
- `web/src/`：
  - `types/internship.ts` —— 前端类型（对齐 schema）
  - `lib/` —— `date.ts` / `filter.ts` / `brand.ts`（纯函数，可测试）
  - `hooks/` —— `useInternships.ts` / `useFavorites.ts`
  - `components/` —— `InternCard` / `FilterBar` / `FavoriteButton`
  - `App.tsx` —— 聚合视图（主视觉、筛选栏、卡片流、空态/加载/错误态）
- 静态数据演示：`web/public/data/internships.json`（12 条示例）。

### 验证方式
- `npm run build` 通过（TS 严格模式 0 错误）。
- 本地 `npm run dev`，headless Edge 截图确认渲染正常、无报错。
- 视觉：渐变主视觉、卡片流、标签、深链「立即投递」、今日新增标记、收藏交互、响应式三列。

### 遗留问题
- 收藏仅本机 localStorage（按 ADR-0003 推迟账号系统）。
- 辅助可访问性细节可后续打磨。

---

## 阶段 3：数据采集器（2025-06-10）

### 前置条件
- 前端类型、schema 已定义；约定「索引层 + 深链」原则。

### 目标
实现可插拔、容错、schema 校验的 Python 采集器，产出标准 JSON 供前端读取。

### 产出
- `collector/`（Python）：
  - `base.py` —— 采集器抽象基类
  - `normalize.py` —— 字段归一化（公司/城市/分类）
  - `validate.py` —— schema 校验（必填、枚举、URL、重复 id 检测）
  - `registry.py` —— 数据源注册表（可插拔）
  - `sources/seed.py` —— 种子数据源（12 条真实感示例，兜底/演示）
  - `sources/nowcoder.py` —— 牛客网采集器（HTTPS + 保守过滤噪声）
  - `run.py` —— 编排入口：采集→去重→归一化→校验→写 JSON
- 采集产物同步写到两处：根 `data/internships.json`（单一事实来源）+ `web/public/data/internships.json`（前端可服务）。

### 验证方式
- `python collector/run.py` 成功运行；输出为合法 JSON（Python 校验通过），含 12 条有效记录。
- 处理了「讨论区含面经/笔试等噪声」问题：新增噪声关键词过滤 + 校验把不合格记录剔除（本次滤掉 1 条缺 city 的记录，符合预期）。
- 容错：`nowcoder` 源失败不会中断整个流程。

### 遗留问题（重要）
- **牛客网数据质量**：`/discuss` 讨论区噪声大，当前保守过滤后有效岗位少。真实上线需改为抓取**牛客的招聘/实习接口或板块**，或优先接入各公司**官方校招网站**（`company_website` 源注释为骨架，待补全）。
- 公司名抽取为启发式，覆盖大厂名单有限，需持续扩充 `_COMPANY_ALIAS` 与 `_extract_company`。
- 抓取频率/合规需遵守平台条款；当前为演示性质的索引抓取。

---

## 阶段 4：端到端联调与版本管理（2025-06-10）

### 前置条件
- 前端 MVP + 采集器均可用。

### 目标
打通「采集→JSON→前端展示」完整链路，并把工程纳入 git 版本管理。

### 验证方式
- 重新构建前端 `npm run build` 通过；headless Edge 截图确认**采集器产出的 12 条数据**正常渲染。
- 数据源徽章、来源标签（牛客网/公司官网/演示数据）正确显示。
- `.gitignore` 覆盖 node_modules、dist、预览截图等，避免仓库污染。

### 遗留问题
- 待补齐 `company_website` 真实源与「提醒（RSS）」功能，见 [`roadmap.md`](./roadmap.md)。
