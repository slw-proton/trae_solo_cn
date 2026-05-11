"""
示例1：基础 Agent 和 Task 示例
演示如何创建简单的 Agent、Task 和 Crew
"""

from crewai import Agent, Task, Crew, Process


def main():
    print("=" * 60)
    print("CrewAI 示例1：基础 Agent 和 Task")
    print("=" * 60)

    # 1. 创建一个研究代理
    researcher = Agent(
        role="高级数据研究员",
        goal="发现关于给定主题的最新发展",
        backstory="你是一位经验丰富的研究员，擅长发现最新的相关信息，"
                 "并以清晰简洁的方式呈现。",
        verbose=True,
        memory=True,
    )

    # 2. 创建一个写作代理
    writer = Agent(
        role="技术文档撰写专家",
        goal="基于研究结果撰写清晰、结构化的技术报告",
        backstory="你是一位专业的技术写作者，能够将复杂的技术概念转化为易于理解的文档。"
                 "你的报告总是结构清晰、内容详实。",
        verbose=True,
        memory=True,
    )

    # 3. 定义研究任务
    research_task = Task(
        description="""
        对 {topic} 进行全面的研究。
        确保找到任何有趣和相关的信息。
        当前年份是2025年。
        """,
        expected_output="""
        关于 {topic} 的10个最相关信息的要点列表
        """,
        agent=researcher,
    )

    # 4. 定义写作任务（依赖于研究任务的输出）
    writing_task = Task(
        description="""
        审查你得到的研究上下文，并将每个主题扩展为完整的报告部分。
        确保报告详细并包含所有相关信息。
        """,
        expected_output="""
        一份完整的报告，包含主要主题，每个主题都有完整的信息部分。
        格式为markdown，不包含代码块标记。
        """,
        agent=writer,
        context=[research_task],  # 这个任务会等待 research_task 完成
        output_file="output/basic_report.md",  # 输出到文件
    )

    # 5. 创建团队（Crew）
    crew = Crew(
        agents=[researcher, writer],
        tasks=[research_task, writing_task],
        process=Process.sequential,  # 顺序执行流程
        verbose=True,
    )

    # 6. 执行任务
    inputs = {
        'topic': '人工智能在医疗领域的应用'
    }

    print("\n🚀 开始执行任务...")
    result = crew.kickoff(inputs=inputs)

    print("\n✅ 任务完成！")
    print(f"\n结果预览：\n{str(result)[:500]}...")

    return result


if __name__ == "__main__":
    result = main()
