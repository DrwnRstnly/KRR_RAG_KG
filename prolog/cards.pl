:- discontiguous card/2.
:- discontiguous has_rarity/2.
:- discontiguous elixir_cost/2.
:- discontiguous in_arena/2.
:- discontiguous damage/2.
:- discontiguous hitpoints/2.
:- discontiguous targets/2.
:- discontiguous melee_or_ranged/2.
:- discontiguous splash/2.
:- discontiguous count/2.
:- discontiguous range_value/2.
:- discontiguous transport/2.
:- discontiguous damage_per_second/2.

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Clash Royale Card Database
% Generated from fandom_arenas_cards.json
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

card(arrows, spell).
has_rarity(arrows, common).
elixir_cost(arrows, 3).
in_arena(arrows, training_camp).
damage(arrows, 122).
targets(arrows, air).
targets(arrows, ground).
splash(arrows, false).

card(minions, troop).
has_rarity(minions, common).
elixir_cost(minions, 3).
in_arena(minions, training_camp).
hitpoints(minions, 230).
damage(minions, 107).
damage_per_second(minions, 97).
transport(minions, air).
targets(minions, air).
targets(minions, ground).
splash(minions, false).
melee_or_ranged(minions, ranged).
range_value(minions, 2).
count(minions, 3).

card(archers, troop).
has_rarity(archers, common).
elixir_cost(archers, 3).
in_arena(archers, training_camp).
hitpoints(archers, 304).
damage(archers, 112).
damage_per_second(archers, 124).
transport(archers, ground).
targets(archers, air).
targets(archers, ground).
splash(archers, false).
melee_or_ranged(archers, ranged).
range_value(archers, 5).
count(archers, 2).

card(knight, troop).
has_rarity(knight, common).
elixir_cost(knight, 3).
in_arena(knight, training_camp).
hitpoints(knight, 1766).
damage(knight, 202).
damage_per_second(knight, 168).
transport(knight, ground).
targets(knight, ground).
splash(knight, false).
melee_or_ranged(knight, melee).
count(knight, 1).

card(fireball, spell).
has_rarity(fireball, rare).
elixir_cost(fireball, 4).
in_arena(fireball, training_camp).
damage(fireball, 688).
targets(fireball, air).
targets(fireball, ground).
splash(fireball, false).

card(mini_p_e_k_k_a, troop).
has_rarity(mini_p_e_k_k_a, rare).
elixir_cost(mini_p_e_k_k_a, 4).
in_arena(mini_p_e_k_k_a, training_camp).
hitpoints(mini_p_e_k_k_a, 1433).
damage(mini_p_e_k_k_a, 755).
damage_per_second(mini_p_e_k_k_a, 471).
transport(mini_p_e_k_k_a, ground).
targets(mini_p_e_k_k_a, ground).
splash(mini_p_e_k_k_a, false).
melee_or_ranged(mini_p_e_k_k_a, melee).
count(mini_p_e_k_k_a, 1).

card(musketeer, troop).
has_rarity(musketeer, rare).
elixir_cost(musketeer, 4).
in_arena(musketeer, training_camp).
hitpoints(musketeer, 721).
damage(musketeer, 217).
damage_per_second(musketeer, 217).
transport(musketeer, ground).
targets(musketeer, air).
targets(musketeer, ground).
splash(musketeer, false).
melee_or_ranged(musketeer, ranged).
range_value(musketeer, 6).
count(musketeer, 1).

card(giant, troop).
has_rarity(giant, rare).
elixir_cost(giant, 5).
in_arena(giant, training_camp).
hitpoints(giant, 4090).
damage(giant, 253).
damage_per_second(giant, 168).
transport(giant, ground).
targets(giant, buildings).
splash(giant, false).
melee_or_ranged(giant, melee).
count(giant, 1).

card(tower_princess, tower_troop).
has_rarity(tower_princess, common).
in_arena(tower_princess, training_camp).
hitpoints(tower_princess, 3052).
damage(tower_princess, 109).
damage_per_second(tower_princess, 136).
targets(tower_princess, air).
targets(tower_princess, ground).
splash(tower_princess, false).
melee_or_ranged(tower_princess, ranged).
range_value(tower_princess, 7).

card(spear_goblins, troop).
has_rarity(spear_goblins, common).
elixir_cost(spear_goblins, 2).
in_arena(spear_goblins, goblin_stadium).
hitpoints(spear_goblins, 133).
damage(spear_goblins, 81).
damage_per_second(spear_goblins, 47).
transport(spear_goblins, ground).
targets(spear_goblins, air).
targets(spear_goblins, ground).
splash(spear_goblins, false).
melee_or_ranged(spear_goblins, ranged).
range_value(spear_goblins, 5).
count(spear_goblins, 3).

card(goblins, troop).
has_rarity(goblins, common).
elixir_cost(goblins, 2).
in_arena(goblins, goblin_stadium).
hitpoints(goblins, 202).
damage(goblins, 120).
damage_per_second(goblins, 109).
transport(goblins, ground).
targets(goblins, ground).
splash(goblins, false).
melee_or_ranged(goblins, melee).
count(goblins, 4).

card(goblin_cage, building).
has_rarity(goblin_cage, rare).
elixir_cost(goblin_cage, 4).
in_arena(goblin_cage, goblin_stadium).
hitpoints(goblin_cage, 780).
splash(goblin_cage, false).
% !!! WARNING: goblin_cage is missing: damage, targets

card(goblin_hut, building).
has_rarity(goblin_hut, rare).
elixir_cost(goblin_hut, 4).
in_arena(goblin_hut, goblin_stadium).
hitpoints(goblin_hut, 1228).
splash(goblin_hut, false).
% !!! WARNING: goblin_hut is missing: targets

card(bomber, troop).
has_rarity(bomber, common).
elixir_cost(bomber, 2).
in_arena(bomber, bone_pit).
hitpoints(bomber, 304).
damage(bomber, 225).
damage_per_second(bomber, 125).
transport(bomber, ground).
targets(bomber, ground).
splash(bomber, true).
melee_or_ranged(bomber, ranged).
range_value(bomber, 4).
count(bomber, 1).

card(skeletons, troop).
has_rarity(skeletons, common).
elixir_cost(skeletons, 1).
in_arena(skeletons, bone_pit).
hitpoints(skeletons, 81).
damage(skeletons, 81).
damage_per_second(skeletons, 81).
transport(skeletons, ground).
targets(skeletons, ground).
splash(skeletons, false).
melee_or_ranged(skeletons, melee).
count(skeletons, 3).

