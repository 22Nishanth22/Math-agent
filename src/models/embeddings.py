from langchain_huggingface import HuggingFaceEmbeddings


def load_model(model_name : str):
    embedding_model = HuggingFaceEmbeddings(model = model_name)
    print(f"Embedding Dimension : {len(embedding_model.embed_query('test'))}")
    return embedding_model