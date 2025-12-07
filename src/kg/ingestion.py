import json
import re
import os
from typing import Dict, List, Any, Optional
from neo4j import GraphDatabase
from dotenv import load_dotenv

from src.domain.models import Card, CardType, Rarity, TargetType, Transport
from src.kg.relationship_rules import RelationshipExtractor, KNOWN_COUNTERS, KNOWN_SYNERGIES

load_dotenv()


class KnowledgeGraphIngestion:

    def __init__(self, uri: str = None, user: str = None, password: str = None):
        self.uri = uri or os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.user = user or os.getenv("NEO4J_USER", "neo4j")
        self.password = password or os.getenv("NEO4J_PASSWORD", "12345678")
        self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))

    def close(self):
        """Close database connection"""
        self.driver.close()

    def clear_database(self):
        """Clear all nodes and relationships - USE WITH CAUTION"""
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
            print("Database cleared")

    def create_constraints(self):
        """Create uniqueness constraints"""
        constraints = [
            "CREATE CONSTRAINT card_name IF NOT EXISTS FOR (c:Card) REQUIRE c.name IS UNIQUE",
            "CREATE CONSTRAINT rarity_name IF NOT EXISTS FOR (r:Rarity) REQUIRE r.name IS UNIQUE",
            "CREATE CONSTRAINT arena_name IF NOT EXISTS FOR (a:Arena) REQUIRE a.name IS UNIQUE",
            "CREATE CONSTRAINT target_name IF NOT EXISTS FOR (t:Target) REQUIRE t.name IS UNIQUE",
            "CREATE CONSTRAINT type_name IF NOT EXISTS FOR (ty:Type) REQUIRE ty.name IS UNIQUE",
            "CREATE CONSTRAINT archetype_name IF NOT EXISTS FOR (ar:Archetype) REQUIRE ar.name IS UNIQUE",
        ]

        with self.driver.session() as session:
            for constraint in constraints:
                try:
                    session.run(constraint)
                    print(f"Created constraint: {constraint.split('FOR')[1].split('REQUIRE')[0].strip()}")
                except Exception as e:
                    print(f"Constraint may already exist: {e}")

    def ingest_card(self, card: Card) -> str:
        """Ingest a single card with all its properties"""
        cypher = """
        MERGE (c:Card {name: $name})
        SET c.elixir = $elixir,
            c.type = $type,
            c.rarity = $rarity,
            c.arena = $arena,
            c.transport = $transport,
            c.hitpoints = $hitpoints,
            c.damage = $damage,
            c.dps = $dps,
            c.description = $description,
            c.level11_stats = $level11_stats

        // Create Rarity node and relationship
        MERGE (r:Rarity {name: $rarity})
        MERGE (c)-[:HAS_RARITY]->(r)

        // Create Arena node and relationship
        MERGE (a:Arena {name: $arena})
        MERGE (c)-[:UNLOCKS_IN]->(a)

        // Create Type node and relationship
        MERGE (ty:Type {name: $type})
        MERGE (c)-[:HAS_TYPE]->(ty)

        // Create Target relationships
        WITH c, $targets AS target_list
        UNWIND target_list AS target_name
            MERGE (t:Target {name: target_name})
            MERGE (c)-[:CAN_HIT]->(t)

        RETURN c.name AS inserted
        """

        params = {
            "name": card.name,
            "elixir": card.elixir,
            "type": card.card_type.value if isinstance(card.card_type, CardType) else card.card_type,
            "rarity": card.rarity.value if isinstance(card.rarity, Rarity) else card.rarity,
            "arena": card.arena,
            "transport": card.transport.value if card.transport else None,
            "hitpoints": card.hitpoints,
            "damage": card.damage,
            "dps": card.dps,
            "description": card.description,
            "level11_stats": json.dumps(card.level11_stats),
            "targets": [t.value if isinstance(t, TargetType) else t for t in card.targets]
        }

        with self.driver.session() as session:
            result = session.run(cypher, params)
            return result.single()["inserted"]

    def ingest_counter_relationship(self, from_card: str, to_card: str, properties: Dict):
        """Create a COUNTERS relationship"""
        cypher = """
        MATCH (from:Card {name: $from_card})
        MATCH (to:Card {name: $to_card})
        MERGE (from)-[r:COUNTERS]->(to)
        SET r.effectiveness = $effectiveness,
            r.reason = $reason
        RETURN from.name AS from, to.name AS to
        """

        params = {
            "from_card": from_card,
            "to_card": to_card,
            "effectiveness": properties.get("effectiveness", "moderate"),
            "reason": properties.get("reason", "")
        }

        with self.driver.session() as session:
            try:
                session.run(cypher, params)
                return True
            except Exception as e:
                print(f"Error creating counter relationship {from_card} -> {to_card}: {e}")
                return False

    def ingest_synergy_relationship(self, card1: str, card2: str, properties: Dict):
        """Create a SYNERGIZES_WITH relationship"""
        cypher = """
        MATCH (c1:Card {name: $card1})
        MATCH (c2:Card {name: $card2})
        MERGE (c1)-[r:SYNERGIZES_WITH]->(c2)
        SET r.synergy_type = $synergy_type,
            r.strength = $strength
        RETURN c1.name AS card1, c2.name AS card2
        """

        params = {
            "card1": card1,
            "card2": card2,
            "synergy_type": properties.get("synergy_type", "unknown"),
            "strength": properties.get("strength", "moderate")
        }

        with self.driver.session() as session:
            try:
                session.run(cypher, params)
                return True
            except Exception as e:
                print(f"Error creating synergy relationship {card1} <-> {card2}: {e}")
                return False

    def ingest_archetype_relationship(self, card_name: str, archetype_name: str, role: str):
        """Create FITS_ARCHETYPE relationship"""
        cypher = """
        MATCH (c:Card {name: $card_name})
        MERGE (a:Archetype {name: $archetype_name})
        MERGE (c)-[r:FITS_ARCHETYPE]->(a)
        SET r.role = $role
        RETURN c.name AS card, a.name AS archetype
        """

        params = {
            "card_name": card_name,
            "archetype_name": archetype_name,
            "role": role
        }

        with self.driver.session() as session:
            try:
                session.run(cypher, params)
                return True
            except Exception as e:
                print(f"Error creating archetype relationship {card_name} -> {archetype_name}: {e}")
                return False

    def ingest_all_from_json(self, json_path: str):
        """
        Ingest all cards from JSON file and create relationships
        """
        print(f"Loading dataset from {json_path}...")
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Phase 1: Ingest all cards
        print("\n=== Phase 1: Ingesting Cards ===")
        all_cards = []
        for arena_key, arena_data in data.items():
            arena_name = arena_data.get("arena_name", arena_key)
            print(f"\nArena: {arena_name}")

            for card_data in arena_data.get("cards", []):
                try:
                    card = self._convert_json_to_card(card_data, arena_name)
                    all_cards.append(card)
                    inserted = self.ingest_card(card)
                    print(f"  [OK] {inserted}")
                except Exception as e:
                    print(f"  [ERR] Error ingesting {card_data.get('name', 'unknown')}: {e}")

        # Phase 2: Extract and ingest relationships
        print("\n=== Phase 2: Creating Relationships ===")

        # Counter relationships
        print("\n--- Counter Relationships ---")
        counter_rels = RelationshipExtractor.extract_counter_relationships(all_cards)
        for from_card, to_card, props in counter_rels[:50]:  # Limit to avoid too many
            if self.ingest_counter_relationship(from_card, to_card, props):
                print(f"  [OK] {from_card} COUNTERS {to_card} ({props['effectiveness']})")

        # Known counters from meta knowledge
        for counter, target, eff, reason in KNOWN_COUNTERS:
            props = {"effectiveness": eff, "reason": reason}
            if self.ingest_counter_relationship(counter, target, props):
                print(f"  [OK] {counter} COUNTERS {target} (known)")

        # Synergy relationships
        print("\n--- Synergy Relationships ---")
        synergy_rels = RelationshipExtractor.extract_synergy_relationships(all_cards)
        for card1, card2, props in synergy_rels[:50]:  # Limit to avoid too many
            if self.ingest_synergy_relationship(card1, card2, props):
                print(f"  [OK] {card1} SYNERGIZES_WITH {card2} ({props['synergy_type']})")

        # Known synergies from meta decks
        for c1, c2, syn_type, strength in KNOWN_SYNERGIES:
            props = {"synergy_type": syn_type, "strength": strength}
            if self.ingest_synergy_relationship(c1, c2, props):
                print(f"  [OK] {c1} SYNERGIZES_WITH {c2} (known)")

        # Archetype assignments
        print("\n--- Archetype Assignments ---")
        archetype_assignments = RelationshipExtractor.assign_archetypes(all_cards)
        for archetype_name, card_roles in archetype_assignments.items():
            for card_name, role in card_roles[:10]:  # Limit per archetype
                if self.ingest_archetype_relationship(card_name, archetype_name, role):
                    print(f"  [OK] {card_name} FITS_ARCHETYPE {archetype_name} as {role}")

        print("\n=== Ingestion Complete ===")
        print(f"Total cards ingested: {len(all_cards)}")

    def _convert_json_to_card(self, card_data: Dict, arena_name: str) -> Card:
        """Convert JSON card data to Card domain model"""
        hp, dmg, dps = self._extract_combat_stats(card_data)

        targets = self._extract_targets(card_data)

        transport = None
        transport_str = card_data.get("transport")
        if transport_str:
            try:
                transport = Transport(transport_str.lower())
            except ValueError:
                pass

        card_type_str = card_data.get("type", "troop").lower()
        try:
            card_type = CardType(card_type_str)
        except ValueError:
            card_type = CardType.TROOP

        rarity_str = card_data.get("rarity", "common").lower()
        try:
            rarity = Rarity(rarity_str)
        except ValueError:
            rarity = Rarity.COMMON

        return Card(
            name=card_data.get("name", "Unknown"),
            elixir=card_data.get("elixir", 0),
            card_type=card_type,
            rarity=rarity,
            arena=arena_name,
            hitpoints=hp,
            damage=dmg,
            dps=dps,
            transport=transport,
            targets=targets,
            description=card_data.get("description", ""),
            level11_stats=card_data.get("level_11_stats", {})
        )

    @staticmethod
    def _extract_combat_stats(card_data: Dict) -> tuple[Optional[int], Optional[int], Optional[int]]:
        """Extract HP, damage, DPS from card stats"""
        stats = card_data.get("level_11_stats", {})
        name = card_data.get("name", "")

        def to_number(value):
            if value is None:
                return None
            s = str(value).strip()
            m = re.search(r"^([\d,\.]+)", s)
            if not m:
                return None
            s = m.group(1).replace(",", "")
            try:
                return int(float(s))
            except:
                return None

        def find_stat(stats_dict, key):
            if not stats_dict:
                return None
            key_lower = key.lower()
            for k, v in stats_dict.items():
                if k.lower() == key_lower:
                    return v
            return None

        # HP
        hp_val = find_stat(stats, "Hitpoints") or find_stat(stats, f"{name} Hitpoints")
        hp = to_number(hp_val)

        # Damage
        dmg_val = (
            find_stat(stats, "Damage") or
            find_stat(stats, "Area Damage") or
            find_stat(stats, f"{name} Damage")
        )
        dmg = to_number(dmg_val)

        # DPS
        dps_val = find_stat(stats, "Damage per second") or find_stat(stats, f"{name} Damage per second")
        dps = to_number(dps_val)

        return hp, dmg, dps

    @staticmethod
    def _extract_targets(card_data: Dict) -> List[TargetType]:
        """Extract target types from card data"""
        attrs = card_data.get("unit_attributes", {})
        target_str = attrs.get("Targets") or attrs.get("Target") or ""

        targets = []
        target_str_lower = target_str.lower()

        if "ground" in target_str_lower:
            targets.append(TargetType.GROUND)
        if "air" in target_str_lower:
            targets.append(TargetType.AIR)
        if "building" in target_str_lower:
            targets.append(TargetType.BUILDINGS)

        if not targets:
            targets.append(TargetType.GROUND)

        return targets


def main():
    """Main ingestion script"""
    ingestion = KnowledgeGraphIngestion()

    # Create constraints first
    ingestion.create_constraints()

    # Optionally clear database (uncomment if needed)
    # ingestion.clear_database()

    # Ingest from JSON
    json_path = "data/raw/fandom_arenas_cards.json"
    ingestion.ingest_all_from_json(json_path)

    ingestion.close()
    print("\n✓ Ingestion completed successfully!")


if __name__ == "__main__":
    main()
