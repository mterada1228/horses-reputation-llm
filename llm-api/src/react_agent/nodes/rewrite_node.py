import os

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

def rewrite(state):
	"""
	より良い質問を生成するためにクエリを変換する

	Args:
		state (messages): 現在の状態
	
	Returns:
		dict: フレーズが変更された質問で、現在の状態を更新する
	"""

	print("---TRANSFORM QUERY---")

	messages = state["messages"]
	question = messages[0].content

	msg = [
		HumanMessage(
			content=f""" \n
			Look at the input and try to reason about the underlying semantic intent / meaning. \n
			Here is the initial question:
			\n ------- \n
			{question}
			\n ------- \n
			Formulate an improved question: """
		)
	]

	# Grader
	model = ChatOpenAI(temperature=os.environ["OPENAI_API_TEMPERATURE"], model=os.environ["OPENAI_API_MODEL"], streaming=True)
	response = model.invoke(msg)

	return {"messages": [response]}
