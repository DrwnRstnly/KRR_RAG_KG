

from typing import List, Dict, Optional, Tuple
from difflib import get_close_matches
import re
from src.rag.deck_analyzer import DeckAnalyzer


class QueryPreprocessor:
    

    def __init__(self, retriever):
        self.retriever = retriever
        self._card_names_cache = None
        self.deck_analyzer = DeckAnalyzer(retriever)

    def get_all_card_names(self) -> List[str]:
        
        if self._card_names_cache is None:
            result = self.retriever.retrieve("MATCH (c:Card) RETURN c.name AS name")
            if not result.error and result.data:
                self._card_names_cache = [record['name'] for record in result.data]
            else:
                self._card_names_cache = []
        return self._card_names_cache

    def find_similar_card_names(self, query_text: str, threshold: float = 0.7) -> List[Tuple[str, str]]:
        
        all_cards = self.get_all_card_names()
        if not all_cards:
            return []

        
        common_words = {
            'the', 'what', 'which', 'card', 'cards', 'tell', 'me', 'about', 'is', 'are',
            'my', 'deck', 'with', 'and', 'or', 'can', 'does', 'how', 'why', 'when',
            'counter', 'counters', 'beat', 'defeat', 'against', 'synergize', 'synergizes',
            'work', 'works', 'good', 'best', 'better', 'for', 'in', 'on', 'at', 'to',
            'cost', 'elixir', 'damage', 'health', 'hit', 'hits', 'attack', 'defense',
            'spell', 'troop', 'building', 'win', 'condition', 'that', 'this', 'have',
            'has', 'well', 'analyze', 'check', 'validate', 'rate', 'compare', 'question'
        }

        
        
        multi_word_pattern = r'\b[A-Z][a-zA-Z.]*(?:\s+[A-Z][a-zA-Z.]*)+\b'
        multi_word_matches = re.findall(multi_word_pattern, query_text)

        
        single_word_pattern = r'\b[A-Z][a-zA-Z.]*\b'
        capitalized_words = re.findall(single_word_pattern, query_text)

        
        all_words = query_text.split()
        potential_cards = set()

        
        for match in multi_word_matches:
            potential_cards.add(match)

        
        used_words = set()
        for multi_word in multi_word_matches:
            for word in multi_word.split():
                used_words.add(word)

        
        for word in capitalized_words:
            if word not in used_words:
                potential_cards.add(word)

        
        for word in all_words:
            word_clean = re.sub(r'[^\w\s]', '', word)  
            if (len(word_clean) >= 4 and
                word_clean.lower() not in common_words and
                not word_clean[0].isupper() and
                word_clean not in used_words):
                potential_cards.add(word_clean)

        suggestions = []
        for word in potential_cards:
            
            if word.lower() in common_words:
                continue

            
            if len(word) < 3:
                continue

            
            exact_matches = [card for card in all_cards if card.lower() == word.lower()]
            if exact_matches:
                if exact_matches[0] != word:  
                    suggestions.append((word, exact_matches[0]))
                continue

            
            matches = get_close_matches(word, all_cards, n=1, cutoff=threshold)
            if matches:
                
                if len(word) >= 4:
                    suggestions.append((word, matches[0]))

        return suggestions

    def correct_card_names_in_query(self, query: str) -> Tuple[str, List[str]]:
        
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
        
        deck_keywords = ['analyze', 'check', 'validate', 'deck', 'my deck', 'rate']
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in deck_keywords)

    def extract_deck_from_query(self, query: str) -> Optional[List[str]]:
        
        
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

        
        potential_cards = []
        if ',' in deck_part:
            potential_cards = [c.strip() for c in deck_part.split(',')]
        else:
            
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

        
        card_aliases = {
            'log': 'The Log',
            'pekka': 'P.E.K.K.A.',
            'mini pekka': 'Mini P.E.K.K.A.',
            'mk': 'Mega Knight',
            'ewiz': 'Electro Wizard',
            'exe': 'Executioner',
            'xbow': 'X-Bow',
            'rg': 'Royal Giant',
            'skeleton': 'Skeletons',
            'gy': 'Graveyard',
        }

        
        all_cards = self.get_all_card_names()
        deck = []

        for card in potential_cards:
            card = card.strip()

            
            if card.lower().startswith('and '):
                card = card[4:].strip()

            
            
            for punct in ['.', '?', '!']:
                if punct in card:
                    card = card.split(punct)[0].strip()

            if not card or len(card) < 2:
                continue

            
            if card.lower() in card_aliases:
                deck.append(card_aliases[card.lower()])
                continue

            
            exact_matches = [c for c in all_cards if c.lower() == card.lower()]
            if exact_matches:
                deck.append(exact_matches[0])
                continue

            
            matches = get_close_matches(card, all_cards, n=1, cutoff=0.6)
            if matches:
                deck.append(matches[0])

        return deck if len(deck) == 8 else None


class SmartResponseEnhancer:
    

    def __init__(self, retriever):
        self.retriever = retriever

    def find_alternative_data(self, question: str, original_cypher: str, original_data: List[Dict]) -> Optional[Dict]:
        
        question_lower = question.lower()

        if 'counter' in question_lower or 'beat' in question_lower or 'defeat' in question_lower:
            return self._find_counter_alternatives(question, original_cypher)

        if 'synerg' in question_lower or 'work with' in question_lower or 'combo' in question_lower:
            return self._find_synergy_alternatives(question, original_cypher)

        if 'MATCH (c:Card {name:' in original_cypher or 'Card {name:' in original_cypher:
            return self._find_similar_card_alternatives(question, original_cypher)

        return None

    def _find_counter_alternatives(self, question: str, original_cypher: str) -> Optional[Dict]:
        
        
        card_name = self._extract_card_name_from_query(question)
        if not card_name:
            return None

        
        card_info_result = self.retriever.retrieve(
            f"MATCH (c:Card {{name: '{card_name}'}}) RETURN c.elixir AS cost, c.type AS type, c.transport AS transport"
        )

        if not card_info_result.data:
            return None

        card_info = card_info_result.data[0]
        elixir_cost = card_info.get('cost', 0)
        card_type = card_info.get('type', '')
        transport = card_info.get('transport', '')

        
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
        
        
        
        return None

    def _extract_card_name_from_query(self, question: str) -> Optional[str]:
        
        words = question.split()

        quoted = re.findall(r"'([^']+)'", question)
        if quoted:
            return quoted[0]

        card_name_pattern = r'\b([A-Z][a-z]*(?:\s+[A-Z][a-z]*)*)\b'
        matches = re.findall(card_name_pattern, question)

        if matches:
            return max(matches, key=len)

        return None
