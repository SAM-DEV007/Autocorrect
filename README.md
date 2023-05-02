# Autocorrect
A limited machine learning model for autocorrect.

# Requirements
- Python 3.7
  - Python 3.7 is needed as later versions does not support the `tensorflow` version used.
- Requirements mentioned in `requirements.txt` file.
  - The file can be initialized by `pip install -r path\to\requirements.txt`

# How To Use
`Autocorrect.py` in the `main` directory can be used to run the pre-trained model. The accuracy of the model might be significantly low due to the limit in hardware specs and limited dataset.

# Train The Model
`Dataset` contains the `.txt` files for training the model in `\Model`. To generate new incorrect words, `Generate_Incorrect_Words.py` can be used to generate incorrect word lists. If you wish to use the `Large_Dataset`, it can be changed in the file itself.

`Pre_Processing.py` should be executed first as `Model_Training.py` will use the parameters made by the former. They can be found under `\Model\Model`. `Data` folder contains the parameters, checkpoints, and the trained model that can be used by `Autocorrect.py`.
