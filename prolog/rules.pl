%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Rules Engine
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% -------------------------------
% Derived rules (reasoning)
% -------------------------------

is_wincon_card(Card) :-
    targets(Card, buildings).

is_wincon_card(Card) :-
    member(Card, [x_bow, mortar, goblin_drill, rocket, graveyard, goblin_barrel, miner]).

can_hit_air(Card) :-
    targets(Card, air).

is_spell(Card) :-
    card(Card, spell).

get_elixir_costs(Deck, Costs) :-
    findall(Cost, (member(Card, Deck), elixir_cost(Card, Cost)), Costs).

calculate_avg_elixir(Deck, Avg) :-
    get_elixir_costs(Deck, Costs),
    sum_list(Costs, Sum),
    ( length(Costs, 8) ->
          Avg is Sum / 8.0
    ; Avg = 0
    ).

is_anti_tank(Card) :-
    member(Card, [mighty_miner, sparky, pekka, inferno_dragon, prince, hunter, three_musketeers, inferno_tower, mini_p_e_k_k_a, elite_barbarians, skeleton_army, goblins, goblin_gang, guards, minion_horde]).

is_small_spell(Card) :-
    is_spell(Card),
    elixir_cost(Card, Cost),
    Cost =< 3.

is_big_spell(Card) :-
    is_spell(Card),
    elixir_cost(Card, Cost),
    Cost > 3.

is_building(Card) :-
    card(Card, building).

is_reset_card(Card) :-
    member(Card, [electro_spirit, electro_wizard, electro_dragon, zap, vines, ice_spirit, lightning, freeze]).

is_tank_or_mini_tank(Card) :-
    card(Card, troop),
    hitpoints(Card, HP),
    HP > 1000.

is_swarm_card(Card) :-
    count(Card, Count),
    Count >= 3.

is_cycle_card(Card) :-
    elixir_cost(Card, Cost),
    Cost =< 2.

is_heavy_tank(Card) :-
    (card(Card, troop) ; card(Card, building)),
    hitpoints(Card, HP),
    HP > 3000.

is_siege_building(Card) :-
    member(Card, [x_bow, mortar]).

is_spell_bait(Card) :-
    member(Card, [goblin_barrel, goblin_gang, skeleton_barrel, suspicious_bush]).

is_spell_bait(Card) :-
    (card(Card, troop) ; card(Card, building)),
    hitpoints(Card, HP),
    HP < 500.

is_bridge_spam_card(Card) :-
    member(Card, [magic_archer, ram_rider, lumberjack, royal_ghost, bandit, prince, pekka, goblin_giant, electro_giant, princess, balloon, royal_hogs, hog_rider, dart_goblin, elite_barbarians, royal_recruits, royal_giant, wall_breakers]).

is_heavy_spell(Card) :-
    member(Card, [fireball, poison, lightning, rocket]).

is_building_killer_spell(Card) :-
    is_heavy_spell(Card).
is_building_killer_spell(Card) :-
    Card = earthquake.

is_cycle_wincon(Card) :-
    is_wincon_card(Card),
    (Card = royal_hogs ; (elixir_cost(Card, Cost), Cost =< 4)).

is_ranged_troop(Card) :-
    card(Card, troop),
    melee_or_ranged(Card, ranged).

info(Card) :-
    card(Card, Type),
    write('Card: '), write(Card), nl,
    write('Type: '), write(Type), nl,
    (has_rarity(Card, Rarity) -> format('Rarity: ~w~n',[Rarity]) ; true),
    (elixir_cost(Card, Cost) -> format('Elixir: ~w~n',[Cost]) ; true),
    (hitpoints(Card, HP) -> format('HP: ~w~n',[HP]) ; true),
    (damage(Card, Dmg) -> format('Damage: ~w~n',[Dmg]) ; true),
    (has_speed_class(Card, Spd) -> format('Speed: ~w~n',[Spd]) ; true),
    nl.

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Archetype Classification Logic
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

classify_archetype(Deck, siege) :-
    findall(C, (member(C, Deck), is_siege_building(C)), List),
    length(List, Count),
    Count > 0, !.

classify_archetype(Deck, bait) :-
    findall(C, (member(C, Deck), is_spell_bait(C)), List),
    length(List, Count),
    Count >= 3, !.

classify_archetype(Deck, bridge_spam) :-
    findall(C, (member(C, Deck), is_bridge_spam_card(C)), List),
    length(List, Count),
    Count >= 3, !.

classify_archetype(Deck, cycle) :-
    calculate_avg_elixir(Deck, Avg),
    Avg > 0,
    Avg =< 3.0, !.

