/**
 * Cypher Query Templates - Retrieval & Utility
 */

MATCH (c:Card {name: $card})
OPTIONAL MATCH (c)-[:HAS_RARITY]->(r)
OPTIONAL MATCH (c)-[:UNLOCKS_IN]->(a)
OPTIONAL MATCH (c)-[:CAN_HIT]->(t)
RETURN c, r.name AS rarity, a.name AS arena, collect(t.name) AS targets;

MATCH (c:Card)-[:CAN_HIT]->(t:Target {name: $target})
RETURN c.name AS card, c.type, c.elixir_cost
ORDER BY c.elixir_cost ASC;

MATCH (c:Card)
WHERE c.elixir_cost <= $max
RETURN c.name AS card, c.elixir_cost
ORDER BY c.elixir_cost;

MATCH (c:Card)
WHERE "buildings" IN c.targets OR c.type = "building"
RETURN c.name AS wincon;

MATCH (c:Card)-[:UNLOCKS_IN]->(a:Arena {name: $arena})
RETURN c.name AS card, c.type, c.elixir_cost
ORDER BY c.type;

CALL db.index.fulltext.queryNodes(
    "cardTextIndex",
    $text
) YIELD node, score
RETURN node.name AS card, score
ORDER BY score DESC
LIMIT 10;


MATCH (c1:Card {name: $card})-[:CAN_HIT]->(t:Target)<-[:CAN_HIT]-(c2:Card)
WHERE c1 <> c2
RETURN c2.name AS similar_card, collect(t.name) AS common_targets;