card(tombstone, building).
has_rarity(tombstone, rare).
elixir_cost(tombstone, 3).
in_arena(tombstone, bone_pit).
hitpoints(tombstone, 529).
splash(tombstone, false).
% !!! WARNING: tombstone is missing: targets

card(valkyrie, troop).
has_rarity(valkyrie, rare).
elixir_cost(valkyrie, 4).
in_arena(valkyrie, bone_pit).
hitpoints(valkyrie, 1907).
damage(valkyrie, 266).
damage_per_second(valkyrie, 177).
transport(valkyrie, ground).
targets(valkyrie, ground).
splash(valkyrie, true).
melee_or_ranged(valkyrie, melee).
count(valkyrie, 1).

card(cannon, building).
has_rarity(cannon, common).
elixir_cost(cannon, 3).
in_arena(cannon, barbarian_bowl).
hitpoints(cannon, 824).
damage(cannon, 212).
damage_per_second(cannon, 212).
targets(cannon, ground).
splash(cannon, false).
melee_or_ranged(cannon, ranged).
range_value(cannon, 5).

card(barbarians, troop).
has_rarity(barbarians, common).
elixir_cost(barbarians, 5).
in_arena(barbarians, barbarian_bowl).
hitpoints(barbarians, 670).
damage(barbarians, 192).
damage_per_second(barbarians, 147).
transport(barbarians, ground).
targets(barbarians, ground).
splash(barbarians, false).
melee_or_ranged(barbarians, melee).
count(barbarians, 5).

card(mega_minion, troop).
has_rarity(mega_minion, rare).
elixir_cost(mega_minion, 3).
in_arena(mega_minion, barbarian_bowl).
hitpoints(mega_minion, 837).
damage(mega_minion, 312).
damage_per_second(mega_minion, 208).
transport(mega_minion, air).
targets(mega_minion, air).
targets(mega_minion, ground).
splash(mega_minion, false).
melee_or_ranged(mega_minion, melee).
count(mega_minion, 1).

card(battle_ram, troop).
has_rarity(battle_ram, rare).
elixir_cost(battle_ram, 4).
in_arena(battle_ram, barbarian_bowl).
hitpoints(battle_ram, 967).
damage(battle_ram, 286).
transport(battle_ram, ground).
targets(battle_ram, buildings).
splash(battle_ram, false).
melee_or_ranged(battle_ram, melee).
count(battle_ram, 1).
% !!! WARNING: battle_ram is missing: damage_per_second

card(electro_spirit, troop).
has_rarity(electro_spirit, common).
elixir_cost(electro_spirit, 1).
in_arena(electro_spirit, spell_valley).
hitpoints(electro_spirit, 230).
damage(electro_spirit, 99).
transport(electro_spirit, ground).
targets(electro_spirit, air).
targets(electro_spirit, ground).
splash(electro_spirit, false).
melee_or_ranged(electro_spirit, ranged).
range_value(electro_spirit, 2).
count(electro_spirit, 1).
% !!! WARNING: electro_spirit is missing: damage_per_second

card(skeleton_dragons, troop).
has_rarity(skeleton_dragons, common).
elixir_cost(skeleton_dragons, 4).
in_arena(skeleton_dragons, spell_valley).
hitpoints(skeleton_dragons, 560).
damage(skeleton_dragons, 161).
damage_per_second(skeleton_dragons, 84).
transport(skeleton_dragons, air).
targets(skeleton_dragons, air).
targets(skeleton_dragons, ground).
splash(skeleton_dragons, true).
melee_or_ranged(skeleton_dragons, ranged).
range_value(skeleton_dragons, 3).
count(skeleton_dragons, 2).

card(fire_spirit, troop).
has_rarity(fire_spirit, common).
elixir_cost(fire_spirit, 1).
in_arena(fire_spirit, spell_valley).
hitpoints(fire_spirit, 230).
damage(fire_spirit, 207).
transport(fire_spirit, ground).
targets(fire_spirit, air).
targets(fire_spirit, ground).
splash(fire_spirit, true).
melee_or_ranged(fire_spirit, ranged).
range_value(fire_spirit, 2).
count(fire_spirit, 1).
% !!! WARNING: fire_spirit is missing: damage_per_second

card(bomb_tower, building).
has_rarity(bomb_tower, rare).
elixir_cost(bomb_tower, 4).
in_arena(bomb_tower, spell_valley).
hitpoints(bomb_tower, 1356).
damage(bomb_tower, 222).
damage_per_second(bomb_tower, 123).
targets(bomb_tower, ground).
splash(bomb_tower, true).
melee_or_ranged(bomb_tower, ranged).
range_value(bomb_tower, 6).

card(inferno_tower, building).
has_rarity(inferno_tower, rare).
elixir_cost(inferno_tower, 5).
in_arena(inferno_tower, spell_valley).
hitpoints(inferno_tower, 1748).
damage(inferno_tower, 847).
damage_per_second(inferno_tower, 2117).
targets(inferno_tower, air).
targets(inferno_tower, ground).
splash(inferno_tower, false).
melee_or_ranged(inferno_tower, ranged).
range_value(inferno_tower, 6).

card(wizard, troop).
has_rarity(wizard, rare).
elixir_cost(wizard, 5).
in_arena(wizard, spell_valley).
hitpoints(wizard, 755).
damage(wizard, 281).
damage_per_second(wizard, 200).
transport(wizard, ground).
targets(wizard, air).
targets(wizard, ground).
splash(wizard, true).
melee_or_ranged(wizard, ranged).
range_value(wizard, 5).
count(wizard, 1).

card(zap, spell).
has_rarity(zap, common).
elixir_cost(zap, 2).
in_arena(zap, builders_workshop).
damage(zap, 192).
targets(zap, air).
targets(zap, ground).
splash(zap, false).

card(mortar, building).
has_rarity(mortar, common).
elixir_cost(mortar, 4).
in_arena(mortar, builders_workshop).
hitpoints(mortar, 1369).
damage(mortar, 266).
damage_per_second(mortar, 53).
targets(mortar, ground).
splash(mortar, true).
melee_or_ranged(mortar, ranged).
range_value(mortar, 3).

card(bats, troop).
has_rarity(bats, common).
elixir_cost(bats, 2).
in_arena(bats, builders_workshop).
hitpoints(bats, 81).
damage(bats, 81).
damage_per_second(bats, 62).
transport(bats, air).
targets(bats, air).
targets(bats, ground).
splash(bats, false).
melee_or_ranged(bats, melee).
count(bats, 5).

card(rocket, spell).
has_rarity(rocket, rare).
elixir_cost(rocket, 6).
in_arena(rocket, builders_workshop).
damage(rocket, 1484).
targets(rocket, air).
targets(rocket, ground).
splash(rocket, false).

