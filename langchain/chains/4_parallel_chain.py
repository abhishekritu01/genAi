from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence

load_dotenv()

model1 = ChatOpenAI(model="gpt-4o-mini")   # initialize the model
model2 = ChatAnthropic(model="claude-2")   # initialize the model



prompt1 = PromptTemplate(
    template="Generate short and simple notes from the following topic text \n: {topic}",
    input_variables=["topic"]
)  

prompt2 = PromptTemplate(
    template="Generate a  5 short questions answere from the following text \n {text}",
    input_variables=["text"]
)

prompt3 = PromptTemplate(
    template="Merge the provided  notes and questions into a single comprehensive summary \n Notes: {text1} \n Questions: {text2}",
    input_variables=['notes', 'questions']
)

parser = StrOutputParser()



parallel_chain = RunnableParallel({
    "notes": prompt1 | model1 | parser,
    "questions": prompt2 | model2 | parser
})

merge_chain = prompt3 | model1 | parser

chain = parallel_chain | merge_chain

text = "Unemployment in India is a significant socio-economic issue that has been exacerbated by various factors, including population growth, economic slowdowns, and structural changes in the economy. The unemployment rate in India has fluctuated over the years, with a notable increase during the COVID-19 pandemic due to lockdowns and reduced economic activity. The government has implemented various schemes and initiatives to address unemployment, such as skill development programs and job creation schemes. However, challenges remain in effectively tackling the issue, particularly in rural areas and among the youth population."

result = chain.invoke({"topic": text})

print(result)

print(chain.get_graph().to_dot())