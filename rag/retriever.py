from langchain_core.runnables import RunnableLambda
from langchain_community.graphs import Neo4jGraph
import os

graph = Neo4jGraph(
    url=os.getenv("NEO4J_URI", "bolt://localhost:7687"),
    username=os.getenv("NEO4J_USER", "neo4j"),
    password=os.getenv("NEO4J_PASSWORD", "password"),
)

def run_cypher(cypher: str):
    try:
        return graph.query(cypher)
    except Exception as e:
        return {"error": str(e), "cypher": cypher}

RetrieverRunnable = RunnableLambda(run_cypher)
