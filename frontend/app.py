import streamlit as st
import os
from dotenv import load_dotenv
from streamlit_option_menu import option_menu
from pages import dashboard, voice_training, voice_generation, voice_library

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Voice Cloning Platform",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .sidebar-header {
        font-size: 1.5rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #c3e6cb;
    }
    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #f5c6cb;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_token' not in st.session_state:
    st.session_state.user_token = None
if 'user_info' not in st.session_state:
    st.session_state.user_info = None

def main():
    # Sidebar navigation
    with st.sidebar:
        st.markdown('<div class="sidebar-header">🎤 Voice Cloning Platform</div>', unsafe_allow_html=True)
        
        if not st.session_state.authenticated:
            st.markdown("### Login Required")
            st.markdown("Please login to access the platform features.")
            
            # Simple login form
            with st.form("login_form"):
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                submit_button = st.form_submit_button("Login")
                
                if submit_button:
                    # Here you would typically make an API call to authenticate
                    if email and password:
                        # For demo purposes, accept any non-empty credentials
                        st.session_state.authenticated = True
                        st.session_state.user_info = {"email": email, "username": email.split("@")[0]}
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Please enter both email and password")
        else:
            st.markdown(f"### Welcome, {st.session_state.user_info['username']}!")
            
            # Navigation menu
            selected = option_menu(
                menu_title="Navigation",
                options=["Dashboard", "Voice Training", "Voice Generation", "Voice Library"],
                icons=["house", "mic", "play-circle", "collection"],
                menu_icon="cast",
                default_index=0,
            )
            
            # Logout button
            if st.button("Logout"):
                st.session_state.authenticated = False
                st.session_state.user_token = None
                st.session_state.user_info = None
                st.success("Logged out successfully!")
                st.rerun()
            
            # Display selected page
            if selected == "Dashboard":
                dashboard.show()
            elif selected == "Voice Training":
                voice_training.show()
            elif selected == "Voice Generation":
                voice_generation.show()
            elif selected == "Voice Library":
                voice_library.show()
    
    # Main content area
    if not st.session_state.authenticated:
        st.markdown('<div class="main-header">🎤 Voice Cloning Platform</div>', unsafe_allow_html=True)
        
        # Welcome message and features
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            ### 🎯 Voice Training
            Upload voice samples and train custom AI voices using state-of-the-art models.
            """)
        
        with col2:
            st.markdown("""
            ### 🎵 Voice Generation
            Generate speech in your trained voices from text input with emotion control.
            """)
        
        with col3:
            st.markdown("""
            ### 📚 Voice Library
            Browse and manage your trained voices and discover public voices.
            """)
        
        # Demo features
        st.markdown("---")
        st.markdown("### 🚀 Platform Features")
        
        features_col1, features_col2 = st.columns(2)
        
        with features_col1:
            st.markdown("""
            - **Advanced Voice Cloning**: Using VITS, So-VITS-SVC, and Bark models
            - **High-Quality Audio**: Support for multiple audio formats (WAV, MP3, FLAC)
            - **Real-time Training**: Monitor training progress with live metrics
            - **Emotion Control**: Generate speech with different emotional styles
            """)
        
        with features_col2:
            st.markdown("""
            - **Multi-language Support**: Train voices in multiple languages
            - **Batch Processing**: Generate multiple audio files at once
            - **API Access**: RESTful API for integration with other applications
            - **Secure Storage**: Cloud storage with user authentication
            """)
        
        # Getting started
        st.markdown("---")
        st.markdown("### 🎬 Getting Started")
        st.markdown("""
        1. **Create an Account**: Sign up with your email and password
        2. **Upload Voice Samples**: Provide 5-10 minutes of clear audio
        3. **Train Your Voice**: Start the training process (takes 1-2 hours)
        4. **Generate Speech**: Create audio in your custom voice
        """)

if __name__ == "__main__":
    main()