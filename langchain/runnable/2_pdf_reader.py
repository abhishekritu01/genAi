from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI


# Load the PDF document
loader = TextLoader("example.pdf")
documents = loader.load()

# Split the document into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
texts = text_splitter.split_documents(documents)

# Create embeddings for the text chunks
vectorstore = FAISS.from_documents(texts, OpenAIEmbeddings())


# Create a retriever and a QA chain
retriever = vectorstore.as_retriever()


#manually set the retriever to return the top 3 most relevant chunks
query = "What are the top 3 most important things to know about the document?"
retriever_docs = retriever.get_relevant_documents(query)[:3]


#combine the retrieved documents into a single string
combined_docs = "\n\n".join([doc.page_content for doc in retriever_docs])


#initialize the LLM and create a prompt to summarize the combined documents
llm = OpenAI(model="gpt-3.5-turbo", temperature=0.9)
prompt = f"Summarize the following information from the document:\n\n{combined_docs}"
#generate the response
summary = llm.predict(prompt)
print(summary)



