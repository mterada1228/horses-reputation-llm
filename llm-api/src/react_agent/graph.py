from langgraph.graph import END, StateGraph, START
from langgraph.prebuilt import ToolNode, tools_condition

from edges.check_relevance_edge import grade_documents

from nodes.agent_node import agent
from nodes.generate_node import generate
from nodes.rewrite_node import rewrite

from state import AgentState
from tools import create_tools

# 新しい Graph を定義する
workflow = StateGraph(AgentState)

# Graph に edge, node を定義する
retrieve = ToolNode(create_tools())

workflow.add_node("agent", agent)
workflow.add_node("retrieve", retrieve)
workflow.add_node("rewrite", rewrite)
workflow.add_node("generate", generate)

workflow.add_edge(START, "agent")

# Graph に、ドキュメントを取得するかどうかの conditional edge を追加する
workflow.add_conditional_edges(
	"agent",
	tools_condition,
	{
		"tools": "retrieve",
		END: END
	}
)

# Graph に、ドキュメントを取得した後のアクションを決める conditional edge を追加する
workflow.add_conditional_edges(
	"retrieve",
	grade_documents
)
workflow.add_edge("generate", END)
workflow.add_edge("rewrite", "agent")

# コンパイル
graph = workflow.compile()
