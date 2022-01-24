from aces_high import Card, choose_best_cribbage_hand_with_score, score_cribbage_hand


def test_chooses_28():
    cards = [Card('Hearts', 'Five', 5), Card('Clubs', 'Five', 5), Card('Spades', 'Five', 5),
             Card('Hearts', 'Ten', 10), Card('Diamonds', 'Nine', 9), Card('Diamonds', 'Eight', 8)]
    hand, score = choose_best_cribbage_hand_with_score(cards)
    assert score == 14
    assert score_cribbage_hand(hand, Card('Diamonds', 'Five', 5), False) == 28


def test_chooses_29():
    cards = [Card('Hearts', 'Five', 5), Card('Clubs', 'Five', 5), Card('Spades', 'Five', 5),
             Card('Hearts', 'Ten', 10), Card('Diamonds', 'Nine', 9), Card('Diamonds', 'Jack', 10)]
    hand, score = choose_best_cribbage_hand_with_score(cards)
    assert score == 14
    assert score_cribbage_hand(hand, Card('Diamonds', 'Five', 5), False) == 28


def test_chooses_straight_8():
    cards = [Card('Clubs', 'Three', 3), Card('Hearts', 'Four', 4), Card('Spades', 'Four', 4), Card('Clubs', 'Five', 5),
             Card('Clubs', 'Seven', 7), Card('Hearts', 'Seven', 7)]
    hand, score = choose_best_cribbage_hand_with_score(cards)
    assert score == 8
    assert Card('Clubs', 'Three', 3) in hand
    assert Card('Hearts', 'Four', 4) in hand
    assert Card('Spades', 'Four', 4) in hand
    assert Card('Clubs', 'Five', 5) in hand
