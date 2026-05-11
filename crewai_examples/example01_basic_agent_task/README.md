# 示例1：基础 Agent 和 Task

## 概述
这个示例展示了 CrewAI 框架的基础用法：
- 创建自定义的 Agent（代理）
- 定义 Task（任务）
- 组建 Crew（团队）并执行任务

## 核心概念

### Agent（代理）
Agent 是具有特定角色、目标和背景故事的自主单元。在本示例中：
- **研究员**：负责收集和研究信息
- **写作者**：负责将研究成果整理成报告

### Task（任务）
Task 是 Agent 需要完成的具体工作单元：
- **研究任务**：收集关于指定主题的信息
- **写作任务**：基于研究结果生成完整报告

### Crew（团队）
Crew 协调多个 Agent 和 Task 的执行：
- 使用 `Process.sequential` 进行顺序执行
- 支持任务间的上下文传递

## 运行步骤

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 配置环境变量
在 `.env` 文件中设置：
```env
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL_NAME=gpt-4
# 或使用其他 LLM 提供商
```

### 3. 运行示例
```bash
python main.py
```

## 输出
程序将在 `output/` 目录下生成 `basic_report.md` 文件，包含完整的研究报告。

## 关键特性展示
- ✅ Agent 的基本配置（role, goal, backstory）
- ✅ Task 的定义和预期输出
- ✅ 顺序流程（Sequential Process）
- ✅ 任务上下文传递（context）
- ✅ 输出到文件（output_file）
- ✅ 记忆功能（memory）
- ✅ 详细日志（verbose）