card(flying_machine, troop).
has_rarity(flying_machine, rare).
elixir_cost(flying_machine, 4).
in_arena(flying_machine, builders_workshop).
hitpoints(flying_machine, 614).
damage(flying_machine, 171).
damage_per_second(flying_machine, 155).
transport(flying_machine, air).
targets(flying_machine, air).
targets(flying_machine, ground).
splash(flying_machine, false).
melee_or_ranged(flying_machine, ranged).
range_value(flying_machine, 6).
count(flying_machine, 1).

card(hog_rider, troop).
has_rarity(hog_rider, rare).
elixir_cost(hog_rider, 4).
in_arena(hog_rider, builders_workshop).
hitpoints(hog_rider, 1697).
damage(hog_rider, 317).
damage_per_second(hog_rider, 198).
transport(hog_rider, ground).
targets(hog_rider, buildings).
splash(hog_rider, false).
melee_or_ranged(hog_rider, melee).
count(hog_rider, 1).

card(goblin_barrel, spell).
has_rarity(goblin_barrel, epic).
elixir_cost(goblin_barrel, 3).
in_arena(goblin_barrel, pekkas_playhouse).
splash(goblin_barrel, false).
% !!! WARNING: goblin_barrel is missing: damage

card(guards, troop).
has_rarity(guards, epic).
elixir_cost(guards, 3).
in_arena(guards, pekkas_playhouse).
hitpoints(guards, 81).
damage(guards, 117).
damage_per_second(guards, 117).
transport(guards, ground).
targets(guards, ground).
splash(guards, false).
melee_or_ranged(guards, melee).
count(guards, 3).

card(baby_dragon, troop).
has_rarity(baby_dragon, epic).
elixir_cost(baby_dragon, 4).
in_arena(baby_dragon, pekkas_playhouse).
hitpoints(baby_dragon, 1152).
damage(baby_dragon, 161).
damage_per_second(baby_dragon, 107).
transport(baby_dragon, air).
targets(baby_dragon, air).
targets(baby_dragon, ground).
splash(baby_dragon, true).
melee_or_ranged(baby_dragon, ranged).
range_value(baby_dragon, 3).
count(baby_dragon, 1).

card(skeleton_army, troop).
has_rarity(skeleton_army, epic).
elixir_cost(skeleton_army, 3).
in_arena(skeleton_army, pekkas_playhouse).
hitpoints(skeleton_army, 81).
damage(skeleton_army, 81).
damage_per_second(skeleton_army, 81).
transport(skeleton_army, ground).
targets(skeleton_army, ground).
splash(skeleton_army, false).
melee_or_ranged(skeleton_army, melee).
count(skeleton_army, 15).

card(witch, troop).
has_rarity(witch, epic).
elixir_cost(witch, 5).
in_arena(witch, pekkas_playhouse).
hitpoints(witch, 839).
damage(witch, 135).
damage_per_second(witch, 122).
transport(witch, ground).
targets(witch, air).
targets(witch, ground).
splash(witch, true).
melee_or_ranged(witch, ranged).
range_value(witch, 5).
count(witch, 1).

card(pekka, troop).
has_rarity(pekka, epic).
elixir_cost(pekka, 7).
in_arena(pekka, pekkas_playhouse).
hitpoints(pekka, 3760).
damage(pekka, 816).
damage_per_second(pekka, 453).
transport(pekka, ground).
targets(pekka, ground).
splash(pekka, false).
melee_or_ranged(pekka, melee).
count(pekka, 1).

card(royal_recruits, troop).
has_rarity(royal_recruits, common).
elixir_cost(royal_recruits, 7).
in_arena(royal_recruits, royal_arena).
hitpoints(royal_recruits, 547).
damage(royal_recruits, 133).
damage_per_second(royal_recruits, 102).
transport(royal_recruits, ground).
targets(royal_recruits, ground).
splash(royal_recruits, false).
melee_or_ranged(royal_recruits, melee).
count(royal_recruits, 6).

card(royal_giant, troop).
has_rarity(royal_giant, common).
elixir_cost(royal_giant, 6).
in_arena(royal_giant, royal_arena).
hitpoints(royal_giant, 3164).
damage(royal_giant, 307).
damage_per_second(royal_giant, 180).
transport(royal_giant, ground).
targets(royal_giant, buildings).
splash(royal_giant, false).
melee_or_ranged(royal_giant, ranged).
range_value(royal_giant, 5).
count(royal_giant, 1).

card(royal_hogs, troop).
has_rarity(royal_hogs, rare).
elixir_cost(royal_hogs, 5).
in_arena(royal_hogs, royal_arena).
hitpoints(royal_hogs, 837).
damage(royal_hogs, 74).
damage_per_second(royal_hogs, 61).
transport(royal_hogs, ground).
targets(royal_hogs, buildings).
splash(royal_hogs, false).
melee_or_ranged(royal_hogs, melee).
count(royal_hogs, 4).

card(three_musketeers, troop).
has_rarity(three_musketeers, rare).
elixir_cost(three_musketeers, 9).
in_arena(three_musketeers, royal_arena).
hitpoints(three_musketeers, 721).
damage(three_musketeers, 217).
damage_per_second(three_musketeers, 217).
transport(three_musketeers, ground).
targets(three_musketeers, air).
targets(three_musketeers, ground).
splash(three_musketeers, false).
melee_or_ranged(three_musketeers, ranged).
range_value(three_musketeers, 6).
count(three_musketeers, 3).

card(dark_prince, troop).
has_rarity(dark_prince, epic).
elixir_cost(dark_prince, 4).
in_arena(dark_prince, royal_arena).
hitpoints(dark_prince, 1200).
damage(dark_prince, 266).
damage_per_second(dark_prince, 204).
transport(dark_prince, ground).
targets(dark_prince, ground).
splash(dark_prince, true).
melee_or_ranged(dark_prince, melee).
count(dark_prince, 1).

card(prince, troop).
has_rarity(prince, epic).
elixir_cost(prince, 5).
in_arena(prince, royal_arena).
hitpoints(prince, 1920).
damage(prince, 391).
damage_per_second(prince, 279).
transport(prince, ground).
targets(prince, ground).
splash(prince, false).
melee_or_ranged(prince, melee).
count(prince, 1).

card(balloon, troop).
has_rarity(balloon, epic).
elixir_cost(balloon, 5).
in_arena(balloon, royal_arena).
hitpoints(balloon, 1679).
damage(balloon, 640).
damage_per_second(balloon, 320).
transport(balloon, air).
targets(balloon, buildings).
splash(balloon, false).
melee_or_ranged(balloon, melee).
count(balloon, 1).

