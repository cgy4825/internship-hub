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

---

## 阶段 8：关键 P0 问题修复（2025-06-10）

### 前置条件
- 阶段 7 数据量扩充完成。代码走查发现三个 P0 级问题：今日新增伪造、标题与数据不符、采集器无测试与零条告警。

### 目标
修复影响「产品可信度」的三个关键问题。

### 产出与修复
1. **今日新增不再伪造**（`yingjiesheng.py` / `date.ts` / `InternCard.tsx` / `validate.py` / `schema.md`）：
   - 采集器新增详情页发布日期提取（`jobInfo-update` → `_parse_pubdate`），仅当来源提供真实发布日才写入 `publishedAt`；
   - 抓取失败则 `publishedAt` 留空，`FETCH_DETAIL_PUBDATE` 可关闭；
   - schema 将 `publishedAt` 从必填改为可选；前端 `isToday`/`relativeTime` 对空值恒为 false/空，卡片不显示"今日新增"与误导时间；
   - 结果：一次采集 45 条中 34 条有真实发布日、11 条诚实留空，UI 不再伪造。
2. **标题名实相符**（`App.tsx` / `index.html` / `README.md` / docs）：
   - 标题/副标题/Hero/页脚由「大厂实习」统一调整为「**校招实习信息聚合**」，说明「含知名大厂及其他优质用人单位」，与真实数据来源一致。
3. **采集器单元测试 + 零条告警**（`tests/test_yingjiesheng.py` / `run.py` / `collect-daily.yml`）：
   - 新增 `_is_campus` / `_parse_pubdate` / `_extract_items` 等 7 项单测（纯函数，不联网），保护解析逻辑防网站改版失效；
   - `run.py` 记录每源抓取数量并输出 `stats`（含 `alert`），空源/无有效岗位时退出码置 1；
   - `collect-daily.yml` 捕获退出码，异常时**创建 GitHub Issue 告警**，避免静默失效。

### 验证方式
- `python collector/tests/test_yingjiesheng.py` → **7/7 通过**。
- `python collector/run.py` → 正常产出 44 条，`stats.alert=false`、退出码 0。
- `npm run build` 通过；headless 截图确认「今日新增」仅出现在真实当天发布岗位，其余显示真实相对时间；标题已更新。

### 遗留问题
- 详情页发布日期提取对部分职位不稳定（"X天内发布"需按天数近似），已通过"留空+前端不标今日"兜底。
- 采集因抓详情页耗时增加（每条 0.5s 间隔），如需更快可关闭 `FETCH_DETAIL_PUBDATE`。

---

## 阶段 9：P1 体验优化（卡片补全字段 / 我的收藏页 / 排序）（2025-06-10）

### 前置条件
- 阶段 8 P0 问题已修复，产品逻辑诚实、数据真实。

### 目标
提升使用体验：卡片展示更丰富字段、提供收藏独立页、支持排序。

### 产出
1. **卡片补全字段**（`yingjiesheng.py` / `InternCard.tsx` / `types` / `schema.md`）：
   - 采集器新增解析 `company-type` → `companyType`（公司类型/规模/行业），
     并从 `job-tag` 提取 `education`（学历）与 `workDuration`（实习周期，如 `5天/周·3个月`）；
   - schema 与前端类型新增 `education` / `workDuration` / `companyType` 可选字段；
   - 卡片新增「关键元信息」行（薪资/实习时长/公司规模）+「学历」标签。
   - 结果：一次采集 47 条，46 条含学历、47 条含公司规模、6 条含实习周期。
2. **我的收藏独立页**（`App.tsx`）：
   - 顶部新增「全部岗位 / 我的收藏(数量)」视图切换；收藏页独立展示已收藏岗位、独立排序；
   - Support 深链：`?_view=favorites`；空态引导；收藏状态卡片爱心实心显示。
3. **排序功能**（`lib/sort.ts` / `SortSelect.tsx`）：
   - 新增排序：最新发布 / 最早发布 / 薪资从高到低 / 薪资从低到高 / 学历从高到低；
   - `parseSalary` 将薪资统一折算为「元/年」便于跨单位比较（正确处理 `20-25万/年`、`8千-1万`、`150元/天` 等）；
   - 全部页与收藏页均可切换排序。

### 验证方式
- `python collector/run.py` → 产出 47 条，新字段（education/companyType/workDuration）已填充。
- `python collector/tests/test_yingjiesheng.py` → **7/7 通过**（更新了 companyType 断言）。
- `npm run build` 通过（38 模块）；截图确认：
  - 全部页卡片展示薪资/学历/公司规模/实习周期；
  - 收藏页（`?_view=favorites`）正确渲染 6 个已收藏岗位，爱心实心；
  - 排序下拉正常呈现。
- 薪资排序算法用真实数据复核：跨单位折算为年薪资后按序合理。

### 遗留问题
- 薪资文本格式多样，少数含"13薪/月"等后缀的混合单位排序为近似值，属可接受。
- 收藏为 localStorage（本机），跨设备不同步（见 ADR-0003，后续可升级账号系统）。

---

## 阶段 10：每日自动采集的可靠性增强（2025-06-10）

### 前置条件
- 阶段 9 采集、前端、部署均已就绪；需确认「每日自动更新」真正可靠运行。

### 目标
让「每天自动更新」尽可能可靠、及时，且无需人工干预。

### 产出
- `collect-daily.yml`：新增 `push: [main]` 触发，推送到 main 即立即采集一次（数据更及时）；
  保留每天 UTC 08:00 定时；抓到 0 条时创建 GitHub Issue 告警。
- `yingjiesheng.py`：`_fetch` 增加 **重试（最多 3 次）** 与 **UA 回退（移动端→桌面端）**，
  并加入退避，提升云端（境外服务器）访问国内网站的稳定性。

### 验证方式
- `python -I collector/run.py`（隔离纯净环境，模拟 CI）成功：45 条，退出码 0。
- 采集器 import 全部为标准库，可直接在 GitHub Actions 云端 Linux 运行。
- 前端 `npm run build` 通过（38 模块）。

### 重要说明（诚实披露）
- 采集工作流运行在 **GitHub 云端（境外）**；对国内网站（应届生求职网）的抓取成功率
  取决于对方是否放行云端 IP/代理。本机（国内）验证成功率高，但不能等同于云端必然成功。
- **是否真正每天更新成功，需以 GitHub Actions 运行记录为准**（本机无法直接查看云端日志）。
  已通过「推送到 main 即触发 + 失败 Issue 告警」提高可发现性。

---

## 观察期：每日自动更新实况（2026-09-06 起，预计观察数天）

### 观察基线（2026-09-06 16:36 记录）
- 远程最新提交：`2c033b0`（docs 补充记录）
- 远程仓库**暂无 github-actions 自动提交**（观察起点）
- 本地数据：`generatedAt=2026-09-06T08:35:21Z`，45 条

### 如何判断「每日自动更新」是否成功（观察方法）
观察几天后，在 GitHub 仓库提交记录中查找是否出现：
- 作者为 `github-actions[bot]` 的提交，信息形如 `chore(data): 每日采集更新 <RUN_ID>`。

**判定标准**：
- 出现这类自动提交 → **自动更新成功**（云端每天抓到了数据并提交）。
- 几天后仍无 → **云端大概率抓不到国内源**，需改用境外可访问的数据源。

### 观察结论（待观察期结束后填写）
- [ ] 待观察（预计 3~7 天后回填结论）
