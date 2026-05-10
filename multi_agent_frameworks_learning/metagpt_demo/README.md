# MetaGPT 入门教程 - 模拟软件公司运作

> **MetaGPT** 是一个独特的多Agent框架，它**模拟真实软件公司的组织结构和运作流程**，让不同的"员工角色"协作完成软件开发任务。

## 📖 框架简介

MetaGPT 将软件开发过程建模为一家**虚拟软件公司**：

- **Role（职位）**：公司中的岗位角色（产品经理、架构师、工程师、测试等）
- **Action（动作）**：角色执行的具体工作（写PRD、设计架构、写代码等）
- **Environment（环境）**：公司办公环境，角色在其中通信协作
- **Message（消息）**：角色之间传递的工作成果
- **Team（团队）**：将多个角色组成项目团队

```
        ┌──────────────────────────────┐
        │        Software Company      │
        │          (Environment)       │
        │                              │
        │  ┌─────┐  ┌─────┐  ┌─────┐  │
        │  │ PM  │─▶│Arch │─▶│Eng  │  │
        │  │     │  │     │  │     │  │
        │  └─────┘  └─────┘  └──┬──┘  │
        │                      │      │
        │                      ▼      │
        │                   ┌─────┐   │
        │                   │ QA  │   │
        │                   └─────┘   │
        └──────────────────────────────┘

工作流: 需求 → PRD → 设计 → 代码 → 测试
```

## 🎯 本示例场景

模拟一个 **软件公司开发「智能任务管理系统」**：

| 角色 | 姓名 | 职位 | 交付物 |
|------|------|------|--------|
| 👩‍💼 Alice | Product Manager | 产品经理 | PRD需求文档 |
| 👨‍💻 Bob | Architect | 架构师 | 系统架构设计文档 |
| 👨‍💻 Charlie | Senior Engineer | 高级工程师 | 源代码实现 |
| 👩‍🔬 Diana | QA Engineer | 测试工程师 | 测试计划与用例 |

### 开发流程

```
📋 公司需求输入
       ↓
┌──────────────────┐
│  产品经理 (Alice) │ → 输出: PRD文档（用户故事、功能清单、验收标准）
└────────┬─────────┘
         ↓ PRD完成
┌──────────────────┐
│  架构师 (Bob)    │ → 输出: 架构文档（技术选型、服务拆分、数据模型）
└────────┬─────────┘
         ↓ 设计完成
┌──────────────────┐
│  工程师 (Charlie)│ → 输出: 代码（后端API + 前端组件 + README）
└────────┬─────────┘
         ↓ 代码完成
┌──────────────────┐
│  测试工程师(Diana)│ → 输出: 测试用例（单元/集成/E2E/性能测试）
└──────────────────┘
```

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
python metagpt_intro.py
```

## 📁 项目文件说明

```
metagpt_demo/
├── metagpt_intro.py   # 主程序：包含完整的软件公司模拟
└── requirements.txt   # Python 依赖
```

## 📚 核心代码解读

### 1. 定义 Action（动作——角色能做什么）

```python
class WritePRD(Action):
    """撰写PRD的动作"""
    name = "WritePRD"

    async def run(self, requirement: str) -> str:
        prd_content = "# 产品需求文档\n..."
        return prd_content


class DesignArchitecture(Action):
    """设计架构的动作"""
    name = "DesignArchitecture"

    async def run(self, prd: str) -> str:
        architecture_doc = "# 系统架构设计\n..."
        return architecture_doc
```

### 2. 定义 Role（角色——谁来做）

```python
class ProductManager(Role):
    name = "Alice"
    profile = "Product Manager"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.actions = [WritePRD]           # 这个角色会做的动作
        self._watch = {WritePRD}            # 监听的消息类型
```

### 3. 组建 Team（团队）

```python
env = Environment(desc="软件开发团队环境")

team = Team(
    roles=[ProductManager(), Architect(), Engineer(), QaEngineer()],
    env=env,
    desc="智能任务管理系统开发团队",
)
```

### 4. 投入需求，启动工作流

```python
requirement = "我们需要开发一个任务管理系统..."
result = await team.run(requirement)  # 一行启动整个开发流程！
```

## 🔑 关键概念对照表

| 概念 | 说明 | 类比 |
|------|------|------|
| `Role` | 公司职位 | 员工岗位（PM/开发/QA） |
| `Action` | 动作/技能 | 岗位职责（写PRD/写代码/写测试） |
| `Environment` | 环境 | 公司办公室/协作空间 |
| `Message` | 消息 | 工作邮件/文档交接 |
| `Team` |团队 | 项目组 |
| `_watch` | 监听 | 关注哪些工作成果 |
| `profile` | 职位描述 | 岗位JD（职位描述） |
| `goal` | 目标 | KPI/OKR |
| `backstory` | 背景 | 个人履历/经验 |

## 📖 内置角色一览

MetaGPT 提供了丰富的预置角色：

| 角色 | 类名 | 功能 |
|------|------|------|
| 产品经理 | `ProductManager` | 写PRD |
| 架构师 | `Architect` | 写设计文档 |
| 工程师 | `Engineer` | 写代码 |
| 测试工程师 | `QaEngineer` | 写测试用例 |
| 项目经理 | `ProjectManager` | 项目规划和进度管理 |
| 技术文档撰写 | `TechnicalWriter` | 写技术文档 |
| 数据分析师 | `DataAnalyst` | 数据分析和可视化 |
| 代码审查员 | `CodeReviewer` | 代码质量检查 |

## 💡 适用场景

- ✅ 软件项目全流程开发
- ✅ 需要多角色协作的复杂任务
- ✅ 文档驱动的开发流程
- ✅ 想要标准化SOP的场景
- ✅ 模拟和演练软件开发流程

## 📖 进阶学习方向

- [MetaGPT 官方文档](https://metagpt.readthedocs.io/)
- 使用内置角色快速搭建团队
- 自定义Role和Action扩展能力
- SOP（标准作业流程）定制
- 人机协作（Human-in-the-loop）
- 持久化和增量开发

---

*基于 MetaGPT >= 0.8.0*
