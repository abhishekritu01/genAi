from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()


model = ChatOpenAI()

# 1st prompt
template1 = PromptTemplate(
    template="write a detailed report on {topic}",
    input_variables=["topic"]
)

# 2nd prompt
template2 = PromptTemplate(
    template="write a 5 line summary on the following text.\n{text}",
    input_variables=["text"]
)

# generate report
prompt1 = template1.invoke({"topic": "Artificial Intelligence"})
result = model.invoke(prompt1)

# generate summary
prompt2 = template2.invoke({"text": result.content})
result1 = model.invoke(prompt2)

print(result1.content)