from typing import Optional
import time
import sys

from src.domain.models import RAGResponse, QueryResult
from src.rag.translator import QueryTranslator
from src.rag.retriever import KGRetriever
from src.rag.generator import AnswerGenerator
from src.rag.query_preprocessor import QueryPreprocessor, SmartResponseEnhancer


class RAGPipeline:
    def __init__(self, llm, verbose: bool = False):
        self.llm = llm
        self.verbose = verbose
        self.translator = QueryTranslator(llm)
        self.retriever = KGRetriever()
        self.generator = AnswerGenerator(llm)
        self.preprocessor = QueryPreprocessor(self.retriever)
        self.response_enhancer = SmartResponseEnhancer(self.retriever)

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
        try:
            if self.preprocessor.is_deck_analysis_query(question):
                deck = self.preprocessor.extract_deck_from_query(question)

                if deck:
                    yield ("info", f"Detected deck analysis request for: {', '.join(deck)}")

                    yield ("generation", "Running rule-based analysis...")
                    analysis = self.preprocessor.deck_analyzer.analyze_deck(deck)

                    yield ("generation", "\nQuerying knowledge graph for synergies...")
                    synergies = self.preprocessor.deck_analyzer.get_deck_synergies(deck)

                    yield ("generation", "\nQuerying knowledge graph for counters...")
                    counters = self.preprocessor.deck_analyzer.get_deck_counters(deck)

                    yield ("generation", "\nGenerating final analysis...\n\n")
                    formatted_analysis = self.preprocessor.deck_analyzer.format_analysis(analysis, synergies, counters)

                    yield ("generation", formatted_analysis)

                    yield ("done", {
                        "sources": deck,
                        "confidence": 1.0,
                        "cypher": "DECK_ANALYSIS_HYBRID"
                    })
                    return
                else:
                    yield ("info", "Could not extract 8 cards from query. Please provide deck as: card1, card2, card3, card4, card5, card6, card7, card8")

            corrected_question, corrections = self.preprocessor.correct_card_names_in_query(question)

            if corrections:
                yield ("info", f"Auto-corrected: {', '.join(corrections)}")
                question = corrected_question

            yield ("cypher", "Translating question to graph query...")

            try:
                cypher_query = self.translator.translate(question)
            except Exception as e:
                yield ("error", f"Translation error: {str(e)}")
                return

            yield ("cypher", cypher_query)

            yield ("retrieval", "Searching knowledge graph...")

            try:
                query_result = self.retriever.retrieve(cypher_query)
            except Exception as e:
                yield ("error", f"Retrieval error: {str(e)}")
                return

            if query_result.error:
                yield ("error", query_result.error)
                return

            yield ("retrieval", f"Found {len(query_result.data)} results")

            if not query_result.data:
                alternative = self.response_enhancer.find_alternative_data(question, cypher_query, query_result.data)

                if alternative:
                    yield ("info", alternative['explanation'])

                    query_result.data = alternative['data']
                    query_result.cypher_query = alternative.get('query', cypher_query)

            try:
                response = self.generator.generate(question, query_result)
            except Exception as e:
                yield ("error", f"Generation error: {str(e)}")
                return

            if not response or not response.answer:
                yield ("error", "Failed to generate answer")
                return

            words = response.answer.split()
            for i, word in enumerate(words):
                if i == 0:
                    yield ("generation", word)
                else:
                    yield ("generation", " " + word)
                time.sleep(0.02)

            yield ("done", {
                "sources": response.sources or [],
                "confidence": response.confidence or 0.0,
                "cypher": response.cypher_query or cypher_query
            })
        except Exception as e:
            import traceback
            yield ("error", f"Pipeline error: {str(e)}\n{traceback.format_exc()}")
            return

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
