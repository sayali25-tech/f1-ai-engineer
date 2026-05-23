import streamlit as st
import random
import matplotlib.pyplot as plt

# Title
st.title("Monte Carlo F1 Strategy Simulator")

# Inputs
total_laps = st.slider(
    "Total Laps",
    20,
    80,
    50
)

base_lap = st.slider(
    "Base Lap Time",
    60.0,
    100.0,
    75.0
)

degradation = st.slider(
    "Tyre Degradation",
    0.01,
    0.30,
    0.08
)

pit_loss = st.slider(
    "Pit Loss",
    10,
    35,
    20
)

simulations = st.slider(
    "Number of Simulations",
    100,
    5000,
    1000
)

# Strategy pits
one_stop = [total_laps // 2]

two_stop = [
    total_laps // 3,
    2 * total_laps // 3
]

# Simulation function
def simulate_race(pit_strategy):

    tyre_age = 0
    total_time = 0

    for lap in range(total_laps):

        random_deg = degradation * random.uniform(
            0.8,
            1.2
        )

        lap_time = (
            base_lap
            + tyre_age * random_deg
        )

        # Random safety car chance
        if random.random() < 0.03:
            lap_time -= 5

        total_time += lap_time

        tyre_age += 1

        if lap in pit_strategy:
            total_time += pit_loss
            tyre_age = 0

    return total_time

# Run simulations
one_stop_wins = 0
two_stop_wins = 0

one_stop_times = []
two_stop_times = []

for _ in range(simulations):

    one_time = simulate_race(one_stop)
    two_time = simulate_race(two_stop)

    one_stop_times.append(one_time)
    two_stop_times.append(two_time)

    if one_time < two_time:
        one_stop_wins += 1
    else:
        two_stop_wins += 1

# Probabilities
one_prob = (
    one_stop_wins / simulations
) * 100

two_prob = (
    two_stop_wins / simulations
) * 100

# Results
st.subheader("Win Probabilities")

st.write(
    f"1 Stop Strategy: {one_prob:.2f}%"
)

st.write(
    f"2 Stop Strategy: {two_prob:.2f}%"
)

# Histogram
fig, ax = plt.subplots(figsize=(12, 6))

ax.hist(
    one_stop_times,
    bins=30,
    alpha=0.6,
    label='1 Stop'
)

ax.hist(
    two_stop_times,
    bins=30,
    alpha=0.6,
    label='2 Stop'
)

ax.set_xlabel("Total Race Time")
ax.set_ylabel("Frequency")
ax.set_title("Monte Carlo Strategy Outcomes")

ax.legend()

st.pyplot(fig)