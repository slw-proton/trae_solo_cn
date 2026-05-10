# AutoGen 入门教程 - 多Agent对话框架

> **AutoGen** 是微软开源的**多Agent对话框架**，专注于让多个 AI Agent 通过对话协作解决问题，尤其擅长**代码生成与执行**。

## 📖 框架简介

AutoGen 的核心是**对话驱动**的多Agent协作：

- **ConversableAgent**：所有可对话Agent的基类
- **AssistantAgent**：AI助手，擅长生成文本和代码
- **UserProxyAgent**：人类代理，可代表人类参与对话并**执行代码**
- **GroupChat**：多Agent群聊模式，支持多人讨论
- **Code Executor**：内置代码执行环境

```
┌──────────────────┐         对话          ┌──────────────────┐
│                  │ ◄────────────────────► │                  │
│ AssistantAgent   │                       │ UserProxyAgent   │
│ (AI助手)         │ ────────────────────▶ │ (人类代理+代码执行)│
│                  │         回复           │                  │
└──────────────────┘                       └──────────────────┘

GroupChat 群聊模式：
         ┌─────────────┐
         │ GroupChat   │
         │  Manager    │
         └──────┬──────┘
    ┌───────────┼───────────┐
    ▼           ▼           ▼
┌───────┐  ┌───────┐  ┌───────┐
│Agent A│  │Agent B│  │Agent C│
└───────┘  └───────┘  └───────┘
```

## 🎯 本示例场景（4个演示）

### 场景1：两Agent对话 — AI编程导师
- **AssistantAgent**：Python编程导师，解答编程问题
- **UserProxyAgent**：学员，发起提问

### 场景2：多Agent群聊 — 技术方案评审会议
- 产品经理 + 架构师 + 开发工程师 + 会议主持人
- 模拟真实的团队讨论和决策过程

### 场景3：编程助手 — 数据分析与可视化
- 利用AutoGen强大的**代码执行**能力
- 生成代码 → 自动运行 → 查看结果 → 错误修复 → 优化

### 场景4：自定义Agent — 专家咨询团
- 继承 `ConversableAgent` 创建专用专家Agent
- 法律顾问 + 财务顾问 + HR顾问

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
# 默认运行场景1（两Agent对话）
python autogen_intro.py
```

## 📁 项目文件说明

```
autogen_demo/
├── autogen_intro.py   # 主程序：包含4个演示场景
└── requirements.txt   # Python 依赖
```

## 📚 核心代码解读

### 1. 创建 AssistantAgent

```python
assistant = AssistantAgent(
    name="编程导师",
    system_message="你是一位资深的Python编程导师...",  # 角色设定
    llm_config={
        "config_list": config_list,     # LLM配置
        "temperature": 0.7,             # 创造性程度
    },
    human_input_mode="NEVER",           # 不需要人工干预
    max_consecutive_auto_reply=10,      # 最大连续自动回复次数
)
```

### 2. 创建 UserProxyAgent（关键：可执行代码）

```python
user_proxy = UserProxyAgent(
    name="学员",
    code_execution_config={             # ⭐ 代码执行配置
        "work_dir": "coding_workspace",# 工作目录
        "use_docker": False,           # 是否使用Docker
    },
    max_consecutive_auto_reply=5,
)
```

### 3. 发起两Agent对话

```python
chat_result = user_proxy.initiate_chat(
    recipient=assistant,               # 对话对象
    message="你好！我想学习Python...",  # 初始消息
    max_turns=10,                      # 最大对话轮次
)
```

### 4. 创建群聊

```python
group_chat_manager = autogen.GroupChatManager(
    groupchat=autogen.GroupChat(
        agents=[pm, architect, dev],   # 参与者
        max_round=12,                  # 最大讨论轮数
        speaker_selection_method="round_robin",  # 发言顺序策略
    ),
)

result = moderator.initiate_chat(     # 由主持人发起群聊
    recipient=group_chat_manager,
    message="让我们讨论一下技术方案...",
)
```

### 5. 自定义Agent

```python
class SpecializedAgent(ConversableAgent):
    def __init__(self, name, specialty, **kwargs):
        super().__init__(
            name=name,
            system_message=f"你是一位{specialty}专家...",
            **kwargs
        )
    
    def generate_reply(self, messages, sender, config):
        # 自定义回复逻辑
        return super().generate_reply(messages, sender, config)
```

## 🔑 关键概念对照表

| 概念 | 说明 | 特点 |
|------|------|------|
| `AssistantAgent` | AI助手 | 擅长生成文本/代码 |
| `UserProxyAgent` | 人类代理 | 可执行代码、可转交人工 |
| `GroupChatManager` | 群聊管理员 | 控制发言顺序和流程 |
| `code_execution_config` | 代码执行环境 | AutoGen核心优势之一 |
| `human_input_mode` | 人工输入模式 | NEVER/ALWAYS/TERMINATE |
| `max_consecutive_auto_reply` | 最大连续自动回复 | 控制对话深度 |
| `is_termination_msg` | 终止判断函数 | 决定何时结束对话 |
| `speaker_selection_method` | 发言选择方式 | round_robin/auto/custom |

## 📖 进阶学习方向

- [AutoGen 官方文档](https://github.com/microsoft/autogen)
- 使用工具（Tool Use）扩展Agent能力
- RAG（检索增强生成）集成
- 多模态Agent（图像/音频处理）
- 与外部系统交互（数据库、API等）
- 使用本地模型（Ollama/LM Studio）

## 💡 适用场景

- ✅ 编程助手（代码生成+执行+调试循环）
- ✅ 多角色讨论和决策
- ✅ 需要代码验证的技术任务
- ✅ 个人AI助手/导师
- ✅ 需要人机协作的场景

---

*基于 pyautogen >= 0.2.0*
