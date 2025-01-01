import os

import streamlit as st
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from langchain.chains import RetrievalQA

from add_document import initialize_vector_store


load_dotenv()

st.title('競争馬の評判を回答します')

# 会話の履歴
if "messages" not in st.session_state:
	st.session_state.messages = []

for message in st.session_state.messages:
	with st.chat_message(message["role"]):
		st.markdown(message["text"])

prompt = st.chat_input("競争馬の名前を入力してください")

if prompt:
	vector_store = initialize_vector_store()

	llm = ChatOpenAI(
		model_name = os.environ["OPENAI_API_MODEL"],
		temperature = os.environ["OPENAI_API_TEMPERATURE"]
	)

	qa_chain = RetrievalQA.from_llm(llm=llm, retriever=vector_store.as_retriever())

	messages = [HumanMessage(content=prompt)]
	response = qa_chain.run(prompt)

	st.session_state.messages.append({"role": "user", "text": prompt})
	st.session_state.messages.append({"role": "assistant", "text": response})

	with st.chat_message("user"):
		st.markdown(prompt)
	with st.chat_message("assistant"):
		st.markdown(response)