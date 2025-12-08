

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from enum import Enum


class CardType(Enum):
    
    TROOP = "troop"
    SPELL = "spell"
    BUILDING = "building"


class Rarity(Enum):
    
    COMMON = "common"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"
    CHAMPION = "champion"


class TargetType(Enum):
    
    GROUND = "ground"
    AIR = "air"
    BUILDINGS = "buildings"


class Transport(Enum):
    
    GROUND = "ground"
    AIR = "air"


class Archetype(Enum):
    
    BEATDOWN = "beatdown"
    CYCLE = "cycle"
    CONTROL = "control"
    SIEGE = "siege"
    BAIT = "bait"
    BRIDGE_SPAM = "bridge_spam"


@dataclass
class Card:
    
    name: str
    elixir: int
    card_type: CardType
    rarity: Rarity
    arena: str

    
    hitpoints: Optional[int] = None
    damage: Optional[int] = None
    dps: Optional[int] = None

    
    transport: Optional[Transport] = None
    targets: List[TargetType] = field(default_factory=list)
    description: Optional[str] = None

    
    level11_stats: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        
        if self.elixir < 0 or self.elixir > 10:
            raise ValueError(f"Invalid elixir cost: {self.elixir}")

    def to_dict(self) -> Dict[str, Any]:
        
        return {
            "name": self.name,
            "elixir": self.elixir,
            "type": self.card_type.value if isinstance(self.card_type, CardType) else self.card_type,
            "rarity": self.rarity.value if isinstance(self.rarity, Rarity) else self.rarity,
            "arena": self.arena,
            "hitpoints": self.hitpoints,
            "damage": self.damage,
            "dps": self.dps,
            "transport": self.transport.value if self.transport else None,
            "targets": [t.value if isinstance(t, TargetType) else t for t in self.targets],
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Card":
        
        card_type = CardType(data.get("type", "troop"))
        rarity = Rarity(data.get("rarity", "common"))

        transport = None
        if data.get("transport"):
            transport = Transport(data["transport"])

        targets = []
        for t in data.get("targets", []):
            if isinstance(t, str):
                try:
                    targets.append(TargetType(t))
                except ValueError:
                    pass
            else:
                targets.append(t)

        return cls(
            name=data["name"],
            elixir=data.get("elixir", 0),
            card_type=card_type,
            rarity=rarity,
            arena=data.get("arena", "unknown"),
            hitpoints=data.get("hitpoints"),
            damage=data.get("damage"),
            dps=data.get("dps"),
            transport=transport,
            targets=targets,
            description=data.get("description"),
            level11_stats=data.get("level11_stats", {}),
        )


@dataclass
class CardRelationship:
    
    from_card: str
    to_card: str
    relationship_type: str  
    properties: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Deck:
    
    cards: List[str]  
    name: Optional[str] = None
    archetype: Optional[Archetype] = None

    def __post_init__(self):
        
        if len(self.cards) != 8:
            raise ValueError(f"Deck must contain exactly 8 cards, got {len(self.cards)}")

    def average_elixir(self, card_elixir_map: Dict[str, int]) -> float:
        
        total = sum(card_elixir_map.get(card, 0) for card in self.cards)
        return total / 8.0


@dataclass
class QueryResult:
    
    data: List[Dict[str, Any]]
    cypher_query: str
    execution_time: float
    error: Optional[str] = None


@dataclass
class RAGResponse:
    
    question: str
    answer: str
    cypher_query: str
    retrieved_data: List[Dict[str, Any]]
    sources: List[str] = field(default_factory=list)
    confidence: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        
        return {
            "question": self.question,
            "answer": self.answer,
            "cypher_query": self.cypher_query,
            "retrieved_data": self.retrieved_data,
            "sources": self.sources,
            "confidence": self.confidence,
        }
