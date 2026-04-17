from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StringOutputParser
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

# chain


parser = StringOutputParser()

chain = template1 | model | parser | template2 | model | parser

result = chain.invoke({"topic": "Artificial Intelligence"})
print(result)