classify_archetype(Deck, beatdown) :-
    findall(C, (member(C, Deck), is_heavy_tank(C)), List),
    length(List, Count),
    Count > 0, !.

classify_archetype(_, 'No Archetype').

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Deck Analysis Logic
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

warning_info(no_win_condition, strong, 'No win condition - Deck has no clear path to tower damage.').
warning_info(no_air_defense, strong, 'No air defense - Vulnerable to air-heavy decks (Lava Hound, Balloon, etc.).').
warning_info(no_spell, strong, 'No spell - Cannot deal spell damage or respond to swarms effectively.').
warning_info(no_ground_units, strong, 'No ground units - Deck contains only spells and cannot defend.').
warning_info(too_many_win_cons, strong, '> 2 win conditions - Deck lacks support/defense due to too many win cons.').
warning_info(too_many_spells, strong, '> 4 spells - Not enough troops to defend or push.').
warning_info(too_expensive, strong, 'Elixir average >= 4.8 - Too slow to cycle, vulnerable to fast decks.').
warning_info(no_anti_tank, strong, 'No anti-tank option - Cannot defend against heavy tanks (e.g., P.E.K.K.A, Golem).').

warning_info(no_small_spell, weak, 'No small spell (<= 3 Elixir) - Struggles with swarms and chip.').
warning_info(no_big_spell, weak, 'No big spell (> 3 Elixir) - Limited high spell damage and tower pressure.').
warning_info(no_building, weak, 'No building - Harder to defend and control tempo.').
warning_info(one_air_defense, weak, 'Only 1 air defense card - Risky against air-heavy decks.').
warning_info(no_reset_card, weak, 'No reset card (e.g., Zap, E-Wiz) - Vulnerable to Inferno Tower/Dragon, Sparky.').
warning_info(no_tank, weak, 'No tank or mini-tank - Difficulty absorbing damage for support troops.').
warning_info(no_splash, weak, 'No splash damage - Struggles against swarm-heavy decks.').
warning_info(no_swarm, weak, 'No swarm cards - Limited defensive versatility.').
warning_info(too_cheap, weak, 'Elixir average <= 2.6 - May lack defensive power against heavy pushes.').
warning_info(no_cheap_cycle, weak, 'No cheap cycle cards (1-2 elixir) - Slower cycle to win condition.').

warning_info(siege_no_secondary_building, strong, 'No secondary defensive building - Siege decks need a second building for defense.').
warning_info(siege_no_anti_tank, strong, 'No anti-tank option - Vulnerable to P.E.K.K.A, Giant, etc.').
warning_info(siege_no_building_killer, strong, 'No building killer spell - No heavy spell (Rocket, Lightning, Fireball, Poison) or Earthquake to damage defensive buildings.').
warning_info(siege_too_expensive, weak, 'Average elixir > 3.8 - Too slow to defend and cycle your siege building.').
warning_info(siege_not_enough_cycle, weak, '< 2 cycle cards (<= 2 Elixir) - Can\'t cycle back to your siege building fast enough.').
warning_info(siege_no_tank, weak, 'No tank/mini-tank - No card to protect your X-Bow or Mortar.').
warning_info(siege_no_alt_wincon, weak, 'No heavy spell wincon - Lacks a secondary win condition (e.g., Rocket) to get tower damage.').

warning_info(bait_has_heavy_tank, strong, 'Presence of heavy tank - Conflicts with bait strategy.').
warning_info(bait_no_mini_tank, weak, 'No mini-tank - Lacks a ground tank for defense and to protect bait units.').
warning_info(bait_no_cycle, weak, 'No cycle cards (<= 2 Elixir) - Slower cycle to your bait win condition.').
warning_info(bait_too_many_big_spells, weak, '2 or more big spells (> 3 Elixir) - Reduces the number of bait troops.').

warning_info(cycle_heavy_wincon, strong, 'Win condition costs > 4 elixir - Too heavy to cycle quickly (exception: Royal Hogs).').
warning_info(cycle_too_heavy, strong, '> 3 cards cost 4+ elixir - Deck may be too heavy for a cycle archetype.').
warning_info(cycle_no_building, strong, 'No defensive building - Cycle decks rely on a building for solid defense.').
warning_info(cycle_not_enough_cycle, weak, '< 2 cycle cards (<= 2 Elixir) - Not fast enough for a true cycle deck.').