card(giant_snowball, spell).
has_rarity(giant_snowball, common).
elixir_cost(giant_snowball, 2).
in_arena(giant_snowball, frozen_peak).
damage(giant_snowball, 179).
targets(giant_snowball, air).
targets(giant_snowball, ground).
splash(giant_snowball, false).

card(ice_spirit, troop).
has_rarity(ice_spirit, common).
elixir_cost(ice_spirit, 1).
in_arena(ice_spirit, frozen_peak).
hitpoints(ice_spirit, 230).
damage(ice_spirit, 110).
transport(ice_spirit, ground).
targets(ice_spirit, air).
targets(ice_spirit, ground).
splash(ice_spirit, true).
melee_or_ranged(ice_spirit, ranged).
range_value(ice_spirit, 2).
% !!! WARNING: ice_spirit is missing: damage_per_second

card(battle_healer, troop).
has_rarity(battle_healer, rare).
elixir_cost(battle_healer, 4).
in_arena(battle_healer, frozen_peak).
hitpoints(battle_healer, 1717).
damage(battle_healer, 148).
damage_per_second(battle_healer, 98).
transport(battle_healer, ground).
targets(battle_healer, ground).
splash(battle_healer, false).
melee_or_ranged(battle_healer, melee).
count(battle_healer, 1).

card(ice_golem, troop).
has_rarity(ice_golem, rare).
elixir_cost(ice_golem, 2).
in_arena(ice_golem, frozen_peak).
hitpoints(ice_golem, 1198).
damage(ice_golem, 84).
damage_per_second(ice_golem, 33).
transport(ice_golem, ground).
targets(ice_golem, buildings).
splash(ice_golem, false).
melee_or_ranged(ice_golem, melee).
count(ice_golem, 1).

card(vines, spell).
has_rarity(vines, epic).
elixir_cost(vines, 3).
in_arena(vines, frozen_peak).
damage_per_second(vines, 153).
targets(vines, air).
targets(vines, ground).
splash(vines, false).
count(vines, 3).
% !!! WARNING: vines is missing: damage

card(lightning, spell).
has_rarity(lightning, epic).
elixir_cost(lightning, 6).
in_arena(lightning, frozen_peak).
damage(lightning, 1057).
targets(lightning, air).
targets(lightning, ground).
splash(lightning, false).
count(lightning, 3).

card(freeze, spell).
has_rarity(freeze, epic).
elixir_cost(freeze, 4).
in_arena(freeze, frozen_peak).
damage(freeze, 115).
targets(freeze, air).
targets(freeze, ground).
splash(freeze, false).

card(giant_skeleton, troop).
has_rarity(giant_skeleton, epic).
elixir_cost(giant_skeleton, 6).
in_arena(giant_skeleton, frozen_peak).
hitpoints(giant_skeleton, 3617).
damage(giant_skeleton, 266).
damage_per_second(giant_skeleton, 190).
transport(giant_skeleton, ground).
targets(giant_skeleton, ground).
splash(giant_skeleton, false).
melee_or_ranged(giant_skeleton, melee).
count(giant_skeleton, 1).

card(cannoneer, tower_troop).
has_rarity(cannoneer, epic).
in_arena(cannoneer, frozen_peak).
hitpoints(cannoneer, 2616).
damage(cannoneer, 320).
damage_per_second(cannoneer, 145).
targets(cannoneer, air).
targets(cannoneer, ground).
splash(cannoneer, false).
melee_or_ranged(cannoneer, ranged).
range_value(cannoneer, 7).

card(berserker, troop).
has_rarity(berserker, common).
elixir_cost(berserker, 2).
in_arena(berserker, jungle_arena).
hitpoints(berserker, 896).
damage(berserker, 102).
damage_per_second(berserker, 170).
transport(berserker, ground).
targets(berserker, ground).
splash(berserker, false).
melee_or_ranged(berserker, melee).
count(berserker, 1).

card(skeleton_barrel, troop).
has_rarity(skeleton_barrel, common).
elixir_cost(skeleton_barrel, 3).
in_arena(skeleton_barrel, jungle_arena).
hitpoints(skeleton_barrel, 532).
transport(skeleton_barrel, air).
targets(skeleton_barrel, buildings).
splash(skeleton_barrel, false).
melee_or_ranged(skeleton_barrel, melee).
% !!! WARNING: skeleton_barrel is missing: damage, damage_per_second

card(goblin_gang, troop).
has_rarity(goblin_gang, common).
elixir_cost(goblin_gang, 3).
in_arena(goblin_gang, jungle_arena).
transport(goblin_gang, ground).
targets(goblin_gang, ground).
splash(goblin_gang, false).
melee_or_ranged(goblin_gang, melee).
count(goblin_gang, 3).
% !!! WARNING: goblin_gang is missing: hitpoints, damage, damage_per_second

card(barbarian_hut, building).
has_rarity(barbarian_hut, rare).
elixir_cost(barbarian_hut, 6).
in_arena(barbarian_hut, jungle_arena).
hitpoints(barbarian_hut, 1164).
splash(barbarian_hut, false).
% !!! WARNING: barbarian_hut is missing: targets

card(dart_goblin, troop).
has_rarity(dart_goblin, rare).
elixir_cost(dart_goblin, 3).
in_arena(dart_goblin, jungle_arena).
hitpoints(dart_goblin, 261).
damage(dart_goblin, 156).
damage_per_second(dart_goblin, 195).
transport(dart_goblin, ground).
targets(dart_goblin, air).
targets(dart_goblin, ground).
splash(dart_goblin, false).
melee_or_ranged(dart_goblin, ranged).
range_value(dart_goblin, 6).
count(dart_goblin, 1).

card(barbarian_barrel, spell).
has_rarity(barbarian_barrel, epic).
elixir_cost(barbarian_barrel, 2).
in_arena(barbarian_barrel, jungle_arena).
damage(barbarian_barrel, 240).
targets(barbarian_barrel, ground).
splash(barbarian_barrel, false).
melee_or_ranged(barbarian_barrel, ranged).
range_value(barbarian_barrel, 4).

card(poison, spell).
has_rarity(poison, epic).
elixir_cost(poison, 4).
in_arena(poison, jungle_arena).
damage_per_second(poison, 92).
targets(poison, air).
targets(poison, ground).
splash(poison, false).
% !!! WARNING: poison is missing: damage

