import streamlit as st
import matplotlib.pyplot as plt

# Streamlit title
st.title("F1 Race Strategy Simulator")

# Inputs
total_laps = st.slider(
    "Total Race Laps",
    20,
    80,
    50
)

base_lap_time = st.slider(
    "Base Lap Time (seconds)",
    60.0,
    100.0,
    75.0
)

degradation = st.slider(
    "Tyre Degradation Per Lap",
    0.01,
    0.30,
    0.08
)

pit_loss = st.slider(
    "Pit Stop Time Loss",
    10,
    35,
    20
)

# Strategy definitions
one_stop_pit = total_laps // 2

two_stop_pits = [
    total_laps // 3,
    2 * total_laps // 3
]

# Simulate strategy
def simulate_strategy(pit_laps):

    tyre_age = 0
    total_time = 0

    lap_times = []

    for lap in range(total_laps):

        lap_time = (
            base_lap_time
            + tyre_age * degradation
        )

        total_time += lap_time

        lap_times.append(lap_time)

        tyre_age += 1

        if lap in pit_laps:
            total_time += pit_loss
            tyre_age = 0

    return total_time, lap_times

# Run simulations
one_stop_time, one_stop_laps = simulate_strategy(
    [one_stop_pit]
)

two_stop_time, two_stop_laps = simulate_strategy(
    two_stop_pits
)

# Results
st.subheader("Strategy Results")

st.write(
    f"1 Stop Strategy Total Time: "
    f"{one_stop_time:.2f}s"
)

st.write(
    f"2 Stop Strategy Total Time: "
    f"{two_stop_time:.2f}s"
)

# Recommendation
if one_stop_time < two_stop_time:
    st.success("1 Stop Strategy Faster")
else:
    st.success("2 Stop Strategy Faster")

# Plot
fig, ax = plt.subplots(figsize=(12, 6))

ax.plot(
    one_stop_laps,
    label='1 Stop Strategy'
)

ax.plot(
    two_stop_laps,
    label='2 Stop Strategy'
)

ax.set_xlabel("Lap")
ax.set_ylabel("Lap Time")
ax.set_title("Race Strategy Simulation")

ax.legend()

st.pyplot(fig)