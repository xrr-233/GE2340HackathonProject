import tensorflow as tf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from tensorflow import keras

assert tf.__version__.startswith('2.')

class myLSTM:

    # batch_size = 16

    def __init__(self, shape0, shape1, output_size, min_max_scaler_x, min_max_scaler_y):
        self.model = keras.Sequential()

        self.model.add(keras.layers.LSTM(64, input_shape=(shape0, shape1)))
        self.model.add(keras.layers.Dense(output_size))

        self.model.compile(loss="mae", optimizer="adam")

        self.min_max_scaler_x = min_max_scaler_x
        self.min_max_scaler_y = min_max_scaler_y

    def train(self, train_x, train_y, valid_x, valid_y):
        self.history = self.model.fit(train_x,
                                      train_y,
                                      validation_data=(valid_x, valid_y),
                                      epochs=256,
                                      batch_size=16,
                                      verbose=1,
                                      shuffle=False)

    def plot(self):
        plt.plot(self.history.history["loss"], label="train loss")
        plt.plot(self.history.history["val_loss"], label="valid loss")
        plt.legend()
        plt.show()

    def evaluate(self, test_x, test_y):
        return self.model.evaluate(test_x, test_y, verbose=0)

    def predict(self, predict_x):
        return self.model.predict(predict_x)