card(rune_giant, troop).
has_rarity(rune_giant, epic).
elixir_cost(rune_giant, 4).
in_arena(rune_giant, jungle_arena).
hitpoints(rune_giant, 2662).
damage(rune_giant, 120).
damage_per_second(rune_giant, 80).
transport(rune_giant, ground).
targets(rune_giant, buildings).
splash(rune_giant, false).
melee_or_ranged(rune_giant, melee).
count(rune_giant, 1).

card(goblin_giant, troop).
has_rarity(goblin_giant, epic).
elixir_cost(goblin_giant, 6).
in_arena(goblin_giant, jungle_arena).
hitpoints(goblin_giant, 3022).
damage(goblin_giant, 176).
damage_per_second(goblin_giant, 117).
transport(goblin_giant, ground).
targets(goblin_giant, buildings).
splash(goblin_giant, false).
melee_or_ranged(goblin_giant, melee).
count(goblin_giant, 1).

card(tesla, building).
has_rarity(tesla, common).
elixir_cost(tesla, 4).
in_arena(tesla, hog_mountain).
hitpoints(tesla, 1152).
damage(tesla, 220).
damage_per_second(tesla, 199).
targets(tesla, air).
targets(tesla, ground).
splash(tesla, false).
melee_or_ranged(tesla, ranged).
range_value(tesla, 5).

card(elite_barbarians, troop).
has_rarity(elite_barbarians, common).
elixir_cost(elite_barbarians, 6).
in_arena(elite_barbarians, hog_mountain).
hitpoints(elite_barbarians, 1341).
damage(elite_barbarians, 384).
damage_per_second(elite_barbarians, 274).
transport(elite_barbarians, ground).
targets(elite_barbarians, ground).
splash(elite_barbarians, false).
melee_or_ranged(elite_barbarians, melee).
count(elite_barbarians, 2).

card(minion_horde, troop).
has_rarity(minion_horde, common).
elixir_cost(minion_horde, 5).
in_arena(minion_horde, hog_mountain).
hitpoints(minion_horde, 230).
damage(minion_horde, 117).
damage_per_second(minion_horde, 117).
transport(minion_horde, air).
targets(minion_horde, air).
targets(minion_horde, ground).
splash(minion_horde, false).
melee_or_ranged(minion_horde, ranged).
range_value(minion_horde, 2).
count(minion_horde, 6).

card(furnace, troop).
has_rarity(furnace, rare).
elixir_cost(furnace, 4).
in_arena(furnace, hog_mountain).
hitpoints(furnace, 727).
damage(furnace, 179).
damage_per_second(furnace, 99).
transport(furnace, ground).
targets(furnace, air).
targets(furnace, ground).
splash(furnace, false).
melee_or_ranged(furnace, ranged).
range_value(furnace, 6).
count(furnace, 1).

card(zappies, troop).
has_rarity(zappies, rare).
elixir_cost(zappies, 4).
in_arena(zappies, hog_mountain).
hitpoints(zappies, 529).
damage(zappies, 117).
damage_per_second(zappies, 55).
transport(zappies, ground).
targets(zappies, air).
targets(zappies, ground).
splash(zappies, false).
melee_or_ranged(zappies, ranged).
range_value(zappies, 4).
count(zappies, 3).

card(x_bow, building).
has_rarity(x_bow, epic).
elixir_cost(x_bow, 6).
in_arena(x_bow, hog_mountain).
hitpoints(x_bow, 1600).
damage(x_bow, 43).
damage_per_second(x_bow, 143).
targets(x_bow, ground).
splash(x_bow, false).
melee_or_ranged(x_bow, ranged).
range_value(x_bow, 11).

card(hunter, troop).
has_rarity(hunter, epic).
elixir_cost(hunter, 4).
in_arena(hunter, hog_mountain).
hitpoints(hunter, 885).
damage(hunter, 84).
damage_per_second(hunter, 381).
transport(hunter, ground).
targets(hunter, air).
targets(hunter, ground).
splash(hunter, false).
melee_or_ranged(hunter, ranged).
range_value(hunter, 4).
count(hunter, 1).

card(golem, troop).
has_rarity(golem, epic).
elixir_cost(golem, 8).
in_arena(golem, hog_mountain).
hitpoints(golem, 5120).
damage(golem, 312).
damage_per_second(golem, 124).
transport(golem, ground).
targets(golem, buildings).
splash(golem, false).
melee_or_ranged(golem, melee).
count(golem, 1).

card(the_log, spell).
has_rarity(the_log, legendary).
elixir_cost(the_log, 2).
in_arena(the_log, electro_valley).
damage(the_log, 266).
targets(the_log, ground).
splash(the_log, false).
melee_or_ranged(the_log, ranged).
range_value(the_log, 10).

card(mega_knight, troop).
has_rarity(mega_knight, legendary).
elixir_cost(mega_knight, 7).
in_arena(mega_knight, electro_valley).
hitpoints(mega_knight, 3993).
damage(mega_knight, 268).
damage_per_second(mega_knight, 157).
transport(mega_knight, ground).
targets(mega_knight, ground).
splash(mega_knight, true).
melee_or_ranged(mega_knight, melee).
count(mega_knight, 1).

card(ram_rider, troop).
has_rarity(ram_rider, legendary).
elixir_cost(ram_rider, 5).
in_arena(ram_rider, electro_valley).
hitpoints(ram_rider, 1697).
transport(ram_rider, ground).
targets(ram_rider, buildings).
splash(ram_rider, false).
melee_or_ranged(ram_rider, melee).
count(ram_rider, 1).
% !!! WARNING: ram_rider is missing: damage, damage_per_second

card(electro_wizard, troop).
has_rarity(electro_wizard, legendary).
elixir_cost(electro_wizard, 4).
in_arena(electro_wizard, electro_valley).
hitpoints(electro_wizard, 714).
damage(electro_wizard, 115).
damage_per_second(electro_wizard, 127).
transport(electro_wizard, ground).
targets(electro_wizard, air).
targets(electro_wizard, ground).
splash(electro_wizard, false).
melee_or_ranged(electro_wizard, ranged).
range_value(electro_wizard, 5).

card(inferno_dragon, troop).
has_rarity(inferno_dragon, legendary).
elixir_cost(inferno_dragon, 4).
in_arena(inferno_dragon, electro_valley).
hitpoints(inferno_dragon, 1295).
damage(inferno_dragon, 422).
damage_per_second(inferno_dragon, 1055).
transport(inferno_dragon, air).
targets(inferno_dragon, air).
targets(inferno_dragon, ground).
splash(inferno_dragon, false).
melee_or_ranged(inferno_dragon, ranged).
range_value(inferno_dragon, 3).
count(inferno_dragon, 1).

