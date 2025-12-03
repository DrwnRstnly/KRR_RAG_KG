from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from rag.llm import llm
import json

answerer_prompt = PromptTemplate.from_template("""
You are a helpful Clash Royale assistant. 
Use the provided Graph Data to answer the User Question.

- If the data is empty, state that you don't know the answer.
- The data contains stats like Hitpoints (HP), Damage, and DPS (Damage Per Second).
- Format the stats clearly.

User Question:
{question}

Graph Data:
{data}

Answer:
""")

def answerer_fn(inputs: dict):
    data = inputs.get("data", [])
    
    if not data or (isinstance(data, list) and len(data) == 0):
        return "I couldn't find any information about that in the database."

    prompt = answerer_prompt.format(
        question=inputs["question"],
        data=json.dumps(data, indent=2)
    )
    
    result = llm(prompt)[0]["generated_text"]
    
    if "Answer:" in result:
        result = result.split("Answer:")[-1].strip()
        
    return result.strip()

AnswererRunnable = RunnableLambda(answerer_fn)