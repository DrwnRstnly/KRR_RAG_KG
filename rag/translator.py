from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from rag.llm import llm

schema_context = """
Graph Schema:
Nodes: 
 - Card (properties: name, elixir, type, hitpoints, damage, dps)
 - Rarity (properties: name)
 - Arena (properties: name)
 - Target (properties: name) -- Values: 'ground', 'air', 'buildings'

Relationships:
 - (:Card)-[:HAS_RARITY]->(:Rarity)
 - (:Card)-[:UNLOCKS_IN]->(:Arena)
 - (:Card)-[:CAN_HIT]->(:Target)

Note: 
- 'hitpoints', 'damage', and 'dps' are numbers on the Card node.
- Use 'CONTAINS' for names to be safe (e.g., "Pekka" might be "P.E.K.K.A").
"""

translator_prompt = PromptTemplate.from_template("""
You are a Cypher translator for a Clash Royale Knowledge Graph.
Use the schema below to translate the user question into a valid Cypher query.
Do NOT output explanations, only the Cypher query.

{schema}

Examples:
Question: How much HP does the Giant have?
Cypher: MATCH (c:Card) WHERE c.name CONTAINS 'Giant' RETURN c.name, c.hitpoints

Question: Which cards target air?
Cypher: MATCH (c:Card)-[:CAN_HIT]->(:Target {{name: 'air'}}) RETURN c.name

Question: List all Legendary cards in Arena 10.
Cypher: MATCH (c:Card)-[:HAS_RARITY]->(:Rarity {{name: 'Legendary'}}) MATCH (c)-[:UNLOCKS_IN]->(a:Arena) WHERE a.name CONTAINS '10' RETURN c.name

Question: What is the elixir cost of a Valkyrie?
Cypher: MATCH (c:Card) WHERE c.name CONTAINS 'Valkyrie' RETURN c.elixir

User question:
{question}

Cypher:
""")

def translator_fn(question: str):
    prompt = translator_prompt.format(question=question, schema=schema_context)
    result = llm.invoke(prompt)
    
    clean_result = result.replace("```cypher", "").replace("```", "").strip()
    if "Cypher:" in clean_result:
        clean_result = clean_result.split("Cypher:")[-1].strip()
    
    return clean_result

TranslatorRunnable = RunnableLambda(translator_fn)