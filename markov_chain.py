import random
import numpy as np
from collections import defaultdict

class LanguageMarkovChain:
    '''
    @neighbors: dict of token to (dict of neighbor to count)
    Every token consists of one or more words
    '''
    def __init__(self, text):
        words = text.split()
        n = len(words)
        self.neighbors = defaultdict(lambda: defaultdict(int))
        total_occurrences = defaultdict(int)
        for i in range(n-1):
            self.neighbors[words[i]][words[i+1]] += 1
            total_occurrences[words[i]] += 1
        for token, neighbors in self.neighbors.items():
            options, weights = list(zip(*neighbors.items()))
            options, weights = list(options), list(weights)
            weights = [float(w) / total_occurrences[token] for w in weights]
            self.neighbors[token] = (options, weights)
        self.reset()
        return

    def reset(self):
        self.current_token = np.random.choice([x for x in self.neighbors.keys() if x[0].isupper()])
        return

    def get_neighbors(self, token):
        return self.neighbors.get(token, ())

    def __get__(self, token):
        return self.get_neighbors(token)

    def __iter__(self):
        while True:
            yield self.current_token
            try:
                options, weights = self.get_neighbors(self.current_token)
                self.current_token = np.random.choice(options, p=weights)
            except (IndexError, ValueError) as e:
                # print(e)
                raise StopIteration
        return
