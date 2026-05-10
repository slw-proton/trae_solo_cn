"""
AutoGen 入门项目：多Agent对话框架
====================================
核心概念：
- ConversableAgent: 可对话的Agent基类
- AssistantAgent: AI助手Agent，擅长生成回复
- UserProxyAgent: 用户代理，可代表人类参与对话
- GroupChat: 多Agent群聊模式
- Code Executor: 代码执行环境

本示例实现三种典型场景：
1. 两Agent对话：AI助手 + 人类代理
2. 多Agent群聊：模拟会议讨论
3. 编程助手：代码生成 + 执行 + 反馈循环
"""

import autogen
from autogen import ConversableAgent, UserProxyAgent, AssistantAgent
from typing import Dict, List


# ============================================================
# 1. 基础配置
# ============================================================

def get_config_list():
    """获取LLM配置"""
    config_list = [
        {
            "model": "gpt-4o-mini",
            "api_key": "your-openai-api-key",  # 替换为实际的API key
            "api_type": "openai",
        }
    ]
    return config_list


# ============================================================
# 2. 场景一：两Agent对话（最简单的入门示例）
# ============================================================

def demo_two_agent_chat():
    """
    场景1: 两Agent对话
    - AssistantAgent: AI助手，负责回答问题和提供建议
    - UserProxyAgent: 人类代理，发起对话并可以批准操作
    
    适用场景：个人AI助手、问答系统、简单任务辅助
    """
    
    print("\n" + "="*70)
    print("  💬 场景一：两Agent对话 - AI编程导师")
    print("="*70 + "\n")
    
    # 获取配置
    config_list = get_config_list()
    
    # 创建AI助手Agent
    assistant = AssistantAgent(
        name="编程导师",  # Agent名称
        
        # 系统消息：定义Agent的角色和行为
        system_message="""你是一位资深的Python编程导师，擅长：
- 用通俗易懂的方式解释编程概念
- 提供清晰的代码示例
- 循序渐进地引导学习者
- 发现并纠正代码中的问题

教学风格：
1. 先解释概念，再给示例
2. 鼓励提问和动手实践
3. 用类比和生活化的例子帮助理解
4. 及时给予正面反馈""",
        
        llm_config={
            "config_list": config_list,
            "temperature": 0.7,
        },
        
        # 对话配置
        human_input_mode="NEVER",  # 不需要人工输入（自动回复）
        max_consecutive_auto_reply=10,  # 最大连续自动回复次数
        is_termination_msg=lambda x: x.get("content", "").find("TERMINATE") >= 0,
    )
    
    # 创建用户代理Agent（代表人类）
    user_proxy = UserProxyAgent(
        name="学员",  # Agent名称
        
        human_input_mode="NEVER",  # 自动模式（不等待人工输入）
        max_consecutive_auto_reply=5,
        
        # 代码执行配置
        code_execution_config={
            "work_dir": "coding_workspace",
            "use_docker": False,  # 不使用Docker
        },
        
        # 系统消息
        system_message="我是一个Python初学者，想要学习编程知识。我会向你提问并尝试运行代码。",
    )
    
    # 发起对话
    chat_result = user_proxy.initiate_chat(
        recipient=assistant,  # 对话对象
        
        # 初始消息
        message="""你好！我是一名Python初学者，想学习以下内容：

1. 什么是面向对象编程（OOP）？
2. 类和对象有什么区别？
3. 能给我一个简单的例子吗？

请帮我理解这些概念，并给我一些可以运行的代码示例。""",
        
        # 对话配置
        summary_method="last_msg",  # 使用最后一条消息作为总结
        max_turns=10,  # 最大对话轮次
    )
    
    # 输出对话总结
    print("\n" + "-"*70)
    print("📝 对话总结:")
    print("-"*70)
    print(chat_result.summary)
    print("-"*70 + "\n")
    
    return chat_result


# ============================================================
# 3. 场景二：多Agent群聊（GroupChat）
# ============================================================

