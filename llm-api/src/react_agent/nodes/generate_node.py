import os

from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

def generate(state):
	"""
	回答を生成する

	Args:
		state (messages): 現在の状態

	Returns:
		dict: 回答
	"""

	print("---GENERATE---")

	messages = state["messages"]
	question = messages[0].content
	last_message = messages[-1]

	docs = last_message.content

	# Prompt
	prompt = hub.pull("rlm/rag-prompt")

	# LLM
	llm = ChatOpenAI(temperature=os.environ["OPENAI_API_TEMPERATURE"], model=os.environ["OPENAI_API_MODEL"], streaming=True)

	# Chain
	rag_chain = prompt | llm | StrOutputParser()

	# Run
	response = rag_chain.invoke({"context": docs, "question": question})

	return {"messages": [response]}
