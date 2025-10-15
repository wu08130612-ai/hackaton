# Google Cloud Run AI 比赛要求

## 🎯 核心任务
构建一个创新的无服务器应用程序，并将其部署在 **Google Cloud Run** 上。

## 🤖 技术核心
应用程序必须与 AI 相关，并从三个指定类别中选择一个方向。

## 📋 比赛类别

### 🤖 AI Studio 类别
- 必须使用 **Google AI Studio** 生成部分应用代码
- 将应用部署到 Cloud Run
- 重点：将创意快速转化为代码并部署

### 🤝 AI 代理类别 ⭐ (推荐选择)
- 必须使用 **Google 的代理开发套件 (ADK)** 构建
- 系统必须包含 **至少两个** AI 代理
- 代理之间需要通信协作来解决实际问题
- 部署到 Cloud Run

### ⚡ GPU 类别
- 必须在 Cloud Run 上利用 **Nvidia L4 GPU** 资源
- 运行开源 AI 模型（如 Gemma）

## 🔧 通用要求
- ✅ **强制**：所有项目必须部署在 Google Cloud Run 上
- 🎁 **鼓励**：集成其他 Google Cloud 服务（Gemini, Gemma, Cloud Storage, BigQuery 等）

## 📤 提交内容
1. 项目总结（文本描述）
2. 演示视频（约3分钟）
3. 公开的代码仓库链接
4. 架构图
5. 可供评委试用的项目链接（强烈推荐）
6. （AI Studio 类别专属）AI Studio 中使用的 Prompt 链接

## 🌟 加分项
- 使用更多 Google AI 模型和 Cloud Run 服务
- 前后端分离架构
- 通过博客、视频或社交媒体进行公开分享和宣传

## 🎯 选择方向：AI 代理类别详情

### 核心要求
- 使用 **Google Agent Development Kit (ADK)** 构建
- 部署到 **Cloud Run**
- **四个 AI 代理** 相互通信协作（超出最低要求的两个代理）
- 完成工作流程，解决现实世界问题或改进流程

### 技术挑战
- 多智能体系统设计
- 代理间通信协议
- 工作流程编排
- 现实问题解决方案

## 🛠️ 确定的技术栈方案

### 🏗️ 核心架构层（必选）
- **Google Agent Development Kit (ADK)** - 四代理系统核心
- **Google Cloud Run** - 部署平台
- **Google Gemini Pro** - AI模型引擎
- **Google Cloud Pub/Sub** - 代理间通信

### 🔧 后端服务层
- **FastAPI** - 异步API框架，支持多代理协调
- **Pydantic** - 数据验证和序列化，确保代理间通信类型安全
- **Google Cloud Storage (GCS)** - 个性化内容文件存储
- **Google Cloud Tasks** - 异步任务队列，支持后台分析

### 🐳 部署和基础设施
- **Docker** - 容器化部署，四个代理独立扩缩容
- **Google Cloud Firestore** - 实时数据库，学习会话同步
- **Google Cloud Monitoring** - 系统监控和可观测性

### 🎨 前端界面
- **React + TypeScript** - 现代前端框架
- **Tailwind CSS** - 快速样式开发
- **WebSocket (FastAPI)** - 实时通信支持

### 🧠 AI和数据处理
- **Google Vertex AI** - 向量数据库，认知模式存储
- **NumPy + Pandas** - 数据处理和分析
- **Scikit-learn** - 轻量级机器学习，个性化推荐

### 📋 项目应用场景
**智能学习助手系统 - 实时动态多维度个性化**
- 🎯 目标用户：K12学生及家长
- 🧠 四个AI代理：认知模式分析、情感智能监测、自适应内容生成、预测干预
- 💡 核心价值：真正的个性化学习体验，超越传统教育机构

---
*此文档将作为整个项目开发的核心参考标准*