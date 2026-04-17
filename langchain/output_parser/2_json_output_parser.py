from langchain_huggingface import HuggingFaceEndpoint,ChatHuggingFace
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv

load_dotenv()


llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-v0.1",
    task="text-generation",
)

model = ChatHuggingFace(llm=llm)

parser = JsonOutputParser()


template = PromptTemplate(
    template="Give me the name ,age and city of a fictional person \n {format_instruction}",    
    input_variables=[],
    partial_variables ={'format_instruction':parser.get_format_instructions() } 
)


# prompt = template.formate()
# result = model.invoke(prompt)  
# final_result = parser.parse(result.content)

chain = template | model | parser 

final_result = chain.invoke({})

print(final_result)
print(type(final_result))


