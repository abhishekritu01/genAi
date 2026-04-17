from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI


#load the document and create embeddings
loader = TextLoader("example.pdf")
documents = loader.load()



#split the text into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
texts = text_splitter.split_documents(documents)


#convert the text into embeddings and store in a FAISS vector store
vectorstore = FAISS.from_documents(texts, OpenAIEmbeddings())


#create a retriever and a QA chain
retriever = vectorstore.as_retriever()

#initialize the LLM and create a RetrievalQA chain
llm = OpenAI(model="gpt-3.5-turbo", temperature=0.9)
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)


#ask a question about the document
query = "What are the top 3 most important things to know about the document?"
response = qa_chain.run(query)

print(response)