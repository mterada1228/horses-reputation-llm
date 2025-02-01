from langchain.tools.retriever import create_retriever_tool

from retriever import create_retriever

def create_tools():
	retriever = create_retriever()
	retriever_tool = create_retriever_tool(
		retriever,
		"retrieve_netkeiba_news",
		"Search and return information about reputation of a horse from netkeiba news."
	)

	tools = [retriever_tool]

	return tools
