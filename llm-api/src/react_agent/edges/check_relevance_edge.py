import os

from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv
from typing import Literal
from pydantic import BaseModel, Field

load_dotenv()

### Edges
def grade_documents(state) -> Literal["generate", "rewrite"]:
	"""
	取得したドキュメントが、質問に関係するかどうかを決定する

	Args:
		state (messages): 現在の state
	
	Returns:
		str: ドキュメントが質問に関係するか、しないのか
	"""

	print("---CHECK RELEVANCE---")

	# Data model
	class grade(BaseModel):
		binary_score: str = Field(description="Relevance score 'yes' or 'no'")

	# LLM
	model = ChatOpenAI(temperature=os.environ["OPENAI_API_TEMPERATURE"], model=os.environ["OPENAI_API_MODEL"], streaming=True)

	# LLM with tool and validation
	llm_with_tool = model.with_structured_output(grade)

	# Prompt
	prompt = PromptTemplate(
		template="""You are a grader assessing relevance of a retrieved document to a user question. \n	
		Here is the retrieved document: \n\n {context} \n\n
		Here is the user question: {question} \n
		If the document contains keyword(s) or semantic meaning related to the user question, grade it as relevant. \n
		Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question.""",
		input_variables=["context", "question"]
	)

	# Chain
	chain = prompt | llm_with_tool

	messages = state["messages"]
	last_message = messages[-1]

	question = messages[0].content
	docs = last_message.content

	scored_result = chain.invoke({"question": question, "context": docs})

	score = scored_result.binary_score

	if score == "yes":
		print("---DECISION: DOCS RELEVANT---")
		return "generate"
	else:
		print("---DECISION:: DOCS NOT RELEVANT---")
		return "rewrite"
