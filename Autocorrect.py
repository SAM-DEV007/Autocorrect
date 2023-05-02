import tensorflow as tf

import pickle
import os


def load_pre_process() -> tuple:
    '''
    Loads the file saved for Pre_Processing.

    Return:
    The tuple containing the data saved
    '''

    path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__))) + '\\Model\\Model\\Data\\', 'preprocess.p')
    with open(path, 'rb') as f:
        return pickle.load(f)


def get_word(txt: str) -> list:
    '''
    Take the word inputted and converts it fit the model.
    '''
    global INCORR_TXT_TO_INT

    if txt in INCORR_TXT_TO_INT.keys():
        return [INCORR_TXT_TO_INT[txt]]
    return [INCORR_TXT_TO_INT['<UNK>']]


if __name__ == '__main__':
    _, (CORR_TXT_TO_INT, INCORR_TXT_TO_INT), (CORR_INT_TO_TXT, INCORR_INT_TO_TXT) = load_pre_process()
    PATH = (os.path.abspath(os.path.join(os.path.dirname(__file__))) + '\\Model\\Model\\Data\\')
    PATH_MODEL = os.path.join(PATH, 'Trained_Model.meta')

    WORD = get_word(input('Type a single word: ').strip())

    batch_size = 128
    loaded_graph = tf.Graph()
    with tf.Session(graph=loaded_graph) as sess:
        # Load saved model
        loader = tf.train.import_meta_graph(PATH_MODEL)
        loader.restore(sess, os.path.join(PATH, 'Trained_Model'))

        input_data = loaded_graph.get_tensor_by_name('input:0')
        logits = loaded_graph.get_tensor_by_name('predictions:0')
        target_sequence_length = loaded_graph.get_tensor_by_name('target_sequence_length:0')
        keep_prob = loaded_graph.get_tensor_by_name('keep_prob:0')

        autocorrect_logits = sess.run(logits, {input_data: [WORD]*batch_size,
                                            target_sequence_length: [len(WORD)*2]*batch_size,
                                            keep_prob: 1.0})[0]
        
        print([CORR_INT_TO_TXT[i] for i in autocorrect_logits])
