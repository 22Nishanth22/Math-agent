from langchain.agents import create_agent
from langchain_openai import ChatOpenAI




class CLIENT:

    def __init__(self):
        self.llm = ChatOpenAI(api_key= 'YOUR-API-KEY',
                              base_url= "YOUR-BASE-URL",
                              temperature= 0,
                              model= "YOUR-MODEL-NAME")

    def get_llm(self):
        return self.llm


class AGENT:
    def __init__(self, llm, tools):
        self.graph = create_agent(
            model=llm,
            tools=tools,
            system_prompt="""You are a math assistant with access to two tools:

            1. search_math_knowledge - searches a knowledge base of math definitions, theorems, and concepts.
            2. equations - performs symbolic computation (simplify or solve) using SymPy.

            STRICT RULES:
            - If the question asks for a definition, theorem statement, or conceptual explanation, 
            you MUST call search_math_knowledge before answering, even if you already know the answer.
            - If the question requires any numeric or symbolic calculation, you MUST call the equations tool 
            to verify the result before answering, even if you are confident in the answer yourself. 
            Do not rely on your own mental arithmetic alone.
            - If the question needs both a concept and a calculation, call both tools.
            - Never skip a tool because you believe you already know the answer. Verification is required."""
        )

    def ask(self, query):
        inputs = {"messages": [{"role": "user", "content": query}]}
        
        for chunk in self.graph.stream(inputs, stream_mode="updates"):
            for value in chunk.values():
                if "messages" in value:
                    message = value["messages"][-1]
                    if message.type == "ai":
                        print(message.content)

    def ask_with_trace(self, query):
        inputs = {"messages": [{"role": "user", "content": query}]}
        
        tools_called = []
        final_answer = None

        for chunk in self.graph.stream(inputs, stream_mode='updates'):
            for node, value in chunk.items():
                if node == "model":
                    message = value["messages"][-1]
                    if message.tool_calls:
                        for tool_call in message.tool_calls:
                            tools_called.append(tool_call["name"])
                    elif message.content:
                        final_answer = message.content

        return {
            "question": query,
            "tools_called": tools_called,
            "final_answer": final_answer
        }