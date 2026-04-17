from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

# LLM
llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct-v0.2",
    task="text-generation",
)

model = ChatHuggingFace(llm=llm)

# Pydantic Schema
class PersonInfo(BaseModel):
    name: str = Field(description="Name of the person")
    age: int = Field(description="Age of the person")
    city: str = Field(description="City where the person lives")

# Output Parser
parser = PydanticOutputParser(pydantic_object=PersonInfo)

# Prompt Template
template = PromptTemplate(
    template="""
Generate information about a random person from {place}.

{format_instruction}
""",
    input_variables=["place"],
    partial_variables={"format_instruction": parser.get_format_instructions()},
)

# Create Prompt
prompt = template.invoke({"place": "India"})

# LLM Call
result = model.invoke(prompt)

# Parse Output
final_result = parser.parse(result.content)

print(final_result)