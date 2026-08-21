from langchain_core.tools import tool


def make_retriever_tool(vectorstore, k=3):
    retriever = vectorstore.as_retriever(search_kwargs={'k': k})

    @tool
    def search_math_knowledge(query: str) -> str:
        """Search a knowledge base of math theorems, definitions, and concepts.

        Use this tool when the user asks about a definition, theorem statement,
        or conceptual explanation of a mathematical topic (e.g., "what is the
        Cauchy-Schwarz inequality", "explain eigenvalues").

        Args:
            query: The user's question or topic to search for.

        Returns:
            Relevant text passages from the knowledge base.
        """
        
        
        
        docs = retriever.invoke(query)
        return "\n\n".join(d.page_content for d in docs)

    return search_math_knowledge