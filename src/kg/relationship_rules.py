from typing import Dict, List, Tuple
from src.domain.models import Card, CardType, TargetType, Transport

class RelationshipExtractor:
    @staticmethod
    def extract_counter_relationships(all_cards: List[Card]) -> List[Tuple[str, str, Dict]]:
        counters = []
        for card in all_cards:
            for target_card in all_cards:
                if card.name == target_card.name:
                    continue
                counter_info = RelationshipExtractor._evaluate_counter(card, target_card)
                if counter_info:
                    counters.append((card.name, target_card.name, counter_info))
        return counters

    @staticmethod
    def _evaluate_counter(card: Card, target: Card) -> Dict | None:
        if card.card_type == CardType.SPELL and card.damage:
            if hasattr(target, 'count') and isinstance(target.count, str) and 'x' in target.count:
                try:
                    count_val = int(target.count.replace('x', ''))
                    if count_val >= 3 and (target.hitpoints and target.hitpoints < 600):
                        return {"effectiveness": "hard-counter", "reason": "Spell clears swarm instantly"}
                except ValueError:
                    pass

        if target.transport == Transport.AIR:
            if TargetType.AIR in card.targets and card.dps:
                if card.dps > 150:
                    return {"effectiveness": "hard-counter", "reason": "High DPS anti-air unit"}
                else:
                    return {"effectiveness": "soft-counter", "reason": "Can target air units"}
            elif card.card_type == CardType.BUILDING and TargetType.AIR in card.targets:
                 return {"effectiveness": "distraction", "reason": "Defensive building pulls air unit"}

        if card.damage and target.hitpoints:
            if card.damage > 500 and target.hitpoints > 2500:
                return {"effectiveness": "hard-counter", "reason": "Tank killer melts high HP unit"}

        return None

    @staticmethod
    def extract_synergy_relationships(all_cards: List[Card]) -> List[Tuple[str, str, Dict]]:
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
        if (card1.hitpoints and card1.hitpoints > 2000) and card2.name == "Graveyard":
            return {"synergy_type": "tanking", "strength": "strong"}
        
        if card1.name == "Miner" and (card2.name in ["Poison", "Wall Breakers", "Bats"]):
            return {"synergy_type": "chip-cycle", "strength": "strong"}

        if (card1.name == "Tornado" and card2.card_type == CardType.TROOP):
            if getattr(card2, 'area_damage', False) or (card2.damage and "Area" in str(card2.description or "")):
                 return {"synergy_type": "control-combo", "strength": "strong"}

        return None

    @staticmethod
    def assign_archetypes(all_cards: List[Card]) -> Dict[str, List[Tuple[str, str]]]:
        assignments = {
            "Beatdown": [],
            "Cycle": [],
            "Control": [],
            "Siege": [],
            "Bait": [],
            "Bridge Spam": [],
            "Split Lane": []
        }

        beatdown_tanks = ["Golem", "Lava Hound", "Electro Giant", "Goblin Giant", "Elixir Golem", "Giant", "Royal Giant"]
        siege_cons = ["X-Bow", "Mortar"]
        bait_triggers = ["Goblin Barrel", "Skeleton Barrel", "Princess", "Dart Goblin", "Goblin Gang", "Skeleton Army", "Minion Horde"]
        bridgespam_cons = ["Battle Ram", "Ram Rider", "Royal Ghost", "Bandit", "Magic Archer", "P.E.K.K.A", "Dark Prince", "Prince"]
        control_cons = ["Graveyard", "Miner", "Balloon"]

        for card in all_cards:
            name = card.name
            
            if name in beatdown_tanks:
                assignments["Beatdown"].append((name, "main-tank"))
            elif name in ["Night Witch", "Baby Dragon", "Lightning", "Lumberjack", "Mega Minion", "Electro Dragon", "Flying Machine", "Heal Spirit"]:
                assignments["Beatdown"].append((name, "support"))

            if name in siege_cons:
                assignments["Siege"].append((name, "win-condition"))
            elif name in ["Tesla", "Archers", "Knight", "Log", "Rocket", "Ice Spirit", "Skeletons"]:
                assignments["Siege"].append((name, "defense"))

            if name in bait_triggers:
                assignments["Bait"].append((name, "bait-card"))
            elif name in ["Inferno Tower", "Rocket", "Valkyrie", "Knight", "Guards"]:
                assignments["Bait"].append((name, "defense"))

            if name in bridgespam_cons:
                assignments["Bridge Spam"].append((name, "pressure-unit"))
            elif name in ["Zap", "Poison", "Electro Wizard", "Battle Healer", "Mother Witch"]:
                assignments["Bridge Spam"].append((name, "support"))

            if card.elixir and card.elixir <= 2.6:
                assignments["Cycle"].append((name, "cycle-card"))
            if name in ["Hog Rider", "Miner", "Royal Hogs", "Goblin Drill", "Wall Breakers"]:
                assignments["Cycle"].append((name, "win-condition"))
            if name in ["Musketeer", "Cannon", "Ice Golem", "Fire Spirit"]:
                assignments["Cycle"].append((name, "defense"))

            if name in control_cons:
                assignments["Control"].append((name, "win-condition"))
            if name in ["Bowler", "Tornado", "Ice Wizard", "Baby Dragon", "Barbarian Barrel", "Zappies", "Tombstone", "Freeze", "Poison"]:
                assignments["Control"].append((name, "control-defense"))

            if name in ["Three Musketeers", "Royal Hogs", "Royal Recruits", "Elite Barbarians", "Flying Machine", "Zappies"]:
                assignments["Split Lane"].append((name, "split-push"))

        return assignments

