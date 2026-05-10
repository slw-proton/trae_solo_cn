"""
CrewAI 入门项目：多角色 AI 团队协作
======================================
核心概念：
- Agent: 具有特定角色、目标、背景的智能代理
- Task: 分配给 Agent 的具体任务
- Crew: 由多个 Agent 组成的团队
- Tool: Agent 可以使用的工具集
- Process: 任务执行顺序（顺序、并行、层级）

本示例创建一个「内容创作团队」：
- 🎭 角色策划师（Researcher）：研究主题，收集素材
- ✍️ 内容撰写人（Writer）：基于素材撰写文章
- 🔍 编辑审稿人（Editor）：审核修改，确保质量
"""

import os
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI


# ============================================================
# 1. 初始化 LLM（所有 Agent 共享）
# ============================================================

def get_llm():
    """初始化大语言模型"""
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "your-api-key-here")
    
    return ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7,
        max_tokens=2000
    )


# ============================================================
# 2. 定义 Agent（智能代理）
# ============================================================

def create_researcher_agent(llm):
    """
    创建研究策划 Agent
    
    角色：资深内容策划师
    目标：深入研究主题，收集相关素材和背景信息
    背景：拥有10年内容策划经验，擅长信息收集和分析
    """
    
    researcher = Agent(
        role="资深内容策划师",
        goal="深入研究和分析主题，收集全面、准确的背景信息和素材",
        backstory="""你是一位拥有10年经验的内容策划专家。
你曾在多家顶级媒体公司工作，擅长：
- 快速理解复杂主题的核心要点
- 从多个角度收集和分析信息
- 识别最有价值的内容方向
- 为后续创作提供扎实的素材基础""",
        
        verbose=True,
        allow_delegation=False,
        llm=llm,
        
        # Agent 的思维模式配置
        max_iter=3,
        max_rpm=60,
        
        # 工具（如果需要搜索等工具可以在这里添加）
        # tools=[search_tool, scrape_tool]
    )
    
    return researcher


def create_writer_agent(llm):
    """
    创建内容撰写 Agent
    
    角色：专业内容创作者
    目标：基于研究素材，撰写高质量、吸引人的文章
    背景：文笔优秀，擅长将复杂概念转化为易懂的内容
    """
    
    writer = Agent(
        role="专业内容创作者",
        goal="基于提供的素材，撰写引人入胜、结构清晰、价值丰富的原创文章",
        backstory="""你是一位才华横溢的内容创作者，拥有：
- 优秀的文字功底和叙事能力
- 将复杂技术概念转化为通俗易懂内容的能力
- 对读者痛点的深刻理解
- 创造独特观点和洞察的能力
你写过的文章多次获得行业奖项，深受读者喜爱。""",
        
        verbose=True,
        allow_delegation=True,  # 允许向其他 Agent 委派任务
        llm=llm,
        
        max_iter=5,
        max_rpm=60,
    )
    
    return writer


def create_editor_agent(llm):
    """
    创建编辑审核 Agent
    
    角色：首席编辑
    目标：审核文章质量，提出改进意见，确保最终输出达到出版标准
    背景：严谨细致，对内容质量有极高要求
    """
    
    editor = Agent(
        role="首席编辑",
        goal="严格审核内容质量，从准确性、可读性、完整性等多维度进行评估和优化",
        backstory="""你是一位要求极其严格的资深编辑，拥有15年编辑经验。
你的审核标准包括：
- 内容准确性和事实核查
- 文章结构和逻辑流畅性
- 语言表达的专业性和可读性
- 标题和摘要的吸引力
- SEO 友好度
你以'零容忍'的态度对待任何质量问题，但也会给出建设性的修改建议。""",
        
        verbose=True,
        allow_delegation=False,
        llm=llm,
        
        max_iter=3,
        max_rpm=60,
    )
    
    return editor


# ============================================================
# 3. 定义 Task（任务）
# ============================================================

