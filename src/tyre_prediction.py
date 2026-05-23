import fastf1
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder

# Enable cache
fastf1.Cache.enable_cache('cache')

# Load race
session = fastf1.get_session(2024, 'Monaco', 'R')
session.load()

# Pick driver
laps = session.laps.pick_driver('VER')

# Remove missing data
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

# Encode tyre compounds
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

# Predictions
predictions = model.predict(X)

# Plot
plt.figure(figsize=(10, 6))

plt.scatter(
    range(len(y)),
    y,
    label='Actual'
)

plt.plot(
    range(len(predictions)),
    predictions,
    label='Predicted'
)

plt.xlabel("Lap Number")
plt.ylabel("Lap Time")
plt.title("Multi-Feature Tyre Degradation Model")

plt.legend()

plt.show()

# Model coefficients
print("Model Coefficients:")
print(model.coef_)