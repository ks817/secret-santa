import streamlit as st
from streamlit_card import card
st.markdown('<link href="https://fonts.googleapis.com/css2?family=Great+Vibes&display=swap" rel="stylesheet">', unsafe_allow_html=True)

#st.title("Secret Santa 🐝")

#st.set_page_config(page_title="Secret Santa", page_icon="🐝", layout="wide")
#title_card = card(title="Secret Santa 🐝", text="add names")

st.markdown("""
    <style>
        @keyframes snow {
            0% {
                text-shadow: 
                    2px 2px 4px #c3b37f,
                    0 0 5px white,
                    0 0 10px white;
            }
            50% {
                text-shadow: 
                    2px 2px 4px #c3b37f,
                    0 0 15px white,
                    0 0 20px white,
                    0 0 30px white;
            }
            100% {
                text-shadow: 
                    2px 2px 4px #c3b37f,
                    0 0 5px white,
                    0 0 10px white;
            }
        }

        .snow-title:hover {
            animation: snow 2s infinite;
            cursor: pointer;
        }
    </style>

    <h1 class='snow-title' style='text-align: center; font-family: "Great Vibes", cursive; color: #FBD30C; font-size: 60px; font-weight: 100;'>
        Secret Santa🎄
    </h1>
    """, unsafe_allow_html=True)
