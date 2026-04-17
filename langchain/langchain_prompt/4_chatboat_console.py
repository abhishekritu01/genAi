# from langchain_openai import ChatOpenAI
# from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
# from dotenv import load_dotenv


# load_dotenv()

# model = ChatOpenAI()

# chat_history = []

# while True:
#     user_input = input("Enter your prompt (or 'exit' to quit): ")
#     chat_history.append({"role": "user", "content": user_input})
#     if user_input.lower() == "exit":
#         print("Exiting the chatbot. Goodbye!")
#         break

#     result = model.invoke(chat_history)
#     chat_history.append({"role": "assistant", "content": result.content})
#     result = model.invoke(user_input)
#     print("Response:")
#     print("AI: " ,result.content)









#=================================== adding chat messages ============================

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv


load_dotenv()

model = ChatOpenAI()

chat_history = [
    SystemMessage(content="You are a helpful assistant that provides information about the latest research papers in AI."),
]

while True:
    user_input = input("Enter your prompt (or 'exit' to quit): ")
    chat_history.append(HumanMessage(content=user_input))
    if user_input.lower() == "exit":
        print("Exiting the chatbot. Goodbye!")
        break

    result = model.invoke(chat_history)
    chat_history.append(AIMessage(content=result.content))
    print("Response:")
    print("AI: " ,result.content)
