from langchain_core.runnables import RunnableLambda
from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

load_dotenv() 

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "12345678")

driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USER, NEO4J_PASSWORD)
)

def run_cypher(cypher: str):
    try:
        with driver.session() as session:
            result = session.run(cypher)
            return [record.data() for record in result]
    except Exception as e:
        return {"error": str(e), "cypher": cypher}

RetrieverRunnable = RunnableLambda(run_cypher)
