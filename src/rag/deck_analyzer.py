

from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class WarningLevel(Enum):
    STRONG = "Strong Warning"
    WEAK = "Weak Warning"


@dataclass
class DeckWarning:
    level: WarningLevel
    message: str
    category: str  


class DeckAnalyzer:
    

    def __init__(self, retriever):
        self.retriever = retriever
        self._card_cache = {}

    def get_card_data(self, card_name: str) -> Optional[Dict]:
        
        if card_name in self._card_cache:
            return self._card_cache[card_name]

        result = self.retriever.retrieve(
            f"""
            MATCH (c:Card {{name: '{card_name}'}})
            OPTIONAL MATCH (c)-[:HAS_TYPE]->(t:Type)
            OPTIONAL MATCH (c)-[:CAN_HIT]->(target:Target)
            RETURN c.name AS name, c.elixir AS elixir, c.hitpoints AS hp,
                   c.damage AS damage, c.transport AS transport,
                   t.name AS type, COLLECT(DISTINCT target.name) AS targets
            """
        )

        if result.data:
            self._card_cache[card_name] = result.data[0]
            return result.data[0]
        return None

    def is_wincon_card(self, card_name: str, card_data: Dict) -> bool:
        
        targets = card_data.get('targets', [])
        if 'buildings' in targets:
            return True

        
        wincon_cards = ['X-Bow', 'Mortar', 'Goblin Drill', 'Rocket', 'Graveyard',
                        'Goblin Barrel', 'Miner', 'Royal Hogs', 'Hog Rider',
                        'Balloon', 'Royal Giant', 'Ram Rider']
        return card_name in wincon_cards

    def can_hit_air(self, card_data: Dict) -> bool:
        
        targets = card_data.get('targets', [])
        return 'air' in targets

    def is_spell(self, card_data: Dict) -> bool:
        
        return card_data.get('type') == 'spell'

    def is_building(self, card_data: Dict) -> bool:
        
        return card_data.get('type') == 'building'

    def is_anti_tank(self, card_name: str, card_data: Dict) -> bool:
        
        anti_tank_cards = ['Mighty Miner', 'Sparky', 'P.E.K.K.A.', 'Inferno Dragon',
                           'Prince', 'Hunter', 'Three Musketeers', 'Inferno Tower',
                           'Mini P.E.K.K.A.', 'Elite Barbarians', 'Skeleton Army',
                           'Goblins', 'Goblin Gang', 'Guards', 'Minion Horde']
        return card_name in anti_tank_cards

    def is_tank_or_mini_tank(self, card_data: Dict) -> bool:
        
        hp = card_data.get('hp', 0)
        return hp and hp > 1000

    def is_heavy_tank(self, card_data: Dict) -> bool:
        
        hp = card_data.get('hp', 0)
        return hp and hp > 3000

    def is_reset_card(self, card_name: str) -> bool:
        
        reset_cards = ['Electro Spirit', 'Electro Wizard', 'Electro Dragon', 'Zap',
                       'Ice Spirit', 'Lightning', 'Freeze', 'Electro Giant']
        return card_name in reset_cards

    def is_small_spell(self, card_data: Dict) -> bool:
        
        return self.is_spell(card_data) and card_data.get('elixir', 99) <= 3

    def is_big_spell(self, card_data: Dict) -> bool:
        
        return self.is_spell(card_data) and card_data.get('elixir', 0) > 3

    def is_building_killer_spell(self, card_name: str, card_data: Dict) -> bool:
        
        heavy_spells = ['Fireball', 'Poison', 'Lightning', 'Rocket']
        return card_name in heavy_spells or card_name == 'Earthquake'

    def is_cycle_card(self, card_data: Dict) -> bool:
        
        return card_data.get('elixir', 99) <= 2

    def is_siege_building(self, card_name: str) -> bool:
        
        return card_name in ['X-Bow', 'Mortar']

    def has_splash(self, card_name: str) -> bool:
        
        splash_cards = ['Wizard', 'Baby Dragon', 'Valkyrie', 'Bomber', 'Bowler',
                        'Executioner', 'Mega Knight', 'Dark Prince', 'Fire Spirit',
                        'Fireball', 'Poison', 'Lightning', 'Arrows', 'Rocket',
                        'Princess', 'Magic Archer', 'Hunter']
        return card_name in splash_cards

    def calculate_avg_elixir(self, deck_data: List[Dict]) -> float:
        
        if len(deck_data) != 8:
            return 0.0
        total = sum(card.get('elixir', 0) for card in deck_data)
        return total / 8.0

    def classify_archetype(self, deck: List[str], deck_data: List[Dict]) -> str:
        
        if any(self.is_siege_building(card) for card in deck):
            return 'siege'

        avg_elixir = self.calculate_avg_elixir(deck_data)
        if 0 < avg_elixir <= 3.0:
            return 'cycle'

        if any(self.is_heavy_tank(card_data) for card_data in deck_data):
            return 'beatdown'

        bridge_spam_cards = ['Magic Archer', 'Ram Rider', 'Lumberjack', 'Royal Ghost',
                            'Bandit', 'Prince', 'P.E.K.K.A.', 'Battle Ram']
        bridge_spam_count = sum(1 for card in deck if card in bridge_spam_cards)
        if bridge_spam_count >= 3:
            return 'bridge_spam'

        return 'No Archetype'

    def analyze_deck(self, deck: List[str]) -> Dict:
        
        if len(deck) != 8:
            return {
                'error': 'Deck must contain exactly 8 cards',
                'provided': len(deck)
            }

        deck_data = []
        for card in deck:
            data = self.get_card_data(card)
            if not data:
                return {'error': f"Card '{card}' not found in database"}
            deck_data.append(data)

        archetype = self.classify_archetype(deck, deck_data)
        avg_elixir = self.calculate_avg_elixir(deck_data)

        general_warnings = self._check_general_warnings(deck, deck_data)
        archetype_warnings = self._check_archetype_warnings(deck, deck_data, archetype)

        return {
            'deck': deck,
            'archetype': archetype,
            'avg_elixir': round(avg_elixir, 2),
            'general_warnings': general_warnings,
            'archetype_warnings': archetype_warnings
        }

    def _check_general_warnings(self, deck: List[str], deck_data: List[Dict]) -> List[DeckWarning]:
        
        warnings = []

        
        if not any(self.is_wincon_card(deck[i], deck_data[i]) for i in range(len(deck))):
            warnings.append(DeckWarning(
                WarningLevel.STRONG,
                'No win condition - Deck has no clear path to tower damage.',
                'general'
            ))

        
        if not any(self.can_hit_air(card_data) for card_data in deck_data):
            warnings.append(DeckWarning(
                WarningLevel.STRONG,
                'No air defense - Vulnerable to air-heavy decks (Lava Hound, Balloon, etc.).',
                'general'
            ))

        
        if not any(self.is_spell(card_data) for card_data in deck_data):
            warnings.append(DeckWarning(
                WarningLevel.STRONG,
                'No spell - Cannot deal spell damage or respond to swarms effectively.',
                'general'
            ))

        
        if not any(card_data.get('transport') == 'ground' for card_data in deck_data):
            warnings.append(DeckWarning(
                WarningLevel.STRONG,
                'No ground units - Deck contains only spells and cannot defend.',
                'general'
            ))

        
        wincon_count = sum(1 for i in range(len(deck)) if self.is_wincon_card(deck[i], deck_data[i]))
        if wincon_count > 2:
            warnings.append(DeckWarning(
                WarningLevel.STRONG,
                '> 2 win conditions - Deck lacks support/defense due to too many win cons.',
                'general'
            ))

        
        spell_count = sum(1 for card_data in deck_data if self.is_spell(card_data))
        if spell_count > 4:
            warnings.append(DeckWarning(
                WarningLevel.STRONG,
                '> 4 spells - Not enough troops to defend or push.',
                'general'
            ))

        
        avg_elixir = self.calculate_avg_elixir(deck_data)
        if avg_elixir >= 4.8:
            warnings.append(DeckWarning(
                WarningLevel.STRONG,
                f'Elixir average {avg_elixir:.1f} >= 4.8 - Too slow to cycle, vulnerable to fast decks.',
                'general'
            ))

        
        if not any(self.is_anti_tank(deck[i], deck_data[i]) for i in range(len(deck))):
            warnings.append(DeckWarning(
                WarningLevel.STRONG,
                'No anti-tank option - Cannot defend against heavy tanks (e.g., P.E.K.K.A, Golem).',
                'general'
            ))

        
        if not any(self.is_small_spell(card_data) for card_data in deck_data):
            warnings.append(DeckWarning(
                WarningLevel.WEAK,
                'No small spell (<= 3 Elixir) - Struggles with swarms and chip.',
                'general'
            ))

        if not any(self.is_big_spell(card_data) for card_data in deck_data):
            warnings.append(DeckWarning(
                WarningLevel.WEAK,
                'No big spell (> 3 Elixir) - Limited high spell damage and tower pressure.',
                'general'
            ))

        if not any(self.is_building(card_data) for card_data in deck_data):
            warnings.append(DeckWarning(
                WarningLevel.WEAK,
                'No building - Harder to defend and control tempo.',
                'general'
            ))

        air_defense_count = sum(1 for card_data in deck_data if self.can_hit_air(card_data))
        if air_defense_count == 1:
            warnings.append(DeckWarning(
                WarningLevel.WEAK,
                'Only 1 air defense card - Risky against air-heavy decks.',
                'general'
            ))

        if not any(self.is_reset_card(deck[i]) for i in range(len(deck))):
            warnings.append(DeckWarning(
                WarningLevel.WEAK,
                'No reset card (e.g., Zap, E-Wiz) - Vulnerable to Inferno Tower/Dragon, Sparky.',
                'general'
            ))

        if not any(self.is_tank_or_mini_tank(card_data) for card_data in deck_data):
            warnings.append(DeckWarning(
                WarningLevel.WEAK,
                'No tank or mini-tank - Difficulty absorbing damage for support troops.',
                'general'
            ))

        if not any(self.has_splash(deck[i]) for i in range(len(deck))):
            warnings.append(DeckWarning(
                WarningLevel.WEAK,
                'No splash damage - Struggles against swarm-heavy decks.',
                'general'
            ))

        if avg_elixir > 0 and avg_elixir <= 2.6:
            warnings.append(DeckWarning(
                WarningLevel.WEAK,
                f'Elixir average {avg_elixir:.1f} <= 2.6 - May lack defensive power against heavy pushes.',
                'general'
            ))

        if not any(self.is_cycle_card(card_data) for card_data in deck_data):
            warnings.append(DeckWarning(
                WarningLevel.WEAK,
                'No cheap cycle cards (1-2 elixir) - Slower cycle to win condition.',
                'general'
            ))

        return warnings

    def _check_archetype_warnings(self, deck: List[str], deck_data: List[Dict], archetype: str) -> List[DeckWarning]:
        
        if archetype == 'siege':
            return self._check_siege_warnings(deck, deck_data)
        elif archetype == 'cycle':
            return self._check_cycle_warnings(deck, deck_data)
        elif archetype == 'beatdown':
            return self._check_beatdown_warnings(deck, deck_data)
        elif archetype == 'bridge_spam':
            return self._check_bridge_spam_warnings(deck, deck_data)
        return []

    def _check_siege_warnings(self, deck: List[str], deck_data: List[Dict]) -> List[DeckWarning]:
        
        warnings = []

        if not any(self.is_building_killer_spell(deck[i], deck_data[i]) for i in range(len(deck))):
            warnings.append(DeckWarning(
                WarningLevel.STRONG,
                'No building killer spell - No heavy spell (Rocket, Lightning, Fireball, Poison) or Earthquake to damage defensive buildings.',
                'siege'
            ))

        building_count = sum(1 for card_data in deck_data if self.is_building(card_data))
        if building_count < 2:
            warnings.append(DeckWarning(
                WarningLevel.STRONG,
                'No secondary defensive building - Siege decks need a second building for defense.',
                'siege'
            ))

        if not any(self.is_anti_tank(deck[i], deck_data[i]) for i in range(len(deck))):
            warnings.append(DeckWarning(
                WarningLevel.STRONG,
                'No anti-tank option - Vulnerable to P.E.K.K.A, Giant, etc.',
                'siege'
            ))

        avg_elixir = self.calculate_avg_elixir(deck_data)
        if avg_elixir > 3.8:
            warnings.append(DeckWarning(
                WarningLevel.WEAK,
                f'Average elixir {avg_elixir:.1f} > 3.8 - Too slow to defend and cycle your siege building.',
                'siege'
            ))

        cycle_count = sum(1 for card_data in deck_data if self.is_cycle_card(card_data))
        if cycle_count < 1:
            warnings.append(DeckWarning(
                WarningLevel.WEAK,
                '< 2 cycle cards (<= 2 Elixir) - Can\'t cycle back to your siege building fast enough.',
                'siege'
            ))

        return warnings

    def _check_cycle_warnings(self, deck: List[str], deck_data: List[Dict]) -> List[DeckWarning]:
        
        warnings = []

        if not any(self.is_building(card_data) for card_data in deck_data):
            warnings.append(DeckWarning(
                WarningLevel.STRONG,
                'No defensive building - Cycle decks rely on a building for solid defense.',
                'cycle'
            ))

        heavy_count = sum(1 for card_data in deck_data if card_data.get('elixir', 0) >= 4)
        if heavy_count > 3:
            warnings.append(DeckWarning(
                WarningLevel.STRONG,
                '> 3 cards cost 4+ elixir - Deck may be too heavy for a cycle archetype.',
                'cycle'
            ))

        cycle_count = sum(1 for card_data in deck_data if self.is_cycle_card(card_data))
        if cycle_count < 2:
            warnings.append(DeckWarning(
                WarningLevel.WEAK,
                '< 2 cycle cards (<= 2 Elixir) - Not fast enough for a true cycle deck.',
                'cycle'
            ))

        return warnings

    def _check_beatdown_warnings(self, deck: List[str], deck_data: List[Dict]) -> List[DeckWarning]:
        
        warnings = []

        avg_elixir = self.calculate_avg_elixir(deck_data)

        if avg_elixir > 0 and avg_elixir < 3.5:
            warnings.append(DeckWarning(
                WarningLevel.STRONG,
                f'Average elixir {avg_elixir:.1f} < 3.5 - Insufficient elixir for a proper beatdown push.',
                'beatdown'
            ))

        if not any(self.is_reset_card(deck[i]) for i in range(len(deck))):
            warnings.append(DeckWarning(
                WarningLevel.STRONG,
                'No reset units - Vulnerable to Inferno Tower/Dragon and Sparky.',
                'beatdown'
            ))

        spell_count = sum(1 for card_data in deck_data if self.is_spell(card_data))
        if spell_count > 2:
            warnings.append(DeckWarning(
                WarningLevel.WEAK,
                'More than 2 spells - Reduces push potential and defensive troops.',
                'beatdown'
            ))

        return warnings

    def _check_bridge_spam_warnings(self, deck: List[str], deck_data: List[Dict]) -> List[DeckWarning]:
        
        warnings = []

        avg_elixir = self.calculate_avg_elixir(deck_data)
        if avg_elixir > 4.3:
            warnings.append(DeckWarning(
                WarningLevel.STRONG,
                f'Average elixir {avg_elixir:.1f} > 4.3 - Too slow for consistent bridge spam pressure.',
                'bridge_spam'
            ))

        cycle_count = sum(1 for card_data in deck_data if self.is_cycle_card(card_data))
        if cycle_count < 2:
            warnings.append(DeckWarning(
                WarningLevel.STRONG,
                'No cycle cards (<= 2 Elixir) - Cannot cycle pressure cards fast enough.',
                'bridge_spam'
            ))

        spell_count = sum(1 for card_data in deck_data if self.is_spell(card_data))
        if spell_count >= 3:
            warnings.append(DeckWarning(
                WarningLevel.WEAK,
                '>= 3 spells - Not enough units to apply constant pressure.',
                'bridge_spam'
            ))

        return warnings

    def get_deck_synergies(self, deck: List[str]) -> Dict:

        synergies = {}
        for card in deck:
            query = f"""
            MATCH (c1:Card {{name: '{card}'}})-[s:SYNERGIZES_WITH]->(c2:Card)
            WHERE c2.name IN {deck}
            RETURN c2.name AS card, s.synergy_type AS synergy_type, s.strength AS strength
            """
            result = self.retriever.retrieve(query)
            if result.data:
                synergies[card] = result.data
        return synergies

    def get_deck_counters(self, deck: List[str]) -> Dict:

        all_counters = []
        for card in deck:
            query = f"""
            MATCH (c1:Card {{name: '{card}'}})-[ct:COUNTERS]->(c2:Card)
            RETURN c1.name AS from_card, c2.name AS counters, ct.reason AS reason
            LIMIT 3
            """
            result = self.retriever.retrieve(query)
            if result.data:
                all_counters.extend(result.data)
        return all_counters

    def format_analysis(self, analysis: Dict, synergies: Dict = None, counters: List = None) -> str:

        if 'error' in analysis:
            return f"Error: {analysis['error']}"

        result = "Deck Analysis\n"
        result += "=" * 50 + "\n\n"
        result += f"Cards: {', '.join(analysis['deck'])}\n"
        result += f"Archetype: {analysis['archetype']}\n"
        result += f"Average Elixir: {analysis['avg_elixir']}\n\n"

        if synergies:
            result += "Card Synergies:\n"
            result += "-" * 50 + "\n"
            synergy_found = False
            for card, synergy_list in synergies.items():
                if synergy_list:
                    synergy_found = True
                    result += f"  {card}:\n"
                    for syn in synergy_list:
                        result += f"    - {syn['card']} ({syn['synergy_type']}, strength: {syn['strength']})\n"
            if not synergy_found:
                result += "  No synergies found in knowledge graph\n"
            result += "\n"

        if counters:
            result += "What Your Deck Counters:\n"
            result += "-" * 50 + "\n"
            if counters:
                shown = set()
                for counter in counters[:5]:
                    key = (counter['from_card'], counter['counters'])
                    if key not in shown:
                        result += f"  {counter['from_card']} counters {counter['counters']}"
                        if counter.get('reason'):
                            result += f" ({counter['reason']})"
                        result += "\n"
                        shown.add(key)
            else:
                result += "  No counter data found in knowledge graph\n"
            result += "\n"

        result += "General Warnings:\n"
        result += "-" * 50 + "\n"
        if analysis['general_warnings']:
            for warning in analysis['general_warnings']:
                result += f"  [{warning.level.value}] {warning.message}\n"
        else:
            result += "  None\n"
        result += "\n"

        result += f"{analysis['archetype'].title()} Archetype Warnings:\n"
        result += "-" * 50 + "\n"
        if analysis['archetype_warnings']:
            for warning in analysis['archetype_warnings']:
                result += f"  [{warning.level.value}] {warning.message}\n"
        else:
            result += "  None\n"

        return result
