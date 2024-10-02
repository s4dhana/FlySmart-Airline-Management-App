import anvil.server
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM

@anvil.server.callable
def load_and_preprocess_data():
    df = anvil.server.request.get_file('weather_data.csv')
    data = pd.read_csv(df, parse_dates=['Date'], index_col='Date')
    
    new_data = data[['Windspeed']].values

    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(new_data)

    return scaled_data, scaler

# Create the LSTM model
def create_model():
    model = Sequential()

    # Add LSTM layers
    model.add(LSTM(units=50, return_sequences=True, input_shape=(60, 1)))
    model.add(LSTM(units=50, return_sequences=False))

    # Add Dense layers
    model.add(Dense(units=25))
    model.add(Dense(units=1))

    # Compile the model
    model.compile(optimizer='adam', loss='mean_squared_error')
    
    return model

@anvil.server.callable
def train_model():
    scaled_data, scaler = load_and_preprocess_data()
    
    def create_dataset(data, look_back=60):
        X, y = [], []
        for i in range(look_back, len(data)):
            X.append(data[i-look_back:i, 0])
            y.append(data[i, 0])
        return np.array(X), np.array(y)

    look_back = 60
    X, y = create_dataset(scaled_data, look_back)
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))

    model = create_model()
    model.fit(X, y, batch_size=32, epochs=5)

    return model, scaler

@anvil.server.callable
def make_prediction(wind):
    model, scaler = train_model()
    predicted_res = model.predict(wind)
    predicted_res = scaler.inverse_transform(predicted_res)

    return predicted_res[0][0]

@anvil.server.callable
def predict_weather(location,preci,wind):
  print(location,preci,wind)
  if make_prediction(wind) > 50 or preci == "heavy_rain" or preci == "rain":
      return True
