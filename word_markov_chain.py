import random
import numpy as np
from collections import defaultdict

def defaultdict_int():
    return defaultdict(int)

class WordMarkovChain:
    '''
    @neighbors: dict of token to (dict of neighbor to count)
    Every token consists of one or more words
    '''
    def __init__(self, text, order=1):
        words = text.split()
        n = len(words)
        self.neighbors = defaultdict(defaultdict_int)
        total_occurrences = defaultdict(int)
        for i in range(n-1):
            for j in range(max(0,i-order+1), i+1):
                token = ' '.join(words[j:i+1])
                # print('Token found:', token, 'with neighbors:')
                for k in range(i+1, min(i+order+1, n)):
                    neighbor = ' '.join(words[i+1:k+1])
                    # print('\t', neighbor)
                    self.neighbors[token][neighbor] += 1
                    total_occurrences[token] += 1
        for token, neighbors in self.neighbors.items():
            options, weights = list(zip(*neighbors.items()))
            options, weights = list(options), list(weights)
            weights = [float(w) / total_occurrences[token] for w in weights]
            self.neighbors[token] = (options, weights)
        self.reset()
        return

    def reset(self):
        try:
            self.current_token = np.random.choice([x for x in self.neighbors.keys() if x and x[0].isupper()])
        except ValueError as e:
            self.current_token = np.random.choice([x for x in self.neighbors.keys()])
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
