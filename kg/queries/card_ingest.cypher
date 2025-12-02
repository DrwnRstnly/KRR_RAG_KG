/**
 * Cypher Template - Card Ingestion
 * 
 * Required parameters:
 *   $name
 *   $type          (troop / spell / building / tower_troop)
 *   $rarity
 *   $arena
 *
 * Optional parameters (gunakan null jika tidak ada):
 *   $elixir_cost
 *   $hitpoints
 *   $damage
 *   $dps
 *   $transport
 *   $range_val
 *   $melee_or_ranged
 *   $splash
 *   $count
 *   $targets       (list of strings: ["air","ground","buildings"])
 */

MERGE (c:Card {name: $name})
SET c.type = $type,
    c.elixir_cost = $elixir_cost,
    c.hitpoints = $hitpoints,
    c.damage = $damage,
    c.damage_per_second = $dps,
    c.transport = $transport,
    c.range_value = $range_val,
    c.melee_or_ranged = $melee_or_ranged,
    c.splash = $splash,
    c.count = $count;

MERGE (r:Rarity {name: $rarity});
MERGE (c)-[:HAS_RARITY]->(r);

MERGE (a:Arena {name: $arena});
MERGE (c)-[:UNLOCKS_IN]->(a);

// Set card targets
WITH c, $targets AS targetList
UNWIND targetList AS tName
    MERGE (t:Target {name: tName})
    MERGE (c)-[:CAN_HIT]->(t);

RETURN c;
