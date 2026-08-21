# Agentic Math Reasoning Assistant
 
An AI agent that answers math questions by deciding, on its own, whether to **look up** a concept or **calculate** an answer — using two separate tools instead of one fixed pipeline.

 
## What the project actually does
 
Ask it a question like *"What is Vector Space?"* and it searches a knowledge base of math concepts to answer.
 
Ask it *"Is x² + 2x + 1 equal to (x+1)²?"* and it uses a math tool to actually calculate and verify the answer, instead of just guessing.
 
Ask it something that needs both, and it uses both tools together.
 
## How it works (in plain terms)
 
```
Wikipedia math articles → cleaned text → split into small chunks
    → each chunk turned into a vector (embedding) → stored in Chroma (a vector database)
 
A math calculation tool, built with SymPy, that can simplify expressions
and solve equations.
 
The Agent (built with LangChain):
    → reads the user's question
    → decides: do I need to search, calculate, both, or neither?
    → calls the right tool(s)
    → uses the tool's result to write a final answer
```
 
## Tools and libraries used
 
- **Wikipedia API** — to pull ~50 math articles (linear algebra, calculus, probability, statistics)
- **LangChain** — the framework used to build the chunking, retrieval, and agent
- **Chroma** — a vector database (different from FAISS, which I used in my earlier projects) that stores the math articles as searchable vectors
- **SentenceTransformers** — turns text into vectors so similar meanings can be found
- **SymPy** — a Python library for real, exact math computation (not just guessing)
- **Langchain's `create_agent`** — lets the AI decide which tool to use, instead of me hardcoding the steps
## Why I built it this way
 
**Two separate tools, not one.** A search tool can tell you the *definition* of something, but it can't *calculate* a specific answer. A calculator can compute things, but it doesn't know what a theorem means. Giving the agent both, and letting it choose, is what makes this "agentic" instead of just another RAG project.
 
**I tested whether the agent actually chooses correctly.** It's not enough for the agent to "seem" smart — I built a set of 50 test questions (a mix of lookup-only, calculation-only, and both) with the correct tool labeled for each, and checked whether the agent picked the right one every time.
 
## Results
 
My first version of the agent's instructions (system prompt) simply said "choose the right tool for the question." Testing this on my 50 questions:
 
| Result | Count |
|---|---|
| Correct tool used | 17 / 50 (34%) |
| No tool used at all | 27 / 50 |
| Wrong tool used | 2 / 50 |
| Tool failed/errored | 4 / 50 |
 
**The biggest problem wasn't the agent picking the wrong tool — it just wasn't bothering to use a tool at all**, more than half the time. It was answering from its own knowledge instead of checking with a tool, even when I wanted it to verify.
 
So I rewrote the instructions to be much more direct: *"Always use a tool to check your answer, even if you think you already know it."* I ran the same 50 questions again:
 
| Result | Count |
|---|---|
| Correct tool used | **31 / 50 (62%)** |
| No tool used at all | 0 |
| Wrong tool used | 10 |
| Tool failed/errored | 9 |
 
**Just by rewording the instructions, correct tool use nearly doubled (34% → 62%), and the agent stopped skipping tools entirely.**
 

## Known limitations
 
- The calculation tool only supports simplifying expressions and solving equations — it can't do calculus (derivatives, integrals) or work with probability distributions yet.
- The calculation tool expects one clean math expression, not multi-step instructions like "first do this, then do that."
- Math equations from Wikipedia are kept in their raw LaTeX form (not rendered as pretty equations) in the knowledge base, since that preserves the exact math instead of losing it.
## What I'd add next
 
- Expand the calculation tool to support differentiation and integration.
- Try a few different prompt wordings to see which gets the best tool-use accuracy.
- Add a simple way to render the LaTeX equations nicely when showing an answer to a user.

