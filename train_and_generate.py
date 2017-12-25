from letter_markov_chain import LetterMarkovChain
from word_markov_chain import WordMarkovChain
from preprocess import preprocess_text
import json
import pickle

def train(text, order=1, letter=True, preprocess=True):
    new_text = preprocess_text(text) if preprocess else text
    MarkovChain = LetterMarkovChain if letter else WordMarkovChain
    return MarkovChain(new_text, order=order)

def train_on_file(file_name, order=1, letter=True, preprocess=True):
    with open(file_name, 'r') as f:
        text = f.read()
    return train(text, order=order, letter=letter, preprocess=preprocess)

def generate_text(markov_chain, n=100, letter=True):
    delim = '' if letter else ' '
    stoppers = '.?!";-`\' \t\n' if letter else '.?!";-`'
    i = 0
    tokens = []
    markov_chain.reset()
    try:
        for token in iter(markov_chain):
            tokens.append(token)
            i += 1
            if i > 2*n or i > n and token[-1] in stoppers:
                break
    except StopIteration as e:
        pass
    return delim.join(tokens)

def save_model(model, file_name):
    with open(file_name, 'wb') as f:
        pickle.dump(model, f)

def load_model(file_name):
    with open(file_name, 'rb') as f:
        return pickle.load(f)

def train_on_lyrics(lyrics_json_file, order=4, letter=True, preprocess=True):
    lyrics = dict()
    with open(lyrics_json_file, 'r') as f:
        lyrics = json.load(f)
    text = '\n'.join(lyrics.values())
    model = train(text, order=order, letter=letter, preprocess=preprocess)
    return model

def train_on_posts(page_posts_json, order=4, letter=True, preprocess=True):
    posts = list()
    with open(page_posts_json, 'r') as f:
        posts = json.load(f)
    text = '\n'.join('\n'.join(x.split('\n')[1:-1]) for x in posts)
    model = train(text, order=order, letter=letter, preprocess=preprocess)
    return model

if __name__ == '__main__':
    # file names for text and lyrics JSONs
    genesis = '/Users/Rohan/Desktop/Computation Institute/Topic_Modelling/test files/genesis.txt'
    trump = '/Users/Rohan/Desktop/Computation Institute/Topic_Modelling/test files/trump_speeches.txt'
    mlk = '/Users/Rohan/Desktop/Computation Institute/Topic_Modelling/test files/MLK.txt'
    caesar = 'test_files/julius_caesar.txt'
    plato = 'test_files/plato_republic.txt'
    kant = 'test_files/kant.txt'
    taylor_swift_lyrics = './getting_data/taylor_swift_lyrics.json'
    queen_lyrics = './getting_data/queen_lyrics.json'

    # training and saving
    # model = train_on_lyrics(queen_lyrics, order=5)
    # model = train_on_posts('./getting_data/uchicago_secrets.json', order=3, letter=False, preprocess=False)
    # save_model(model, 'models/uchicago_secrets_markov_word_3.pkl')

    # loading and generating
    taylor_swift_model = 'models/taylor_swift_markov_5.pkl'
    queen_model = 'models/queen_markov_5.pkl'
    trump_model = 'models/trump_markov_4.pkl'
    uchicago_secrets_model = 'models/uchicago_secrets_markov_word_3.pkl'
    model = load_model(uchicago_secrets_model)
    print(generate_text(model, n=30, letter=False))
