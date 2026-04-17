from langchain_huggingface import HuggingFaceEndpoint,ChatHuggingFace
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.output_parsers import StractureOutParser, ResponeseSchema
from dotenv import load_dotenv

load_dotenv()


llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-v0.1",
    task="text-generation",
)

model = ChatHuggingFace(llm=llm)


schema =[
    ResponeseSchema(name='fact_1',description ='Fact1 about the topic'),
    ResponeseSchema(name='fact_2',description ='Fact2 about the topic'),
    ResponeseSchema(name='fact_3',description ='Fact3 about the topic'),
]

parser = StractureOutParser.form_response_schemas(schema)

template = PromptTemplate(
     
    template="Give me 3 facts about the topic \n {format_instruction}",   
    input_variables=[],
    partial_variables ={'format_instruction':parser.get_format_instructions() }
)


prompt = template.invoke({'topic':'Artificial Intelligence'})
result = model.invoke(prompt)

final_result = parser.parse(result.content)
print(final_result)