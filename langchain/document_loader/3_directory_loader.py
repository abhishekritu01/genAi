from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader

loader = DirectoryLoader(
    path='books',
    glob='*.pdf',                      # glob pattern to match files
    loader_cls=PyPDFLoader
)

#glob pattern to match files
# *.pdf - matches all PDF files
# *.txt - matches all text files


docs = loader.lazy_load()

for document in docs:
    print(document.metadata)  