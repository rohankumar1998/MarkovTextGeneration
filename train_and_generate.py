from markov_chain import LanguageMarkovChain
import pickle

def train(text):
    return LanguageMarkovChain(text)

def train_on_file(file_name):
    with open(file_name, 'r') as f:
        text = f.read()
    return train(text)

def generate_text(markov_chain, n=10):
    i = 0
    words = []
    try:
        for word in iter(markov_chain):
            words.append(word)
            i += 1
            if i > n and word[-1] in '.?!':
                break
    except StopIteration as e:
        pass
    return ' '.join(words)

if __name__ == '__main__':
    genesis = '/Users/Rohan/Desktop/Computation Institute/Topic_Modelling/test files/genesis.txt'
    trump = '/Users/Rohan/Desktop/Computation Institute/Topic_Modelling/test files/trump_speeches.txt'
    mlk = '/Users/Rohan/Desktop/Computation Institute/Topic_Modelling/test files/MLK.txt'
    caesar = 'test_files/julius_caesar.txt'
    model = train_on_file(caesar)
    print(generate_text(model))
