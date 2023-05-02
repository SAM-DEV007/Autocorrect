from copy import copy

import os
import pickle


def get_data():
    '''
    Loads the data for correct and incorrect lists.

    Return:
    corr_data[str] : The string in the correct_words file
    incorr_data[list] : List of string in the three incorrect_words file
    '''

    # Loads the file containing the correct words
    corr_dir = os.path.join(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))) + '\\Dataset\\', 'correct_words.txt')
    with open(corr_dir, 'r') as f:
        corr_data = f.read().lower()
    
    # Loads the file containing the incorrect words
    # As there are three files
    incorr_data = list()
    for num in range(1, 4):
        incorr_dir = os.path.join(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))) + '\\Dataset\\', f'incorrect_words{num}.txt')
        with open(incorr_dir, 'r') as f:
            incorr_data.append(f.read().lower())
    
    return corr_data, incorr_data


def lookup_table(txt: str, incorr_lookup = None) -> dict:
    '''
    Creates lookup table for the text passed.

    Parameters:
    txt[str] : The text to create lookup table

    Return:
    txt_to_int[dict], int_to_txt[dict] : Lookup table
    '''
    
    # Tokens for special words
    special = {'<PAD>': 0, '<EOS>': 1, '<UNK>': 2, '<GO>': 3}

    # If the list is of incorrect words,
    # Joins them line by line
    if type(txt) == list:
        txt = '\n'.join(txt)

    text = set(txt.split()) # Gets unique words

    txt_to_int = copy(special) # Copies the special characters

    for i, v in enumerate(text, len(special)):
        txt_to_int[v] = i

    int_to_txt = {v: i for i, v in txt_to_int.items()}

    if incorr_lookup:
        text = set(incorr_lookup.split())
        i = len(txt_to_int)
        for v in text:
            if v not in txt_to_int.keys():
                txt_to_int[v] = i
                i += 1

        int_to_txt = {v: i for i, v in txt_to_int.items()}

    return txt_to_int, int_to_txt


def text_id(corr_txt: str, incorr_txt_list: list, corr_txt_to_int: dict, incorr_txt_to_int: dict) -> list:
    '''
    Associates the text passed with the corresponding ID with lookup table.

    Parameters:
    corr_txt[str] : The text for correct words
    incorr_txt[str] : The  text for incorrect words
    corr_txt_to_int[dict], incorr_txt_to_int[dict] : txt_to_int dictionary

    Return:
    corr_txt_id[list], incorr_txt_id[list] : Text IDs converted
    '''

    # Lists containing Text IDs
    corr_txt_id, incorr_txt_id = list(), list()

    # Lists of words
    corr_txt = corr_txt.split()

    # Correct words
    for word in corr_txt:
        corr_id = list()
        incorr_id = list()
        if corr_txt != '':
            corr_id.append(corr_txt_to_int[word])
            corr_id.append(incorr_txt_to_int['<EOS>'])
            incorr_id.append(incorr_txt_to_int[word])
            #incorr_id.append(incorr_txt_to_int['<EOS>'])
        corr_txt_id.append(corr_id)
        incorr_txt_id.append(incorr_id)
    
    for i in range(len(incorr_txt_list)):
        incorr_words = incorr_txt_list[i].split()
        
        # Incorrect Words to be added to main list
        for word in incorr_words:
            incorr_id = list()
            if word != '':
                incorr_id.append(incorr_txt_to_int[word])
                #incorr_id.append(incorr_txt_to_int['<EOS>'])

            # Adds converted words to the main list
            incorr_txt_id.append(incorr_id)

        # Creating a list for correct words
        for word in corr_txt:
            corr_id = list()
            if corr_txt != '':
                    corr_id.append(corr_txt_to_int[word])
                    corr_id.append(incorr_txt_to_int['<EOS>'])
            corr_txt_id.append(corr_id)

    return corr_txt_id, incorr_txt_id

def preprocess():
    '''
    Preprocesses and saves data for faster loading.
    '''

    # Gets the data
    correct_text, incorrect_list = get_data()

    # Creates lookup tables
    correct_txt_to_int, correct_int_to_txt = lookup_table(correct_text)
    incorrect_txt_to_int, incorrect_int_to_txt = lookup_table(incorrect_list, correct_text)

    # Converted text
    correct, incorrect = text_id(correct_text, incorrect_list, correct_txt_to_int, incorrect_txt_to_int)

    # Save data
    data = (
        (correct, incorrect),
        (correct_txt_to_int, incorrect_txt_to_int),
        (correct_int_to_txt, incorrect_int_to_txt)
    )
    path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__))) + '\\Data\\', 'preprocess.p')
    pickle.dump(data, open(path, 'wb'))


if __name__ == '__main__':
    preprocess()