KNOWN_COUNTERS = [
    ("Arrows", "Minion Horde", "hard", "Positive elixir trade, instant kill"),
    ("Arrows", "Goblin Barrel", "hard", "Prevents all damage"),
    ("Arrows", "Princess", "hard", "Kills and damages tower"),
    ("Arrows", "Firecracker", "hard", "One shots her"),
    ("Log", "Skeleton Army", "hard", "Positive elixir trade"),
    ("Log", "Goblin Barrel", "hard", "Prevents all damage"),
    ("Log", "Princess", "hard", "Positive elixir trade"),
    ("Log", "Tombstone", "hard", "Clears spawned skellies"),
    ("Zap", "Inferno Tower", "hard", "Resets damage ramp-up"),
    ("Zap", "Sparky", "hard", "Resets charge"),
    ("Zap", "Skeleton Army", "hard", "Instant clear"),
    ("Zap", "Bats", "hard", "Instant clear"),
    ("Lightning", "Inferno Tower", "hard", "Resets and destroys"),
    ("Lightning", "Archer Queen", "moderate", "High damage but negative trade"),
    ("Lightning", "Wizard", "hard", "Kills support troop"),
    ("Lightning", "Witch", "hard", "Kills support troop"),
    ("Rocket", "Sparky", "hard", "Complete destruction"),
    ("Rocket", "X-Bow", "hard", "Destroys win condition"),
    ("Rocket", "Balloon", "hard", "Complete destruction"),
    ("Rocket", "Executioner", "hard", "Kills support troop"),
    ("Fireball", "Three Musketeers", "hard", "Critical damage, value trade"),
    ("Fireball", "Minion Horde", "hard", "Instant kill"),
    ("Fireball", "Barbarians", "hard", "Leaves them critical"),
    ("Poison", "Graveyard", "hard", "Kills skeletons as they spawn"),
    ("Poison", "Furnace", "hard", "Denies spirits"),
    ("Poison", "Goblin Hut", "hard", "Denies spear goblins"),
    ("P.E.K.K.A", "Mega Knight", "hard", "High DPS shreds MK"),
    ("P.E.K.K.A", "Golem", "hard", "High DPS tank killer"),
    ("P.E.K.K.A", "Electro Giant", "hard", "High DPS tank killer"),
    ("P.E.K.K.A", "Giant", "hard", "High DPS tank killer"),
    ("Mini P.E.K.K.A", "Hog Rider", "hard", "Kills before extensive damage"),
    ("Mini P.E.K.K.A", "Giant", "hard", "Melts tank"),
    ("Hunter", "Balloon", "hard", "High damage at close range"),
    ("Hunter", "Hog Rider", "hard", "Two shots at close range"),
    ("Inferno Dragon", "P.E.K.K.A", "hard", "Melts high HP if distracted"),
    ("Inferno Dragon", "Golem", "hard", "Melts high HP"),
    ("Inferno Dragon", "Mega Knight", "hard", "Melts high HP"),
    ("Valkyrie", "Witch", "hard", "Splash kills skeletons and witch"),
    ("Valkyrie", "Skeleton Army", "hard", "Instant clear"),
    ("Valkyrie", "Graveyard", "moderate", "Clears skeletons if placed well"),
    ("Bowler", "Hog Rider", "hard", "Knockback prevents hits"),
    ("Bowler", "Battle Ram", "hard", "Knockback prevents connection"),
    ("Tornado", "Hog Rider", "hard", "Activates King Tower"),
    ("Tornado", "Goblin Barrel", "hard", "Activates King Tower"),
    ("Cannon", "Hog Rider", "hard", "Full counter with placement"),
    ("Tesla", "Balloon", "hard", "Kills balloon with pulling"),
    ("Tesla", "Hog Rider", "hard", "Pulls and kills"),
    ("Mother Witch", "Graveyard", "hard", "Turns skeletons into hogs"),
    ("Mother Witch", "Skeleton Army", "hard", "Spawns massive hog army"),
    ("Monk", "Rocket", "hard", "Reflects spell back"),
    ("Monk", "Sparky", "hard", "Reflects shot"),
    ("Little Prince", "Balloon", "moderate", "Ramp up damage"),
    ("Electro Giant", "Inferno Tower", "hard", "Reflect damage destroys it"),
    ("Royal Delivery", "Goblin Barrel", "hard", "Kills goblins on spawn"),
    ("Earthquake", "X-Bow", "hard", "Massive building damage"),
    ("Earthquake", "Tesla", "hard", "Massive building damage")
]

