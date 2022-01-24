from .scorers import score_cribbage_hand
from itertools import combinations


class Player:
    def __init__(self):
        self.cards = list()

    def take_card(self, card):
        self.cards.append(card)

    def take_cards(self, cards):
        self.cards += cards


class CribbagePlayer(Player):
    def __init__(self, is_computer=False):
        super().__init__()
        self.score = 0
        self.is_computer = is_computer

    def score_hand(self, turn_card):
        print(f'Old score: {self.score}')
        score = score_cribbage_hand(self.cards, turn_card, False)
        print(f'Hand score: {score}')
        self.score += score
        print(f'New score: {self.score}')

    def get_cards_for_crib(self):
        combos = combinations(self.cards, 4)
        print(combos)
        print(f'Combinations: {len(combos)}')