def demo_group_chat():
    """
    场景2: 多Agent群聊讨论
    模拟一个技术评审会议，多个角色共同讨论方案
    
    适用场景：头脑风暴、方案评审、决策讨论
    """
    
    print("\n" + "="*70)
    print("  👥 场景二：多Agent群聊 - 技术方案评审会议")
    print("="*70 + "\n")
    
    config_list = get_config_list()
    
    # 定义参会角色
    
    # 产品经理
    product_manager = AssistantAgent(
        name="产品经理",
        system_message="""你是一位经验丰富的产品经理。
你的关注点：
- 用户需求和体验
- 产品价值和市场竞争力
- 功能优先级和排期
- 商业目标和KPI

沟通风格：从用户价值出发，关注产品整体规划。""",
        llm_config={"config_list": config_list, "temperature": 0.8},
    )
    
    # 架构师
    architect = AssistantAgent(
        name="架构师",
        system_message="""你是一位资深技术架构师。
你的关注点：
- 系统设计的合理性和可扩展性
- 技术选型和风险评估
- 性能和安全考虑
- 技术债务和长期维护

沟通风格：从技术可行性出发，提供专业的技术建议。""",
        llm_config={"config_list": config_list, "temperature": 0.6},
    )
    
    # 开发工程师
    developer = AssistantAgent(
        name="开发工程师",
        system_message="""你是一位高级开发工程师。
你的关注点：
- 实现难度和工作量估计
- 代码质量和最佳实践
- 技术细节和潜在坑点
    - 测试和部署考虑

沟通风格：务实，关注落地实现的细节。""",
        llm_config={"config_list": config_list, "temperature": 0.7},
    )
    
    # 会议主持人（用户代理）
    moderator = UserProxyAgent(
        name="主持人",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=3,
        system_message="你是会议主持人，负责引导讨论流程，确保各方充分表达意见后做出决策。",
        code_execution_config=False,  # 不执行代码
    )
    
    # 配置群聊
    group_chat_config = {
        "agents": [product_manager, architect, developer, moderator],
        "messages": [],
        "max_round": 12,  # 最大对话轮数
        "speaker_selection_method": "round_robin",  # 轮流发言
        # 或使用 "auto" 让模型自动选择下一个发言者
        # 或使用自定义函数
    }
    
    # 创建群聊管理器
    group_chat_manager = autogen.GroupChatManager(
        groupchat=autogen.GroupChat(**group_chat_config),
        llm_config={"config_list": config_list, "temperature": 0.5},
        system_message="""你是一个技术评审会议的主持人。
你的职责：
1. 确保每个角色都有机会发表意见
2. 引导讨论聚焦在关键问题上
3. 在充分讨论后推动达成共识
4. 最终输出会议决议和行动项

会议流程：
1. 先让各方表达初步看法
2. 针对分歧点深入讨论
3. 寻求共识或折中方案
4. 总结决议和下一步计划""",
    )
    
    # 发起群聊
    chat_result = moderator.initiate_chat(
        recipient=group_chat_manager,
        
        message="""各位好，今天我们要评审一个新的功能方案：

**方案概述**：开发一个智能文档处理系统
- 支持多种格式文档上传（PDF、Word、图片）
- 使用AI自动提取文档内容和结构
- 支持智能问答和内容检索
- 提供文档对比和版本管理功能

**讨论议题**：
1. 这个方案的用户价值是什么？优先级如何？
2. 技术架构应该如何设计？有哪些风险？
3. 开发周期和资源需求预估
4. MVP版本应该包含哪些最小功能集？

请大家发表意见，我们来讨论出一个可行的实施计划。""",
        
        summary_method="reflection_with_llm",  # 使用LLM生成更详细的总结
    )
    
    print("\n" + "-"*70)
    print("📋 会议纪要:")
    print("-"*70)
    print(chat_result.summary)
    print("-"*70 + "\n")
    
    return chat_result


# ============================================================
# 4. 场景三：编程助手（代码生成+执行+反馈）
# ============================================================

def demo_code_assistant():
    """
    场景3: 编程助手
    展示AutoGen强大的代码能力：
    - 生成代码 → 执行代码 → 查看结果 → 修复错误 → 优化
    
    适用场景：数据分析、自动化脚本、算法开发
    """
    
    print("\n" + "="*70)
    print("  💻 场景三：编程助手 - 数据分析与可视化")
    print("="*70 + "\n")
    
    config_list = get_config_list()
    
    # 创建编程助手
    coding_assistant = AssistantAgent(
        name="Python专家",
        system_message="""你是一位Python编程专家，特别擅长：
- 数据分析和数据处理（pandas, numpy）
- 数据可视化（matplotlib, seaborn）
- 编写清晰、高效、有注释的代码
- 调试和修复代码问题

工作原则：
1. 先理解需求，再写代码
2. 代码要有注释，方便理解
3. 处理可能的异常情况
4. 输出结果要清晰易读

当用户给你一个编程任务时：
1. 分析需求，确定实现思路
2. 编写完整的可执行代码
3. 如果代码有错误，根据错误信息修复
4. 如果结果不理想，优化代码""",
        llm_config={"config_list": config_list, "temperature": 0.3},
    )
    
    # 创建用户代理（可以执行代码）
    user_proxy = UserProxyAgent(
        name="数据分析师",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=8,  # 允许多轮交互
        
        # 关键：启用代码执行
        code_execution_config={
            "work_dir": "data_analysis_workspace",
            "use_docker": False,
        },
        
        system_message="我是数据分析师，需要处理数据并生成可视化图表。我会描述需求，请你帮我编写和运行代码。",
    )
    
    # 发起编程任务
    chat_result = user_proxy.initiate_chat(
        recipient=coding_assistant,
        
        message="""请帮我完成以下数据分析任务：

**任务描述**：
创建一组模拟的销售数据，然后进行分析和可视化

**具体要求**：
1. 生成12个月的销售数据（包含月份、销售额、订单数、客户数）
2. 计算月环比增长率
3. 找出销售最好的月份
4. 计算平均客单价
5. 创建两个可视化图表：
   - 图1：月度销售额柱状图
   - 图2：销售额和订单数的双轴趋势图

**数据要求**：
- 销售额范围：50万-150万
- 显示中文标签
- 图表美观专业

请编写完整的Python代码并运行它。""",
        
        max_turns=15,  # 允许更多轮次来完成复杂任务
    )
    
    print("\n" + "-"*70)
    print("✅ 编程任务完成!")
    print("-"*70)
    print(chat_result.summary[:500] if chat_result.summary else "任务已完成")
    print("-"*70 + "\n")
    
    return chat_result


