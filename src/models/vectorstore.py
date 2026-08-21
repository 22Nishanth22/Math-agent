from langchain_chroma import Chroma

def build_vectorstore(chunks, embedding, directory):
    vs = Chroma.from_documents(chunks, embedding=embedding, persist_directory=directory)
    print(f"collection count : {vs._collection.count()}")
    return vs
