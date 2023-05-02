import string
import random
import os

if __name__ == '__main__':
    NUM = 100 # No. of incorrect files to generate
    a = list(string.ascii_lowercase) # Gets all the lowercase ascii letters

    # Reads the file with correct words
    with open(os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__))) + '\\Dataset\\', 'correct_words.txt'), 'r') as f:
        x = f.read()

    y = x.split() # Creates a list for each of the correct word
    nl = list() # An empty incorrect word list

    for num in range(1, NUM+1): # Generates 3 files
        # Writes the incorrect word list to 'incorrect_words.txt'
        # Chooses a random no. between 1 and 2 to determine the no. of letters to change
        # Goes letter by letter in a string and gambles to change the letter
        with open(os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__))) + '\\Dataset\\', f'incorrect_words{num}.txt'), 'w') as file:
            for s in y:
                f = list()
                allowed = random.randint(1, 2)
                for i, l in enumerate(s):
                    rand = random.randint(0, 1)
                    if i > 0 and rand and allowed: # i > 0 makes sure that the first letter remains unchanged
                        l = random.sample(a, k=1)
                        f.extend(l)
                        allowed -= 1
                        continue
                    f.append(l)
                file.write(f'{"".join(f)}\n') # Writes the incorrect word to the file