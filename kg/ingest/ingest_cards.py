import json
import re
import os
from neo4j import GraphDatabase

def to_number_maybe(x):
    if x is None:
        return None
    s = str(x).strip()
    m = re.search(r"^([\d,\.]+)", s)
    if not m:
        return None
    s = m.group(1).replace(",", "")
    try:
        return int(float(s))
    except:
        return None

def find_stat_case_insensitive(stats_dict, key):
    if not stats_dict:
        return None
    key_lower = key.lower()
    for k, v in stats_dict.items():
        if k.lower() == key_lower:
            return v
    return None

def extract_targets(card):
    attrs = card.get("unit_attributes", {})
    t = attrs.get("Targets") or attrs.get("Target")

    if t:
        t = t.lower()
        if "ground" in t and "air" in t:
            return ["ground", "air"]
        if "ground" in t:
            return ["ground"]
        if "air" in t:
            return ["air"]
        if "building" in t:
            return ["buildings"]

    return ["ground"]

def extract_combat_stats(card):
    stats = card.get("level_11_stats", {})
    name = card.get("name", "")
    ctype = card.get("type", "").lower()

    hp_val = dmg_val = dps_val = None
    hp_num = dmg_num = dps_num = None

    hp_val = find_stat_case_insensitive(stats, "Hitpoints")
    if not hp_val:
        hp_val = find_stat_case_insensitive(stats, f"{name} Hitpoints")
    hp_num = to_number_maybe(hp_val)

    tough_units = ["Inferno Dragon", "Inferno Tower", "Mighty Miner"]

    if name in tough_units:
        dmg_val = find_stat_case_insensitive(stats, "Damage (Stage 3)")
        dps_val = find_stat_case_insensitive(stats, "Damage per second (Stage 3)")
    else:
        dmg_val = (
            find_stat_case_insensitive(stats, "Area Damage") or
            find_stat_case_insensitive(stats, "Damage") or
            find_stat_case_insensitive(stats, "Spawn Damage") or
            find_stat_case_insensitive(stats, "Dash Damage")
        )
        dps_val = find_stat_case_insensitive(stats, "Damage per second")

        if not dmg_val:
            dmg_val = find_stat_case_insensitive(stats, f"{name} Damage")

        if not dps_val:
            dps_val = find_stat_case_insensitive(stats, f"{name} Damage per second")

    dmg_num = to_number_maybe(dmg_val)
    dps_num = to_number_maybe(dps_val)

    return hp_num, dmg_num, dps_num


NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "12345678")

driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USER, NEO4J_PASSWORD)
)

CYPHER = """
MERGE (c:Card {name: $name})
SET  c.elixir = $elixir,
     c.rarity = $rarity,
     c.type = $type,
     c.arena = $arena,
     c.transport = $transport,
     c.level11_stats = $level11_stats,
     c.hitpoints = $hitpoints,
     c.damage = $damage,
     c.dps = $dps

MERGE (r:Rarity {name: $rarity})
MERGE (c)-[:HAS_RARITY]->(r)

MERGE (a:Arena {name: $arena})
MERGE (c)-[:UNLOCKS_IN]->(a)

WITH c, $targets AS tlist
UNWIND tlist AS tname
    MERGE (t:Target {name: tname})
    MERGE (c)-[:CAN_HIT]->(t)

RETURN c.name AS inserted
"""


def ingest_card(card, arena_name):
    hp, dmg, dps = extract_combat_stats(card)

    params = {
        "name": card.get("name"),
        "elixir": card.get("elixir"),
        "rarity": card.get("rarity"),
        "type": card.get("type"),
        "arena": arena_name,
        "transport": card.get("transport"),
        "level11_stats": json.dumps(card.get("level_11_stats", {})),
        "hitpoints": hp,
        "damage": dmg,
        "dps": dps,
        "targets": extract_targets(card)
    }

    with driver.session() as session:
        res = session.run(CYPHER.strip(), params)
        print("Inserted:", res.single()["inserted"])

def main():
    print("Loading dataset...")
    with open("../../data/raw/fandom_arenas_cards.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    for _, arena_data in data.items():
        arena = arena_data.get("arena_name")

        print(f"\n=== Arena: {arena} ===")
        for card in arena_data.get("cards", []):
            ingest_card(card, arena)

    print("\n=== DONE ===")


if __name__ == "__main__":
    main()
