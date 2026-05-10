# CrewAI 入门教程 - 角色扮演式Agent团队

> **CrewAI** 是一个用于构建**多角色 AI 团队**的框架，让多个具有不同专业背景的 AI Agent 协作完成复杂任务。

## 📖 框架简介

CrewAI 的核心哲学是模拟真实团队协作：

- **Agent（智能体）**：拥有特定角色、目标、背景和能力的"虚拟员工"
- **Task（任务）**：分配给 Agent 的具体工作项
- **Crew（团队）**：组织多个 Agent 协同工作的容器
- **Process（流程）**：定义任务的执行顺序和依赖关系

```
        ┌─────────────┐
        │    Crew     │  ← 团队容器
        │             │
   ┌────┴────┬────────┴────┐
   ▼         ▼             ▼
┌──────┐ ┌──────┐     ┌──────┐
│Agent │ │Agent │ ... │Agent │  ← 角色成员
│  A   │ │  B   │     │  N   │
└──┬───┘ └──┬───┘     └──┬───┘
   │        │            │
   ▼        ▼            ▼
 Task A   Task B      Task N   ← 分配的任务
   │                    ↑
   └────────────────────┘
        Context（依赖）
```

## 🎯 本示例场景

构建一个 **内容创作团队**：

| 角色 | 代号 | 职责 |
|------|------|------|
| 🎭 资深内容策划师 | Researcher | 研究主题，收集素材 |
| ✍️ 专业内容创作者 | Writer | 基于素材撰写文章 |
| 🔍 首席编辑 | Editor | 审核修改，确保质量 |

**工作流程**：研究策划 → 内容撰写 → 编辑审核

## 🚀 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 设置环境变量

```bash
export OPENAI_API_KEY="your-openai-api-key"
```

### 运行示例

```bash
python crewai_intro.py
```

## 📁 项目文件说明

```
crewai_demo/
├── crewai_intro.py   # 主程序：包含完整的内容创作团队示例
└── requirements.txt  # Python 依赖
```

## 📚 核心代码解读

### 1. 创建 Agent（定义角色）

```python
researcher = Agent(
    role="资深内容策划师",          # 角色名称
    goal="深入研究和分析主题",       # 目标
    backstory="10年经验...",        # 背景故事（影响行为风格）
    verbose=True,                   # 显示思考过程
    allow_delegation=False,         # 是否允许委派任务给其他Agent
    llm=llm,                        # 使用的LLM模型
)
```

### 2. 创建 Task（定义任务）

```python
research_task = Task(
    description="请对以下主题进行全面研究...",  # 任务描述
    expected_output="一份详细的研究报告...",     # 期望输出格式
    agent=researcher,                           # 负责该任务的Agent
    context=[],                                 # 依赖的前置任务
)
```

### 3. 组装 Crew（组建团队）

```python
crew = Crew(
    agents=[researcher, writer, editor],       # 团队成员
    tasks=[research_task, writing_task, edit_task],  # 任务列表
    process=Process.sequential,                 # 顺序执行
    verbose=True,
    memory=True,                                # 启用团队记忆
)
```

### 4. 启动团队

```python
result = crew.kickoff()  # 开始执行！
print(result)            # 输出最终结果
```

## 🔑 关键概念对照表

| 概念 | 说明 | 参数/属性 |
|------|------|-----------|
| `role` | Agent的角色名称 | `"产品经理"` |
| `goal` | Agent的目标 | `"分析用户需求"` |
| `backstory` | Agent的背景故事 | 影响回复风格和专业度 |
| `Task.description` | 任务的具体要求 | 详细指令 |
| `Task.expected_output` | 期望的输出格式 | 结构化输出要求 |
| `Task.context` | 任务依赖关系 | `[task_a, task_b]` |
| `Process.sequential` | 顺序执行 | A→B→C |
| `Process.hierarchical` | 层级执行 | 经理分配给下属 |
| `allow_delegation` | 允许任务委派 | Agent间可以分活 |

## 📖 进阶学习方向

- [CrewAI 官方文档](https://docs.crewai.com/)
- 为 Agent 配置工具（搜索、代码执行、API调用等）
- 并行任务执行（多个研究员同时调研）
- 层级管理结构（经理→组长→组员）
- 自定义工具开发
- 集成本地 LLM（Ollama）

## 💡 适用场景

- ✅ 内容创作与生成（文案、报告、方案）
- ✅ 多角度研究和分析
- ✅ 需要多轮审核的质量控制流程
- ✅ 模拟专业团队协作

---

*基于 CrewAI >= 0.51.0*
