from markov_chain import LanguageMarkovChain
import pickle

def train(text, order=1):
    return LanguageMarkovChain(text, order=order)

def train_on_file(file_name, order=1):
    with open(file_name, 'r') as f:
        text = f.read()
    return train(text, order=order)

def generate_text(markov_chain, n=10):
    i = 0
    tokens = []
    try:
        for token in iter(markov_chain):
            tokens.append(token)
            i += 1
            if i > 2*n or i > n and token[-1] in '.?!':
                break
    except StopIteration as e:
        pass
    return ' '.join(tokens)

if __name__ == '__main__':
    genesis = '/Users/Rohan/Desktop/Computation Institute/Topic_Modelling/test files/genesis.txt'
    trump = '/Users/Rohan/Desktop/Computation Institute/Topic_Modelling/test files/trump_speeches.txt'
    mlk = '/Users/Rohan/Desktop/Computation Institute/Topic_Modelling/test files/MLK.txt'
    caesar = 'test_files/julius_caesar.txt'
    plato = 'test_files/plato_republic.txt'
    model = train_on_file(plato, order=2)
    # model = train('hello world what is up world yo hello yo yo', order=3)
    print(generate_text(model))
