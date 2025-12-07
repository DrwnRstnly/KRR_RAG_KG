"""
Query Preprocessor for handling typos, case sensitivity, and query enhancement
"""

from typing import List, Dict, Optional, Tuple
from difflib import get_close_matches
import re
from src.rag_v2.deck_analyzer import DeckAnalyzer


class QueryPreprocessor:
    """Preprocesses queries to handle typos and improve matching"""

    def __init__(self, retriever):
        self.retriever = retriever
        self._card_names_cache = None
        self.deck_analyzer = DeckAnalyzer(retriever)

    def get_all_card_names(self) -> List[str]:
        """Get all card names from the database (cached)"""
        if self._card_names_cache is None:
            result = self.retriever.retrieve("MATCH (c:Card) RETURN c.name AS name")
            if not result.error and result.data:
                self._card_names_cache = [record['name'] for record in result.data]
            else:
                self._card_names_cache = []
        return self._card_names_cache

    def find_similar_card_names(self, query_text: str, threshold: float = 0.7) -> List[Tuple[str, str]]:
        """
        Find card names mentioned in query and suggest corrections for typos

        Returns: List of (original_word, suggested_card_name) tuples
        """
        all_cards = self.get_all_card_names()
        if not all_cards:
            return []

        # Common words to ignore (expanded list)
        common_words = {
            'the', 'what', 'which', 'card', 'cards', 'tell', 'me', 'about', 'is', 'are',
            'my', 'deck', 'with', 'and', 'or', 'can', 'does', 'how', 'why', 'when',
            'counter', 'counters', 'beat', 'defeat', 'against', 'synergize', 'synergizes',
            'work', 'works', 'good', 'best', 'better', 'for', 'in', 'on', 'at', 'to',
            'cost', 'elixir', 'damage', 'health', 'hit', 'hits', 'attack', 'defense',
            'spell', 'troop', 'building', 'win', 'condition', 'that', 'this', 'have',
            'has', 'well', 'analyze', 'check', 'validate', 'rate', 'compare'
        }

        # Only look for capitalized words (likely card names)
        words = re.findall(r'\b[A-Z][a-zA-Z.]*(?:\s+[A-Z][a-zA-Z.]*)*\b', query_text)

        suggestions = []
        for word in words:
            # Skip common words
            if word.lower() in common_words:
                continue

            # Skip very short words (less than 3 chars) unless they match exactly
            if len(word) < 3:
                continue

            # Try exact match (case-insensitive)
            exact_matches = [card for card in all_cards if card.lower() == word.lower()]
            if exact_matches:
                if exact_matches[0] != word:  # Case mismatch
                    suggestions.append((word, exact_matches[0]))
                continue

            # Try fuzzy matching with higher threshold
            matches = get_close_matches(word, all_cards, n=1, cutoff=threshold)
            if matches:
                # Extra validation: only suggest if similarity is very high OR word is long enough
                if len(word) >= 4:
                    suggestions.append((word, matches[0]))

        return suggestions

    def correct_card_names_in_query(self, query: str) -> Tuple[str, List[str]]:
        """
        Correct card names in the query

        Returns: (corrected_query, list_of_corrections_made)
        """
        suggestions = self.find_similar_card_names(query)

        if not suggestions:
            return query, []

        corrected_query = query
        corrections = []

        for original, suggested in suggestions:
            if original != suggested:
                corrected_query = re.sub(
                    r'\b' + re.escape(original) + r'\b',
                    suggested,
                    corrected_query,
                    flags=re.IGNORECASE
                )
                corrections.append(f"'{original}' -> '{suggested}'")

        return corrected_query, corrections

    def is_deck_analysis_query(self, query: str) -> bool:
        """Check if query is asking for deck analysis"""
        deck_keywords = ['analyze', 'check', 'validate', 'deck', 'my deck', 'rate']
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in deck_keywords)

    def extract_deck_from_query(self, query: str) -> Optional[List[str]]:
        """
        Extract deck (list of 8 cards) from query

        Expected formats:
        - "Analyze my deck: Giant, Witch, Arrows, ..."
        - "Check deck with Giant Witch Arrows ..."
        - "Rate my deck [Giant, Witch, Arrows, ...]"
        """
        # Try to find cards separated by commas
        if ':' in query:
            deck_part = query.split(':', 1)[1]
        elif 'with' in query.lower():
            parts = query.lower().split('with')
            if len(parts) > 1:
                deck_part = parts[1]
            else:
                deck_part = query
        elif '[' in query and ']' in query:
            deck_part = query[query.index('[')+1:query.index(']')]
        else:
            deck_part = query

        # Split by commas or spaces
        potential_cards = []
        if ',' in deck_part:
            potential_cards = [c.strip() for c in deck_part.split(',')]
        else:
            # Try to extract capitalized words
            words = deck_part.split()
            current_card = []
            for word in words:
                if word[0].isupper() if word else False:
                    if current_card:
                        potential_cards.append(' '.join(current_card))
                    current_card = [word]
                elif current_card:
                    current_card.append(word)
            if current_card:
                potential_cards.append(' '.join(current_card))

        # Validate and correct card names
        all_cards = self.get_all_card_names()
        deck = []

        for card in potential_cards:
            card = card.strip()
            if not card or len(card) < 2:
                continue

            # Try exact match
            exact_matches = [c for c in all_cards if c.lower() == card.lower()]
            if exact_matches:
                deck.append(exact_matches[0])
                continue

            # Try fuzzy match
            matches = get_close_matches(card, all_cards, n=1, cutoff=0.6)
            if matches:
                deck.append(matches[0])

        return deck if len(deck) == 8 else None


