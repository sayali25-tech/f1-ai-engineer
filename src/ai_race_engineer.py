import streamlit as st

st.title("🏎️ F1 Race Engineer Dashboard")

question = st.text_input("Enter strategy question")

if st.button("Analyze Strategy"):

    if "ferrari" in question.lower():
        st.write("Ferrari should consider an earlier pit stop in Monaco.")

    elif "red bull" in question.lower():
        st.write("Red Bull can extend tyre life for better race pace.")

    else:
        st.write("Strategy analysis complete.")