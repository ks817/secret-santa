import streamlit as st
from streamlit_card import card
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
from datetime import datetime
from twilio.rest import Client

# Initialize session state variables
if 'matches' not in st.session_state:
    st.session_state.matches = None
if 'names' not in st.session_state:
    st.session_state.names = ""

def match_secret_santa(names_text):
    # Convert the text area input into a list of names and shuffle them
    names = [name.strip() for name in names_text.split('\n') if name.strip()]
    
    # Check if we have enough people
    if len(names) < 2:
        return None, "Please enter at least 2 names!"
    
    # Keep trying until we get a valid matching where no one gets themselves
    max_attempts = 100
    for _ in range(max_attempts):
        givers = names.copy()
        receivers = names.copy()
        random.shuffle(givers)    # Randomize givers order
        random.shuffle(receivers) # Randomize receivers order
        matches = {}
        valid = True
        
        # Try to match each giver with a receiver
        for giver in givers:
            possible_receivers = [r for r in receivers if r != giver]
            if not possible_receivers:
                # If the last person would get themselves, start over
                valid = False
                break
            
            # Pick a random receiver from possible matches
            receiver = random.choice(possible_receivers)
            matches[giver] = receiver
            receivers.remove(receiver)
        
        if valid:
            return matches, None
            
    return None, "Couldn't generate valid matches. Please try again!"

def save_matches(matches):
    date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    df = pd.DataFrame(list(matches.items()), columns=['Giver', 'Receiver'])
    filename = f'secret_santa_matches_{date}.csv'
    df.to_csv(filename, index=False)
    return filename

def send_secret_santa_texts(matches, phone_dict):
    account_sid = st.secrets["twilio"]["account_sid"]
    auth_token = st.secrets["twilio"]["auth_token"]
    twilio_number = st.secrets["twilio"]["phone_number"]
    
    try:
        client = Client(account_sid, auth_token)
        
        for giver, receiver in matches.items():
            if giver in phone_dict:
                st.write(f"Attempting to send message to {giver} at {phone_dict[giver]}")  # Debug
                try:
                    message = client.messages.create(
                        body=f"""
Ho Ho Ho {giver}! 🎅
                    
You are the Secret Santa for: {receiver}
                    
Remember to keep it a secret and have fun shopping! 🎁

Happy Holidays! ✨
                        """,
                        from_=twilio_number,
                        to=phone_dict[giver]
                    )
                    st.write(f"Message sent to {giver}, SID: {message.sid}")  # Debug
                except Exception as e:
                    st.error(f"Error sending to {giver}: {e}")
        return True, None
    except Exception as e:
        return False, str(e)

# Title and styling
st.markdown('<link href="https://fonts.googleapis.com/css2?family=Great+Vibes&display=swap" rel="stylesheet">', unsafe_allow_html=True)

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

# Background styling
st.markdown("""
    <style>
        .stApp {
            background-color: #081430;
        }

        .stApp::before {
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: url('https://images.unsplash.com/photo-1732559336539-7bc2c6388a22?q=80&w=2670&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D');
            background-size: cover;
            background-position: top center;
            background-repeat: no-repeat;
            opacity: 0.4;
            z-index: 0;
        }

        .stApp::after {
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(
                to bottom,
                #081430 0%,
                rgba(8, 20, 48, 0.8) 20%,
                rgba(8, 20, 48, 0.6) 40%,
                rgba(8, 20, 48, 0.4) 60%
            );
            z-index: 0;
        }

        .stMarkdown, .stButton, div[data-testid="stExpander"] {
            background-color: transparent !important;
            position: relative;
            z-index: 1;
        }
        
        .stTextArea textarea {
            background-color: rgba(8, 20, 48, 0.7) !important;
            color: #FBD30C !important;
            position: relative;
            z-index: 1;
        }

        /* Style for form input fields */
        .stTextInput input {
            background-color: rgba(8, 20, 48, 0.7) !important;
            color: #FBD30C !important;
            border: 1px solid #FBD30C !important;
        }
    </style>
""", unsafe_allow_html=True)

