"""
Enhanced Knowledge Graph Schema for Clash Royale

This module defines the schema with nodes and relationships
optimized for RAG queries.

Nodes:
- Card: Individual cards with stats
- Rarity: Card rarity (Common, Rare, Epic, Legendary, Champion)
- Arena: Unlock arenas
- Target: What the card can hit (ground, air, buildings)
- Archetype: Deck archetypes (Beatdown, Control, Cycle, etc.)
- Type: Card types (Troop, Spell, Building)

Relationships:
- (Card)-[:HAS_RARITY]->(Rarity)
- (Card)-[:UNLOCKS_IN]->(Arena)
- (Card)-[:CAN_HIT]->(Target)
- (Card)-[:HAS_TYPE]->(Type)
- (Card)-[:COUNTERS]->(Card)  # Strategic counters
- (Card)-[:SYNERGIZES_WITH]->(Card)  # Works well with
- (Card)-[:FITS_ARCHETYPE]->(Archetype)  # Deck archetype fit
"""

from typing import Dict, List, Any
from dataclasses import dataclass


@dataclass
class NodeSchema:
    """Schema definition for a node type"""
    label: str
    properties: Dict[str, str]  # property_name -> property_type
    description: str


@dataclass
class RelationshipSchema:
    """Schema definition for a relationship type"""
    type: str
    from_label: str
    to_label: str
    properties: Dict[str, str]
    description: str


