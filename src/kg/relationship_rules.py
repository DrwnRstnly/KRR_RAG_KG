"""
Relationship rules for inferring counters and synergies

Based on Clash Royale game mechanics and the original Prolog rules
"""

from typing import Dict, List, Tuple
from src.domain.models import Card, CardType, TargetType, Transport


class RelationshipExtractor:
    """Extracts relationships between cards based on game mechanics"""

    @staticmethod
    def extract_counter_relationships(all_cards: List[Card]) -> List[Tuple[str, str, Dict]]:
        """
        Extract COUNTERS relationships
        Returns: List of (from_card, to_card, properties)
        """
        counters = []
        card_map = {card.name: card for card in all_cards}

        for card in all_cards:
            # Find cards this card counters
            for target_card in all_cards:
                if card.name == target_card.name:
                    continue

                counter_info = RelationshipExtractor._evaluate_counter(card, target_card)
                if counter_info:
                    counters.append((card.name, target_card.name, counter_info))

        return counters

    @staticmethod
    def _evaluate_counter(card: Card, target: Card) -> Dict | None:
        """Evaluate if card counters target, return properties if true"""

        if card.card_type == CardType.SPELL and card.damage:
            if hasattr(target, 'count') or (target.hitpoints and target.hitpoints < 500):
                return {
                    "effectiveness": "strong",
                    "reason": "Spell damage effective against low HP units"
                }

        if target.transport == Transport.AIR:
            if TargetType.AIR in card.targets and card.dps:
                if card.dps > 150:
                    return {
                        "effectiveness": "strong",
                        "reason": "High DPS anti-air unit"
                    }
                else:
                    return {
                        "effectiveness": "moderate",
                        "reason": "Can target air units"
                    }

        if card.card_type == CardType.BUILDING:
            if TargetType.BUILDINGS in target.targets:
                return {
                    "effectiveness": "moderate",
                    "reason": "Distracts building-targeting units"
                }

        if card.damage and target.hitpoints:
            if card.damage > 500 and target.hitpoints > 2000:
                return {
                    "effectiveness": "strong",
                    "reason": "High damage effective against tanks"
                }


        return None

    @staticmethod
    def extract_synergy_relationships(all_cards: List[Card]) -> List[Tuple[str, str, Dict]]:
        """
        Extract SYNERGIZES_WITH relationships
        Returns: List of (card1, card2, properties)
        """
        synergies = []

        for i, card1 in enumerate(all_cards):
            for card2 in all_cards[i + 1:]:
                synergy_info = RelationshipExtractor._evaluate_synergy(card1, card2)
                if synergy_info:
                    synergies.append((card1.name, card2.name, synergy_info))
                    synergies.append((card2.name, card1.name, synergy_info))

        return synergies

    @staticmethod
    def _evaluate_synergy(card1: Card, card2: Card) -> Dict | None:
        """Evaluate synergy between two cards"""

        # Tank + Support synergy
        if card1.hitpoints and card2.damage:
            if card1.hitpoints > 2000 and card2.hitpoints and card2.hitpoints < 1000:
                if card2.transport == Transport.GROUND or card2.card_type == CardType.TROOP:
                    return {
                        "synergy_type": "tank-support",
                        "strength": "strong"
                    }

        # Spell + Swarm bait synergy
        if card1.card_type == CardType.SPELL and card2.hitpoints:
            if card2.hitpoints < 500:
                return {
                    "synergy_type": "spell-bait",
                    "strength": "moderate"
                }

        # Building-targeting + Tank synergy
        if TargetType.BUILDINGS in card1.targets and card2.hitpoints:
            if card2.hitpoints > 2000:
                return {
                    "synergy_type": "push-combo",
                    "strength": "strong"
                }

        return None

    @staticmethod
    def assign_archetypes(all_cards: List[Card]) -> Dict[str, List[Tuple[str, str]]]:
        """
        Assign cards to archetypes with roles
        Returns: Dict[archetype_name -> List[(card_name, role)]]
        """
        archetype_assignments = {
            "Beatdown": [],
            "Cycle": [],
            "Control": [],
            "Siege": [],
            "Bait": [],
            "Bridge Spam": []
        }

        for card in all_cards:
            # Beatdown: Heavy tanks and support
            if card.hitpoints and card.hitpoints > 3000:
                archetype_assignments["Beatdown"].append((card.name, "tank"))
            elif card.elixir >= 5 and card.hitpoints and card.hitpoints > 1500:
                archetype_assignments["Beatdown"].append((card.name, "support"))

            # Cycle: Low elixir cards
            if card.elixir <= 2:
                archetype_assignments["Cycle"].append((card.name, "cycle"))
            elif card.elixir <= 4 and TargetType.BUILDINGS in card.targets:
                archetype_assignments["Cycle"].append((card.name, "win-condition"))

            # Control: Buildings and spells
            if card.card_type == CardType.BUILDING:
                archetype_assignments["Control"].append((card.name, "defense"))
            elif card.card_type == CardType.SPELL and card.elixir >= 4:
                archetype_assignments["Control"].append((card.name, "spell"))

            # Siege: X-Bow, Mortar
            if card.name.lower() in ["x-bow", "mortar"]:
                archetype_assignments["Siege"].append((card.name, "win-condition"))
            elif card.card_type == CardType.BUILDING:
                archetype_assignments["Siege"].append((card.name, "defense"))

            # Bait: Low HP cards
            if card.hitpoints and card.hitpoints < 500 and card.elixir <= 4:
                archetype_assignments["Bait"].append((card.name, "bait-unit"))

            # Bridge Spam: Fast-paced pressure cards
            if card.elixir <= 5 and (
                TargetType.BUILDINGS in card.targets or
                (card.damage and card.damage > 200)
            ):
                archetype_assignments["Bridge Spam"].append((card.name, "pressure"))

        return archetype_assignments


# Define known strong counters from Clash Royale meta knowledge
KNOWN_COUNTERS = [
    # (counter_card, target_card, effectiveness, reason)
    ("Arrows", "Minion Horde", "strong", "One-shots minions"),
    ("Fireball", "Three Musketeers", "strong", "Massive value against clustered musketeers"),
    ("Lightning", "Sparky", "strong", "Resets and damages Sparky"),
    ("Zap", "Inferno Tower", "strong", "Resets inferno damage"),
    ("Skarmy", "P.E.K.K.A", "strong", "Surrounds and overwhelms single-target unit"),
    ("Valkyrie", "Skeleton Army", "strong", "Splash damage clears swarm"),
    ("Bats", "Mega Knight", "moderate", "Air units avoid splash"),
    ("Mini P.E.K.K.A", "Giant", "strong", "High damage melts tanks"),
    ("Inferno Dragon", "Golem", "strong", "Ramping damage against high HP"),
]

# Define known synergies from meta decks
KNOWN_SYNERGIES = [
    # (card1, card2, synergy_type, strength)
    ("Giant", "Musketeer", "tank-support", "strong"),
    ("Golem", "Night Witch", "tank-support", "strong"),
    ("Hog Rider", "Fireball", "push-spell", "strong"),
    ("Goblin Barrel", "Princess", "spell-bait", "strong"),
    ("X-Bow", "Tesla", "siege-defense", "strong"),
    ("Balloon", "Lumberjack", "push-combo", "strong"),
    ("Miner", "Poison", "chip-control", "strong"),
    ("Royal Giant", "Fisherman", "pull-combo", "moderate"),
]
