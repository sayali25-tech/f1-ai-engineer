import streamlit as st
import fastf1
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

fastf1.Cache.enable_cache('cache')

# =========================
# TYRE COLORS
# =========================

COMPOUND_COLORS = {
    "SOFT": "red",
    "MEDIUM": "yellow",
    "HARD": "white",
    "INTERMEDIATE": "green",
    "WET": "blue"
}

# =========================
# LOAD SESSION
# =========================

@st.cache_data
def load_session(year, gp, session_type):

    session = fastf1.get_session(
        year,
        gp,
        session_type
    )

    session.load()

    return session

# =========================
# SIDEBAR
# =========================

st.sidebar.title("F1 Dashboard")

year = st.sidebar.selectbox(
    "Year",
    [2023, 2024]
)

grand_prix = st.sidebar.selectbox(
    "Grand Prix",
    [
        "Monaco",
        "Silverstone",
        "Monza",
        "Spa"
    ]
)

session_type = st.sidebar.selectbox(
    "Session",
    ["Q", "R"]
)

page = st.sidebar.radio(
    "Select Page",
    [
        "Telemetry",
        "Track Map",
        "Tyre Strategy",
        "Sector Analysis",
        "Race Pace"
    ]
)

# =========================
# TELEMETRY PAGE
# =========================

if page == "Telemetry":

    st.title("Telemetry Comparison")

    session = load_session(
        year,
        grand_prix,
        session_type
    )

    laps = session.laps

    drivers = laps['Driver'].unique()

    driver1 = st.selectbox(
        "Driver 1",
        drivers,
        index=0
    )

    driver2 = st.selectbox(
        "Driver 2",
        drivers,
        index=1
    )

    lap1 = laps.pick_driver(driver1).pick_fastest()
    lap2 = laps.pick_driver(driver2).pick_fastest()

    tel1 = lap1.get_car_data().add_distance()
    tel2 = lap2.get_car_data().add_distance()

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(
        tel1['Distance'],
        tel1['Speed'],
        label=driver1
    )

    ax.plot(
        tel2['Distance'],
        tel2['Speed'],
        label=driver2
    )

    ax.set_xlabel("Distance")
    ax.set_ylabel("Speed")
    ax.set_title("Speed Comparison")

    ax.legend()

    st.pyplot(fig)

# =========================
# TRACK MAP PAGE
# =========================

elif page == "Track Map":

    st.title("Track Map")

    session = load_session(
        year,
        grand_prix,
        session_type
    )

    laps = session.laps

    driver = st.selectbox(
        "Select Driver",
        laps['Driver'].unique()
    )

    lap = laps.pick_driver(driver).pick_fastest()

    pos = lap.get_pos_data()

    fig, ax = plt.subplots(figsize=(8, 8))

    ax.plot(
        pos['X'],
        pos['Y']
    )

    ax.set_title(f"{driver} Track Map")

    st.pyplot(fig)

# =========================
# TYRE STRATEGY PAGE
# =========================

elif page == "Tyre Strategy":

    st.title("Tyre Strategy")

    session = load_session(
        year,
        grand_prix,
        "R"
    )

    laps = session.laps

    drivers = laps['Driver'].unique()

    driver = st.selectbox(
        "Select Driver",
        drivers
    )

    driver_laps = laps.pick_driver(driver)

    stints = (
        driver_laps[
            ['Stint', 'Compound', 'LapNumber']
        ]
        .groupby(
            ['Stint', 'Compound']
        )
        .count()
        .reset_index()
    )

    stints = stints.rename(
        columns={
            'LapNumber': 'StintLength'
        }
    )

    fig, ax = plt.subplots(figsize=(10, 4))

    for _, row in stints.iterrows():

        ax.barh(
            driver,
            row['StintLength'],
            left=row['Stint'],
            color=COMPOUND_COLORS.get(
                row['Compound'],
                'gray'
            )
        )

    ax.set_title("Tyre Stints")

    st.pyplot(fig)

# =========================
# SECTOR ANALYSIS PAGE
# =========================

elif page == "Sector Analysis":

    st.title("Sector Analysis")

    session = load_session(
        year,
        grand_prix,
        session_type
    )

    laps = session.laps

    driver1 = st.selectbox(
        "Driver 1",
        laps['Driver'].unique(),
        index=0
    )

    driver2 = st.selectbox(
        "Driver 2",
        laps['Driver'].unique(),
        index=1
    )

    lap1 = laps.pick_driver(driver1).pick_fastest()
    lap2 = laps.pick_driver(driver2).pick_fastest()

    sector_data = pd.DataFrame({
        "Sector": [
            "Sector 1",
            "Sector 2",
            "Sector 3"
        ],
        driver1: [
            lap1['Sector1Time'].total_seconds(),
            lap1['Sector2Time'].total_seconds(),
            lap1['Sector3Time'].total_seconds()
        ],
        driver2: [
            lap2['Sector1Time'].total_seconds(),
            lap2['Sector2Time'].total_seconds(),
            lap2['Sector3Time'].total_seconds()
        ]
    })

    st.table(sector_data)

# =========================
# RACE PACE PAGE
# =========================

elif page == "Race Pace":

    st.title("Race Pace Analysis")

    session = load_session(
        year,
        grand_prix,
        "R"
    )

    laps = session.laps

    drivers = st.multiselect(
        "Select Drivers",
        laps['Driver'].unique(),
        default=list(laps['Driver'].unique())[:2]
    )

    fig, ax = plt.subplots(figsize=(12, 6))

    for driver in drivers:

        driver_laps = (
            laps
            .pick_driver(driver)
            .pick_quicklaps()
        )

        for compound in driver_laps['Compound'].unique():

            compound_laps = driver_laps[
                driver_laps['Compound']
                == compound
            ]

            lap_times = (
                compound_laps['LapTime']
                .dt.total_seconds()
            )

            ax.plot(
                compound_laps['LapNumber'],
                lap_times,
                label=f"{driver} - {compound}",
                color=COMPOUND_COLORS.get(
                    compound,
                    "gray"
                )
            )

            x = compound_laps['LapNumber']
            y = lap_times

            if len(x) > 2:

                coefficients = np.polyfit(
                    x,
                    y,
                    1
                )

                trend = np.poly1d(
                    coefficients
                )

                ax.plot(
                    x,
                    trend(x),
                    linestyle='dashed'
                )

                degradation = coefficients[0]

                st.write(
                    f"{driver} ({compound}) "
                    f"degradation: "
                    f"{degradation:.3f}s/lap"
                )

    ax.set_xlabel("Lap Number")
    ax.set_ylabel("Lap Time")

    ax.set_title("Race Pace Comparison")

    ax.legend()

    st.pyplot(fig)