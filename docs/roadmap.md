# 路线图（Roadmap）

> 从当前 MVP 到完整产品的演进规划。按优先级排序，随项目推进逐步勾选。

## 当前状态：MVP v0.1 已完成

- ✅ 静态站点 + 定时采集架构（近零成本）
- ✅ 实习信息卡片流 + 点击深链跳转
- ✅ 搜索 / 筛选（城市、方向、类型）/ 今日新增 / 收藏（localStorage）
- ✅ 采集器流水线：可插拔源 + 归一化 + schema 校验 + 容错
- ✅ 规范文档体系

## 下一步（P1）

- [ ] **接入真实有效数据源**：
  - 接入各公司**官方校招/招聘网站**（补全 `company_website` 源，字节/腾讯/阿里/美团等）。
  - 牛客网改为抓取**招聘/实习接口或板块**，替代噪声较多的讨论区；扩充公司名抽取。
- [x] **每日自动更新**：配置 GitHub Actions cron 定时运行采集器并提交 JSON（`.github/workflows/collect-daily.yml`）。
- [x] **部署到 Vercel / GitHub Pages**（免费静态托管，配置见 `web/vercel.json` 与 `.github/workflows/deploy-pages.yml`）。
- [x] **提醒功能**：生成 RSS feed（`data/feed.xml`，静态文件即可），供订阅。

## 后续（P2）

- [ ] **用户系统 + 云端收藏同步**（从 localStorage 升级）。
- [ ] 收藏独立视图 / 我的订阅。
- [ ] 公司详情页、按公司聚合。
- [ ] 邮件/微信提醒。

## 长期（P3，按需）

- [ ] 基于用户的个性化推荐。
- [ ] 数据可视化（岗位分布、行业热度）。
- [ ] 前端可访问性（a11y）与性能精调。
- [ ] 数据源监控与失败告警。

## 质量与合规持续项

- 始终遵守「索引层 + 深链」原则（见 [`architecture/overview.md`](../architecture/overview.md)）。
- 控制抓取频率、尊重平台条款与 robots。
- 数据 schema 变更需同步更新 [`data/schema.md`](../data/schema.md) 与前端类型、采集器三方。
