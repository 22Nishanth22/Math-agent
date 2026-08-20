from langchain_chroma import Chroma

def vectorstore(chunks, embedding, directory):
    vectorstore = Chroma.from_documents(chunks, embedding=embedding, persist_directory=directory)
    
    print(f"collection count : {vectorstore._collection.count()}")
    return vectorstore


def retrieval(vectorstore, k):
    return vectorstore.as_retriever(search_kwargs= {'k' : k})