warning_info(beatdown_no_ranged, strong, 'No ranged troops - Beatdown pushes lack crucial support from behind the tank.').
warning_info(beatdown_too_cheap, strong, 'Average elixir < 3.5 - Insufficient elixir for a proper beatdown push.').
warning_info(beatdown_expensive_no_pump, strong, 'Average elixir >= 4.3 and no Elixir Collector - Deck is too expensive to function without elixir generation.').
warning_info(beatdown_no_reset, strong, 'No reset units - Vulnerable to Inferno Tower/Dragon and Sparky.').
warning_info(beatdown_too_many_spells, weak, 'More than 2 spells - Reduces push potential and defensive troops.').

warning_info(bridgespam_too_expensive, strong, 'Average elixir > 4.3 - Too slow for consistent bridge spam pressure.').
warning_info(bridgespam_not_enough_cycle, strong, 'No cycle cards (<= 2 Elixir) - Cannot cycle pressure cards fast enough.').
warning_info(bridgespam_too_many_spells, weak, '>= 3 spells - Not enough units to apply constant pressure.').

format_warning(strong, Text, FinalString) :-
    format(string(FinalString), 'Strong Warning: ~w', [Text]).

format_warning(weak, Text, FinalString) :-
    format(string(FinalString), 'Weak Warning: ~w', [Text]).


check_for_warning(Deck, FinalWarningString) :-
    \+ (member(Card, Deck), is_wincon_card(Card)),
    warning_info(no_win_condition, Type, Text),
    format_warning(Type, Text, FinalWarningString).

check_for_warning(Deck, FinalWarningString) :-
    \+ (member(Card, Deck), can_hit_air(Card)),
    warning_info(no_air_defense, Type, Text),
    format_warning(Type, Text, FinalWarningString).

check_for_warning(Deck, FinalWarningString) :-
    \+ (member(Card, Deck), is_spell(Card)),
    warning_info(no_spell, Type, Text),
    format_warning(Type, Text, FinalWarningString).

check_for_warning(Deck, FinalWarningString) :-
    \+ (member(Card, Deck), transport(Card, ground)),
    warning_info(no_ground_units, Type, Text),
    format_warning(Type, Text, FinalWarningString).

check_for_warning(Deck, FinalWarningString) :-
    findall(Card, (member(Card, Deck), is_wincon_card(Card)), WinCons),
    length(WinCons, Count),
    Count > 2,
    warning_info(too_many_win_cons, Type, Text),
    format_warning(Type, Text, FinalWarningString).

check_for_warning(Deck, FinalWarningString) :-
    findall(Card, (member(Card, Deck), is_spell(Card)), Spells),
    length(Spells, Count),
    Count > 4,
    warning_info(too_many_spells, Type, Text),
    format_warning(Type, Text, FinalWarningString).

check_for_warning(Deck, FinalWarningString) :-
    calculate_avg_elixir(Deck, Avg),
    Avg >= 4.8,
    warning_info(too_expensive, Type, Text),
    format_warning(Type, Text, FinalWarningString).

check_for_warning(Deck, FinalWarningString) :-
    \+ (member(Card, Deck), is_anti_tank(Card)),
    warning_info(no_anti_tank, Type, Text),
    format_warning(Type, Text, FinalWarningString).

check_for_warning(Deck, FinalWarningString) :-
    \+ (member(Card, Deck), is_small_spell(Card)),
    warning_info(no_small_spell, Type, Text),
    format_warning(Type, Text, FinalWarningString).

check_for_warning(Deck, FinalWarningString) :-
    \+ (member(Card, Deck), is_big_spell(Card)),
    warning_info(no_big_spell, Type, Text),
    format_warning(Type, Text, FinalWarningString).

check_for_warning(Deck, FinalWarningString) :-
    \+ (member(Card, Deck), is_building(Card)),
    warning_info(no_building, Type, Text),
    format_warning(Type, Text, FinalWarningString).

check_for_warning(Deck, FinalWarningString) :-
    findall(Card, (member(Card, Deck), can_hit_air(Card)), AirCards),
    length(AirCards, 1),
    warning_info(one_air_defense, Type, Text),
    format_warning(Type, Text, FinalWarningString).

check_for_warning(Deck, FinalWarningString) :-
    \+ (member(Card, Deck), is_reset_card(Card)),
    warning_info(no_reset_card, Type, Text),
    format_warning(Type, Text, FinalWarningString).

check_for_warning(Deck, FinalWarningString) :-
    \+ (member(Card, Deck), is_tank_or_mini_tank(Card)),
    warning_info(no_tank, Type, Text),
    format_warning(Type, Text, FinalWarningString).

