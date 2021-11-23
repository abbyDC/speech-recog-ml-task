import json
import io
import requests

from flask import Flask, Response, request
import tensorflow as tf

# Load model
import os
import pickle
import time

import os
import pathlib

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import tensorflow as tf

from tensorflow.keras import layers
from tensorflow.keras import models
from IPython import display
import pickle

import requests
import json

def decode_audio(audio_binary):
  audio, _ = tf.audio.decode_wav(contents=audio_binary)
  return tf.squeeze(audio, axis=-1)

def get_label(file_path):
  parts = tf.strings.split(
      input=file_path,
      sep=os.path.sep)
  return parts[-2]

def get_waveform_and_label(file_path):
  label = get_label(file_path)
  audio_binary = tf.io.read_file(file_path)
  waveform = decode_audio(audio_binary)
  return waveform, label

AUTOTUNE = tf.data.AUTOTUNE

def get_spectrogram(waveform):
  # Zero-padding for an audio waveform with less than 16,000 samples.
  input_len = 16000
  waveform = waveform[:input_len]
  zero_padding = tf.zeros(
      [16000] - tf.shape(waveform),
      dtype=tf.float32)
  # Cast the waveform tensors' dtype to float32.
  waveform = tf.cast(waveform, dtype=tf.float32)
  # Concatenate the waveform with `zero_padding`, which ensures all audio
  # clips are of the same length.
  equal_length = tf.concat([waveform, zero_padding], 0)
  # Convert the waveform to a spectrogram via a STFT.
  spectrogram = tf.signal.stft(
      equal_length, frame_length=255, frame_step=128)
  # Obtain the magnitude of the STFT.
  spectrogram = tf.abs(spectrogram)
  # Add a `channels` dimension, so that the spectrogram can be used
  # as image-like input data with convolution layers (which expect
  # shape (`batch_size`, `height`, `width`, `channels`).
  spectrogram = spectrogram[..., tf.newaxis]
  return spectrogram

def get_spectrogram_and_label_id(audio, label):
  spectrogram = get_spectrogram(audio)
  label_id = tf.argmax(label == commands)
  return spectrogram, label_id


def preprocess_dataset(files):
  files_ds = tf.data.Dataset.from_tensor_slices(files)

  output_ds = files_ds.map(
      map_func=get_waveform_and_label,
      num_parallel_calls=AUTOTUNE)
  output_ds = output_ds.map(
      map_func=get_spectrogram_and_label_id,
      num_parallel_calls=AUTOTUNE)
  return output_ds

model_path = "cnn_keras_model/3"
commands = np.array(['no', '_silence_','left','go','stop','off','down','on','right','yes',
 '_unknown_','up'])
app = Flask(__name__)

model = tf.keras.models.load_model(model_path)

@app.route("/")
def index():
    app.logger.info("Healthcheck!")
    return "Healthcheck!"


@app.route("/query", methods=["POST"])
def query():
    data = request.files['audio']
    data.save("/app"+data.filename)

    sample_file = pathlib.Path("/app"+data.filename)
    sample_ds = preprocess_dataset([str(sample_file)])

    for spectrogram, label in sample_ds.batch(1):
      prediction = model(spectrogram)
      keyword = commands[tf.argmax(tf.nn.softmax(prediction[0]))]
        
    os.remove("/app"+data.filename)
    return Response(
        response=json.dumps({"detected_keyword":keyword}),
        mimetype='application/json',
        status=200
        )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)