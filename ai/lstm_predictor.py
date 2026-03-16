import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
from sklearn.preprocessing import MinMaxScaler

class LSTMModel:
    def __init__(self, look_back=1):
        self.look_back = look_back
        self.model = Sequential()

    def create_model(self):
        self.model.add(LSTM(50, return_sequences=True, input_shape=(self.look_back, 1)))
        self.model.add(Dropout(0.2))
        self.model.add(LSTM(50, return_sequences=False))
        self.model.add(Dropout(0.2))
        self.model.add(Dense(1, activation='sigmoid'))  # Output layer for probability
        self.model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    def fit(self, X_train, y_train, epochs=10, batch_size=1):
        self.model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, verbose=2)

    def predict(self, data):
        return self.model.predict(data)

# Example usage:
# scaler = MinMaxScaler(feature_range=(0, 1))
# dataset_scaled = scaler.fit_transform(dataset)
# model = LSTMModel(look_back=5)
# model.create_model() 
# model.fit(X_train, y_train)
# predictions = model.predict(X_test)  # Final prediction for bullish/bearish probability
