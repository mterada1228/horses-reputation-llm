import os

from langchain_openai import ChatOpenAI

from tools import create_tools

def agent(state):
	"""
	現在の state に基づいて、回答を生成するための agent model を実行する。
	質問が与えられると、retriever tool を用いて、ドキュメントを取得する、もしくは処理を終了する

	Args:
		state (messages): 現在の状態
	
	Returns:
		dict: agent のレスポンスを messages に追加して、現在の状態を更新する
	"""

	print("---CALL AGENT---")

	messages = state["messages"]
	model = ChatOpenAI(temperature=os.environ["OPENAI_API_TEMPERATURE"], model=os.environ["OPENAI_API_MODEL"], streaming=True)
	tools = create_tools()
	model = model.bind_tools(tools)
	response = model.invoke(messages)

	return {"messages": [response]}