card(sparky, troop).
has_rarity(sparky, legendary).
elixir_cost(sparky, 6).
in_arena(sparky, electro_valley).
hitpoints(sparky, 1451).
damage(sparky, 1331).
damage_per_second(sparky, 332).
transport(sparky, ground).
targets(sparky, ground).
splash(sparky, true).
melee_or_ranged(sparky, ranged).
range_value(sparky, 5).
count(sparky, 1).

card(miner, troop).
has_rarity(miner, legendary).
elixir_cost(miner, 3).
in_arena(miner, electro_valley).
hitpoints(miner, 1210).
damage(miner, 194).
damage_per_second(miner, 149).
transport(miner, ground).
targets(miner, ground).
splash(miner, false).
melee_or_ranged(miner, melee).
count(miner, 1).

card(princess, troop).
has_rarity(princess, legendary).
elixir_cost(princess, 3).
in_arena(princess, electro_valley).
hitpoints(princess, 261).
damage(princess, 168).
damage_per_second(princess, 56).
transport(princess, ground).
targets(princess, air).
targets(princess, ground).
splash(princess, true).
melee_or_ranged(princess, ranged).
range_value(princess, 9).
count(princess, 1).

card(dagger_duchess, tower_troop).
has_rarity(dagger_duchess, legendary).
in_arena(dagger_duchess, electro_valley).
hitpoints(dagger_duchess, 2768).
damage(dagger_duchess, 107).
damage_per_second(dagger_duchess, 214).
targets(dagger_duchess, air).
targets(dagger_duchess, ground).
splash(dagger_duchess, false).
melee_or_ranged(dagger_duchess, ranged).
range_value(dagger_duchess, 7).

card(firecracker, troop).
has_rarity(firecracker, common).
elixir_cost(firecracker, 3).
in_arena(firecracker, spooky_town).
hitpoints(firecracker, 304).
damage(firecracker, 64).
damage_per_second(firecracker, 106).
transport(firecracker, ground).
targets(firecracker, air).
targets(firecracker, ground).
splash(firecracker, false).
melee_or_ranged(firecracker, ranged).
range_value(firecracker, 6).
count(firecracker, 1).

card(earthquake, spell).
has_rarity(earthquake, rare).
elixir_cost(earthquake, 3).
in_arena(earthquake, spooky_town).
damage(earthquake, 84).
targets(earthquake, ground).
splash(earthquake, false).

card(goblin_demolisher, troop).
has_rarity(goblin_demolisher, rare).
elixir_cost(goblin_demolisher, 4).
in_arena(goblin_demolisher, spooky_town).
hitpoints(goblin_demolisher, 1300).
damage(goblin_demolisher, 186).
damage_per_second(goblin_demolisher, 155).
transport(goblin_demolisher, ground).
targets(goblin_demolisher, ground).
splash(goblin_demolisher, true).
melee_or_ranged(goblin_demolisher, ranged).
range_value(goblin_demolisher, 5).
count(goblin_demolisher, 1).

card(electro_dragon, troop).
has_rarity(electro_dragon, epic).
elixir_cost(electro_dragon, 5).
in_arena(electro_dragon, spooky_town).
hitpoints(electro_dragon, 949).
damage(electro_dragon, 192).
damage_per_second(electro_dragon, 91).
transport(electro_dragon, air).
targets(electro_dragon, air).
targets(electro_dragon, ground).
splash(electro_dragon, false).
melee_or_ranged(electro_dragon, ranged).
range_value(electro_dragon, 3).
count(electro_dragon, 1).

card(wall_breakers, troop).
has_rarity(wall_breakers, epic).
elixir_cost(wall_breakers, 2).
in_arena(wall_breakers, spooky_town).
hitpoints(wall_breakers, 330).
damage(wall_breakers, 391).
transport(wall_breakers, ground).
targets(wall_breakers, buildings).
splash(wall_breakers, true).
melee_or_ranged(wall_breakers, melee).
count(wall_breakers, 2).
% !!! WARNING: wall_breakers is missing: damage_per_second

card(graveyard, spell).
has_rarity(graveyard, legendary).
elixir_cost(graveyard, 5).
in_arena(graveyard, spooky_town).
splash(graveyard, false).
% !!! WARNING: graveyard is missing: damage

card(phoenix, troop).
has_rarity(phoenix, legendary).
elixir_cost(phoenix, 4).
in_arena(phoenix, spooky_town).
hitpoints(phoenix, 1052).
damage(phoenix, 217).
damage_per_second(phoenix, 217).
transport(phoenix, air).
targets(phoenix, air).
targets(phoenix, ground).
splash(phoenix, false).
melee_or_ranged(phoenix, melee).
count(phoenix, 1).

card(royal_ghost, troop).
has_rarity(royal_ghost, legendary).
elixir_cost(royal_ghost, 3).
in_arena(royal_ghost, spooky_town).
hitpoints(royal_ghost, 1210).
damage(royal_ghost, 261).
damage_per_second(royal_ghost, 145).
transport(royal_ghost, ground).
targets(royal_ghost, ground).
splash(royal_ghost, true).
melee_or_ranged(royal_ghost, melee).
count(royal_ghost, 1).

card(ice_wizard, troop).
has_rarity(ice_wizard, legendary).
elixir_cost(ice_wizard, 3).
in_arena(ice_wizard, spooky_town).
hitpoints(ice_wizard, 688).
damage(ice_wizard, 89).
damage_per_second(ice_wizard, 52).
transport(ice_wizard, ground).
targets(ice_wizard, air).
targets(ice_wizard, ground).
splash(ice_wizard, true).
melee_or_ranged(ice_wizard, ranged).
range_value(ice_wizard, 5).
count(ice_wizard, 1).

card(rascals, troop).
has_rarity(rascals, common).
elixir_cost(rascals, 5).
in_arena(rascals, spooky_town).
transport(rascals, ground).
targets(rascals, ground).
splash(rascals, false).
melee_or_ranged(rascals, melee).
count(rascals, 1).
% !!! WARNING: rascals is missing: hitpoints, damage, damage_per_second

card(heal_spirit, troop).
has_rarity(heal_spirit, rare).
elixir_cost(heal_spirit, 1).
in_arena(heal_spirit, rascals_hideout).
hitpoints(heal_spirit, 230).
damage(heal_spirit, 110).
transport(heal_spirit, ground).
targets(heal_spirit, air).
targets(heal_spirit, ground).
splash(heal_spirit, true).
melee_or_ranged(heal_spirit, ranged).
range_value(heal_spirit, 2).
% !!! WARNING: heal_spirit is missing: damage_per_second