class SmartResponseEnhancer:
    """Enhances responses when exact data is not available"""

    def __init__(self, retriever):
        self.retriever = retriever

    def find_alternative_data(self, question: str, original_cypher: str, original_data: List[Dict]) -> Optional[Dict]:
        """
        When no data is found, try to find related/helpful information

        Returns: Dict with 'alternative_query', 'data', and 'explanation'
        """
        question_lower = question.lower()

        if 'counter' in question_lower or 'beat' in question_lower or 'defeat' in question_lower:
            return self._find_counter_alternatives(question, original_cypher)

        if 'synerg' in question_lower or 'work with' in question_lower or 'combo' in question_lower:
            return self._find_synergy_alternatives(question, original_cypher)

        if 'MATCH (c:Card {name:' in original_cypher or 'Card {name:' in original_cypher:
            return self._find_similar_card_alternatives(question, original_cypher)

        return None

    def _find_counter_alternatives(self, question: str, original_cypher: str) -> Optional[Dict]:
        """Find alternative counter suggestions based on card type/cost"""
        # Extract card name from question
        card_name = self._extract_card_name_from_query(question)
        if not card_name:
            return None

        # Get card info
        card_info_result = self.retriever.retrieve(
            f"MATCH (c:Card {{name: '{card_name}'}}) RETURN c.elixir AS cost, c.type AS type, c.transport AS transport"
        )

        if not card_info_result.data:
            return None

        card_info = card_info_result.data[0]
        elixir_cost = card_info.get('cost', 0)
        card_type = card_info.get('type', '')
        transport = card_info.get('transport', '')

        # Find cheaper cards that might counter it
        alternative_query = f"""
        MATCH (c:Card)
        WHERE c.elixir <= {elixir_cost}
        RETURN c.name AS card, c.elixir AS cost, c.type AS type
        ORDER BY c.elixir
        LIMIT 5
        """

        result = self.retriever.retrieve(alternative_query)

        if result.data:
            return {
                'data': result.data,
                'explanation': f"While there's no specific counter data for {card_name}, here are some lower-cost cards that might work effectively against it",
                'query': alternative_query
            }

        return None

    def _find_synergy_alternatives(self, question: str, original_cypher: str) -> Optional[Dict]:
        """Find cards that might synergize based on type/cost"""
        card_name = self._extract_card_name_from_query(question)
        if not card_name:
            return None

        archetype_result = self.retriever.retrieve(
            f"MATCH (c:Card {{name: '{card_name}'}})-[:FITS_ARCHETYPE]->(a:Archetype) "
            f"RETURN a.name AS archetype"
        )

        if archetype_result.data:
            archetype = archetype_result.data[0]['archetype']

            alternative_query = f"""
            MATCH (c:Card)-[:FITS_ARCHETYPE]->(a:Archetype {{name: '{archetype}'}})
            WHERE c.name <> '{card_name}'
            RETURN c.name AS card, c.elixir AS cost
            ORDER BY c.elixir
            LIMIT 5
            """

            result = self.retriever.retrieve(alternative_query)

            if result.data:
                return {
                    'data': result.data,
                    'explanation': f"While there's no specific synergy data, here are cards from the same '{archetype}' archetype that typically work well together",
                    'query': alternative_query
                }

        return None

    def _find_similar_card_alternatives(self, question: str, original_cypher: str) -> Optional[Dict]:
        """Find similar cards when specific card query returns nothing"""
        # This could suggest cards with similar stats/cost
        # For now, we'll skip this and let the preprocessor handle it
        return None

    def _extract_card_name_from_query(self, question: str) -> Optional[str]:
        """Extract likely card name from natural language question"""
        words = question.split()

        quoted = re.findall(r"'([^']+)'", question)
        if quoted:
            return quoted[0]

        card_name_pattern = r'\b([A-Z][a-z]*(?:\s+[A-Z][a-z]*)*)\b'
        matches = re.findall(card_name_pattern, question)

        if matches:
            return max(matches, key=len)

        return None
