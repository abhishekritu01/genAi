from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()


# model = ChatGoogleGenAI(model="gemini-1.5-pro", temperature=0.9, max_completion_tokens=100)

model = ChatGoogleGenerativeAI(model="gemini-1.5-pro" )
response = model.invoke("What is the capital of india?")
print(response.content)     