def create_research_task(agent, topic):
    """
    创建研究任务
    """
    
    research_task = Task(
        description=f"""请对以下主题进行全面研究和分析：

**主题**: {topic}

**研究要求**:
1. 主题背景和重要性说明
2. 当前发展趋势和热点
3. 目标受众的关注点和痛点
4. 可用的关键数据、案例或引用
5. 建议的文章切入角度和独特视角
6. 可能涉及的子话题

**输出格式**:
请提供结构化的研究报告，包含以上所有要点，
为后续的内容创作提供充分的素材支撑。

注意：研究要深入但聚焦，避免泛泛而谈。""",
        
        expected_output="""一份详细的研究报告，包含：
- 主题概述（200字以内）
- 关键发现点（至少5个）
- 数据和案例素材
- 建议的文章结构和角度
- 引用来源（如有）""",
        
        agent=agent,
        
        # 任务配置
        async_execution=False,
        context=[],  # 可以依赖其他任务的输出
    )
    
    return research_task


def create_writing_task(agent, research_task, topic):
    """
    创建写作任务（依赖研究任务的输出）
    """
    
    writing_task = Task(
        description=f"""基于研究员提供的研究报告，撰写一篇高质量的文章：

**文章主题**: {topic}

**写作要求**:
1. 使用研究员收集的所有有价值素材
2. 文章结构清晰，逻辑严密
3. 语言生动有趣，易于理解
4. 提供独特的见解和价值
5. 包含吸引人的标题和简洁的摘要
6. 字数控制在1500-2500字之间

**文章结构建议**:
- 引人入胜的开头（引起共鸣或好奇心）
- 清晰的主体段落（分点论述）
- 有力的结尾（总结+行动号召）

请确保文章具有原创性和实用性，能够真正帮助到读者。""",
        
        expected_output="""一篇完整的原创文章，包含：
- 吸引人的标题（主标题+副标题）
- 100-150字的摘要
- 正文内容（1500-2500字）
- 关键要点总结（3-5个bullet points）""",
        
        agent=agent,
        
        # 关键：这个任务依赖研究任务的输出
        context=[research_task],
    )
    
    return writing_task


def create_editing_task(agent, writing_task, topic):
    """
    创建编辑审核任务（依赖写作任务的输出）
    """
    
    editing_task = Task(
        description=f"""对撰写的文章进行全面的质量审核和优化：

**原文主题**: {topic}

**审核维度**:

1️⃣ **事实准确性**
   - 所有数据和引用是否准确
   - 是否有需要验证的声明

2️⃣ **内容质量**
   - 论点是否清晰有力
   - 逻辑是否连贯
   - 是否提供了真正的价值

3️⃣ **可读性**
   - 语言是否流畅自然
   - 段落长度是否合适
   - 是否有足够的视觉层次感

4️⃣ **完整性**
   - 是否覆盖了重要方面
   - 开头和结尾是否有力
   - 行动号召是否明确

5️⃣ **SEO 和传播性**
   - 标题是否有吸引力
   - 关键词布局是否合理
   - 是否适合社交媒体分享

**输出要求**:
- 提供详细的审核意见
- 给出具体的修改建议
- 输出最终优化后的完整版本""",

        expected_output="""一份完整的审核报告，包含：
1. 总体评分（1-10分）和评价
2. 各维度的具体审核意见
3. 修改建议清单
4. 最终定稿版本（如需重大修改则重写）""",

        agent=agent,
        
        context=[writing_task],
    )
    
    return editing_task


# ============================================================
# 4. 组装 Crew（团队）
# ============================================================

def create_content_crew(topic):
    """
    创建完整的内容创作团队
    """
    
    # 获取 LLM 实例
    llm = get_llm()
    
    # 创建三个 Agent
    researcher = create_researcher_agent(llm)
    writer = create_writer_agent(llm)
    editor = create_editor_agent(llm)
    
    # 创建任务（注意依赖关系）
    research_task = create_research_task(researcher, topic)
    writing_task = create_writing_task(writer, research_task, topic)
    editing_task = create_editing_task(editor, writing_task, topic)
    
    # 组装团队
    crew = Crew(
        agents=[researcher, writer, editor],
        tasks=[research_task, writing_task, editing_task],
        
        # 执行流程：顺序执行（研究→写作→编辑）
        process=Process.sequential,
        
        # 团队配置
        verbose=True,
        memory=True,           # 启用团队记忆
        cache=True,            # 缓存 LLM 调用
        max_rpm=100,           # 限制 API 调用频率
        
        # 回调函数（可选）
        # step_callback=my_callback,
    )
    
    return crew


# ============================================================
# 5. 运行演示
# ============================================================

