"""
示例4：复杂工作流示例
演示 CrewAI 的高级特性：
- 分层流程 (Hierarchical Process)
- 防护措施 (Guardrails)
- Pydantic 结构化输出
- 回调函数
- 上下文窗口管理
- 推理模式 (Reasoning)
- 任务重试和错误处理
"""

from typing import List, Optional
from pydantic import BaseModel, Field
from crewai import Agent, Task, Crew, Process, TaskOutput


# ============ Pydantic 输出模型 ============

class MarketInsight(BaseModel):
    """市场洞察的数据模型"""
    category: str = Field(description="洞察类别")
    finding: str = Field(description="具体发现")
    impact: str = Field(description="影响程度: high/medium/low")
    confidence: float = Field(description="置信度 0.0-1.0")

class StrategicRecommendation(BaseModel):
    """战略建议的数据模型"""
    priority: int = Field(description="优先级 1-5")
    action: str = Field(description="具体行动")
    rationale: str = Field(description="理由说明")
    timeline: str = Field(description="建议时间线")
    resources: str = Field(description="所需资源")

class FinalReport(BaseModel):
    """最终报告的结构化输出模型"""
    executive_summary: str = Field(description="执行摘要，200字以内")
    key_insights: List[MarketInsight] = Field(description="关键洞察列表，3-5个")
    recommendations: List[StrategicRecommendation] = Field(description="战略建议列表，3-5个")
    risk_assessment: str = Field(description="风险评估")
    next_steps: str = Field(description="下一步行动计划")


# ============ 防护措施函数 ============

def validate_executive_summary(result: TaskOutput) -> tuple:
    """验证执行摘要的质量"""
    try:
        text = result.raw.strip()

        # 检查长度
        word_count = len(text.split())
        if word_count < 50:
            return (False, f"执行摘要太短: {word_count} 字。至少需要50字。")
        if word_count > 300:
            return (False, f"执行摘要太长: {word_count} 字。最多300字。")

        # 检查是否包含关键要素
        required_keywords = ['结论', '建议', '风险']
        missing = [kw for kw in required_keywords if kw not in text]
        if missing:
            return (False, f"执行摘要缺少关键要素: {', '.join(missing)}")

        return (True, text)

    except Exception as e:
        return (False, f"验证失败: {str(e)}")


def validate_recommendations(result: TaskOutput) -> tuple:
    """验证战略建议的质量"""
    try:
        text = result.raw

        # 检查是否包含具体的行动项
        if '1.' not in text and '•' not in text and '-' not in text:
            return (False, "建议必须以编号或项目符号列表格式呈现")

        # 检查最小数量（至少3个建议）
        lines = [line for line in text.split('\n') if line.strip()
                 and (line.strip().startswith(('1.', '2.', '3.', '4.', '5.',
                                               '-', '*', '•')))]
        if len(lines) < 3:
            return (False, f"至少需要3个战略建议，当前只有{len(lines)}个")

        return (True, result.raw)

    except Exception as e:
        return (False, f"验证失败: {str(e)}")


# ============ 回调函数 ============

def task_completion_callback(task_output: TaskOutput):
    """任务完成时的回调函数"""
    print(f"\n📋 任务完成回调:")
    print(f"   描述: {task_output.summary}")
    print(f"   输出长度: {len(task_output.raw)} 字符")


def step_callback(step_info):
    """每个步骤的回调"""
    print(f"  ⚙️  执行步骤: {step_info}")


# ============ 主程序 ============

