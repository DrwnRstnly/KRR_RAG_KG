"""
RAG Service Layer

Provides clean request/response interface for RAG operations.
This layer can be easily wrapped as REST API or gRPC service.
"""

from typing import Dict, Any, Optional, Generator
from dataclasses import asdict
import time

from src.domain.models import RAGResponse
from src.rag_v2.pipeline import RAGPipeline


class RAGService:
    """Service layer for RAG operations"""

    def __init__(self, llm, verbose: bool = False):
        self.pipeline = RAGPipeline(llm, verbose=verbose)

    def query(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a RAG query

        Request format:
        {
            "question": str,
            "options": {
                "verbose": bool (optional),
                "include_metadata": bool (optional)
            }
        }

        Response format:
        {
            "success": bool,
            "data": {
                "answer": str,
                "sources": List[str],
                "confidence": float,
                "cypher_query": str (if include_metadata),
                "retrieved_data": List[Dict] (if include_metadata)
            },
            "error": str (if success=False),
            "timestamp": float
        }
        """
        timestamp = time.time()

        try:
            question = request.get("question", "")
            if not question:
                return {
                    "success": False,
                    "error": "Question is required",
                    "timestamp": timestamp
                }

            options = request.get("options", {})
            include_metadata = options.get("include_metadata", False)

            rag_response = self.pipeline.query(question)

            # Build response
            response_data = {
                "answer": rag_response.answer,
                "sources": rag_response.sources,
                "confidence": rag_response.confidence,
            }

            if include_metadata:
                response_data["cypher_query"] = rag_response.cypher_query
                response_data["retrieved_data"] = rag_response.retrieved_data

            return {
                "success": True,
                "data": response_data,
                "timestamp": timestamp
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": timestamp
            }

    def query_stream(self, request: Dict[str, Any]) -> Generator[Dict[str, Any], None, None]:
        """
        Process query with streaming responses

        Yields response chunks as they become available:
        {
            "type": "cypher" | "retrieval" | "generation" | "done" | "error",
            "content": Any,
            "timestamp": float
        }
        """
        question = request.get("question", "")
        if not question:
            yield {
                "type": "error",
                "content": "Question is required",
                "timestamp": time.time()
            }
            return

        for stage, content in self.pipeline.query_with_streaming(question):
            yield {
                "type": stage,
                "content": content,
                "timestamp": time.time()
            }

    def get_stats(self) -> Dict[str, Any]:
        """
        Get knowledge graph statistics

        Response format:
        {
            "success": bool,
            "data": {
                "cards": int,
                "rarities": int,
                ...
            }
        }
        """
        try:
            stats = self.pipeline.get_stats()
            return {
                "success": True,
                "data": stats
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def health_check(self) -> Dict[str, Any]:
        """
        Check service health

        Response format:
        {
            "healthy": bool,
            "components": {
                "neo4j": bool,
                "llm": bool
            }
        }
        """
        neo4j_healthy = False
        llm_healthy = False

        try:
            neo4j_healthy = self.pipeline.test_connection()
        except:
            pass

        try:
            test_response = self.pipeline.llm.invoke("Test")
            llm_healthy = True
        except Exception:
            pass

        return {
            "healthy": neo4j_healthy and llm_healthy,
            "components": {
                "neo4j": neo4j_healthy,
                "llm": llm_healthy
            }
        }

    def close(self):
        """Cleanup resources"""
        self.pipeline.close()


# Factory function
def create_rag_service(llm, verbose: bool = False) -> RAGService:
    """Create a RAG service instance"""
    return RAGService(llm, verbose=verbose)
