from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

from sklearn.metrics.pairwise import cosine_similarity  
import numpy as np

load_dotenv()

embbeding = OpenAIEmbeddings(model="text-embedding-3-small", dimensions=300)


document = [
    "Virat Kohli is a former Indian cricketer and captain of the Indian national team.",
    "Sachin Tendulkar is a former Indian cricketer and one of the greatest batsmen in the history of cricket.",
    "MS Dhoni is a former Indian cricketer and captain of the Indian national team.",
    "Rohit Sharma is an Indian cricketer and the current captain of the Indian national team.",
    "Anil Kumble is a former Indian cricketer and captain of the Indian national team."
]


query = "Who is the current captain of the Indian national cricket team?"


document_embeddings = embbeding.embed_documents(document)
query_embedding = embbeding.embed_query(query)


similarity_scores = cosine_similarity([query_embedding], document_embeddings)[0]    

# print(list(enumerate(similarity_scores)))

index ,score  =sorted(list(enumerate(similarity_scores)), key=lambda x: x[1])[-1]

print(query)
print(document[index])
