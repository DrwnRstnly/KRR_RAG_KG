

import json
from typing import List, Dict, Any
from langchain_core.prompts import PromptTemplate

from src.domain.models import RAGResponse, QueryResult


class AnswerGenerator:
    

    def __init__(self, llm):
        self.llm = llm
        self.prompt_template = self._build_prompt_template()

    def _build_prompt_template(self) -> PromptTemplate:
        
        template = """You are a helpful Clash Royale assistant providing accurate information from a knowledge graph.

## Instructions:
1. Use ONLY the information provided in the Graph Data below
2. **IMPORTANT**: Include ALL cards from the data - do not skip or omit any entries
3. **CRITICAL**: Only say "I don't have information about that" if NO data was retrieved at all (data is completely empty). If ANY data exists, provide a complete answer using that data.
4. **For basic card info questions**: If the data contains card properties (name, elixir, hp, damage, dps, description, etc.), provide a complete answer with ALL those details. Don't just list the name.
5. **For synergy/counter questions**:
   - If the data has 'synergy_type' or 'strength' fields, use those to explain WHY cards work well together
   - If these fields are missing, simply list the cards WITHOUT making up reasons (don't invent explanations like "complements X's slow movement")
6. **For counter relationships**: If effectiveness/reason fields exist, explain WHY. Otherwise, just list the counters.
7. Format card stats clearly (HP, Damage, DPS, Elixir cost, etc.)
8. Be concise but complete - mention EVERY card and ALL stats in the retrieved data
9. Cite specific numbers and facts from the data
10. For Champions: If a card has rarity='champion', check the 'stats' or 'level11_stats' field for ability information
   - Look for stats with pattern "stat_name (with Ability Name)": value
   - Extract and explain the ability name and its effect on stats

## FORMATTING RULES:
- Do NOT use markdown formatting (no **, ##, -, etc.)
- Use plain text only
- When listing multiple cards:
  * If synergy_type/strength/effectiveness fields exist: "Cards that work well with Giant: Dark Prince (tank synergy, high strength), Prince (beatdown synergy, medium strength)"
  * If NO synergy fields exist: Simply list "Cards that work well with Giant: Dark Prince, Prince, Mega Minion, Musketeer" WITHOUT parenthetical explanations
- Include ALL cards from the data, separated by commas
- Separate into readable sentences

## User Question:
{question}

## Graph Data Retrieved:
{data}

## Your Answer:
Provide a clear, concise answer based strictly on the graph data above. List ALL cards from the data. Only include explanations in parentheses if synergy_type/strength/effectiveness fields are present in the data. If these fields are missing, just list the card names without explanations. DO NOT make up reasons or explanations. DO NOT omit any cards."""

        return PromptTemplate.from_template(template)

    def generate(self, question: str, query_result: QueryResult) -> RAGResponse:
        
        
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
        
        if not data:
            return "No data retrieved."

        formatted = json.dumps(data, indent=2, ensure_ascii=False)
        return formatted

    def _clean_answer(self, raw_answer: str) -> str:
        
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
        
        sources = set()

        for record in data:
            for key, value in record.items():
                if isinstance(value, str) and key.lower() in ['card', 'name', 'from', 'to']:
                    sources.add(value)
                elif key == 'card' and isinstance(value, dict) and 'name' in value:
                    sources.add(value['name'])

        return sorted(list(sources))

    def _estimate_confidence(self, data: List[Dict[str, Any]], answer: str) -> float:
        
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

        
        if len(answer) < 20:
            base_confidence *= 0.8
        elif len(answer) > 100:
            base_confidence *= 1.1

        
        return min(base_confidence, 1.0)


def create_generator(llm) -> AnswerGenerator:
    
    return AnswerGenerator(llm)