# Create centered container
col1, col2, col3 = st.columns([1,2,1])

with col2:
    st.markdown("""
        <div style="
            text-align: center;
            padding: 20px;
            background-color: rgba(8, 20, 48, 0.7);
            border: 2px solid #FBD30C;
            border-radius: 15px;
            margin: 20px 0;
        ">
            <p style="
                color: #FBD30C;
                font-size: 20px;
                font-family: sans-serif;
                margin: 0;
            ">Enter your friends' names</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Text area for names
    names = st.text_area("", height=200, key="names")
    
    # Match button and results
    if st.button("Match Secret Santas! ✨", type="primary"):
        if names:  # If names were entered
            matches, error = match_secret_santa(names)
            if error:
                st.error(error)
            else:
                st.session_state.matches = matches
                st.snow()
                
                # Display matches
                st.markdown("""
                    <div style="
                        padding: 20px;
                        background-color: rgba(8, 20, 48, 0.7);
                        border: 2px solid #FBD30C;
                        border-radius: 15px;
                        margin: 20px 0;
                    ">
                        <h3 style="color: #FBD30C; text-align: center;">🎄 Secret Santa Matches 🎁</h3>
                    </div>
                """, unsafe_allow_html=True)
                
                for giver, receiver in matches.items():
                    st.markdown(f"""
                        <div style="
                            padding: 10px;
                            background-color: rgba(8, 20, 48, 0.5);
                            border: 1px solid #FBD30C;
                            border-radius: 10px;
                            margin: 10px 0;
                            text-align: center;
                            color: #FBD30C;
                        ">
                            {giver} → {receiver}
                        </div>
                    """, unsafe_allow_html=True)
                
                # Save matches button
                if st.button("Save Matches"):
                    filename = save_matches(st.session_state.matches)
                    st.success(f"Matches saved to {filename}")
        else:
            st.warning("Please enter some names first!")
    
# Initialize session state at the top
if 'phone_numbers' not in st.session_state:
    st.session_state.phone_numbers = {}

# Phone number section
if st.session_state.matches:
    st.write("---")
    
    st.markdown("""
        <div style="
            text-align: center;
            padding: 20px;
            background-color: rgba(8, 20, 48, 0.7);
            border: 2px solid #FBD30C;
            border-radius: 15px;
            margin: 20px 0;
        ">
            <p style="
                color: #FBD30C;
                font-size: 20px;
                font-family: sans-serif;
                margin: 0;
            ">Enter Phone Numbers</p>
            <p style="
                color: #FBD30C;
                font-size: 16px;
                font-family: sans-serif;
                margin-top: 10px;
            ">Format: name: +1234567890</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Text area for phone numbers
    phone_text = st.text_area(
        "",
        height=200,
        key="phone_input",
        placeholder="Example:\nMary: +17739783\njkl: +17837189"
    )
    
    # Process phone numbers when entered
    if phone_text:
        phone_dict = {}
        valid_format = True
        
        for line in phone_text.strip().split('\n'):
            if ':' not in line:
                st.error(f"Missing colon in line: {line}")
                valid_format = False
                continue
            name, phone = line.split(':', 1)
            name = name.strip()
            phone = phone.strip()
            
            if not phone.startswith('+'):
                st.error(f"Phone number must start with '+': {phone}")
                valid_format = False
                continue
                
            if name not in st.session_state.matches:
                st.error(f"Name '{name}' not found in Secret Santa list")
                valid_format = False
                continue
                
            phone_dict[name] = phone
        
        # Show send button if format is valid and we have numbers
        if valid_format and phone_dict:
            if st.button("Send Messages 📱", type="primary"):
                success, error = send_secret_santa_texts(st.session_state.matches, phone_dict)
                if success:
                    st.success("Messages sent successfully! 🎄")
                    st.snow()
                else:
                    st.error(f"Error sending messages: {error}")