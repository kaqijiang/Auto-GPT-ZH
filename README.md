# Auto-GPT：自主 GPT-4 实验

> 这里是 Auto-GPT 中文项目- 同步 fork Auto-GPT Auto-GPT 修改了分支规则，Fork 同步于 Stable 最新分支

<img src="docs/imgs/gzh.png" width="400">

### 公众号<阿杰与 AI>回复"Auto-GPT"加入群聊，共同探讨更多玩法

### 开源专栏推荐，欢迎你的加入

[【学习使用 ChatGPT MidJourney 助力工作学习创作】](https://github.com/kaqijiang/SutdyChatGPT)

### 无需部署中文网页版欢迎体验

# AutoGPT: 构建、部署和运行 AI 代理

**AutoGPT** 是一个强大的平台，允许您创建、部署和管理可以自动化复杂工作流程的持续性 AI 代理。

## 📦 版本说明

AutoGPT 目前有三个主要版本：

### 1. AutoGPT 平台版（最新）

- 完整的可视化界面
- 拖拽式代理构建器
- 云端部署选项
- 适合所有用户，特别是非技术用户
- 本文档主要介绍此版本

### 2. AutoGPT 经典版（实验性项目）

> ⚠️ **注意：此版本已停止维护，依赖项不会更新。它是一个已完成初始研究阶段的实验项目。**

经典版是最早实现自主 AI 代理的项目之一，它能够：

- 将复杂目标分解为小任务
- 使用可用工具和 API 执行任务
- 从结果中学习并调整方法
- 链接多个动作以实现目标

**主要特性：**

- 🔄 自主任务链接
- 🛠 工具和 API 集成能力
- 💾 上下文记忆管理
- 🔍 网页浏览和信息收集
- 📝 文件操作和内容创建

**历史影响：**

- 展示了 AI 自主性的实践实现
- 启发了众多衍生项目和研究
- 推动了 AI 代理架构的发展

[查看经典版完整文档](classic/README.md)

### 3. Forge 工具包（开发者工具集）

> 🚀 **为开发者打造的 AI 代理开发工具包**

Forge 是一个专门用于构建自定义 AI 代理的开发框架，它提供：

**核心优势：**

- 💤 **无需样板代码** - 直接专注于 AI 开发
- 🧠 **以大脑为中心** - 所有工具都服务于 AI 逻辑开发
- 🛠️ **完整工具生态** - 集成最佳实践工具

**学习资源：**

1. [入门指南：你的第一步](https://aiedge.medium.com/autogpt-forge-a-comprehensive-guide-to-your-first-steps-a1dfdf46e3b4)
2. [AI 代理的蓝图](https://aiedge.medium.com/autogpt-forge-the-blueprint-of-an-ai-agent-75cd72ffde6)
3. [与你的代理交互](https://aiedge.medium.com/autogpt-forge-interacting-with-your-agent-1214561b06b)
4. [构建智能代理逻辑](https://medium.com/@aiedge/autogpt-forge-crafting-intelligent-agent-logic-bc5197b14cb4)

📘 [查看 Forge 文档](classic/forge/README.md)

> [!提示]
>
> - 🌟 **普通用户**：推荐使用平台版（本文档）
> - 💻 **开发者**：
>   - 如果想学习 AI 代理的历史实现：参考经典版
>   - 如果要开发自己的 AI 代理：使用 Forge 工具包
>   - 如果要在生产环境使用：选择平台版

## 🚀 快速开始

### 托管选项

1. 自托管部署（请参考下方教程）
2. [加入云托管测试版等待名单](https://bit.ly/3ZDijAI)（推荐：开箱即用的解决方案）

### 系统要求

在开始之前，请确保您的系统满足以下要求：

#### 必需软件

- Node.js 和 NPM
- Docker 和 Docker Compose
- Git
- VSCode（推荐的 IDE）

#### 检查环境

1. **检查 Node.js 和 NPM**

```bash
node -v
npm -v
```

如需安装：

- Node.js：https://nodejs.org/en/download/
- NPM：https://docs.npmjs.com/downloading-and-installing-node-js-and-npm

2. **检查 Docker 和 Docker Compose**

```bash
docker -v
docker compose -v
```

如需安装：

- Docker Desktop：https://docs.docker.com/desktop/
- Docker Compose：https://docs.docker.com/compose/install/

> [!警告] > **请勿使用其他外部教程，因为它们可能已经过时**

## 💻 部署指南

### 1. 克隆项目

```bash
# 克隆主仓库
git clone https://github.com/Significant-Gravitas/AutoGPT.git

# 初始化并更新子模块
cd AutoGPT
git submodule update --init --recursive --progress
```

### 2. 后端设置

AutoGPT 服务器是平台的核心，负责运行您的 AI 代理。它提供：

- **核心功能**：驱动代理和自动化流程的核心逻辑
- **可靠基础设施**：确保稳定和可扩展的性能
- **代理市场**：提供各种预构建的代理

#### 部署步骤

1. **进入后端目录**：

```bash
cd autogpt_platform
```

2. **配置环境变量**：

```bash
# 复制环境变量模板
cp supabase/docker/.env.example .env
```

> 提示：您可以根据需要修改 `.env` 文件中的配置

3. **启动后端服务**：

```bash
docker compose up -d --build
```

4. **更新加密密钥**（可选但推荐）：

```python
# 在 Python 中生成新密钥
from cryptography.fernet import Fernet;Fernet.generate_key().decode()

# 或使用 CLI 工具
poetry run cli gen-encrypt-key
```

将生成的密钥更新到 `autogpt_platform/backend/.env` 文件中

### 3. 前端设置

AutoGPT 前端提供直观的用户界面，支持多平台（Web、Android、iOS、Windows、Mac）。

#### 主要功能

- 📋 任务管理
- 💬 智能对话
- 📱 响应式设计
- 🔄 实时监控
- 📊 性能分析

#### 部署步骤

1. **进入前端目录**：

```bash
cd frontend
```

2. **配置环境变量**：

```bash
cp .env.example .env
```

3. **安装依赖并启动**：

```bash
npm install
npm run dev
```

### 4. 验证部署

1. **检查服务状态**

访问以下地址确认服务正常运行：

- 前端界面：http://localhost:3000
- WebSocket 服务：8001 端口
- REST API：8006 端口

2. **常见端口说明**

```
前端 UI：3000
WebSocket：8001
REST API：8006
```

## 🎯 示例应用

### 1. 视频内容自动生成

- 监控 Reddit 热门话题
- 智能识别趋势
- 自动创建短视频

### 2. 社媒内容助手

- 自动处理 YouTube 视频
- 生成文字记录
- 提取关键引用
- 发布社交媒体内容

## 📖 更多资源

- [详细文档](https://docs.agpt.co)
- [贡献指南](CONTRIBUTING.md)
- [API 参考](https://docs.agpt.co/api)