check_for_warning(Deck, FinalWarningString) :-
    \+ (member(Card, Deck), splash(Card, true)),
    warning_info(no_splash, Type, Text),
    format_warning(Type, Text, FinalWarningString).

check_for_warning(Deck, FinalWarningString) :-
    \+ (member(Card, Deck), is_swarm_card(Card)),
    warning_info(no_swarm, Type, Text),
    format_warning(Type, Text, FinalWarningString).

check_for_warning(Deck, FinalWarningString) :-
    calculate_avg_elixir(Deck, Avg),
    Avg > 0,
    Avg =< 2.6,
    warning_info(too_cheap, Type, Text),
    format_warning(Type, Text, FinalWarningString).

check_for_warning(Deck, FinalWarningString) :-
    \+ (member(Card, Deck), is_cycle_card(Card)),
    warning_info(no_cheap_cycle, Type, Text),
    format_warning(Type, Text, FinalWarningString).

check_for_archetype_warning(Deck, siege, FinalWarningString) :-
    \+ (member(Card, Deck), is_building_killer_spell(Card)),
    warning_info(siege_no_building_killer, Type, Text),
    format_warning(Type, Text, FinalWarningString).

check_for_archetype_warning(Deck, siege, FinalWarningString) :-
    findall(C, (member(C, Deck), is_building(C)), Buildings),
    length(Buildings, Count),
    Count < 2,
    warning_info(siege_no_secondary_building, Type, Text),
    format_warning(Type, Text, FinalWarningString).

check_for_archetype_warning(Deck, siege, FinalWarningString) :-
    \+ (member(Card, Deck), is_anti_tank(Card)),
    warning_info(siege_no_anti_tank, Type, Text),
    format_warning(Type, Text, FinalWarningString).

check_for_archetype_warning(Deck, siege, FinalWarningString) :-
    calculate_avg_elixir(Deck, Avg),
    Avg > 3.8,
    warning_info(siege_too_expensive, Type, Text),
    format_warning(Type, Text, FinalWarningString).

check_for_archetype_warning(Deck, siege, FinalWarningString) :-
    findall(C, (member(C, Deck), is_cycle_card(C)), CycleCards),
    length(CycleCards, Count),
    Count < 1,
    warning_info(siege_not_enough_cycle, Type, Text),
    format_warning(Type, Text, FinalWarningString).

check_for_archetype_warning(Deck, siege, FinalWarningString) :-
    \+ (member(Card, Deck), is_tank_or_mini_tank(Card)),
    warning_info(siege_no_tank, Type, Text),
    format_warning(Type, Text, FinalWarningString).

check_for_archetype_warning(Deck, siege, FinalWarningString) :-
    \+ (member(Card, Deck), is_heavy_spell(Card)),
    warning_info(siege_no_alt_wincon, Type, Text),
    format_warning(Type, Text, FinalWarningString).

check_for_archetype_warning(Deck, bait, FinalWarningString) :-
    (member(Card, Deck), is_heavy_tank(Card)),
    warning_info(bait_has_heavy_tank, Type, Text),
    format_warning(Type, Text, FinalWarningString).

check_for_archetype_warning(Deck, bait, FinalWarningString) :-
    \+ (member(Card, Deck), is_tank_or_mini_tank(Card)),
    warning_info(bait_no_mini_tank, Type, Text),
    format_warning(Type, Text, FinalWarningString).

check_for_archetype_warning(Deck, bait, FinalWarningString) :-
    \+ (member(Card, Deck), is_cycle_card(Card)),
    warning_info(bait_no_cycle, Type, Text),
    format_warning(Type, Text, FinalWarningString).

check_for_archetype_warning(Deck, bait, FinalWarningString) :-
    findall(C, (member(C, Deck), is_big_spell(C)), Spells),
    length(Spells, Count),
    Count >= 2,
    warning_info(bait_too_many_big_spells, Type, Text),
    format_warning(Type, Text, FinalWarningString).

check_for_archetype_warning(Deck, cycle, FinalWarningString) :-
    \+ (member(Card, Deck), is_cycle_wincon(Card)),
    (member(Card, Deck), is_wincon_card(Card)),
    warning_info(cycle_heavy_wincon, Type, Text),
    format_warning(Type, Text, FinalWarningString).

check_for_archetype_warning(Deck, cycle, FinalWarningString) :-
    findall(C, (member(C, Deck), elixir_cost(C, Cost), Cost >= 4), HeavyCards),
    length(HeavyCards, Count),
    Count > 3,
    warning_info(cycle_too_heavy, Type, Text),
    format_warning(Type, Text, FinalWarningString).

