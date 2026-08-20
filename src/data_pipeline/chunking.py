import json
import tiktoken
from typing import Literal
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter



def langchain_docs(corpus_path):
    
    with open(corpus_path, "r") as f:
        corpus = json.load(f)
    
    document = []
    
    for doc in corpus:
        docs = Document(page_content=doc['content'],
                        metadata = {
                            "title" : doc['title'],
                            "pageid" : doc['pageid']
                        })
        document.append(docs)
        
    return document


class CHUNK:
    
    def load_encoder(self, encoder: Literal["r50k_base", "p50k_base", "cl100k_base", "o200k_base"]):
        return tiktoken.get_encoding(encoding_name=encoder)
    
    def length_function(self, encoding):
        return lambda text: len(encoding.encode(text))
    
    def text_splitter(self, chunk_size, chunk_overlap, encoding):
        return RecursiveCharacterTextSplitter(chunk_size = chunk_size,
                                              chunk_overlap = chunk_overlap,
                                              length_function = self.length_function(encoding))
    
    
    
    
    