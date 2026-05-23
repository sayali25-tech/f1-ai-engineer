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

# Driver laps
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
st.title("F1 Pit Strategy Optimizer")

# User Inputs
tyre_life = st.slider(
    "Current Tyre Life",
    1,
    40,
    20
)

compound = st.selectbox(
    "Current Compound",
    laps['Compound'].unique()
)

stint = st.slider(
    "Current Stint",
    1,
    5,
    1
)

# Encode compound
compound_encoded = encoder.transform(
    [compound]
)[0]

# Predict current lap pace
predicted_lap = model.predict(
    [[
        tyre_life,
        compound_encoded,
        stint
    ]]
)[0]

# Predict next 5 laps
future_times = []

for future_tyre in range(
    tyre_life,
    tyre_life + 5
):

    pred = model.predict(
        [[
            future_tyre,
            compound_encoded,
            stint
        ]]
    )[0]

    future_times.append(pred)

average_future = sum(future_times) / len(future_times)

# Pit stop threshold
pit_threshold = predicted_lap + 1.5

# Decision
st.subheader("Strategy Decision")

if average_future > pit_threshold:
    st.error("BOX BOX — Pit Stop Recommended")
else:
    st.success("Stay Out")

# Show predictions
st.subheader("Predicted Pace")

st.write(
    f"Current Predicted Lap: {predicted_lap:.2f}s"
)

st.write(
    f"Average Next 5 Laps: {average_future:.2f}s"
)