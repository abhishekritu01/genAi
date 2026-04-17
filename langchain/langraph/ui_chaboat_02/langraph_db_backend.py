from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage
from numpy.__config__ import CONFIG

import sqlite3

load_dotenv()

llm = ChatOpenAI()

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def chat_node(state: ChatState):
    messages = state['messages']
    response = llm.invoke(messages)
    return {"messages": [response]}


conn = sqlite3.connect('chatbot.db', check_same_thread=False)

# Checkpointer
checkpointer = SqliteSaver(conn = conn)

graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

chatbot = graph.compile(checkpointer=checkpointer)


# testing db is working or not 

CONFIG = {'configurable':{'thread_id': 'test_thread_id'}}


respone = chatbot.invoke(
    {'messages': [HumanMessage(content="Hello, how are you?")]},
    config=CONFIG
    )

print(respone)



# chatbot.invoke(
#     {'messages': [HumanMessage(content="Hello, how are you?")]},
#     config=CONFIG
#     )

# # print(chatbot.get_state(config=CONFIG).values['messages'][0].content)
# print(chatbot.get_state(config=CONFIG).values['messages'][0].content)













