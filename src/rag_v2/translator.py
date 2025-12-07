from typing import Optional
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda

from src.kg.schema import KGSchema


class QueryTranslator:
    """Translates natural language questions to Cypher queries"""

    def __init__(self, llm):
        self.llm = llm
        self.schema = KGSchema()
        self.prompt_template = self._build_prompt_template()

    def _build_prompt_template(self) -> PromptTemplate:
        """Build comprehensive prompt template"""

        raw_schema_desc = self.schema.get_schema_description()
        schema_desc = raw_schema_desc.replace("{", "{{").replace("}", "}}")

        examples = self.schema.get_cypher_examples()

        raw_examples_text = "\n\n".join([
            f"Question: {ex['question']}\nCypher: {ex['cypher']}"
            for ex in examples
        ])
        examples_text = raw_examples_text.replace("{", "{{").replace("}", "}}")

        template = """You are an expert Cypher query translator for a Clash Royale Knowledge Graph.

""" + schema_desc + """

1. Use MATCH for querying nodes and relationships
2. Use WHERE for filtering (prefer WHERE over inline {{}} for clarity)
3. Use RETURN to specify what data to return
4. For name matching, use "c.name = 'ExactName'" or "c.name CONTAINS 'PartialName'" for partial matches
5. Always return meaningful column names with AS keyword
6. For aggregations, use COUNT(), SUM(), AVG(), etc.
7. For multi-hop queries, chain multiple MATCH patterns
8. Order results when relevant using ORDER BY
9. Limit results if asking for "top" or "best" using LIMIT
10. **For Champion cards**: Always include c.level11_stats in RETURN clause to capture ability information
11. **For Champion queries**: Include c.rarity to identify if card is a champion


""" + examples_text + """

## Your Task:
Translate the following question into a valid Cypher query.
Output ONLY the Cypher query, no explanations or markdown formatting.

Question: {question}

Cypher:"""

        return PromptTemplate.from_template(template)

    def translate(self, question: str) -> str:
        """Translate natural language question to Cypher query"""
        prompt = self.prompt_template.format(question=question)
        result = self.llm.invoke(prompt)
        clean_result = self._clean_cypher_output(result)
        return clean_result

    def _clean_cypher_output(self, raw_output: str) -> str:
        """Clean LLM output to extract pure Cypher query"""
        if hasattr(raw_output, 'content'):
            text = raw_output.content
        else:
            text = str(raw_output)

        text = text.replace("```cypher", "").replace("```", "").strip()

        if "Cypher:" in text:
            text = text.split("Cypher:")[-1].strip()

        lines = text.split("\n")
        cypher_lines = []
        for line in lines:
            line = line.strip()
            if line.startswith("//") or line.startswith("#"):
                continue
            if line:
                cypher_lines.append(line)

        return " ".join(cypher_lines)

    def create_runnable(self):
        """Create a LangChain runnable"""
        return RunnableLambda(self.translate)


# Factory function for easy instantiation
def create_translator(llm) -> QueryTranslator:
    """Create a query translator instance"""
    return QueryTranslator(llm)