KNOWN_SYNERGIES = [
    ("Golem", "Night Witch", "tank-support", "strong"),
    ("Golem", "Baby Dragon", "tank-support", "strong"),
    ("Golem", "Lumberjack", "tank-support", "strong"),
    ("Golem", "Mega Minion", "tank-support", "moderate"),
    ("Golem", "Tornado", "control-combo", "strong"),
    ("Golem", "Lightning", "spell-support", "strong"),
    ("Golem", "Electro Dragon", "tank-support", "strong"),
    ("Night Witch", "Clone", "swarm-combo", "strong"),
    ("Lava Hound", "Balloon", "air-combo", "strong"),
    ("Lava Hound", "Inferno Dragon", "air-support", "strong"),
    ("Lava Hound", "Flying Machine", "air-support", "moderate"),
    ("Lava Hound", "Skeleton Dragons", "air-support", "moderate"),
    ("Lava Hound", "Miner", "tank-distraction", "strong"),
    ("Balloon", "Lumberjack", "rage-loon", "strong"),
    ("Balloon", "Freeze", "freeze-loon", "strong"),
    ("Balloon", "Miner", "distraction-combo", "strong"),
    ("Electro Giant", "Tornado", "pull-reflect", "strong"),
    ("Electro Giant", "Lightning", "reset-support", "strong"),
    ("Electro Giant", "Golden Knight", "dash-support", "moderate"),
    ("Giant", "Sparky", "tank-support", "strong"),
    ("Giant", "Prince", "giant-double-prince", "strong"),
    ("Giant", "Dark Prince", "giant-double-prince", "strong"),
    ("Giant", "Graveyard", "tank-yard", "strong"),
    ("Giant", "Witch", "classic-combo", "moderate"),
    ("Giant", "Mini P.E.K.K.A", "tank-support", "strong"),
    ("Sparky", "Tornado", "nado-sparky", "strong"),
    ("Sparky", "Goblin Giant", "green-sparky", "strong"),
    ("Hog Rider", "Ice Golem", "push-shield", "strong"),
    ("Hog Rider", "Ice Spirit", "freeze-push", "strong"),
    ("Hog Rider", "Earthquake", "building-killer", "strong"),
    ("Hog Rider", "Fireball", "building-killer", "moderate"),
    ("Hog Rider", "Musketeer", "trifecta", "moderate"),
    ("Hog Rider", "Valkyrie", "push-clear", "moderate"),
    ("Hog Rider", "Log", "spell-support", "strong"),
    ("Miner", "Wall Breakers", "speed-combo", "strong"),
    ("Miner", "Poison", "chip-control", "strong"),
    ("Miner", "Bats", "distraction-dps", "moderate"),
    ("Miner", "Mortar", "siege-chip", "strong"),
    ("Miner", "Skeleton Barrel", "bait-combo", "strong"),
    ("Wall Breakers", "Magic Archer", "geometry-chip", "moderate"),
    ("Goblin Barrel", "Princess", "bait-synergy", "strong"),
    ("Goblin Barrel", "Goblin Gang", "bait-synergy", "strong"),
    ("Goblin Barrel", "Rocket", "chip-finish", "moderate"),
    ("Goblin Barrel", "Inferno Tower", "defense-offense", "moderate"),
    ("Goblin Barrel", "Dart Goblin", "bait-synergy", "strong"),
    ("Princess", "Rocket", "defense-finish", "moderate"),
    ("Mighty Miner", "Goblin Barrel", "lane-pressure", "strong"),
    ("P.E.K.K.A", "Battle Ram", "pekka-bs", "strong"),
    ("Battle Ram", "Bandit", "pressure-combo", "strong"),
    ("Royal Ghost", "Bandit", "stealth-pressure", "strong"),
    ("Magic Archer", "Tornado", "geometry-nado", "strong"),
    ("Ram Rider", "Lumberjack", "speed-bridge", "strong"),
    ("X-Bow", "Tesla", "siege-defense", "strong"),
    ("X-Bow", "Archers", "siege-support", "strong"),
    ("X-Bow", "Ice Spirit", "cycle-defense", "moderate"),
    ("Mortar", "Skeleton King", "swarm-defense", "strong"),
    ("Mortar", "Miner", "hybrid-siege", "strong"),
    ("Graveyard", "Poison", "yard-poison", "strong"),
    ("Graveyard", "Freeze", "yard-freeze", "strong"),
    ("Graveyard", "Baby Dragon", "tank-splash", "strong"),
    ("Graveyard", "Ice Wizard", "defense-counter", "moderate"),
    ("Graveyard", "Knight", "tank-yard", "strong"),
    ("Graveyard", "Bowler", "control-yard", "strong"),
    ("Royal Giant", "Fisherman", "pull-support", "strong"),
    ("Royal Giant", "Hunter", "defense-support", "strong"),
    ("Royal Giant", "Mother Witch", "swarm-counter", "strong"),
    ("Royal Giant", "Lightning", "reset-break", "strong"),
    ("Fisherman", "Hunter", "pull-shoot", "strong"),
    ("Three Musketeers", "Royal Hogs", "split-bait", "strong"),
    ("Three Musketeers", "Elixir Collector", "pump-beatdown", "strong"),
    ("Three Musketeers", "Ice Golem", "kiting-tank", "strong"),
    ("Goblin Drill", "Bomber", "drill-cycle", "strong"),
    ("Goblin Drill", "Fire Spirit", "chip-support", "moderate"),
    ("Royal Recruits", "Royal Hogs", "fireball-bait", "strong"),
    ("Royal Recruits", "Flying Machine", "fireball-bait", "strong"),
    ("Lumberjack", "Ram Rider", "rage-bridge", "strong"),
    ("Skeleton King", "Tombstone", "soul-farming", "strong"),
    ("Executioner", "Tornado", "exe-nado", "strong"),
    ("Ice Wizard", "Tornado", "ice-nado", "strong")
]