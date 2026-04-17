# HumanMessage(content="I want to request a refund for my order #1234")
# AIMessage(content="Your refund request for order #1234 has been received. We will process it within 3-5 business days and notify you once it's complete.")  


# we have to store as txt file and then load it as a prompt template


#step 1 : chat template 
# step 2 : load chat history from txt file
#step 3: create prompt

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# step 1: chat template
chat_template = ChatPromptTemplate([
    ('system','You are a helpful customer support assistant agent.'),
    MessagesPlaceholder(variable_name='chat_history'),
    ('human','{input}'),
])

# step 2: load chat history
chat_history = []

with open('langchain_prompt/chat_history.txt') as file:
    for line in file:
        chat_history.append(HumanMessage(content=line.strip()))

print(chat_history)

# step 3: create prompt
prompt = chat_template.invoke({
    'chat_history': chat_history,
    'input': 'where is my refund'
})

print(prompt.messages)