def main():
    print("=" * 70)
    print("CrewAI 示例4：高级工作流特性演示")
    print("=" * 70)

    # 1. 创建具有高级特性的 Agents

    # 首席分析师 - 使用推理模式
    chief_analyst = Agent(
        role="首席战略分析师",
        goal="提供深度战略分析和决策支持",
        backstory="你是一位拥有20年经验的顶级战略顾问，曾为全球500强企业提供咨询。"
                 "你擅长系统思考和复杂的战略规划。"
                 "你总是先深入思考再给出建议。",
        verbose=True,
        memory=True,
        reasoning=True,  # 启用推理模式
        max_reasoning_attempts=3,
        max_iter=25,
        respect_context_window=True,  # 自动管理上下文窗口
        allow_delegation=True,
        step_callback=step_callback,
    )

    # 市场情报专家 - 配备搜索工具
    market_intelligence_agent = Agent(
        role="市场情报专家",
        goal="收集和分析市场情报数据",
        backstory="你是一位专业的市场情报分析师，精通竞争情报和市场趋势分析。"
                 "你能够从海量信息中提取有价值的洞察。",
        verbose=True,
        memory=True,
        max_iter=20,
        max_rpm=15,  # 限制API调用速率
        respect_context_window=True,
    )

    # 风险评估专家
    risk_analyst = Agent(
        role="风险管理专家",
        goal="识别、评估和缓解潜在风险",
        backstory="你是一位认证风险管理师(FRM)，专注于企业战略风险。"
                 "你能够预见潜在问题并提供实用的缓解策略。",
        verbose=True,
        memory=True,
        max_iter=15,
        reasoning=True,
        inject_date=True,  # 注入当前日期
        date_format="%Y年%m月%d日",
    )

    # 战略规划专家
    strategist = Agent(
        role="战略规划总监",
        goal="制定清晰、可执行的战略计划",
        backstory="你是一位前麦肯锡合伙人，专长于将复杂分析转化为简单、可执行的策略。"
                 "你的建议总是务实且结果导向。",
        verbose=True,
        memory=True,
        allow_delegation=False,
        max_iter=20,
    )

    # 2. 定义带有防护措施的任务

    # 任务1：市场情报收集
    intelligence_gathering_task = Task(
        description="""
        对 {business_domain} 进行全面的市场情报收集：

        **市场环境分析：**
        - 市场规模和增长趋势（2023-2026预测）
        - 主要参与者和市场份额
        - 监管环境和政策影响

        **技术趋势：**
        - 新兴技术的影响
        - 数字化转型进展
        - 创新驱动力

        **客户洞察：**
        - 客户行为变化
        - 需求演变趋势
        - 痛点和机会

        当前日期请使用系统提供的日期。
        """,
        expected_output="""
        详细的市场情报报告，包括：
        - 定量数据（市场规模、增长率等）
        - 竞争格局图
        - 技术采用曲线
        - 客户细分分析
        """,
        agent=market_intelligence_agent,
    )

    # 任务2：风险评估（带防护措施）
    risk_assessment_task = Task(
        description="""
        基于市场情报，对 {business_domain} 进行全面的风险评估：

        **风险类别：**
        1. 战略风险 - 市场定位、竞争优势
        2. 运营风险 - 供应链、运营效率
        3. 技术风险 - 技术过时、网络安全
        4. 财务风险 - 现金流、成本控制
        5. 合规风险 - 法规变化、合规要求

        **对每个风险：**
        - 可能性评估（高/中/低）
        - 影响程度评估（严重/中等/轻微）
        - 风险评分（1-10）
        - 缓解策略
        """,
        expected_output="""
        结构化的风险评估矩阵，包括：
        - 风险热力图描述
        - Top 5 关键风险详解
        - 风险缓解优先级列表
        - 监控指标和预警信号
        """,
        agent=risk_analyst,
        context=[intelligence_gathering_task],
        guardrails=[
            validate_recommendations,  # 自定义防护措施
            "风险评估必须覆盖至少5个不同的风险类别",  # LLM防护措施
        ],
        guardrail_max_retries=3,  # 失败时最多重试3次
    )

    # 任务3：战略建议生成（带Pydantic输出）
    strategy_formulation_task = Task(
        description="""
        整合市场情报和风险评估，制定战略建议：

        **战略框架：**
        1. 短期战术（0-6个月）- 快速见效的行动
        2. 中期战略（6-18个月）- 能力建设重点
        3. 长期愿景（18-36个月）- 差异化定位

        **每个建议必须包含：**
        - 明确的行动项
        - 成功度量标准
        - 所需资源估算
        - 时间里程碑
        - 责任主体建议

        **质量标准：**
        - 建议必须具体可执行
        - 必须考虑资源约束
        - 必须与风险评估关联
        """,
        expected_output="""
        使用提供的Pydantic格式输出结构化的战略建议，
        包含3-5个优先级明确的行动建议。
        """,
        agent=strategist,
        context=[intelligence_gathering_task, risk_assessment_task],
        output_pydantic=StrategicRecommendation,  # 单个Pydantic对象
    )

    # 任务4：最终综合报告（带多重防护措施和完整Pydantic输出）
    final_report_task = Task(
        description="""
        创建最终的Executive Summary级别的综合报告：

        **报告结构：**

        ## Executive Summary (200字以内)
        - 核心发现（3点）
        - 关键建议（2点）
        - 主要风险警示（1点）

        ## 关键洞察 (3-5个)
        每个洞察包含：类别、发现、影响程度、置信度

        ## 战略建议 (3-5个)
        每个建议包含：优先级、行动、理由、时间线、资源

        ## 风险评估总结
        整体风险评级和主要关切

        ## 下一步行动
        具体的30-60-90天行动计划

        **格式要求：**
        - 专业、简洁、适合C-level阅读
        - 数据驱动，避免空泛陈述
        - 所有建议必须有据可依
        """,
        expected_output="""
        完整的综合报告，使用FinalReport Pydantic模型格式化输出。
        """,
        agent=chief_analyst,
        context=[intelligence_gathering_task, risk_assessment_task,
                 strategy_formulation_task],
        output_file="output/advanced_workflow_report.md",
        output_pydantic=FinalReport,  # 完整的Pydantic输出模型
        guardrails=[
            validate_executive_summary,  # 自定义验证函数
            "报告必须包含定量数据和具体数字",  # LLM验证
            "所有建议必须是可操作的，不能是泛泛而谈",  # LLM验证
        ],
        guardrail_max_retries=4,
        callback=task_completion_callback,  # 完成回调
        markdown=True,
    )

    # 3. 创建使用分层流程的团队
    hierarchical_crew = Crew(
        agents=[chief_analyst, market_intelligence_agent,
                risk_analyst, strategist],
        tasks=[intelligence_gathering_task, risk_assessment_task,
               strategy_formulation_task, final_report_task],
        process=Process.hierarchical,  # 使用分层流程！
        manager_agent=chief_analyst,  # 首席分析师作为管理者
        verbose=True,
        memory=True,
        embedder={
            "provider": "openai",
            "config": {
                "model": "text-embedding-ada-002"
            }
        },
    )

    # 同时也展示顺序流程
    sequential_crew = Crew(
        agents=[market_intelligence_agent, risk_analyst,
                strategist, chief_analyst],
        tasks=[intelligence_gathering_task, risk_assessment_task,
               strategy_formulation_task, final_report_task],
        process=Process.sequential,  # 顺序流程
        verbose=True,
        memory=True,
    )

    # 4. 执行任务
    inputs = {
        'business_domain': 'AI驱动的企业级SaaS平台'
    }

    print("\n" + "=" * 70)
    print(f"🎯 业务领域: {inputs['business_domain']}")
    print("=" * 70)
    print("\n🤖 团队成员及角色:")
    print("  ┌─────────────────────────────────────────────────────────────┐")
    print("  │ 🎩 首席战略分析师 (Manager)                                │")
    print("  │    ├─ 推理模式: ✅ 启用                                     │")
    print("  │    ├─ 任务委派: ✅ 允许                                     │")
    print("  │    └─ 最大迭代: 25                                         │")
    print("  ├─────────────────────────────────────────────────────────────┤")
    print("  │ 🔍 市场情报专家                                            │")
    print("  │    ├─ 速率限制: 15 RPM                                      │")
    print("  │    └─ 上下文管理: ✅ 自动                                   │")
    print("  ├─────────────────────────────────────────────────────────────┤")
    print("  │ ⚠️  风险管理专家                                            │")
    print("  │    ├─ 推理模式: ✅ 启用                                     │")
    print("  │    ├─ 日期注入: ✅ 启用                                     │")
    print("  │    └─ 格式: YYYY年MM月DD日                                  │")
    print("  ├─────────────────────────────────────────────────────────────┤")
    print("  │ ♟️  战略规划总监                                            │")
    print("  │    └─ 专注: 可执行策略制定                                   │")
    print("  └─────────────────────────────────────────────────────────────┘")

    print("\n🛡️  已启用的防护措施:")
    print("  ✓ 执行摘要长度验证 (50-300字)")
    print("  ✓ 执行摘要内容完整性检查")
    print("  ✓ 建议数量验证 (≥3个)")
    print("  ✓ 建议格式验证 (列表形式)")
    print("  ✓ LLM语义验证 (定量数据、可操作性)")

    print("\n📦 输出模型:")
    print("  • MarketInsight - 市场洞察结构化数据")
    print("  • StrategicRecommendation - 战略建议结构化数据")
    print("  • FinalReport - 完整报告结构化输出")

    print("\n⚙️  流程选项:")
    print("  [A] 分层流程 (Hierarchical) - Manager代理智能分配任务")
    print("  [B] 顺序流程 (Sequential) - 按定义顺序执行")
    print("=" * 70)

    # 选择流程类型
    use_hierarchical = True  # 可以改为 False 来测试顺序流程

    if use_hierarchical:
        print("\n🚀 使用【分层流程】执行...")
        print("   (首席分析师作为Manager协调所有任务)\n")
        result = hierarchical_crew.kickoff(inputs=inputs)
    else:
        print("\n🚀 使用【顺序流程】执行...")
        print("   (按预定义顺序依次执行任务)\n")
        result = sequential_crew.kickoff(inputs=inputs)

    print("\n" + "=" * 70)
    print("✅ 高级工作流示例执行完成！")
    print("=" * 70)
    print(f"\n📄 报告已保存到: output/advanced_workflow_report.md")

    # 访问结构化输出
    if final_report_task.output and final_report_task.output.pydantic:
        report_data = final_report_task.output.pydantic
        print(f"\n📊 结构化输出访问示例:")
        print(f"\n  执行摘要:\n  {report_data.executive_summary}")
        print(f"\n  关键洞察数量: {len(report_data.key_insights)}")
        print(f"  战略建议数量: {len(report_data.recommendations)}")

        if report_data.recommendations:
            print(f"\n  最高优先级建议:")
            top_rec = sorted(report_data.recommendations, key=lambda x: x.priority)[0]
            print(f"    • [{top_rec.priority}] {top_rec.action}")
            print(f"      理由: {top_rec.rationale[:100]}...")

    print(f"\n原始输出预览:\n{str(result)[:400]}...")

    return result


if __name__ == "__main__":
    result = main()
