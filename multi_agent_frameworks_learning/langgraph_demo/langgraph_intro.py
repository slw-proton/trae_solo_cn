"""
LangGraph 入门项目：智能客服工作流编排
==========================================
核心概念：
- State: 工作流中的共享状态，在节点间传递
- Node: 处理状态的函数/节点
- Edge: 连接节点的边，决定执行流程
- Conditional Edge: 条件边，根据状态动态路由

本示例实现一个智能客服系统：
1. 意图识别 → 2. 分类路由 → 3. 专业回答 → 4. 总结输出
"""

from typing import TypedDict, Annotated, Literal
from operator import add
import os

# LangGraph 核心组件
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver

# LangChain 组件（用于LLM调用）
from langchain_openai import ChatOpenAI


# ============================================================
# 1. 定义 State（状态）- 工作流中流转的数据结构
# ============================================================
class CustomerServiceState(TypedDict):
    """客服工作流的状态定义"""
    user_query: str                          # 用户原始问题
    intent: str                              # 识别出的意图
    category: str                            # 问题分类
    response: str                            # 生成的回答
    messages: Annotated[list, add_messages]  # 对话消息历史


# ============================================================
# 2. 定义 Node（节点）- 每个节点是一个处理函数
# ============================================================

def intent_recognition_node(state: CustomerServiceState) -> dict:
    """
    节点1: 意图识别
    分析用户问题，识别用户意图
    """
    query = state["user_query"]
    
    # 简单的规则匹配（实际项目中使用 LLM）
    query_lower = query.lower()
    
    if any(word in query_lower for word in ["价格", "费用", "多少钱", "贵"]):
        intent = "price_inquiry"
    elif any(word in query_lower for word in ["退货", "退款", "退换"]):
        intent = "return_request"
    elif any(word in query_lower for word in ["技术", "故障", "bug", "错误", "不能用"]):
        intent = "technical_support"
    elif any(word in query_lower for word in ["订单", "物流", "发货", "快递"]):
        intent = "order_status"
    else:
        intent = "general_inquiry"
    
    print(f"🔍 [意图识别] 用户问题: '{query}'")
    print(f"   → 识别意图: {intent}")
    
    return {"intent": intent}


def categorize_node(state: CustomerServiceState) -> dict:
    """
    节点2: 问题分类
    根据意图将问题分类到不同处理部门
    """
    intent = state["intent"]
    
    category_map = {
        "price_inquiry": "sales_department",
        "return_request": "after_sales_service",
        "technical_support": "technical_department",
        "order_status": "logistics_department",
        "general_inquiry": "general_service"
    }
    
    category = category_map.get(intent, "general_service")
    
    print(f"📂 [问题分类] 意图: {intent} → 部门: {category}")
    
    return {"category": category}


def generate_response_node(state: CustomerServiceState) -> dict:
    """
    节点3: 生成专业回答
    根据分类生成对应的专业回复
    """
    category = state["category"]
    query = state["user_query"]
    
    response_templates = {
        "sales_department": f"【销售部门回复】\n关于您咨询的'{query}'，我们的产品价格透明公道。\n建议您访问官网查看最新价格表，或联系销售顾问获取专属优惠。",
        
        "after_sales_service": f"【售后服务回复】\n关于您的'{query}'请求，我们非常重视。\n请在7天内保留商品原包装，填写退货申请表，我们会在3个工作日内处理。",
        
        "technical_department": f"【技术支持回复】\n收到您反馈的技术问题：'{query}'\n请提供具体的错误截图和操作步骤，我们的技术专家将在24小时内为您排查解决。",
        
        "logistics_department": f"【物流部门回复】\n关于您的'{query}'查询：\n您可以通过订单号在我们的官网或APP上实时追踪物流状态。如有异常请联系在线客服。",
        
        "general_service": f"【综合服务回复】\n感谢您的咨询：'{query}'\n我们会尽快安排专业人员为您解答，也可以拨打400-XXX-XXXX获取即时帮助。"
    }
    
    response = response_templates.get(category, response_templates["general_service"])
    
    print(f"💬 [{category}] 生成回复")
    
    return {"response": response}


def summarize_node(state: CustomerServiceState) -> dict:
    """
    节点4: 总结输出
    整理完整的客服记录
    """
    summary = f"""
{'='*50}
           客服工单总结
{'='*50}
📝 用户问题: {state['user_query']}
🎯 问题意图: {state['intent']}
📂 处理部门: {state['category']}
💬 客服回复: {state['response'][:50]}...
{'='*50}
    """
    
    print(summary)
    
    return {"messages": [{"role": "assistant", "content": state["response"]}]}


# ============================================================
# 3. 定义条件路由函数（Conditional Edge）
# ============================================================

def route_by_category(state: CustomerServiceState) -> Literal["generate_response", "human_escalation"]:
    """
    条件路由：根据问题类型决定是否需要人工介入
    """
    complex_categories = ["technical_department", "after_sales_service"]
    
    if state["category"] in complex_categories:
        # 复杂问题走特殊处理流程
        return "generate_response"
    else:
        # 简单问题直接生成回复
        return "generate_response"


# ============================================================
# 4. 构建工作流图（Graph）
# ============================================================