card(suspicious_bush, troop).
has_rarity(suspicious_bush, rare).
elixir_cost(suspicious_bush, 2).
in_arena(suspicious_bush, rascals_hideout).
transport(suspicious_bush, ground).
targets(suspicious_bush, buildings).
splash(suspicious_bush, false).
melee_or_ranged(suspicious_bush, melee).
count(suspicious_bush, 1).
% !!! WARNING: suspicious_bush is missing: hitpoints, damage, damage_per_second

card(electro_giant, troop).
has_rarity(electro_giant, epic).
elixir_cost(electro_giant, 7).
in_arena(electro_giant, rascals_hideout).
hitpoints(electro_giant, 3855).
damage(electro_giant, 163).
damage_per_second(electro_giant, 77).
transport(electro_giant, ground).
targets(electro_giant, buildings).
splash(electro_giant, false).
melee_or_ranged(electro_giant, melee).
count(electro_giant, 1).

card(bowler, troop).
has_rarity(bowler, epic).
elixir_cost(bowler, 5).
in_arena(bowler, rascals_hideout).
hitpoints(bowler, 2081).
damage(bowler, 289).
damage_per_second(bowler, 115).
transport(bowler, ground).
targets(bowler, ground).
splash(bowler, false).
melee_or_ranged(bowler, ranged).
range_value(bowler, 4).
count(bowler, 1).

card(magic_archer, troop).
has_rarity(magic_archer, legendary).
elixir_cost(magic_archer, 4).
in_arena(magic_archer, rascals_hideout).
hitpoints(magic_archer, 529).
damage(magic_archer, 133).
damage_per_second(magic_archer, 120).
transport(magic_archer, ground).
targets(magic_archer, air).
targets(magic_archer, ground).
splash(magic_archer, false).
melee_or_ranged(magic_archer, ranged).
range_value(magic_archer, 7).
count(magic_archer, 1).

card(bandit, troop).
has_rarity(bandit, legendary).
elixir_cost(bandit, 3).
in_arena(bandit, rascals_hideout).
hitpoints(bandit, 906).
damage(bandit, 194).
damage_per_second(bandit, 194).
transport(bandit, ground).
targets(bandit, ground).
splash(bandit, false).
melee_or_ranged(bandit, melee).
count(bandit, 1).

card(lava_hound, troop).
has_rarity(lava_hound, legendary).
elixir_cost(lava_hound, 7).
in_arena(lava_hound, rascals_hideout).
hitpoints(lava_hound, 3581).
damage(lava_hound, 53).
damage_per_second(lava_hound, 40).
transport(lava_hound, air).
targets(lava_hound, buildings).
splash(lava_hound, false).
melee_or_ranged(lava_hound, ranged).
range_value(lava_hound, 3).
count(lava_hound, 1).

card(royal_chef, tower_troop).
has_rarity(royal_chef, legendary).
in_arena(royal_chef, rascals_hideout).
hitpoints(royal_chef, 2703).
damage(royal_chef, 109).
damage_per_second(royal_chef, 109).
targets(royal_chef, air).
targets(royal_chef, ground).
splash(royal_chef, false).
melee_or_ranged(royal_chef, ranged).
range_value(royal_chef, 7).

card(royal_delivery, spell).
has_rarity(royal_delivery, common).
elixir_cost(royal_delivery, 3).
in_arena(royal_delivery, serenity_peak).
damage(royal_delivery, 437).
targets(royal_delivery, air).
targets(royal_delivery, ground).
splash(royal_delivery, false).

card(elixir_golem, troop).
has_rarity(elixir_golem, rare).
elixir_cost(elixir_golem, 3).
in_arena(elixir_golem, serenity_peak).
hitpoints(elixir_golem, 1569).
damage(elixir_golem, 253).
damage_per_second(elixir_golem, 229).
transport(elixir_golem, ground).
targets(elixir_golem, buildings).
splash(elixir_golem, false).
melee_or_ranged(elixir_golem, melee).
count(elixir_golem, 1).

card(goblin_curse, spell).
has_rarity(goblin_curse, epic).
elixir_cost(goblin_curse, 2).
in_arena(goblin_curse, serenity_peak).
damage_per_second(goblin_curse, 30).
targets(goblin_curse, air).
targets(goblin_curse, ground).
splash(goblin_curse, false).
% !!! WARNING: goblin_curse is missing: damage

card(rage, spell).
has_rarity(rage, epic).
elixir_cost(rage, 2).
in_arena(rage, serenity_peak).
damage(rage, 179).
targets(rage, buildings).
splash(rage, false).

card(goblin_drill, building).
has_rarity(goblin_drill, epic).
elixir_cost(goblin_drill, 4).
in_arena(goblin_drill, serenity_peak).
hitpoints(goblin_drill, 1313).
splash(goblin_drill, false).
% !!! WARNING: goblin_drill is missing: damage, targets

card(executioner, troop).
has_rarity(executioner, epic).
elixir_cost(executioner, 5).
in_arena(executioner, serenity_peak).
hitpoints(executioner, 1280).
damage(executioner, 168).
damage_per_second(executioner, 140).
transport(executioner, ground).
targets(executioner, air).
targets(executioner, ground).
splash(executioner, false).
melee_or_ranged(executioner, ranged).
range_value(executioner, 4).
count(executioner, 1).

card(night_witch, troop).
has_rarity(night_witch, legendary).
elixir_cost(night_witch, 4).
in_arena(night_witch, serenity_peak).
hitpoints(night_witch, 906).
damage(night_witch, 314).
damage_per_second(night_witch, 241).
transport(night_witch, ground).
targets(night_witch, ground).
splash(night_witch, false).
melee_or_ranged(night_witch, melee).
count(night_witch, 1).

card(lumberjack, troop).
has_rarity(lumberjack, legendary).
elixir_cost(lumberjack, 4).
in_arena(lumberjack, serenity_peak).
hitpoints(lumberjack, 1282).
damage(lumberjack, 256).
damage_per_second(lumberjack, 320).
transport(lumberjack, ground).
targets(lumberjack, ground).
splash(lumberjack, false).
melee_or_ranged(lumberjack, melee).

card(mother_witch, troop).
has_rarity(mother_witch, legendary).
elixir_cost(mother_witch, 4).
in_arena(mother_witch, serenity_peak).
hitpoints(mother_witch, 529).
damage(mother_witch, 133).
damage_per_second(mother_witch, 133).
transport(mother_witch, ground).
targets(mother_witch, air).
targets(mother_witch, ground).
splash(mother_witch, false).
melee_or_ranged(mother_witch, ranged).
range_value(mother_witch, 5).
count(mother_witch, 1).

