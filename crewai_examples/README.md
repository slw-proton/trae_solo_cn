# CrewAI 学习示例集合 🚀

基于 [CrewAI 官方文档](https://docs.crewai.org.cn/) 开发的完整学习示例，涵盖从入门到高级的所有核心概念。

## 📚 示例列表

### 1️⃣ **基础 Agent 和 Task** (`example01_basic_agent_task/`)
**难度**: ⭐ 入门 | **预计时间**: 15分钟

学习 CrewAI 的最基本用法：
- ✅ 创建自定义 Agent（角色、目标、背景故事）
- ✅ 定义 Task（描述、预期输出）
- ✅ 组建 Crew 并执行顺序流程
- ✅ 任务间的上下文传递
- ✅ 输出到文件

**适用场景**: 第一次接触 CrewAI，想快速上手

---

### 2️⃣ **多 Agent 协作** (`example02_multi_agent_collaboration/`)
**难度**: ⭐⭐ 进阶 | **预计时间**: 20分钟

体验多个专业化 Agent 的团队协作：
- ✅ 5个不同角色的专业 Agent
- ✅ 复杂的任务链式依赖
- ✅ 任务委派机制
- ✅ 大规模上下文共享
- ✅ 综合报告生成

**适用场景**: 需要模拟真实团队的复杂任务

---

### 3️⃣ **工具使用** (`example03_tools_usage/`)
**难度**: ⭐⭐ 进阶 | **预计时间**: 20分钟

掌握如何为 Agent 配置强大的工具集：
- ✅ SerperDevTool - Google 搜索
- ✅ FileReadTool - 本地文件读取
- ✅ DirectoryReadTool - 目录浏览
- ✅ TXTSearchTool - 文本搜索
- ✅ WebsiteSearchTool - 网站内搜索
- ✅ 工具与角色的最佳匹配策略

**适用场景**: 需要 Agent 与外部世界交互

---

### 4️⃣ **高级工作流** (`example04_advanced_workflow/`)
**难度**: ⭐⭐⭐⭐ 高级 | **预计时间**: 30分钟

探索 CrewAI 的所有高级特性：
- ✅ **分层流程 vs 顺序流程**
- ✅ **防护措施** - 函数式 + LLM 语义验证
- ✅ **Pydantic 结构化输出** - 类型安全的数据模型
- ✅ **推理模式** - Agent 执行前先思考
- ✅ **回调函数** - 任务监控和日志
- ✅ **上下文窗口管理** - 自动处理长对话
- ✅ **日期注入** - 时间感知的任务执行
- ✅ **错误处理和重试机制**

**适用场景**: 生产级应用，需要质量控制和可靠性

## 🎯 学习路径建议

```
新手路径:
  Example 1 → Example 2 → Example 3 → Example 4

有经验开发者:
  Example 1 (快速浏览) → Example 3 (重点) → Example 4 (深入)

研究人员:
  Example 2 → Example 4 (重点关注流程和输出控制)
```

## 🔧 环境配置

### 1. 安装 Python 依赖

每个示例目录都有独立的 `requirements.txt`：

```bash
# 进入任意示例目录
cd example01_basic_agent_task

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置环境变量

在项目根目录或各示例目录创建 `.env` 文件：

```env
# 必需: OpenAI API 密钥
OPENAI_API_KEY=sk-your_openai_api_key_here

# 可选: 模型选择（默认 gpt-4）
OPENAI_MODEL_NAME=gpt-4

# 可选: 用于搜索功能（Example 3, 4）
SERPER_API_KEY=your_serper_dev_api_key
```

#### 获取 API 密钥：
- **OpenAI**: https://platform.openai.com/api-keys
- **Serper**: https://serper.dev (有免费额度)

## 🚀 快速开始

### 运行第一个示例

```bash
cd crewai_examples/example01_basic_agent_task

# 配置环境变量
cp .env.example .env
# 编辑 .env 填入你的 API 密钥

# 运行
python main.py
```

### 预期输出

你将在 `output/` 目录看到生成的报告文件，并在控制台看到详细的执行日志。

## 📁 项目结构

```
crewai_examples/
├── README.md                           # 本文件
├── example01_basic_agent_task/         # 基础示例
│   ├── main.py                         # 主程序
│   ├── requirements.txt                # 依赖
│   ├── README.md                       # 详细说明
│   └── output/                         # 输出目录
│       └── basic_report.md             # 生成的报告
│
├── example02_multi_agent_collaboration/ # 多Agent协作
│   ├── main.py
│   ├── requirements.txt
│   ├── README.md
│   └── output/
│       └── comprehensive_market_analysis.md
│
├── example03_tools_usage/              # 工具使用
│   ├── main.py
│   ├── requirements.txt
│   ├── README.md
│   └── output/
│       └── tools_analysis_report.md
│
└── example04_advanced_workflow/        # 高级工作流
    ├── main.py
    ├── requirements.txt
    ├── README.md
    └── output/
        └── advanced_workflow_report.md
```

## 💡 核心概念速查

### Agent（代理）
```python
agent = Agent(
    role="角色定义",
    goal="目标",
    background="背景故事",
    verbose=True,           # 详细日志
    memory=True,            # 记忆功能
    allow_delegation=True,  # 允许委派任务
    tools=[...],            # 工具列表
)
```

### Task（任务）
```python
task = Task(
    description="任务描述",
    expected_output="预期输出",
    agent=agent,                    # 负责的Agent
    context=[other_task],           # 依赖的任务
    output_file="report.md",        # 输出文件
    guardrails=[validate_func],     # 防护措施
    output_pydantic=MyModel,        # 结构化输出
)
```

### Crew（团队）
```python
crew = Crew(
    agents=[...],
    tasks=[...],
    process=Process.sequential,      # 或 Process.hierarchical
    verbose=True,
    memory=True,
)

result = crew.kickoff(inputs={'key': 'value'})
```

## 🎨 流程类型对比

| 特性 | Sequential (顺序) | Hierarchical (分层) |
|------|------------------|---------------------|
| 执行顺序 | 按定义顺序 | Manager智能分配 |
| 适用场景 | 简单线性流程 | 复杂协作 |
| 任务分配 | 明确指定 | 动态决定 |
| 推荐度 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

## 🛡️ 质量控制特性

### Guardrails（防护措施）
- **函数式验证**: 精确控制（长度、格式等）
- **LLM验证**: 语义理解（质量、完整性等）
- **自动重试**: 验证失败时自动改进

### Pydantic 输出
- 强制数据结构
- 类型安全
- 易于程序化处理
- 支持嵌套模型

## 📊 性能优化建议

### 降低成本
```python
# 使用更便宜的模型做工具调用
function_calling_llm="gpt-4o-mini"

# 限制API调用速率
max_rpm=15

# 控制迭代次数
max_iter=15
```

### 提高质量
```python
# 启用推理模式
reasoning=True

# 增加记忆
memory=True

# 使用防护措施
guardrails=[validate_func]
```

### 处理长文本
```python
# 自动管理上下文窗口
respect_context_window=True
```

## ❓ 常见问题

### Q: 需要哪个 OpenAI 模型？
A: 推荐 GPT-4 以获得最佳效果。GPT-3.5 可以运行但质量较低。

### Q: API 成本高怎么办？
A: 
- 使用 `gpt-4o-mini` 作为 `function_calling_llm`
- 设置合理的 `max_iter` 和 `max_rpm`
- 使用 `cache=True` (默认启用)

### Q: 如何调试？
A: 设置 `verbose=True` 查看详细日志，使用回调函数监控执行。

### Q: 支持其他 LLM 提供商吗？
A: 是！CrewAI 支持 OpenAI、Anthropic、Azure、本地模型等。

## 🌟 最佳实践

1. **明确的角色定义**: 每个 Agent 应该有清晰的专业领域
2. **具体的任务描述**: 避免模糊的指令
3. **合理的预期输出**: 定义清晰的输出格式要求
4. **适当的工具匹配**: 根据角色配备合适的工具
5. **质量控制**: 在生产环境使用 Guardrails 和 Pydantic
6. **成本意识**: 平衡质量和 API 成本

## 📖 延伸学习

- [CrewAI 官方文档](https://docs.crewai.org.cn/)
- [CrewAI GitHub](https://github.com/crewAIInc/crewAI)
- [CrewAI 工具库](https://github.com/joaomdmoura/crewai-tools)
- [CrewAI 社区](https://community.crewai.com/)

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

---

**Happy Coding with CrewAI! 🎉**

如有问题或建议，欢迎在社区讨论。
