# 大厂实习信息聚合站 · 文档中心

> 本目录是项目的**唯一权威文档源**（single source of truth）。
> 所有开发规范、架构决策、数据结构、进度记录均以 markdown 形式沉淀于此。

## 文档导航

| 目录 | 内容 | 说明 |
|------|------|------|
| [`standards/`](./standards/) | 开发规范与代码风格 | 团队/开发必须遵守的强制性标准 |
| [`architecture/`](./architecture/) | 系统架构与技术选型 | 整体结构、模块职责、技术决策 |
| [`data/`](./data/) | 数据结构与 schema | 数据字段定义、数据来源说明 |
| [`decisions/`](./decisions/) | ADR（架构决策记录） | 每次重要决策的背景与结论，可追溯 |

## 文件索引

### standards/
- [`standards/development-standards.md`](./standards/development-standards.md) —— **开发规范（总纲）**：命令行、目录结构、Git 提交、代码风格、质量门禁
- [`standards/documentation-standards.md`](./standards/documentation-standards.md) —— 文档书写规范：本仓库所有 markdown 的写法约定

### progress / roadmap
- [`progress.md`](./progress.md) —— 开发进度日志：按阶段记录目标、产出、验证、遗留问题
- [`roadmap.md`](./roadmap.md) —— 路线图：从 MVP 到完整产品的演进规划

### architecture/
- [`architecture/overview.md`](./architecture/overview.md) —— 系统总体架构与模块划分
- [`architecture/frontend.md`](./architecture/frontend.md) —— 前端架构与设计规范
- [`architecture/collector.md`](./architecture/collector.md) —— 数据采集端架构

### data/
- [`data/schema.md`](./data/schema.md) —— 实习信息数据模型定义（权威字段表）

### decisions/
- [`decisions/0001-tech-stack.md`](./decisions/0001-tech-stack.md) —— ADR-0001：技术栈选型
- [`decisions/0002-static-site.md`](./decisions/0002-static-site.md) —— ADR-0002：为何采用静态站点 + 定时采集（近零成本）

## 阅读顺序建议

第一次接触本项目，按下面顺序读即可快速理解全貌：

1. [`../README.md`](../README.md) —— 项目是什么
2. [`architecture/overview.md`](./architecture/overview.md) —— 系统怎么搭
3. [`data/schema.md`](./data/schema.md) —— 数据长什么样
4. [`standards/development-standards.md`](./standards/development-standards.md) —— 怎么改代码
5. [`decisions/0002-static-site.md`](./decisions/0002-static-site.md) —— 为什么这么设计
