# 示例4：复杂工作流

## 概述
这是最全面的示例，展示了 CrewAI 的所有高级特性和最佳实践。

## 核心特性演示

### 1️⃣ **分层流程 vs 顺序流程**
```python
# 分层流程 - Manager Agent 智能分配任务
process=Process.hierarchical,
manager_agent=chief_analyst,

# 顺序流程 - 按预定义顺序执行
process=Process.sequential,
```

**区别：**
- **Hierarchical**: Manager 根据角色自动决定谁执行什么任务
- **Sequential**: 严格按照任务定义顺序执行

### 2️⃣ **防护措施**
两种类型的防护机制：

#### 函数式防护（精确控制）
```python
def validate_summary(result: TaskOutput) -> tuple:
    word_count = len(result.raw.split())
    if word_count < 50:
        return (False, "太短了")
    return (True, result.raw)
```

#### LLM 防护（语义理解）
```python
guardrail="报告必须包含定量数据和具体数字"
```

**优势：**
- ✅ 确保输出质量
- ✅ 自动重试机制
- ✅ 支持多重验证

### 3️⃣ **Pydantic 结构化输出**
```python
class FinalReport(BaseModel):
    executive_summary: str
    key_insights: List[MarketInsight]
    recommendations: List[StrategicRecommendation]

task = Task(
    ...,
    output_pydantic=FinalReport
)
```

**好处：**
- 类型安全的数据结构
- 易于程序化处理
- 强制字段完整性
- 支持嵌套模型

### 4️⃣ **推理模式**
```python
agent = Agent(
    ...,
    reasoning=True,
    max_reasoning_attempts=3
)
```
Agent 在执行前会先进行反思和规划。

### 5️⃣ **上下文窗口管理**
```python
respect_context_window=True  # 自动总结超长对话
```

### 6️⃣ **回调函数**
```python
# 任务完成回调
callback=task_completion_callback

# 步骤级回调
step_callback=step_callback
```

### 7️⃣ **日期注入**
```python
inject_date=True,
date_format="%Y年%m月%d日"
```

## 架构图

```
┌─────────────────────────────────────────────────────┐
│                  Hierarchical Process                │
│                                                      │
│  ┌──────────┐                                        │
│  │ Manager   │ ← Chief Analyst                      │
│  │ (协调者)   │   推理模式 + 委派权限                   │
│  └────┬─────┘                                        │
│       │                                              │
│  ┌────┴────────────────────────────┐                 │
│  ↓         ↓          ↓           ↓                 │
│ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────────┐             │
│ │市场   │ │风险  │ │战略  │ │最终报告  │             │
│ │情报   │ │评估  │ │规划  │ │(防护措施) │             │
│ └──────┘ └──────┘ └──────┘ └──────────┘             │
│    ↑         ↑         ↑         ↑                  │
│    └─────────┴─────────┴─────────┘                  │
│              Context Passing                        │
│                                                      │
│  Guardrails:                                         │
│  ✓ 长度验证                                          │
│  ✓ 内容完整性                                        │
│  ✓ 格式检查                                          │
│  ✓ LLM语义验证                                       │
│                                                      │
│  Output:                                             │
│  ✓ Pydantic Model (FinalReport)                     │
│  ✓ Markdown File                                    │
│  ✓ Structured Data                                  │
└─────────────────────────────────────────────────────┘
```

## 数据流

```
Inputs: business_domain
    ↓
[Task 1] Market Intelligence Gathering
    ↓ Output: Market data, trends
[Task 2] Risk Assessment (with Guardrails)
    ↓ Output: Risk matrix, mitigations
    ↓ Validation: ✓ Custom function + LLM check
[Task 3] Strategy Formulation
    ↓ Output: Strategic recommendations (Pydantic)
[Task 4] Final Report Generation
    ↓ Multiple Guardrails validation
    ↓ Output: FinalReport (Pydantic) + Markdown file
Result → Access via task.output.pydantic
```

## 运行方式

### 安装
```bash
pip install -r requirements.txt
```

### 环境变量 (.env)
```env
OPENAI_API_KEY=your_key
OPENAI_MODEL_NAME=gpt-4  # 推荐 GPT-4 以获得最佳效果
SERPER_API_KEY=your_serper_key  # 可选，用于搜索
```

### 运行
```bash
python main.py
```

### 切换流程类型
在 `main.py` 中修改：
```python
use_hierarchical = True   # 分层流程
use_hierarchical = False  # 顺序流程
```

## 输出文件
- `output/advanced_workflow_report.md` - 完整的分析报告
- 通过 `final_report_task.output.pydantic` 访问结构化数据

## 性能优化提示

### 1. **速率限制**
```python
max_rpm=15  # 避免 API 限流
```

### 2. **迭代控制**
```python
max_iter=25  # 平衡质量和成本
```

### 3. **上下文管理**
```python
respect_context_window=True  # 处理长文档
```

### 4. **模型选择**
- **GPT-4**: 最佳质量，适合复杂推理
- **GPT-4o-mini**: 性价比高，适合简单任务
- **function_calling_llm**: 可为工具调用使用更便宜的模型

## 学习要点总结

### 基础概念
- ✅ Agent 的核心属性配置
- ✅ Task 的详细参数设置
- ✅ Crew 的组织方式

### 中级特性
- ✅ 多种流程模式选择
- ✅ 工具集成和使用
- ✅ 上下文传递机制

### 高级特性
- ✅ 输出质量控制（Guardrails）
- ✅ 结构化数据输出（Pydantic）
- ✅ 推理和规划能力
- ✅ 回调和监控
- ✅ 错误处理和重试

### 生产就绪
- ✅ 速率限制和成本控制
- ✅ 上下文窗口管理
- ✅ 内存和状态保持
- ✅ 日志和可观察性

## 适用场景

这个示例适用于：
- 🏢 企业战略规划
- 📊 市场进入分析
- 💼 投资决策支持
- 🎯 产品路线图制定
- ⚠️ 风险评估和管理
- 📋 综合报告生成

## 扩展建议

1. **添加更多工具**: 集成数据库查询、API调用等
2. **自定义嵌入器**: 使用领域特定的嵌入模型
3. **知识源**: 添加公司内部文档库
4. **异步执行**: 对独立任务启用 `async_execution=True`
5. **人工审核**: 在关键节点添加 `human_input=True`
6. **持久化**: 保存和恢复长时间运行的工作流
