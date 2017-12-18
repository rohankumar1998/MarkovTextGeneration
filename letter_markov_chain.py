import random
import numpy as np
from collections import defaultdict

def defaultdict_int():
    return defaultdict(int)

class LetterMarkovChain:
    '''
    @neighbors: dict of token to (dict of neighbor to count)
    Every token consists of one or more letters
    '''
    def __init__(self, text, order=1):
        n = len(text)
        self.neighbors = defaultdict(defaultdict_int)
        total_occurrences = defaultdict(int)
        for i in range(n):
            token = text[i:i+order]
            neighbor = text[i+order:i+2*order]
            # consider wrap around to prevent neighbor-less tokens
            if i >= n-order+1:
                token = text[i:] + text[:(i+order)%n]
                neighbor = text[(i+order)%n:(i+2*order)%n]
            elif i >= n-2*order+1:
                neighbor = text[i+order:] + text[:(i+2*order)%n]
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
        return self.neighbors.get(token, ([], []))

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
