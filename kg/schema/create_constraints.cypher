/* CARD */
CREATE CONSTRAINT card_name_unique IF NOT EXISTS
FOR (c:Card)
REQUIRE c.name IS UNIQUE;

/* RARITY */
CREATE CONSTRAINT rarity_name_unique IF NOT EXISTS
FOR (r:Rarity)
REQUIRE r.name IS UNIQUE;

/* ARENA */
CREATE CONSTRAINT arena_name_unique IF NOT EXISTS
FOR (a:Arena)
REQUIRE a.name IS UNIQUE;

CREATE INDEX arena_level_index IF NOT EXISTS
FOR (a:Arena) ON (a.arena_level);

/* TARGET */
CREATE CONSTRAINT target_name_unique IF NOT EXISTS
FOR (t:Target)
REQUIRE t.name IS UNIQUE;
