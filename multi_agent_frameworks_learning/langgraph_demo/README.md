# LangGraph 入门教程 - 工作流编排

> **LangGraph** 是 LangChain 生态中用于构建有状态、多步骤 AI 应用的框架，通过**图（Graph）**结构编排复杂的工作流。

## 📖 框架简介

LangGraph 核心思想是将 AI 应用建模为**状态图**：

- **State（状态）**：在工作流节点间传递的共享数据
- **Node（节点）**：处理状态的函数
- **Edge（边）**：连接节点，决定执行流程
- **Conditional Edge（条件边）**：根据状态动态路由到不同节点

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  Node A  │───▶│  Node B  │───▶│  Node C  │───▶│   END    │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
                     │
                     ▼ 条件路由
              ┌──────────────┐
              │  Node D (可选) │
              └──────────────┘
```

## 🎯 本示例场景

实现一个 **智能客服工作流系统**：

| 步骤 | 节点 | 功能 |
|------|------|------|
| 1 | `intent_recognition` | 识别用户问题意图 |
| 2 | `categorize` | 将问题分类到对应部门 |
| 3 | `generate_response` | 生成专业回复 |
| 4 | `summarize` | 输出完整工单总结 |

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
python langgraph_intro.py
```

## 📁 项目文件说明

```
langgraph_demo/
├── langgraph_intro.py   # 主程序：包含完整的客服工作流示例
└── requirements.txt     # Python 依赖
```

## 📚 核心代码解读

### 1. 定义 State

```python
class CustomerServiceState(TypedDict):
    user_query: str       # 用户原始问题
    intent: str           # 识别出的意图
    category: str         # 问题分类
    response: str         # 生成的回答
    messages: Annotated[list, add_messages]  # 对话历史
```

### 2. 定义 Node（每个节点是一个函数）

```python
def intent_recognition_node(state: CustomerServiceState) -> dict:
    """分析用户问题，识别意图"""
    query = state["user_query"]
    # ... 处理逻辑
    return {"intent": "price_inquiry"}  # 返回需要更新的字段
```

### 3. 构建工作流图

```python
workflow = StateGraph(CustomerServiceState)
workflow.add_node("intent_recognition", intent_recognition_node)
workflow.add_edge("intent_recognition", "categorize")
workflow.add_conditional_edges("categorize", route_by_category, {...})
app = workflow.compile(checkpointer=MemorySaver())
```

### 4. 执行工作流

```python
result = app.invoke(
    {"user_query": "这个产品多少钱？"},
    config={"configurable": {"thread_id": "session-1"}}
)
```

## 🔑 关键概念对照表

| 概念 | 说明 | 类比 |
|------|------|------|
| `StateGraph` | 有状态的工作流图 | 流水线 |
| `TypedDict` | 状态的数据类型定义 | 传送带上的货物清单 |
| `Node` | 处理函数 | 工位上的工人 |
| `Edge` | 固定连接 | 固定传送路径 |
| `Conditional Edge` | 条件连接 | 分拣机，根据货物走不同路线 |
| `MemorySaver` | 记忆/检查点 | 流水线的记录仪，可恢复 |

## 📖 进阶学习方向

- [LangGraph 官方文档](https://langchain-ai.github.io/langgraph/)
- 使用 LLM 增强节点能力（见代码中的 `build_llm_customer_service_graph`）
- 添加 Tool（工具调用）支持
- 实现人机协作（Human-in-the-loop）
- 使用持久化检查点（SQLite/PostgreSQL）

## 💡 适用场景

- ✅ 多步骤任务处理流程
- ✅ 需要条件分支的业务逻辑
- ✅ 需要状态管理和恢复的应用
- ✅ 复杂的 AI Agent 编排

---

*基于 LangGraph >= 0.2.0*