# ============================================================
# 5. 自定义Agent示例
# ============================================================

class SpecializedAgent(ConversableAgent):
    """
    自定义Agent示例：继承ConversableAgent创建专用Agent
    
    展示如何：
    - 自定义Agent行为
    - 添加特殊功能
    - 实现特定的交互逻辑
    """
    
    def __init__(self, name: str, specialty: str, **kwargs):
        super().__init__(
            name=name,
            system_message=f"""你是一位{specialty}专家。
你的专长领域是{specialty}相关的知识和技能。
请始终保持专业、准确、有帮助的回答风格。
如果遇到超出专业范围的问题，诚实说明并建议寻求其他专业人士的帮助。""",
            **kwargs
        )
        
        self.specialty = specialty
        self.question_count = 0
        
    def generate_reply(self, messages, sender, config):
        """自定义回复生成逻辑"""
        self.question_count += 1
        
        # 调用父类的默认实现
        reply = super().generate_reply(messages, sender, config)
        
        # 可以在这里添加自定义逻辑
        # 例如：记录日志、过滤内容、添加额外信息等
        
        return reply


def demo_custom_agent():
    """展示自定义Agent的使用"""
    
    print("\n" + "="*70)
    print("  🎨 场景四：自定义Agent - 专家咨询团")
    print("="*70 + "\n")
    
    config_list = get_config_list()
    
    # 创建多位专家
    legal_expert = SpecializedAgent(
        name="法律顾问",
        specialty="企业法律合规",
        llm_config={"config_list": config_list},
        human_input_mode="NEVER",
    )
    
    finance_expert = SpecializedAgent(
        name="财务顾问",
        specialty="企业财务管理",
        llm_config={"config_list": config_list},
        human_input_mode="NEVER",
    )
    
    hr_expert = SpecializedAgent(
        name="人力资源顾问",
        specialty="人才招聘与管理",
        llm_config={"config_list": config_list},
        human_input_mode="NEVER",
    )
    
    # 企业家（用户代理）
    entrepreneur = UserProxyAgent(
        name="创业者",
        human_input_mode="NEVER",
        code_execution_config=False,
        system_message="我准备创办一家科技公司，需要咨询各方面的问题。",
    )
    
    print("已创建专家咨询团：")
    print(f"  - {legal_expert.name} ({legal_expert.specialty})")
    print(f"  - {finance_expert.name} ({finance_expert.specialty})")
    print(f"  - {hr_expert.name} ({hr_expert.specialty})")
    print(f"  - {entrepreneur.name} (创业者)\n")


# ============================================================
# 6. 主程序：运行所有演示
# ============================================================

def main():
    """运行所有AutoGen演示场景"""
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║         📚 AutoGen 入门教程 - 多Agent对话框架                ║
║                                                              ║
║  核心概念学习要点:                                            ║
║  ─────────────────                                           ║
║  1. ConversableAgent: 可对话Agent的基类                       ║
║  2. AssistantAgent: AI助手，擅长生成回复                      ║
║  3. UserProxyAgent: 人类代理，可执行代码                      ║
║  4. GroupChat: 多Agent群聊，支持复杂协作                      ║
║  5. Code Execution: 内置代码执行环境                          ║
║  6. Custom Agent: 可继承和自定义Agent行为                     ║
║                                                              ║
║  三大典型应用场景:                                            ║
║  ─────────────────                                           ║
║  💬 两Agent对话 - 个人AI助手                                  ║
║  👥 多Agent群聊 - 团队协作决策                                ║
║  💻 编程助手 - 代码生成执行循环                               ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")
    
    # 选择运行的场景
    demos = {
        "1": ("两Agent对话", demo_two_agent_chat),
        "2": ("多Agent群聊", demo_group_chat),
        "3": ("编程助手", demo_code_assistant),
        "4": ("自定义Agent", demo_custom_agent),
    }
    
    print("\n可用演示场景:")
    print("-"*50)
    for key, (name, _) in demos.items():
        print(f"  {key}. {name}")
    print("-"*50)
    
    # 默认运行第一个场景作为入门示例
    selected = "1"
    
    print(f"\n🚀 运行场景 {selected}: {demos[selected][0]}\n")
    
    try:
        demos[selected][1]()
    except Exception as e:
        print(f"\n❌ 运行出错: {e}")
        print("\n💡 提示：")
        print("   1. 请确保已安装 autogen: pip install pyautogen")
        print("   2. 请设置 OPENAI_API_KEY 环境变量")
        print("   3. 或者修改代码中的 API key 配置")


if __name__ == "__main__":
    main()
