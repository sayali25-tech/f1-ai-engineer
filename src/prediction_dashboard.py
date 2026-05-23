import streamlit as st
import fastf1
import pandas as pd

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder

# Enable cache
fastf1.Cache.enable_cache('cache')

# Load session
session = fastf1.get_session(2024, 'Monaco', 'R')
session.load()

# Driver data
laps = session.laps.pick_driver('VER')

# Clean data
laps = laps.dropna(
    subset=[
        'LapTime',
        'TyreLife',
        'Compound',
        'Stint'
    ]
)

# Convert lap time
laps['LapTimeSeconds'] = (
    laps['LapTime']
    .dt.total_seconds()
)

# Encode compounds
encoder = LabelEncoder()

laps['CompoundEncoded'] = encoder.fit_transform(
    laps['Compound']
)

# Features
X = laps[
    [
        'TyreLife',
        'CompoundEncoded',
        'Stint'
    ]
]

# Target
y = laps['LapTimeSeconds']

# Train model
model = LinearRegression()
model.fit(X, y)

# Streamlit UI
st.title("F1 Lap Time Predictor")

# Inputs
tyre_life = st.slider(
    "Tyre Life",
    1,
    40,
    10
)

compound = st.selectbox(
    "Tyre Compound",
    laps['Compound'].unique()
)

stint = st.slider(
    "Stint Number",
    1,
    5,
    1
)

# Encode selected compound
compound_encoded = encoder.transform(
    [compound]
)[0]

# Prediction
prediction = model.predict(
    [[
        tyre_life,
        compound_encoded,
        stint
    ]]
)

# Output
st.subheader("Predicted Lap Time")

st.write(
    f"{prediction[0]:.2f} seconds"
)