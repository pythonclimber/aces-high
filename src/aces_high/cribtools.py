from itertools import combinations

from .scorers import score_cribbage_hand


def choose_best_cribbage_hand_with_score(cards: list) -> tuple:
    max_score = -1
    best_hand = None
    for combo in combinations(cards, 4):
        current_score = score_cribbage_hand(combo)
        if current_score > max_score:
            best_hand = combo
            max_score = current_score

    return best_hand, max_score
