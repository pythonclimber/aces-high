import os
import time
from random import randrange

import click

from .cribtools import choose_best_cribbage_hand_with_score
from .deck import Deck
from .scorers import score_cribbage_hand, score_poker_hand, PokerHands


class StopWatch:
    def __init__(self):
        self._start = 0
        self._stop = 0

    def __enter__(self):
        self.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def start(self):
        self._start = time.time()

    def stop(self):
        self._stop = time.time()

    def display_elapsed(self):
        print(f'Start-{self._start} : Stop-{self._stop} : Difference-{self._stop - self._start}-seconds')


def create_data_directory():
    if not os.path.exists('data'):
        os.mkdir('data')


def cribbage_tests(max_iterations):
    scores = {i: 0 for i in range(0, 30)}
    stopwatch = StopWatch()

    with stopwatch:
        for i in range(0, max_iterations):
            deck = Deck().full_shuffle()

            cards = [deck.deal() for _ in range(6)]
            card = deck.deal()

            hand, pre_turn_score = choose_best_cribbage_hand_with_score(cards)
            score = score_cribbage_hand(hand, card)

            # print(cards)
            # print(hand, card, pre_turn_score, score)
            scores[score] += 1

            if score in [28, 29]:
                print(f'Found a 29-point hand at {i}')

            if i % 10000 == 0:
                print(i)

    [print(f'{key}: {value}: {(value / (max_iterations * 1.0)) * 100}') for key, value in scores.items()]
    stopwatch.display_elapsed()


def crib_collect(max_iterations):
    with open('data/cribbage_hands.txt', 'a') as file:
        for _ in range(max_iterations):
            deck = Deck().full_shuffle()
            full_hand = [deck.deal() for _ in range(6)]
            crib_hand, pre_cut_score = choose_best_cribbage_hand_with_score(full_hand)
            passed_to_crib = [card for card in full_hand if card not in crib_hand]
            cut_card = deck[randrange(len(deck))]
            score = score_cribbage_hand(crib_hand, cut_card)

            file.write('{}|{}|{}|{}|{}|{}\n'.format(
                full_hand,
                crib_hand,
                cut_card,
                passed_to_crib,
                pre_cut_score,
                score
            ))


def poker_tests(max_iterations):
    results = {hand_type: 0 for hand_type in PokerHands.get_all()}
    stopwatch = StopWatch()

    with stopwatch:
        for _ in range(max_iterations):
            deck = Deck().full_shuffle()
            hand1 = []
            for _ in range(5):
                hand1.append(deck.deal())
                [deck.deal() for _ in range(4)]
            score1 = score_poker_hand(hand1)
            hand_type = PokerHands.get_by_value(score1)
            results[hand_type] += 1

    [print(f'{key}: {value}: {((value / (max_iterations * 1.0)) * 100):.2f}%') for key, value in results.items()]
    stopwatch.display_elapsed()


test_functions = {
    'cribbage': cribbage_tests,
    'crib_collect': crib_collect,
    'poker': poker_tests
}


@click.command()
@click.option('-md', '--mode', required=True, type=str)
@click.option('-max', '--max_iterations', required=False, type=int)
def run_process(mode, max_iterations):
    try:
        max_iterations = 10000 if max_iterations is None else max_iterations
        test_function = test_functions[mode]
        test_function(max_iterations)
    except KeyError:
        raise ValueError('Invalid mode provided')


if __name__ == '__main__':
    run_process()
