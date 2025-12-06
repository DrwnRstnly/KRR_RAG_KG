"""
Enhanced Answer Generator with Source Grounding

Improvements:
- Source citations and grounding
- Better formatting of stats
- Confidence scoring
- Structured output
"""

import json
from typing import List, Dict, Any
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda

from src.domain.models import RAGResponse, QueryResult


class AnswerGenerator:
    """Generates natural language answers from retrieved graph data"""

    def __init__(self, llm):
        self.llm = llm
        self.prompt_template = self._build_prompt_template()

    def _build_prompt_template(self) -> PromptTemplate:
        """Build answer generation prompt"""
        template = """You are a helpful Clash Royale assistant providing accurate information from a knowledge graph.

## Instructions:
1. Use ONLY the information provided in the Graph Data below
2. If the data is empty or doesn't answer the question, say "I don't have information about that"
3. Format card stats clearly (HP, Damage, DPS, Elixir cost, etc.)
4. Be concise but complete
5. If the data includes relationships (counters, synergies), mention them naturally
6. Cite specific numbers and facts from the data

## User Question:
{question}

## Graph Data Retrieved:
{data}

## Your Answer:
Provide a clear, concise answer based strictly on the graph data above."""

        return PromptTemplate.from_template(template)

    def generate(self, question: str, query_result: QueryResult) -> RAGResponse:
        """
        Generate answer from question and retrieved data

        Args:
            question: Original user question
            query_result: QueryResult from retriever

        Returns:
            RAGResponse with answer, sources, and metadata
        """
        
        if query_result.error:
            return RAGResponse(
                question=question,
                answer=f"I encountered an error while searching: {query_result.error}",
                cypher_query=query_result.cypher_query,
                retrieved_data=[],
                sources=[],
                confidence=0.0
            )

        
        if not query_result.data:
            return RAGResponse(
                question=question,
                answer="I couldn't find any information about that in the database.",
                cypher_query=query_result.cypher_query,
                retrieved_data=[],
                sources=[],
                confidence=0.0
            )

        
        formatted_data = self._format_data_for_prompt(query_result.data)

        
        prompt = self.prompt_template.format(
            question=question,
            data=formatted_data
        )

        result = self.llm.invoke(prompt)

        
        if hasattr(result, 'content'):
            answer_text = result.content
        else:
            answer_text = str(result)

        
        answer_text = self._clean_answer(answer_text)

        
        sources = self._extract_sources(query_result.data)

        
        confidence = self._estimate_confidence(query_result.data, answer_text)

        return RAGResponse(
            question=question,
            answer=answer_text,
            cypher_query=query_result.cypher_query,
            retrieved_data=query_result.data,
            sources=sources,
            confidence=confidence
        )

    def _format_data_for_prompt(self, data: List[Dict[str, Any]]) -> str:
        """Format retrieved data for LLM prompt"""
        if not data:
            return "No data retrieved."

        formatted = json.dumps(data, indent=2, ensure_ascii=False)
        return formatted

    def _clean_answer(self, raw_answer: str) -> str:
        """Clean up LLM-generated answer"""
        # Remove common prefixes
        answer = raw_answer.strip()

        prefixes_to_remove = [
            "Answer:",
            "Based on the data,",
            "According to the graph data,",
        ]

        for prefix in prefixes_to_remove:
            if answer.startswith(prefix):
                answer = answer[len(prefix):].strip()

        return answer

    def _extract_sources(self, data: List[Dict[str, Any]]) -> List[str]:
        """Extract source cards/entities from retrieved data"""
        sources = set()

        for record in data:
            for key, value in record.items():
                if isinstance(value, str) and key.lower() in ['card', 'name', 'from', 'to']:
                    sources.add(value)
                elif key == 'card' and isinstance(value, dict) and 'name' in value:
                    sources.add(value['name'])

        return sorted(list(sources))

    def _estimate_confidence(self, data: List[Dict[str, Any]], answer: str) -> float:
        """
        Estimate confidence score based on:
        - Amount of data retrieved
        - Completeness of data
        - Answer length

        Returns: Confidence score between 0.0 and 1.0
        """
        if not data:
            return 0.0

        
        num_results = len(data)
        if num_results >= 5:
            base_confidence = 0.9
        elif num_results >= 3:
            base_confidence = 0.8
        elif num_results >= 1:
            base_confidence = 0.7
        else:
            base_confidence = 0.5

        # Adjust based on answer length (too short might mean incomplete)
        if len(answer) < 20:
            base_confidence *= 0.8
        elif len(answer) > 100:
            base_confidence *= 1.1

        # Cap at 1.0
        return min(base_confidence, 1.0)

    def create_runnable(self):
        """Create a LangChain runnable"""
        def generate_fn(inputs: dict):
            question = inputs.get("question", "")
            query_result = inputs.get("query_result")
            if not query_result:
                # Fallback: create QueryResult from inputs
                query_result = QueryResult(
                    data=inputs.get("data", []),
                    cypher_query=inputs.get("cypher", ""),
                    execution_time=0.0
                )
            return self.generate(question, query_result)

        return RunnableLambda(generate_fn)


# Factory function
def create_generator(llm) -> AnswerGenerator:
    """Create an answer generator instance"""
    return AnswerGenerator(llm)
