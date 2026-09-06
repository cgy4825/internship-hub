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

---

## 阶段 5：提醒（RSS）、每日自动更新与部署配置（2025-06-10）

### 前置条件
- 阶段 4 端到端链路已打通；MVP v0.1 已提交。

### 目标
补齐「每日更新」「提醒」「可部署」三块能力，健全工程设计。

### 产出
- **RSS 提醒**：新增 [`collector/rss.py`](../collector/rss.py)（RSS 2.0 生成器）。
  `run.py` 采集后生成 `data/feed.xml` 并同步到 `web/public/feed.xml`，供订阅源使用；并同步一份到 `data/`。
- **每日自动更新**：[`.github/workflows/collect-daily.yml`](../.github/workflows/collect-daily.yml)，
  GitHub Actions 每天定时（cron `0 8 * * *`）运行采集器并自动提交采集产物，实现「每日更新」。
- **部署配置**：
  - `web/vercel.json` —— Vercel 静态托管配置（免费，近零成本）。
  - [`.github/workflows/deploy-pages.yml`](../.github/workflows/deploy-pages.yml) —— GitHub Pages 自动构建发布。
- **前端数据路径修复**：`useInternships.ts` 改用 `import.meta.env.BASE_URL` 拼接数据路径，
  兼容 Vercel（根路径）与 GitHub Pages（子路径 `/repo/`）两种部署，修复潜在部署缺陷。
- **开发端口固定**：`web/vite.config.ts` 设定 `server.port = 5300` 且 `host: true`（局域网调试）。

### 验证方式
- `python collector/run.py` 成功：JSON + RSS 均产出，`feed.xml` 解析为合法 RSS（12 条 item）。
- `npm run build` 通过；`dist/` 包含 `data/internships.json` 与 `feed.xml`。
- dev 服务器重启后监听 **5300**；HTTP 200，`/data/internships.json` 返回 12 条；`5173` 已失效（符合预期）。
- 两个 workflow YAML 结构规范（GitHub Actions 标准 schema）。

### 遗留问题（重要）
- 真实数据源（`company_website` 等）与牛客招聘接口仍未接入；当前主数据来自 `seed` 演示源。
  这是下一步 P1 的关键工作。RSS 的 `SITE_LINK` 为占位域名，上线后需替换为实际站点地址。

---

## 阶段 6：接入真实数据源（应届生求职网）（2025-06-10）

### 前置条件
- 阶段 5 已具备 RSS/CI/CD/部署能力，但站点仍展示 `seed` 演示数据。
- 目标：接入真实、稳定的校招/实习数据，替换演示数据。

### 侦察过程与结论
- **牛客网**：实测公开接口 `/jobs/intern/` 等已失效（加载 404 JS）；`/completeness/all-career-jobs`
  只返回岗位分类树，不是岗位列表；讨论区全是面经/笔试噪声。结论：不稳定，弃用。
- **腾讯等大厂官网**：`careers.tencent.com/api/post/Query` 返回 2261 条真实岗位 JSON，但**全是社招**
  （工作年限三年/五年），实习/应届岗位为 0。结论：不含实习数据，不满足需求。
- **应届生求职网（51job 旗下）**：`m.yingjiesheng.com` 移动端 SSR 页，含结构化职位条目：
  标题、薪资、公司、城市、学历、jobdetail 投递深链，**且 tags 含「在校生/应届生」**。
  结论：稳定、真实、字段齐全，符合「只要校招/实习」的定位。

### 产出
- 新增 [`collector/sources/yingjiesheng.py`](../collector/sources/yingjiesheng.py)：
  - 抓取移动端首页，解析职位条目（title/salary/company/city/tags/jobdetail）。
  - **只保留校招/实习**（tags 含「在校生/应届生」），丢弃社招岗位。
  - 投递 `applyUrl` 指向真实 `jobdetail/<id>` 深链（已验证可访问，含投递入口）。
- 更新 `registry.py`：主力为 `yingjiesheng`，停用 `nowcoder` 与 `seed`（注释保留可回退）。
- 前端 `InternCard.tsx`：新增来源中文标签 `yingjiesheng → 应届生求职网`。
- 同步文档：`docs/data/schema.md` 更新 source 枚举；`docs/architecture/collector.md`、
  `overview.md` 更新数据源说明。

### 验证方式
- `python collector/run.py` 成功：采集到 **15 条真实校招/实习**（纯 `yingjiesheng`，无演示数据）。
- 用 Python 校验 JSON：15 条均为真实公司/岗位/薪资/城市，`applyUrl` 为真实 `jobdetail` 深链。
- `npm run build` 通过；headless Edge 截图确认页面展示**全部真实数据**，
  来源标签正确显示「应届生求职网」，共 15 个机会。
- 数据量：单次运行约 8~15 条（首页为推荐流，数量变动属正常），符合校招/实习定位。

### 遗留问题
- 单次数据量有限（首页推荐流 8~15 条）；后续可扩展到 `/searchresult/k实习` 等分类入口
  或增加分页以扩充数据量。
- 服务端渲染结构如有变动可能影响解析，需定期验证采集稳定性。
- RSS 的 `SITE_LINK` 仍为占位域名。

---

## 阶段 7：扩充数据量（多页面合并去重）（2025-06-10）

### 前置条件
- 阶段 6 已接入真实数据源，但单页数据量有限（8~15 条）。

### 目标
稳定扩充单次采集的校招/实习岗位数量。

### 产出
- 升级 `collector/sources/yingjiesheng.py`：
  - 从「单一首页」扩展为「**首页推荐流 + 多个分类关键词搜索页**」：
    `/searchresult/k实习`、`k校招`、`k校园招聘`、`k管培生`、`k应届生`。
  - 抓取后**按 jobid 去重**，合并为统一列表。
  - 增加 `MAX_TOTAL`（总条数上限）与单个页面容错（某页失败不中断整体）。
- 数据量从约 15 条提升到 **43 条**（约 3 倍），全部真实校招/实习。

### 验证方式
- `python collector/run.py` 成功：采集到 **43 条校招/实习**，全为 `yingjiesheng`，全部含 `jobdetail` 投递深链。
- `npm run build` 通过；headless Edge 截图确认页面展示 43 个真实岗位，内容丰富。

### 遗留问题
- 关键词页每页返回约 10 条，可进一步接分页 API 以继续扩充；当前 40+ 条已满足日常更新。
- RSS 的 `SITE_LINK` 仍为占位域名。
