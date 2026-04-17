from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

load_dotenv()

prompt1 = PromptTemplate(
    template="Generate a detail repot on  {topic}",
    input_variables=["topic"]
)

prompt2 = PromptTemplate(
    template="Generate a  5 pointer summary from the following text \n {text}",
    input_variables=["topic"]
)


model = ChatOpenAI(model="gpt-4o-mini")   # initialize the model

parser = StrOutputParser()

chain = prompt1 | model | parser | prompt2 | model | parser

result = chain.invoke({"topic": "Unemployment in india"})
print(result)