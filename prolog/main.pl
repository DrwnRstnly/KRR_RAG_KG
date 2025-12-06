:- consult('rules.pl').
:- consult('cards.pl').

start :-
    write('Welcome to the Clash Royale Deck Analyzer!'), nl,
    write('Please enter your 8 card names, one per line.'), nl,
    write('---'), nl,
    read_deck(8, [], Deck),
    nl,
    analyze_deck(Deck),
    nl,
    write('Analysis complete. Enter start. to analyze another deck.'), nl.

read_deck(0, Acc, Deck) :-
    reverse(Acc, Deck),
    write('---'), nl,
    write('Deck accepted. Analyzing...'), nl.

read_deck(N, Acc, Deck) :-
    N > 0,
    CardNum is 9 - N,
    format('Enter card ~w: ', [CardNum]),
    read_line_to_string(user_input, String),
    atom_string(Atom, String),

    ( card(Atom, _) ->
        NewN is N - 1,
        read_deck(NewN, [Atom | Acc], Deck)
    ;
        write('Error: "'), write(Atom), write('" is not a valid card. Please try again.'), nl,
        read_deck(N, Acc, Deck)
    ).