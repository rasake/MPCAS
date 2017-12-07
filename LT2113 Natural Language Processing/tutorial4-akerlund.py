import math
import nltk


def entropy(labels):
    freqdist = nltk.FreqDist(labels)
    probs = [freqdist.freq(l) for l in freqdist]
    return -sum(p * math.log(p,2) for p in probs)

def part4a():
    print('4a) entropy: {:.3f}'.format(entropy(['spam', 'spam', 'spam'])))

def part4b():
    print('4b) entropy: {:.3f}'.format(entropy(['spam', 'spam', 'ham', 'ham'])))

def part4c():
    print('4c) entropy: {:.3f}'.format(entropy(['horse', 'giraffe', 'horse', 
        'aardvark', 'kangaroo', 'aardvark', 'aardvark'])))

def part4d():
    print('\n == part 4d) ')
    joint_data = [('Max',	 'dog'), ('Rex', 'dog'), ('Brutus',	'dog'), ('Lulu',
                  'dog'), ('Max', 'human'), ('Bella', 'human'), ('Max', 'dog'),
                  ('Lulu', 'human')]
    (names, species) = zip(*joint_data)
    print('Entropy for name+species jointly: {:.3f}'.format(entropy(joint_data)))
    print('Entropy for names only: {:.3f}'.format(entropy(names)))
    print('Entropy for species only: {:.3f}'.format(entropy(species)))

if __name__ == '__main__':
    part4a()
    part4b()
    part4c()
    part4d()
