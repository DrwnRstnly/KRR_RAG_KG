"""
Enhanced Knowledge Graph Retriever

Improvements:
- Better error handling
- Query execution time tracking
- Result enrichment (fetch related data)
- Relevance scoring
"""

import time
from typing import List, Dict, Any, Optional
from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

from src.domain.models import QueryResult

load_dotenv()


class KGRetriever:
    """Retrieves data from Neo4j Knowledge Graph"""

    def __init__(self, uri: str = None, user: str = None, password: str = None):
        self.uri = uri or os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.user = user or os.getenv("NEO4J_USER", "neo4j")
        self.password = password or os.getenv("NEO4J_PASSWORD", "12345678")
        self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))

    def close(self):
        """Close database connection"""
        self.driver.close()

    def retrieve(self, cypher_query: str) -> QueryResult:
        """
        Execute Cypher query and return results with metadata

        Args:
            cypher_query: Cypher query string

        Returns:
            QueryResult with data, query, execution time, and potential errors
        """
        start_time = time.time()

        try:
            with self.driver.session() as session:
                result = session.run(cypher_query)
                data = [record.data() for record in result]
                execution_time = time.time() - start_time

                return QueryResult(
                    data=data,
                    cypher_query=cypher_query,
                    execution_time=execution_time,
                    error=None
                )

        except Exception as e:
            execution_time = time.time() - start_time
            error_msg = f"Query execution error: {str(e)}"

            return QueryResult(
                data=[],
                cypher_query=cypher_query,
                execution_time=execution_time,
                error=error_msg
            )

    def retrieve_with_context(self, cypher_query: str, card_name: Optional[str] = None) -> QueryResult:
        """
        Execute query and enrich results with contextual information

        For example, if querying a specific card, also fetch its:
        - Counters
        - Synergies
        - Archetype fits

        Args:
            cypher_query: Main Cypher query
            card_name: Optional card name for context enrichment

        Returns:
            QueryResult with enriched data
        """
        main_result = self.retrieve(cypher_query)

        if main_result.error or not card_name:
            return main_result

        try:
            context_data = self._fetch_card_context(card_name)
            if context_data and main_result.data:
                main_result.data[0]["_context"] = context_data
        except Exception:
            pass

        return main_result

    def _fetch_card_context(self, card_name: str) -> Dict[str, Any]:
        """Fetch contextual information about a card"""
        context_query = """
        MATCH (c:Card {name: $card_name})

        // Get counters
        OPTIONAL MATCH (c)-[counters_rel:COUNTERS]->(countered:Card)
        WITH c, COLLECT({card: countered.name, effectiveness: counters_rel.effectiveness}) AS counters

        // Get what it's countered by
        OPTIONAL MATCH (counter:Card)-[counter_rel:COUNTERS]->(c)
        WITH c, counters, COLLECT({card: counter.name, effectiveness: counter_rel.effectiveness}) AS countered_by

        // Get synergies
        OPTIONAL MATCH (c)-[syn_rel:SYNERGIZES_WITH]->(syn:Card)
        WITH c, counters, countered_by, COLLECT({card: syn.name, synergy_type: syn_rel.synergy_type}) AS synergies

        // Get archetype fits
        OPTIONAL MATCH (c)-[fit_rel:FITS_ARCHETYPE]->(arch:Archetype)
        WITH c, counters, countered_by, synergies, COLLECT({archetype: arch.name, role: fit_rel.role}) AS archetypes

        RETURN {
            counters: counters,
            countered_by: countered_by,
            synergies: synergies,
            archetypes: archetypes
        } AS context
        """

        with self.driver.session() as session:
            result = session.run(context_query, card_name=card_name)
            record = result.single()
            if record:
                return record["context"]
        return {}

    def test_connection(self) -> bool:
        """Test if connection to Neo4j is working"""
        try:
            with self.driver.session() as session:
                result = session.run("RETURN 1 AS test")
                return result.single()["test"] == 1
        except Exception as e:
            print(f"Connection test failed: {e}")
            return False

    def get_stats(self) -> Dict[str, int]:
        """Get database statistics"""
        stats_query = """
        MATCH (c:Card) WITH COUNT(c) AS cards
        MATCH (r:Rarity) WITH cards, COUNT(r) AS rarities
        MATCH (a:Arena) WITH cards, rarities, COUNT(a) AS arenas
        MATCH ()-[rel:COUNTERS]->() WITH cards, rarities, arenas, COUNT(rel) AS counters
        MATCH ()-[syn:SYNERGIZES_WITH]->() WITH cards, rarities, arenas, counters, COUNT(syn) AS synergies
        MATCH ()-[fit:FITS_ARCHETYPE]->() WITH cards, rarities, arenas, counters, synergies, COUNT(fit) AS archetype_fits

        RETURN {
            cards: cards,
            rarities: rarities,
            arenas: arenas,
            counter_relationships: counters,
            synergy_relationships: synergies,
            archetype_fits: archetype_fits
        } AS stats
        """

        try:
            with self.driver.session() as session:
                result = session.run(stats_query)
                record = result.single()
                if record:
                    return record["stats"]
        except:
            pass

        return {}


def create_retriever() -> KGRetriever:
    """Create a KG retriever instance"""
    return KGRetriever()
