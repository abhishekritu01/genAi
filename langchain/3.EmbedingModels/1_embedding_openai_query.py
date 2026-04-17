from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()


# notes 
# bydefaul embedding vector for small models is 1536 dimensions, but we can specify the dimensions as per our requirement.
# for large models it 3072 dimensions and it cannot be changed.


embedding = OpenAIEmbeddings(model="text-embedding-3-small", dimensions=32)
response = embedding.embed_query("Delhi is the capital of India.")

print(str(response))