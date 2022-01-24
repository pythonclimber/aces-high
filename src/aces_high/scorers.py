from itertools import combinations
from typing import List

from .deck import Card


full_house_types = {
    'three_low': 0,
    'three_high': 1
}


class PokerHands:
    HIGH_CARD = 0
    PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    STRAIGHT = 4
    FLUSH = 5
    FULL_HOUSE = 6
    FOUR_OF_A_KIND = 7
    STRAIGHT_FLUSH = 8

    @staticmethod
    def get_all() -> List[str]:
        return ['HIGH_CARD', 'PAIR', 'TWO_PAIR', 'THREE_OF_A_KIND', 'STRAIGHT',
                'FLUSH', 'FULL_HOUSE', 'FOUR_OF_A_KIND', 'STRAIGHT_FLUSH']

    @classmethod
    def get(cls, name: str) -> int:
        return cls.__getattribute__(cls, name)

    @classmethod
    def get_by_value(cls, value: int) -> str:
        values_with_hand = {cls.get(hand): hand for hand in cls.get_all()}
        return values_with_hand[value]


def score_poker_hand(cards: list) -> int:
    temp_cards = sorted(cards, key=lambda card: card.value)
    values = {c1.face: sum(1 for c2 in cards if c1.value == c2.value) for c1 in cards}
    suits = {card.suit for card in cards}
    value_count = len(values)

    if value_count == 5:
        is_straight = is_a_poker_straight(temp_cards)
        is_flush = len(suits) == 1

        if not is_straight and not is_flush:
            return PokerHands.HIGH_CARD
        if is_straight and is_flush:
            return PokerHands.STRAIGHT_FLUSH
        elif is_straight:
            return PokerHands.STRAIGHT
        elif is_flush:
            return PokerHands.FLUSH
    else:
        if value_count == 4:
            return PokerHands.PAIR
        if value_count == 3:
            is_two_pair = len([key for (key, value) in values.items() if value == 2]) == 2
            return PokerHands.TWO_PAIR if is_two_pair else PokerHands.THREE_OF_A_KIND
        if value_count == 2:
            is_four_kind = len([key for (key, value) in values.items() if value == 4]) > 0
            return PokerHands.FOUR_OF_A_KIND if is_four_kind else PokerHands.FULL_HOUSE


def score_cribbage_hand(cards: list, cut_card: Card = None, is_crib: bool = False) -> int:
    score = 0
    temp_cards = [card for card in cards]
    run_counts = {i: 0 for i in range(3, 6)}

    score += count_flush(temp_cards, is_crib, cut_card)

    if cut_card is not None:
        score += count_nobs(temp_cards, cut_card)
        temp_cards.append(cut_card)

    sum_values = [c.value if c.value < 10 else 10 for c in temp_cards]
    values = [c.value for c in temp_cards]

    # this is a complicated statement.  It calculates the points for pairs, runs, and combos of 15 all in one loop
    # for efficiency
    for i in range(2, len(temp_cards) + 1):
        # calculate all sums for i number of cards.  Score 2 points for any sum of 15
        sums = [sum(c) for c in combinations(sum_values, i)]
        score += sum(2 for s in sums if s == 15)

        if i == 2:
            set_points = sum(2 for x, y in combinations(values, 2) if x == y)
            score += set_points
        else:
            sorted_combos = [c for c in combinations(values, i)]
            runs = [True for sc in sorted_combos if (max(sc) - min(sc) + 1) == len(sc) and len(set(sc)) == len(sc)]
            score += len(runs) * i
            run_counts[i] = len(runs)
            if i > 3 and len(runs) > 0:
                score -= run_counts[i - 1] * (i - 1)  # undo previous runs as new runs invalidated it

    return score


def is_a_poker_straight(sorted_cards: list) -> bool:
    max_value = sorted_cards[-1].value
    min_value = sorted_cards[0].value
    contains_ace = any([c.face == "Ace" for c in sorted_cards])
    contains_king = any([c.face == "King" for c in sorted_cards])

    if (max_value - min_value == 4) or (contains_ace and contains_king):
        start = 2 if contains_ace and contains_king else 1
        for i in range(start, len(sorted_cards)):
            if sorted_cards[i].value - sorted_cards[i - 1].value != 1:
                return False

        return True

    return False


def count_nobs(cards: list, turn_card: Card) -> int:
    nob_cards = [True for card in cards if card.face == "Jack" and card.suit == turn_card.suit]
    return 1 if any(nob_cards) else 0


def count_flush(cards: list, is_crib: bool, turn_card: Card = None) -> int:
    suits = {c1.suit: 1 for c1 in cards}

    if len(suits) == 1:
        if turn_card is not None and any(True for key in suits.keys() if key == turn_card.suit):
            return 5
        else:
            return 4 if not is_crib else 0

    return 0
