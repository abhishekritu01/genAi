from langchain_huggingface import ChatHuggingFace, HuggingFacePipeline
from dotenv import load_dotenv

# import os
load_dotenv()

# os.environ["HF_HOME"] = "C:/Users/abhis/.cache/huggingface"

llm = HuggingFacePipeline.from_model_id(
    model_id="TinyLlama/TinyLlama-1T-1.1B-GGUF",
    task="text-generation",
    pipeline_kwargs= dict(max_new_tokens=100, temperature=0.9)

)


chat = ChatHuggingFace(llm=llm)
response = chat.invoke("What is the capital of India?")
print(response.content)