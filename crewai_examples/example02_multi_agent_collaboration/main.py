"""
示例2：多 Agent 协作示例
演示多个专业 Agent 如何协同完成复杂任务
展示分层流程、任务委派、上下文共享等高级特性
"""

from crewai import Agent, Task, Crew, Process


def main():
    print("=" * 60)
    print("CrewAI 示例2：多 Agent 协作")
    print("=" * 60)

    # 1. 创建项目经理代理（作为协调者）
    project_manager = Agent(
        role="项目经理",
        goal="协调团队完成产品市场分析报告",
        backstory="你是一位经验丰富的项目经理，擅长协调不同专家的工作。"
                 "你能够将复杂任务分解并分配给合适的团队成员。",
        verbose=True,
        allow_delegation=True,  # 允许将任务委派给其他代理
        memory=True,
    )

    # 2. 创建市场研究分析师
    market_researcher = Agent(
        role="市场研究分析师",
        goal="收集和分析市场数据、趋势和竞争对手信息",
        backstory="你是一位专业的市场分析师，拥有10年行业经验。"
                 "你擅长数据收集、趋势分析和竞争情报。",
        verbose=True,
        allow_delegation=False,
        memory=True,
    )

    # 3. 创建技术评估专家
    tech_evaluator = Agent(
        role="技术评估专家",
        goal="评估产品的技术可行性、创新性和竞争优势",
        backstory="你是一位资深的技术顾问，专注于技术创新和市场应用。"
                 "你能够识别技术趋势并评估其商业价值。",
        verbose=True,
        allow_delegation=False,
        memory=True,
    )

    # 4. 创建财务分析师
    financial_analyst = Agent(
        role="财务分析师",
        goal="分析成本结构、收入预测和投资回报率",
        backstory="你是一位认证财务分析师(CFA)，专精于科技公司的财务建模和估值。",
        verbose=True,
        allow_delegation=False,
        memory=True,
    )

    # 5. 创建报告撰写专家
    report_writer = Agent(
        role="高级报告撰写专家",
        goal="整合所有分析结果，撰写专业、清晰的综合报告",
        backstory="你是一位顶级的管理咨询顾问，曾为财富500强公司撰写战略报告。"
                 "你的报告以数据驱动、逻辑严密、建议可行而著称。",
        verbose=True,
        allow_delegation=False,
        memory=True,
    )

    # 6. 定义任务

    # 任务1：市场调研（由市场研究员执行）
    market_research_task = Task(
        description="""
        对 {product_category} 市场进行全面分析：
        - 市场规模和增长预测
        - 主要竞争对手及其市场份额
        - 目标客户群体特征
        - 市场趋势和机会
        - 潜在威胁和挑战

        当前年份：2025年
        """,
        expected_output="""
        详细的市场分析报告，包括：
        - 市场规模数据（美元）
        - 竞争对手对比表格
        - SWOT分析
        - 市场机会评分（1-10）
        """,
        agent=market_researcher,
    )

    # 任务2：技术评估（由技术专家执行，使用市场研究结果作为上下文）
    tech_evaluation_task = Task(
        description="""
        基于{product_category}的市场背景，进行技术评估：
        - 技术可行性和成熟度分析
        - 创新点和差异化优势
        - 技术风险和挑战
        - 所需技术栈和资源
        - 与现有技术的兼容性
        """,
        expected_output="""
        技术评估文档，包括：
        - 技术就绪水平(TRL)评级
        - 创新性评分（1-10）
        - 实施路线图
        - 技术风险矩阵
        """,
        agent=tech_evaluator,
        context=[market_research_task],  # 依赖市场研究的输出
    )

    # 任务3：财务分析（由财务分析师执行）
    financial_analysis_task = Task(
        description="""
        对{product_category}进行全面的财务分析：
        - 初期投资成本估算
        - 运营成本结构
        - 收入模型和预测（3年期）
        - 盈亏平衡点分析
        - ROI和NPV计算
        - 敏感性分析
        """,
        expected_output="""
        财务分析报告，包含：
        - 成本明细表
        - 3年财务预测表
        - 关键财务指标（ROI, NPV, IRR）
        - 风险调整后的回报分析
        """,
        agent=financial_analyst,
    )

    # 任务4：综合报告（由报告撰写者执行，整合所有前序任务的输出）
    comprehensive_report_task = Task(
        description="""
        整合所有分析结果，为{product_category}撰写一份 executive summary 级别的综合报告：

        执行摘要部分：
        - 核心发现（3-5个关键点）
        - 战略建议（具体可执行的步骤）
        - 资源需求和时间表
        - 成功指标和里程碑

        报告要求：
        - 专业、简洁、数据驱动
        - 适合向高层管理者汇报
        - 包含明确的下一步行动建议
        """,
        expected_output="""
        完整的综合报告（markdown格式），包括：
        1. 执行摘要（1页）
        2. 市场分析要点
        3. 技术评估总结
        4. 财务概览
        5. 战略建议（5-7个具体行动项）
        6. 风险缓解策略
        7. 附录：详细数据
        """,
        agent=report_writer,
        context=[market_research_task, tech_evaluation_task, financial_analysis_task],
        output_file="output/comprehensive_market_analysis.md",
        markdown=True,
    )

    # 7. 创建团队 - 使用顺序流程
    sequential_crew = Crew(
        agents=[project_manager, market_researcher, tech_evaluator,
                financial_analyst, report_writer],
        tasks=[market_research_task, tech_evaluation_task,
               financial_analysis_task, comprehensive_report_task],
        process=Process.sequential,
        verbose=True,
        memory=True,
    )

    # 8. 执行任务
    inputs = {
        'product_category': 'AI驱动的智能家居设备'
    }

    print("\n🚀 开始多 Agent 协作任务...")
    print(f"📋 产品类别: {inputs['product_category']}")
    print("\n" + "=" * 60)
    print("团队成员:")
    print("  1. 项目经理 (协调者)")
    print("  2. 市场研究分析师")
    print("  3. 技术评估专家")
    print("  4. 财务分析师")
    print("  5. 高级报告撰写专家")
    print("=" * 60 + "\n")

    result = sequential_crew.kickoff(inputs=inputs)

    print("\n✅ 多 Agent 协作任务完成！")
    print(f"\n📊 最终报告已保存到: output/comprehensive_market_analysis.md")
    print(f"\n结果预览:\n{str(result)[:800]}...")

    return result


if __name__ == "__main__":
    result = main()
