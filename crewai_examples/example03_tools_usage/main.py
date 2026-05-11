"""
示例3：工具使用示例
演示如何在 Agent 中集成各种工具来增强其能力
包括：搜索工具、文件操作工具、代码执行等
"""

from crewai import Agent, Task, Crew, Process
from crewai_tools import (
    SerperDevTool,
    FileReadTool,
    DirectoryReadTool,
    TXTSearchTool,
    WebsiteSearchTool,
)


def main():
    print("=" * 60)
    print("CrewAI 示例3：工具使用")
    print("=" * 60)

    # 1. 初始化各种工具
    print("\n🔧 初始化工具...")

    # 搜索工具 - 用于网络搜索
    search_tool = SerperDevTool()

    # 文件读取工具 - 用于读取本地文件
    file_read_tool = FileReadTool()

    # 目录读取工具 - 用于读取目录结构
    directory_read_tool = DirectoryReadTool()

    # 文本搜索工具 - 用于在文件中搜索内容
    txt_search_tool = TXTSearchTool()

    # 网站搜索工具 - 用于在特定网站内搜索
    website_search_tool = WebsiteSearchTool()

    print("✅ 工具初始化完成:")
    print("   - SerperDevTool (网络搜索)")
    print("   - FileReadTool (文件读取)")
    print("   - DirectoryReadTool (目录读取)")
    print("   - TXTSearchTool (文本搜索)")
    print("   - WebsiteSearchTool (网站搜索)")

    # 2. 创建配备不同工具的专业化 Agent

    # 信息研究员 - 使用搜索工具
    information_researcher = Agent(
        role="高级信息研究员",
        goal="使用搜索工具收集最新的、准确的信息",
        backstory="你是一位专业的研究员，擅长利用各种搜索工具快速找到相关信息。"
                 "你能够评估信息来源的可信度并提取关键要点。",
        verbose=True,
        tools=[search_tool, website_search_tool],
        memory=True,
        max_iter=15,
    )

    # 文档分析师 - 使用文件操作工具
    document_analyst = Agent(
        role="文档分析专家",
        goal="分析和处理本地文档，提取关键信息",
        backstory="你是一位文档处理专家，能够高效地读取和分析各种格式的文档。"
                 "你擅长从大量文本中提取结构化信息。",
        verbose=True,
        tools=[file_read_tool, directory_read_tool, txt_search_tool],
        memory=True,
    )

    # 综合分析师 - 整合所有来源的信息
    synthesis_analyst = Agent(
        role="综合分析顾问",
        goal="整合来自不同来源的信息并提供深度洞察",
        backstory="你是一位资深分析师，专长于整合多源信息并提供可执行的建议。"
                 "你的分析总是基于数据且具有战略眼光。",
        verbose=True,
        tools=[search_tool],  # 可以补充搜索更多信息
        memory=True,
        max_iter=20,
    )

    # 3. 定义任务

    # 任务1：网络研究
    web_research_task = Task(
        description="""
        对 {research_topic} 进行全面的网络研究：

        1. 搜索最新的行业报告和新闻
        2. 找到权威数据源和统计信息
        3. 识别关键趋势和发展方向
        4. 收集专家观点和预测

        要求：
        - 信息必须是2024-2025年的最新内容
        - 优先选择官方和权威来源
        - 记录所有信息来源
        """,
        expected_output="""
        结构化的研究报告，包括：
        - 10-15个关键发现（带来源引用）
        - 5大趋势总结
        - 数据支持的结论
        - 完整的参考来源列表
        """,
        agent=information_researcher,
    )

    # 任务2：本地文档分析（如果存在相关文档）
    local_document_task = Task(
        description="""
        分析本地文档目录中的相关文件：

        1. 读取 data/ 目录下的所有文本文件
        2. 搜索与 {research_topic} 相关的内容
        3. 提取关键数据和见解
        4. 识别文档中的模式和关联

        注意：
        - 如果 data/ 目录不存在或为空，请说明情况
        - 重点提取定量数据
        """,
        expected_output="""
        文档分析摘要：
        - 发现的关键数据点
        - 从文档中提取的主要观点
        - 数据质量和完整性评估
        - 与网络研究的对比发现
        """,
        agent=document_analyst,
        context=[web_research_task],
    )

    # 任务3：综合分析与建议
    comprehensive_analysis_task = Task(
        description="""
        基于网络研究和本地文档分析的结果，提供综合分析：

        1. 整合所有信息源的数据
        2. 识别一致性和矛盾点
        3. 提供深度洞察和战略建议
        4. 制定行动计划

        输出要求：
        - Executive Summary 格式
        - 数据驱动的建议
        - 明确的优先级排序
        - 可执行的下一步行动
        """,
        expected_output="""
        最终综合分析报告 (Markdown格式)：
        ## 执行摘要
        [核心发现和建议]

        ## 关键洞察
        [5-7个最重要的发现]

        ## 战略建议
        [具体、可执行的建议列表]

        ## 行动计划
        [时间线和里程碑]

        ## 风险与缓解措施
        [潜在风险和应对策略]
        """,
        agent=synthesis_analyst,
        context=[web_research_task, local_document_task],
        output_file="output/tools_analysis_report.md",
        markdown=True,
    )

    # 4. 创建团队
    tools_crew = Crew(
        agents=[information_researcher, document_analyst, synthesis_analyst],
        tasks=[web_research_task, local_document_task, comprehensive_analysis_task],
        process=Process.sequential,
        verbose=True,
        memory=True,
    )

    # 5. 执行任务
    inputs = {
        'research_topic': '生成式AI在企业中的应用现状和未来趋势'
    }

    print("\n" + "=" * 60)
    print(f"📚 研究主题: {inputs['research_topic']}")
    print("=" * 60)
    print("\n🤖 团队成员:")
    print("  1. 高级信息研究员 (配备: 搜索工具 + 网站搜索)")
    print("  2. 文档分析专家 (配备: 文件/目录/文本搜索工具)")
    print("  3. 综合分析顾问 (配备: 搜索工具)")
    print("\n🛠️  已集成的工具:")
    print("  • SerperDevTool - Google搜索")
    print("  • FileReadTool - 本地文件读取")
    print("  • DirectoryReadTool - 目录浏览")
    print("  • TXTSearchTool - 文本内容搜索")
    print("  • WebsiteSearchTool - 网站内搜索")
    print("=" * 60 + "\n")

    print("🚀 开始执行工具增强的分析任务...\n")
    result = tools_crew.kickoff(inputs=inputs)

    print("\n✅ 工具使用示例执行完成！")
    print(f"\n📄 报告已保存到: output/tools_analysis_report.md")
    print(f"\n📊 结果预览:\n{str(result)[:600]}...")

    return result


if __name__ == "__main__":
    result = main()