check_for_archetype_warning(Deck, cycle, FinalWarningString) :-
    \+ (member(Card, Deck), is_building(Card)),
    warning_info(cycle_no_building, Type, Text),
    format_warning(Type, Text, FinalWarningString).

check_for_archetype_warning(Deck, cycle, FinalWarningString) :-
    findall(C, (member(C, Deck), is_cycle_card(C)), CycleCards),
    length(CycleCards, Count),
    Count < 2,
    warning_info(cycle_not_enough_cycle, Type, Text),
    format_warning(Type, Text, FinalWarningString).

check_for_archetype_warning(Deck, beatdown, FinalWarningString) :-
    \+ (member(Card, Deck), is_ranged_troop(Card)),
    warning_info(beatdown_no_ranged, Type, Text),
    format_warning(Type, Text, FinalWarningString).

check_for_archetype_warning(Deck, beatdown, FinalWarningString) :-
    calculate_avg_elixir(Deck, Avg),
    Avg > 0,
    Avg < 3.5,
    warning_info(beatdown_too_cheap, Type, Text),
    format_warning(Type, Text, FinalWarningString).

check_for_archetype_warning(Deck, beatdown, FinalWarningString) :-
    calculate_avg_elixir(Deck, Avg),
    Avg >= 4.3,
    \+ member(elixir_collector, Deck),
    warning_info(beatdown_expensive_no_pump, Type, Text),
    format_warning(Type, Text, FinalWarningString).

check_for_archetype_warning(Deck, beatdown, FinalWarningString) :-
    \+ (member(Card, Deck), is_reset_card(Card)),
    warning_info(beatdown_no_reset, Type, Text),
    format_warning(Type, Text, FinalWarningString).

check_for_archetype_warning(Deck, beatdown, FinalWarningString) :-
    findall(C, (member(C, Deck), is_spell(C)), Spells),
    length(Spells, Count),
    Count > 2,
    warning_info(beatdown_too_many_spells, Type, Text),
    format_warning(Type, Text, FinalWarningString).

check_for_archetype_warning(Deck, bridge_spam, FinalWarningString) :-
    calculate_avg_elixir(Deck, Avg),
    Avg > 4.3,
    warning_info(bridgespam_too_expensive, Type, Text),
    format_warning(Type, Text, FinalWarningString).

check_for_archetype_warning(Deck, bridge_spam, FinalWarningString) :-
    findall(C, (member(C, Deck), is_cycle_card(C)), CycleCards),
    length(CycleCards, Count),
    Count < 2,
    warning_info(bridgespam_not_enough_cycle, Type, Text),
    format_warning(Type, Text, FinalWarningString).

check_for_archetype_warning(Deck, bridge_spam, FinalWarningString) :-
    findall(C, (member(C, Deck), is_spell(C)), Spells),
    length(Spells, Count),
    Count >= 3,
    warning_info(bridgespam_too_many_spells, Type, Text),
    format_warning(Type, Text, FinalWarningString).


find_warnings(Deck, Archetype, GeneralWarnings, ArchetypeWarnings) :-
    findall(W, check_for_warning(Deck, W), GeneralWarnings),
    findall(AW, check_for_archetype_warning(Deck, Archetype, AW), ArchetypeWarnings).

display_warnings(GeneralWarnings, ArchetypeWarnings) :-
    write('--- General Warnings ---'), nl,
    print_warning_list(GeneralWarnings),
    nl,
    write('--- Archetype-Specific Warnings ---'), nl,
    print_warning_list(ArchetypeWarnings).

print_warning_list([]) :-
    write('  (None)'), nl.
print_warning_list([Head | Tail]) :-
    print_warning_list_items([Head | Tail]).

print_warning_list_items([]).
print_warning_list_items([Head | Tail]) :-
    write('- '), write(Head), nl,
    print_warning_list_items(Tail).

analyze_deck(Deck) :-
    length(Deck, 8),
    write('Analyzing deck: '), write(Deck), nl,
    write('---'), nl,
    
    classify_archetype(Deck, Archetype),
    calculate_avg_elixir(Deck, Avg),
    
    format('Deck Archetype: ~w~n', [Archetype]),
    format('Average Elixir: ~1f~n', [Avg]),
    nl,
    
    find_warnings(Deck, Archetype, GeneralWarnings, ArchetypeWarnings),
    display_warnings(GeneralWarnings, ArchetypeWarnings),
    write('---'), nl.

analyze_deck(Deck) :-
    \+ length(Deck, 8),
    write('Error: Deck must contain exactly 8 cards.'), nl.