from typing import Dict, Any, Optional, Generator
from dataclasses import asdict
import time

from src.domain.models import RAGResponse
from src.rag.pipeline import RAGPipeline
class RAGService:

    def __init__(self, llm, verbose: bool = False):
        self.pipeline = RAGPipeline(llm, verbose=verbose)

    def query(self, request: Dict[str, Any]) -> Dict[str, Any]:
        
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
        
        self.pipeline.close()


def create_rag_service(llm, verbose: bool = False) -> RAGService:
    
    return RAGService(llm, verbose=verbose)
