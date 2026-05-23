import fastf1
import streamlit as st

# Enable cache
fastf1.Cache.enable_cache('cache')

@st.cache_data
def load_session(
    year,
    grand_prix,
    session_type
):

    session = load_session(
        year,
        grand_prix,
        session_type
    )


    return session