class KGSchema:
    """Clash Royale Knowledge Graph Schema"""

    NODES = {
        "Card": NodeSchema(
            label="Card",
            properties={
                "name": "string",
                "elixir": "integer",
                "type": "string",
                "rarity": "string",
                "arena": "string",
                "transport": "string",  # ground, air, or null
                "hitpoints": "integer",
                "damage": "integer",
                "dps": "integer",
                "description": "string",
                "level11_stats": "string",  # JSON string containing detailed stats. For champions, includes ability information with format "stat_name (with Ability Name)": "value"
            },
            description="Individual Clash Royale cards with stats. Champions (rarity='champion') have special abilities that enhance their stats when activated."
        ),
        "Rarity": NodeSchema(
            label="Rarity",
            properties={
                "name": "string",  # Common, Rare, Epic, Legendary, Champion
                "color": "string",
            },
            description="Card rarity levels"
        ),
        "Arena": NodeSchema(
            label="Arena",
            properties={
                "name": "string",
                "number": "integer",
                "trophy_requirement": "integer",
            },
            description="Arena unlock requirements"
        ),
        "Target": NodeSchema(
            label="Target",
            properties={
                "name": "string",  # ground, air, buildings
            },
            description="Valid targets for cards"
        ),
        "Archetype": NodeSchema(
            label="Archetype",
            properties={
                "name": "string",  # Beatdown, Cycle, Bait, Siege, etc.
                "description": "string",
                "avg_elixir_range": "string",  # e.g., "2.8-3.2"
            },
            description="Deck archetype classifications"
        ),
        "Type": NodeSchema(
            label="Type",
            properties={
                "name": "string",  # Troop, Spell, Building
            },
            description="Card type categories"
        ),
    }

    RELATIONSHIPS = {
        "HAS_RARITY": RelationshipSchema(
            type="HAS_RARITY",
            from_label="Card",
            to_label="Rarity",
            properties={},
            description="Card belongs to a rarity tier"
        ),
        "UNLOCKS_IN": RelationshipSchema(
            type="UNLOCKS_IN",
            from_label="Card",
            to_label="Arena",
            properties={},
            description="Card unlocks in specific arena"
        ),
        "CAN_HIT": RelationshipSchema(
            type="CAN_HIT",
            from_label="Card",
            to_label="Target",
            properties={},
            description="Card can target specific unit types"
        ),
        "HAS_TYPE": RelationshipSchema(
            type="HAS_TYPE",
            from_label="Card",
            to_label="Type",
            properties={},
            description="Card belongs to a type"
        ),
        "COUNTERS": RelationshipSchema(
            type="COUNTERS",
            from_label="Card",
            to_label="Card",
            properties={
                "effectiveness": "string",  # weak, moderate, strong
                "reason": "string",
            },
            description="Card A is effective against Card B"
        ),
        "SYNERGIZES_WITH": RelationshipSchema(
            type="SYNERGIZES_WITH",
            from_label="Card",
            to_label="Card",
            properties={
                "synergy_type": "string",  # tank-support, spell-bait, etc.
                "strength": "string",  # weak, moderate, strong
            },
            description="Card A works well with Card B"
        ),
        "FITS_ARCHETYPE": RelationshipSchema(
            type="FITS_ARCHETYPE",
            from_label="Card",
            to_label="Archetype",
            properties={
                "role": "string",  # win-condition, support, defense, spell
            },
            description="Card fits into deck archetype"
        ),
    }

    @classmethod
    def get_schema_description(cls) -> str:
        """Get a formatted schema description for LLM prompts"""
        schema_desc = "# Clash Royale Knowledge Graph Schema\n\n"

        schema_desc += "## Node Types\n"
        for node_name, node in cls.NODES.items():
            schema_desc += f"\n### {node_name}\n"
            schema_desc += f"{node.description}\n"
            schema_desc += "Properties:\n"
            for prop_name, prop_type in node.properties.items():
                schema_desc += f"  - {prop_name}: {prop_type}\n"

        schema_desc += "\n## Relationship Types\n"
        for rel_name, rel in cls.RELATIONSHIPS.items():
            schema_desc += f"\n### :{rel_name}\n"
            schema_desc += f"{rel.description}\n"
            schema_desc += f"Pattern: (:{rel.from_label})-[:{rel.type}]->(:{rel.to_label})\n"
            if rel.properties:
                schema_desc += "Properties:\n"
                for prop_name, prop_type in rel.properties.items():
                    schema_desc += f"  - {prop_name}: {prop_type}\n"

        return schema_desc

    @classmethod
    def get_cypher_examples(cls) -> List[Dict[str, str]]:
        """Get example Cypher queries for different question types"""
        return [
            {
                "question": "What is the elixir cost of the Giant?",
                "cypher": "MATCH (c:Card {name: 'Giant'}) RETURN c.name AS card, c.elixir AS cost"
            },
            {
                "question": "Which cards can hit air units?",
                "cypher": "MATCH (c:Card)-[:CAN_HIT]->(:Target {name: 'air'}) RETURN c.name AS card ORDER BY c.name"
            },
            {
                "question": "What are all Legendary cards?",
                "cypher": "MATCH (c:Card)-[:HAS_RARITY]->(:Rarity {name: 'legendary'}) RETURN c.name AS card ORDER BY c.elixir"
            },
            {
                "question": "Which cards counter P.E.K.K.A?",
                "cypher": "MATCH (c:Card)-[r:COUNTERS]->(target:Card {name: 'P.E.K.K.A'}) RETURN c.name AS card, r.effectiveness AS effectiveness, r.reason AS reason"
            },
            {
                "question": "What cards synergize well with Giant?",
                "cypher": "MATCH (giant:Card {name: 'Giant'})-[s:SYNERGIZES_WITH]->(c:Card) RETURN c.name AS card, s.synergy_type AS synergy, s.strength AS strength"
            },
            {
                "question": "Which cards fit the Beatdown archetype?",
                "cypher": "MATCH (c:Card)-[f:FITS_ARCHETYPE]->(:Archetype {name: 'Beatdown'}) RETURN c.name AS card, f.role AS role ORDER BY c.elixir DESC"
            },
            {
                "question": "Compare the stats of Musketeer and Wizard",
                "cypher": "MATCH (c:Card) WHERE c.name IN ['Musketeer', 'Wizard'] RETURN c.name AS card, c.elixir AS cost, c.hitpoints AS hp, c.damage AS damage, c.dps AS dps"
            },
            {
                "question": "What are the cheapest spell cards?",
                "cypher": "MATCH (c:Card)-[:HAS_TYPE]->(:Type {name: 'spell'}) RETURN c.name AS card, c.elixir AS cost ORDER BY c.elixir LIMIT 5"
            },
            {
                "question": "Tell me about the Archer Queen and her ability",
                "cypher": "MATCH (c:Card {name: 'Archer Queen'}) RETURN c.name AS card, c.elixir AS cost, c.hitpoints AS hp, c.damage AS damage, c.dps AS dps, c.level11_stats AS stats, c.rarity AS rarity"
            },
            {
                "question": "What are all the champion cards?",
                "cypher": "MATCH (c:Card)-[:HAS_RARITY]->(:Rarity {name: 'champion'}) RETURN c.name AS card, c.elixir AS cost, c.level11_stats AS stats ORDER BY c.elixir"
            },
        ]