card(elixir_collector, building).
has_rarity(elixir_collector, rare).
elixir_cost(elixir_collector, 6).
in_arena(elixir_collector, serenity_peak).
hitpoints(elixir_collector, 1070).
splash(elixir_collector, false).
% !!! WARNING: elixir_collector is missing: targets

card(void, spell).
has_rarity(void, epic).
elixir_cost(void, 3).
in_arena(void, miners_mine).
targets(void, air).
targets(void, ground).
splash(void, false).
% !!! WARNING: void is missing: damage

card(clone, spell).
has_rarity(clone, epic).
elixir_cost(clone, 3).
in_arena(clone, miners_mine).
splash(clone, false).

card(tornado, spell).
has_rarity(tornado, epic).
elixir_cost(tornado, 3).
in_arena(tornado, miners_mine).
damage(tornado, 84).
targets(tornado, air).
targets(tornado, ground).
splash(tornado, false).

card(mirror, spell).
has_rarity(mirror, epic).
in_arena(mirror, miners_mine).
splash(mirror, false).
% !!! WARNING: mirror is missing: elixir

card(cannon_cart, troop).
has_rarity(cannon_cart, epic).
elixir_cost(cannon_cart, 5).
in_arena(cannon_cart, miners_mine).
hitpoints(cannon_cart, 1809).
damage(cannon_cart, 212).
damage_per_second(cannon_cart, 235).
transport(cannon_cart, ground).
targets(cannon_cart, ground).
splash(cannon_cart, false).
melee_or_ranged(cannon_cart, ranged).
range_value(cannon_cart, 5).
count(cannon_cart, 1).

card(spirit_empress, troop).
has_rarity(spirit_empress, legendary).
elixir_cost(spirit_empress, 6).
in_arena(spirit_empress, miners_mine).
damage(spirit_empress, 307).
splash(spirit_empress, false).
count(spirit_empress, 1).
% !!! WARNING: spirit_empress is missing: hitpoints, damage_per_second, transport, targets, range (melee/ranged)

card(goblin_machine, troop).
has_rarity(goblin_machine, legendary).
elixir_cost(goblin_machine, 5).
in_arena(goblin_machine, miners_mine).
hitpoints(goblin_machine, 2150).
damage(goblin_machine, 212).
damage_per_second(goblin_machine, 176).
transport(goblin_machine, ground).
targets(goblin_machine, ground).
splash(goblin_machine, false).
melee_or_ranged(goblin_machine, melee).
count(goblin_machine, 1).

card(fisherman, troop).
has_rarity(fisherman, legendary).
elixir_cost(fisherman, 3).
in_arena(fisherman, miners_mine).
hitpoints(fisherman, 870).
damage(fisherman, 194).
damage_per_second(fisherman, 149).
transport(fisherman, ground).
targets(fisherman, ground).
splash(fisherman, false).
melee_or_ranged(fisherman, melee).
count(fisherman, 1).

card(golden_knight, troop).
has_rarity(golden_knight, champion).
elixir_cost(golden_knight, 4).
in_arena(golden_knight, executioners_kitchen).
hitpoints(golden_knight, 1799).
damage(golden_knight, 161).
damage_per_second(golden_knight, 178).
transport(golden_knight, ground).
targets(golden_knight, ground).
splash(golden_knight, false).
melee_or_ranged(golden_knight, melee).
count(golden_knight, 1).

card(skeleton_king, troop).
has_rarity(skeleton_king, champion).
elixir_cost(skeleton_king, 4).
in_arena(skeleton_king, executioners_kitchen).
hitpoints(skeleton_king, 2298).
damage(skeleton_king, 204).
damage_per_second(skeleton_king, 127).
transport(skeleton_king, ground).
targets(skeleton_king, ground).
splash(skeleton_king, true).
melee_or_ranged(skeleton_king, melee).
count(skeleton_king, 1).

card(boss_bandit, troop).
has_rarity(boss_bandit, champion).
elixir_cost(boss_bandit, 6).
in_arena(boss_bandit, royal_crypt).
hitpoints(boss_bandit, 2624).
damage(boss_bandit, 268).
damage_per_second(boss_bandit, 223).
transport(boss_bandit, ground).
targets(boss_bandit, ground).
splash(boss_bandit, false).
melee_or_ranged(boss_bandit, melee).
count(boss_bandit, 1).

card(archer_queen, troop).
has_rarity(archer_queen, champion).
elixir_cost(archer_queen, 5).
in_arena(archer_queen, royal_crypt).
hitpoints(archer_queen, 1000).
damage(archer_queen, 225).
damage_per_second(archer_queen, 187).
transport(archer_queen, ground).
targets(archer_queen, air).
targets(archer_queen, ground).
splash(archer_queen, false).
melee_or_ranged(archer_queen, ranged).
range_value(archer_queen, 5).
count(archer_queen, 1).

card(mighty_miner, troop).
has_rarity(mighty_miner, champion).
elixir_cost(mighty_miner, 4).
in_arena(mighty_miner, royal_crypt).
hitpoints(mighty_miner, 2250).
damage(mighty_miner, 409).
damage_per_second(mighty_miner, 1022).
transport(mighty_miner, ground).
targets(mighty_miner, ground).
splash(mighty_miner, false).
melee_or_ranged(mighty_miner, melee).
count(mighty_miner, 1).

card(goblinstein, troop).
has_rarity(goblinstein, champion).
elixir_cost(goblinstein, 5).
in_arena(goblinstein, silent_sanctuary).
transport(goblinstein, ground).
targets(goblinstein, air).
targets(goblinstein, ground).
splash(goblinstein, false).
melee_or_ranged(goblinstein, ranged).
range_value(goblinstein, 5).
count(goblinstein, 1).
% !!! WARNING: goblinstein is missing: hitpoints, damage, damage_per_second

card(little_prince, troop).
has_rarity(little_prince, champion).
elixir_cost(little_prince, 3).
in_arena(little_prince, silent_sanctuary).
hitpoints(little_prince, 698).
damage(little_prince, 99).
transport(little_prince, ground).
targets(little_prince, air).
targets(little_prince, ground).
splash(little_prince, false).
melee_or_ranged(little_prince, ranged).
range_value(little_prince, 5).
count(little_prince, 1).
% !!! WARNING: little_prince is missing: damage_per_second

card(monk, troop).
has_rarity(monk, champion).
elixir_cost(monk, 5).
in_arena(monk, silent_sanctuary).
hitpoints(monk, 2150).
damage(monk, 140).
damage_per_second(monk, 175).
transport(monk, ground).
targets(monk, ground).
splash(monk, false).
melee_or_ranged(monk, melee).
count(monk, 1).
