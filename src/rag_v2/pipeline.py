from typing import Optional
import time

from src.domain.models import RAGResponse, QueryResult
from src.rag_v2.translator import QueryTranslator
from src.rag_v2.retriever import KGRetriever
from src.rag_v2.generator import AnswerGenerator


class RAGPipeline:
    def __init__(self, llm, verbose: bool = False):
        self.llm = llm
        self.verbose = verbose
        self.translator = QueryTranslator(llm)
        self.retriever = KGRetriever()
        self.generator = AnswerGenerator(llm)

    def query(self, question: str) -> RAGResponse:
        if self.verbose:
            print(f"\n{'='*60}")
            print(f"Question: {question}")
            print(f"{'='*60}")

        if self.verbose:
            print("\n[1/3] Translating to Cypher...")

        cypher_query = self.translator.translate(question)

        if self.verbose:
            print(f"Generated Cypher:\n{cypher_query}")

        if self.verbose:
            print("\n[2/3] Retrieving from Knowledge Graph...")

        query_result = self.retriever.retrieve(cypher_query)

        if self.verbose:
            if query_result.error:
                print(f"Error: {query_result.error}")
            else:
                print(f"Retrieved {len(query_result.data)} records in {query_result.execution_time:.3f}s")
                if query_result.data:
                    print(f"Sample: {query_result.data[0]}")

        if self.verbose:
            print("\n[3/3] Generating answer...")

        response = self.generator.generate(question, query_result)

        if self.verbose:
            print(f"\nAnswer:\n{response.answer}")
            if response.sources:
                print(f"\nSources: {', '.join(response.sources)}")
            print(f"Confidence: {response.confidence:.2f}")
            print(f"{'='*60}\n")

        return response

    def query_with_streaming(self, question: str):
        yield ("cypher", "Translating question to graph query...")
        cypher_query = self.translator.translate(question)
        yield ("cypher", cypher_query)

        yield ("retrieval", "Searching knowledge graph...")
        query_result = self.retriever.retrieve(cypher_query)

        if query_result.error:
            yield ("error", query_result.error)
            return

        yield ("retrieval", f"Found {len(query_result.data)} results")

        yield ("generation", "Generating answer...")

        response = self.generator.generate(question, query_result)

        words = response.answer.split()
        for i, word in enumerate(words):
            if i == 0:
                yield ("generation", word)
            else:
                yield ("generation", " " + word)
            time.sleep(0.02)

        yield ("done", {
            "sources": response.sources,
            "confidence": response.confidence,
            "cypher": response.cypher_query
        })

    def close(self):
        self.retriever.close()

    def test_connection(self) -> bool:
        return self.retriever.test_connection()

    def get_stats(self):
        return self.retriever.get_stats()


def create_pipeline(llm, verbose: bool = False) -> RAGPipeline:
    return RAGPipeline(llm, verbose=verbose)


def query(question: str, llm, verbose: bool = False) -> RAGResponse:
    pipeline = create_pipeline(llm, verbose=verbose)
    try:
        return pipeline.query(question)
    finally:
        pipeline.close()