def run_demo():
    """运行 CrewAI 内容创作团队演示"""
    
    print("\n" + "="*70)
    print("  🎭 CrewAI 多角色 AI 团队协作演示")
    print("  场景：专业内容创作团队")
    print("="*70 + "\n")
    
    # 定义创作主题
    topic = "2024年人工智能在医疗健康领域的应用与未来趋势"
    
    print(f"📝 创作主题: {topic}\n")
    print("-"*70)
    print("👥 团队成员:")
    print("  1. 🎭 资深内容策划师 (Researcher) - 负责研究策划")
    print("  2. ✍️ 专业内容创作者 (Writer) - 负责内容撰写")
    print("  3. 🔍 首席编辑 (Editor) - 负责审核优化")
    print("-"*70)
    print("\n🔄 工作流程:")
    print("   Researcher → Writer → Editor")
    print("   (研究素材) → (撰写初稿) → (审核定稿)")
    print("-"*70 + "\n")
    
    # 创建团队
    crew = create_content_crew(topic)
    
    print("\n🚀 开始执行...\n")
    print("="*70 + "\n")
    
    try:
        # 执行任务
        result = crew.kickoff()
        
        # 输出最终结果
        print("\n" + "="*70)
        print("  ✅ 团队任务完成！")
        print("="*70)
        print("\n📄 最终输出:\n")
        print(result)
        print("\n" + "="*70 + "\n")
        
    except Exception as e:
        print(f"\n❌ 执行出错: {e}")
        print("\n提示：请确保已设置 OPENAI_API_KEY 环境变量")


# ============================================================
# 6. 进阶示例：并行任务团队
# ============================================================

def create_parallel_research_crew(topic):
    """
    进阶：创建并行执行的调研团队
    多个研究员同时从不同角度研究同一主题
    """
    
    llm = get_llm()
    
    # 创建多个专注于不同领域的研究员
    tech_researcher = Agent(
        role="技术研究专家",
        goal=f"从技术角度研究 {topic}",
        backstory="你是一位技术专家，专注于技术原理和创新点的研究。",
        verbose=True,
        llm=llm,
    )
    
    market_researcher = Agent(
        role="市场分析师",
        goal=f"从市场商业角度研究 {topic}",
        backstory="你是一位资深市场分析师，擅长市场规模、竞争格局分析。",
        verbose=True,
        llm=llm,
    )
    
    trend_researcher = Agent(
        role="趋势预测专家",
        goal=f"从未来趋势角度研究 {topic}",
        backstory="你是一位前瞻性思考者，善于发现和预测行业趋势。",
        verbose=True,
        llm=llm,
    )
    
    # 并行研究任务
    tech_task = Task(
        description=f"从技术层面深度分析：{topic}",
        expected_output="技术研究报告",
        agent=tech_researcher,
    )
    
    market_task = Task(
        description=f"从市场商业层面分析：{topic}",
        expected_output="市场分析报告",
        agent=market_researcher,
    )
    
    trend_task = Task(
        description=f"从未来趋势层面预测：{topic}",
        expected_output="趋势预测报告",
        agent=trend_researcher,
    )
    
    # 综合分析员
    synthesizer = Agent(
        role="首席分析师",
        goal="整合多方研究成果，形成综合报告",
        background="你擅长整合不同来源的信息，形成全面的洞察。",
        verbose=True,
        llm=llm,
    )
    
    synthesis_task = Task(
        description="整合三份研究报告，形成最终的综合分析报告",
        expected_output="综合分析报告",
        agent=synthesizer,
        context=[tech_task, market_task, trend_task],  # 依赖所有研究任务
    )
    
    # 并行执行团队
    crew = Crew(
        agents=[tech_researcher, market_researcher, trend_researcher, synthesizer],
        tasks=[tech_task, market_task, trend_task, synthesis_task],
        process=Process.sequential,  # 前三个并行，最后汇总
        verbose=True,
    )
    
    return crew


if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║         📚 CrewAI 入门教程 - 多角色Agent团队协作             ║
║                                                              ║
║  核心概念学习要点:                                            ║
║  ─────────────────                                           ║
║  1. Agent: 定义角色的职责、目标和背景                         ║
║  2. Task: 明确的任务描述和期望输出                            ║
║  3. Crew: 组织Agent和Task的容器                              ║
║  4. Process: 控制任务执行顺序（sequential/hierarchical）      ║
║  5. Context: 任务间的依赖和数据传递                          ║
║  6. Delegation: Agent间任务委派机制                           ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")
    
    run_demo()