def build_customer_service_graph():
    """
    构建客服工作流图
    
    流程示意:
    ┌─────────────────┐
    │  开始 (Start)   │
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐     ┌─────────────────┐
    │  意图识别       │────▶│  问题分类       │
    │ (intent_node)   │     │(categorize_node)│
    └─────────────────┘     └────────┬────────┘
                                     │
                              条件路由
                                     │
                    ┌────────────────┼────────────────┐
                    ▼                ▼                 ▼
           ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
           │ 生成回复      │  │ 生成回复      │  │ 人工升级     │
           │(简单问题)     │  │(复杂问题)     │  │(可选扩展)     │
           └──────┬───────┘  └──────┬───────┘  └──────────────┘
                  │                 │
                  └────────┬────────┘
                           ▼
                  ┌─────────────────┐
                  │  总结输出        │
                  │(summarize_node) │
                  └────────┬────────┘
                           │
                           ▼
                      ┌────────┐
                      │  END   │
                      └────────┘
    """
    
    # 创建状态图
    workflow = StateGraph(CustomerServiceState)
    
    # 添加节点
    workflow.add_node("intent_recognition", intent_recognition_node)
    workflow.add_node("categorize", categorize_node)
    workflow.add_node("generate_response", generate_response_node)
    workflow.add_node("summarize", summarize_node)
    
    # 设置入口点
    workflow.set_entry_point("intent_recognition")
    
    # 添加边（定义节点间的连接关系）
    workflow.add_edge("intent_recognition", "categorize")
    
    # 添加条件边
    workflow.add_conditional_edges(
        "categorize",
        route_by_category,
        {
            "generate_response": "generate_response"
        }
    )
    
    workflow.add_edge("generate_response", "summarize")
    
    # 添加结束边
    workflow.add_edge("summarize", END)
    
    # 编译工作流（添加记忆功能支持对话历史）
    memory = MemorySaver()
    app = workflow.compile(checkpointer=memory)
    
    return app


# ============================================================
# 5. 运行示例
# ============================================================

def run_demo():
    """运行 LangGraph 客服工作流演示"""
    
    print("\n" + "="*60)
    print("  🤖 LangGraph 智能客服工作流演示")
    print("="*60 + "\n")
    
    # 构建工作流
    graph_app = build_customer_service_graph()
    
    # 测试用例：不同类型的用户问题
    test_queries = [
        "这个产品多少钱？",
        "我想退货，质量有问题",
        "系统一直报错500怎么办？",
        "我的订单什么时候能到？",
        "你们公司几点上班？"
    ]
    
    print("-"*60)
    print("📋 测试用例:")
    print("-"*60)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{'─'*60}")
        print(f"📌 测试案例 {i}: {query}")
        print(f"{'─'*60}\n")
        
        # 初始状态
        initial_state = {
            "user_query": query,
            "intent": "",
            "category": "",
            "response": "",
            "messages": []
        }
        
        # 配置（用于记忆/会话管理）
        config = {"configurable": {"thread_id": f"session-{i}"}}
        
        # 执行工作流
        result = graph_app.invoke(initial_state, config=config)
        
        print(f"\n✅ 最终结果:\n{result['response']}\n")


# ============================================================
# 6. 进阶示例：带 LLM 的真实场景
# ============================================================

def build_llm_customer_service_graph():
    """
    使用 LLM 增强的客服工作流
    展示如何在实际项目中集成大语言模型
    """
    
    from langchain_core.messages import SystemMessage, HumanMessage
    
    class EnhancedState(TypedDict):
        user_query: str
        intent: str
        category: str
        response: str
        messages: Annotated[list, add_messages]
    
    def llm_intent_node(state: EnhancedState) -> dict:
        """使用 LLM 进行意图识别"""
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        
        prompt = """你是一个意图识别引擎。分析用户问题，返回JSON格式的结果：
{{"intent": "price|return|tech|order|general", "confidence": 0.95}}

用户问题: {query}""".format(query=state["user_query"])
        
        response = llm.invoke([HumanMessage(content=prompt)])
        print(f"🤖 LLM意图识别: {response.content}")
        
        return {"intent": response.content}
    
    def llm_response_node(state: EnhancedState) -> dict:
        """使用 LLM 生成专业回复"""
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
        
        prompt = """你是一个专业的{category}客服代表。
请针对用户的问题给出专业、友好、有帮助的回复。

用户问题: {query}
问题类别: {category}

请直接给出回复内容，不要加任何前缀。""".format(
            category=state["category"],
            query=state["user_query"]
        )
        
        response = llm.invoke([HumanMessage(content=prompt)])
        
        return {"response": response.content}
    
    workflow = StateGraph(EnhancedState)
    workflow.add_node("llm_intent", llm_intent_node)
    workflow.add_node("categorize", categorize_node)
    workflow.add_node("llm_response", llm_response_node)
    
    workflow.set_entry_point("llm_intent")
    workflow.add_edge("llm_intent", "categorize")
    workflow.add_edge("categorize", "llm_response")
    workflow.add_edge("llm_response", END)
    
    return workflow.compile()


if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║          📚 LangGraph 入门教程 - 工作流编排                   ║
║                                                              ║
║  核心概念学习要点:                                            ║
║  ─────────────────                                           ║
║  1. StateGraph: 有状态的工作流图                               ║
║  2. State(TypedDict): 定义节点间传递的数据结构                  ║
║  3. Node: 处理函数，接收state返回更新的state部分               ║
║  4. Edge: 节点间的连接，控制流程走向                           ║
║  5. Conditional Edge: 根据state动态决定下一个节点              ║
║  6. Checkpoint: 记忆机制，支持持久化和恢复                     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")
    
    run_demo()
