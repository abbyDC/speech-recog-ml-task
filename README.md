# Machine Learning Task - Keyword Spotting
ML Task which shows a proof of concept in developing a keyword spotting model

This repository contains the documentation done during experimentation as well as the jupyter notebooks for training and inference.

## I. Data Gathering

Dataset source: https://www.tensorflow.org/datasets/catalog/speech_commands

For manual inspection and preprocessing of data, I downloaded the official data splits as stated from the source code in `tfds.audio.SpeechCommands`

Official train and val set: http://download.tensorflow.org/data/speech_commands_v0.02.tar.gz

Official test set: http://download.tensorflow.org/data/speech_commands_test_set_v0.02.tar.gz

12 keywords are expected to be detected namely:

- down
- go
- left
- no
- off
- on
- right
- stop
- up
- yes
- _silence_
- _unknown_

## II. Data Preprocessing

Upon closer inspection of the data, the 12 labels used in testing were not the same as the labels for training

1. `unknown.py` script was used to compile all words which are not part of the 12 keywords into one label called '_unknown_'
    - only a subset of these were used to closely match the number of samples for the other labels


2. `split_bg.py` script was used to split each sample in the '_background_noises_' label into 1 second chunks
    - each sample from the other labels were 1 second wavs so there was a need to match the file size with this label
    - the preprocessed wavs were saved under the '_silence_' label

## III. Training

For the training script, please see `kws_training.ipynb` for the source code

It was heavily based from the tutorial in https://www.tensorflow.org/tutorials/audio/simple_audio with modifications to fit the complete and train datasets from the tf dataset speech_commands

### Notes

1. Visualizations were added to inspect the data as well as results

2. There's already a trained model available so no need to run this to get a model.

Model available here: <insert_link>

## IV. Test Data Evaluation and Inference

For data evaluation and inference, please see `kws_eval_inference.ipynb`


## V. Experiments Documentation

Google Colab was utilized to run training and inference for the entire experimentation.

| # of Training Data Samples | Epochs  | Batch Size | Accuracy on Full Test Data |
| :--------------------------|:--------|:-----------|:---------------------------|
| 16,000                     | 30      | 64         | 89%                        |
| 16,000                     | 35      | 64         | 90%                        |
| 24,000                     | 35      | 64         | 91.45%                     |
| **24,000**                 | **45**  | **64**     | **91.59%**                 |
| 24,000                     | 50      | 64         | 91.17%                     |

## VI. References

TensorFlow Audio Recognition - https://www.tensorflow.org/tutorials/audio/simple_audio

Keyword Spotting Implementations - https://paperswithcode.com/paper/keyword-transformer-a-self-attention-model

