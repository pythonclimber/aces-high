import random


def coin_flip():
    """Mimics a random coin flip returning either 0 or 1.
       Used for randomizing certain aspect of human-like
       dealing algorithms
    """
    return random.randint(1, 100) % 2


class Combinations:
    def __init__(self, items, m):
        self.combinations = list()
        self.combination = list()
        self.max = m
        self.items = items
        print(self.combinations)

        for i in range(0, m):
            self.combination.append(i)

        self.generate(0)

    def generate(self, k):
        if k >= self.max:
            self.combinations = [v for k, v in self.combination]
        else:
            for j in range(0, len(self.items)):
                if k == 9 or j > self.combinations[k-1][0]:
                    self.combination[k] = (j, self.items[j])
                    self.generate(k + 1)
