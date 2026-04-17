
# from langchain_community.document_loaders import TextLoader

# loader = TextLoader("example.txt",encoding = "utf-8")

# documents = loader.load()

# print(documents)
# print(type(documents))   # <class 'list'> 
# print(type(documents[0]))   # <class 'langchain_core.document.Document'>
# print(documents[0].page_content)   # page_content
# print(documents[0].metadata)   # metadata




from langchain_community.document_loaders import TextLoader
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI()

prompt = PromptTemplate(
    template='Write a summary for the following poem - \n {poem}',
    input_variables=['poem']
)

parser = StrOutputParser()

loader = TextLoader('cricket.txt', encoding='utf-8')

docs = loader.load()

print(type(docs))

print(len(docs))

print(docs[0].page_content)

print(docs[0].metadata)

chain = prompt | model | parser

print(chain.invoke({'poem':docs[0].page_content}))
