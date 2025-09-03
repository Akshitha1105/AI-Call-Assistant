import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import time

def show():
    st.markdown('<div class="main-header">🎵 Voice Generation</div>', unsafe_allow_html=True)
    
    # Page description
    st.markdown("""
    ### Generate Speech with Your Custom Voices
    
    Create high-quality audio using your trained AI voices. Control emotion, speed, and pitch for the perfect output.
    """)
    
    # Create tabs for different sections
    tab1, tab2, tab3 = st.tabs(["🎤 Generate Speech", "📊 Generation History", "⚙️ Voice Settings"])
    
    with tab1:
        st.markdown("### 🎤 Generate New Speech")
        
        # Voice selection
        st.markdown("#### 1. Select Voice")
        
        # Sample available voices
        available_voices = [
            {"name": "My Professional Voice", "model": "VITS", "quality": "9.2/10", "status": "Ready"},
            {"name": "My Casual Voice", "model": "So-VITS-SVC", "quality": "8.8/10", "status": "Ready"},
            {"name": "My Storytelling Voice", "model": "Bark", "quality": "9.5/10", "status": "Ready"},
            {"name": "My Singing Voice", "model": "VITS", "quality": "8.5/10", "status": "Training"}
        ]
        
        # Filter ready voices
        ready_voices = [v for v in available_voices if v["status"] == "Ready"]
        
        if not ready_voices:
            st.warning("⚠️ No trained voices available. Please complete voice training first.")
            st.info("Navigate to Voice Training to start training your voice.")
        else:
            # Voice selection dropdown
            voice_options = [f"{v['name']} ({v['model']}) - {v['quality']}" for v in ready_voices]
            selected_voice = st.selectbox("Choose Voice", voice_options, index=0)
            
            # Get selected voice details
            selected_voice_name = selected_voice.split(" (")[0]
            selected_voice_model = selected_voice.split("(")[1].split(")")[0]
            
            st.markdown(f"**Selected**: {selected_voice_name} using {selected_voice_model} model")
            
            # Text input
            st.markdown("#### 2. Enter Text")
            
            text_input_method = st.radio("Input Method", ["Single Text", "Batch Text", "File Upload"])
            
            if text_input_method == "Single Text":
                text_input = st.text_area(
                    "Enter text to convert to speech",
                    placeholder="Enter your text here...",
                    height=150,
                    help="Maximum 1000 characters"
                )
                
                # Character count
                if text_input:
                    char_count = len(text_input)
                    st.markdown(f"**Characters**: {char_count}/1000")
                    
                    if char_count > 1000:
                        st.error("Text exceeds 1000 character limit. Please shorten your text.")
                        text_input = None
                
                # Quick text examples
                st.markdown("**Quick Examples:**")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("Hello World", key="ex1"):
                        st.session_state.example_text = "Hello, world! Welcome to the voice cloning platform."
                        st.rerun()
                
                with col2:
                    if st.button("Professional", key="ex2"):
                        st.session_state.example_text = "Thank you for your time today. I look forward to our next meeting."
                        st.rerun()
                
                with col3:
                    if st.button("Story", key="ex3"):
                        st.session_state.example_text = "Once upon a time, in a land far away, there lived a brave knight who protected the kingdom."
                        st.rerun()
                
                # Set example text if available
                if 'example_text' in st.session_state:
                    text_input = st.text_area(
                        "Enter text to convert to speech",
                        value=st.session_state.example_text,
                        height=150
                    )
            
            elif text_input_method == "Batch Text":
                st.markdown("**Batch Processing**")
                st.info("Upload a text file (TXT, CSV) with multiple lines for batch generation.")
                
                batch_file = st.file_uploader(
                    "Upload text file",
                    type=["txt", "csv"],
                    help="Each line will be processed as a separate audio file"
                )
                
                if batch_file:
                    st.success(f"✅ File uploaded: {batch_file.name}")
                    # In real app, would read and display file contents
            
            else:  # File Upload
                st.markdown("**File Upload**")
                st.info("Upload a document (PDF, DOCX, TXT) to extract text for speech generation.")
                
                doc_file = st.file_uploader(
                    "Upload document",
                    type=["pdf", "docx", "txt"],
                    help="Text will be extracted and converted to speech"
                )
                
                if doc_file:
                    st.success(f"✅ Document uploaded: {doc_file.name}")
            
            # Voice parameters
            st.markdown("#### 3. Voice Parameters")
            
            col1, col2 = st.columns(2)
            
            with col1:
                emotion = st.selectbox(
                    "Emotion",
                    ["Neutral", "Happy", "Sad", "Angry", "Calm", "Excited", "Professional", "Casual"],
                    index=0
                )
                
                speed = st.slider(
                    "Speed",
                    min_value=0.5,
                    max_value=2.0,
                    value=1.0,
                    step=0.1,
                    help="1.0 = normal speed, 0.5 = half speed, 2.0 = double speed"
                )
                
                pitch = st.slider(
                    "Pitch",
                    min_value=0.5,
                    max_value=2.0,
                    value=1.0,
                    step=0.1,
                    help="1.0 = normal pitch, 0.5 = lower pitch, 2.0 = higher pitch"
                )
            
            with col2:
                volume = st.slider(
                    "Volume",
                    min_value=0.1,
                    max_value=2.0,
                    value=1.0,
                    step=0.1,
                    help="1.0 = normal volume"
                )
                
                clarity = st.slider(
                    "Clarity",
                    min_value=0.5,
                    max_value=1.0,
                    value=0.8,
                    step=0.05,
                    help="Higher values produce clearer speech"
                )
                
                stability = st.slider(
                    "Stability",
                    min_value=0.1,
                    max_value=1.0,
                    value=0.7,
                    step=0.1,
                    help="Higher values produce more consistent output"
                )
            
            # Advanced settings
            with st.expander("🔧 Advanced Settings"):
                col1, col2 = st.columns(2)
                
                with col1:
                    sample_rate = st.selectbox("Sample Rate", [16000, 22050, 44100], index=2)
                    audio_format = st.selectbox("Output Format", ["WAV", "MP3", "FLAC"], index=0)
                    noise_reduction = st.checkbox("Enable Noise Reduction", value=True)
                
                with col2:
                    silence_padding = st.number_input("Silence Padding (ms)", min_value=0, max_value=1000, value=100, step=50)
                    voice_cloning_strength = st.slider("Voice Cloning Strength", min_value=0.0, max_value=1.0, value=0.8, step=0.1)
                    temperature = st.slider("Creativity (Temperature)", min_value=0.1, max_value=2.0, value=0.8, step=0.1)
            
            # Generate button
            st.markdown("#### 4. Generate Speech")
            
            if st.button("🚀 Generate Speech", use_container_width=True, type="primary"):
                if text_input_method == "Single Text" and (not text_input or len(text_input.strip()) == 0):
                    st.error("Please enter text to convert to speech.")
                else:
                    # Show generation progress
                    with st.spinner("Generating speech..."):
                        # Simulate generation process
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        for i in range(101):
                            time.sleep(0.02)  # Simulate processing time
                            progress_bar.progress(i)
                            if i < 30:
                                status_text.text("Processing text...")
                            elif i < 60:
                                status_text.text("Generating audio...")
                            elif i < 90:
                                status_text.text("Applying voice parameters...")
                            else:
                                status_text.text("Finalizing audio...")
                        
                        progress_bar.empty()
                        status_text.empty()
                        
                        st.success("✅ Speech generated successfully!")
                        
                        # Display generated audio
                        st.markdown("#### 🎵 Generated Audio")
                        
                        # Simulate audio player
                        col1, col2, col3 = st.columns([2, 1, 1])
                        
                        with col1:
                            st.markdown("**Audio Preview**")
                            st.markdown("🎵 [Generated Audio - Click to Play]")
                            st.markdown("*Audio duration: 12.5 seconds*")
                        
                        with col2:
                            st.markdown("**Download Options**")
                            if st.button("📥 WAV", key="dl_wav"):
                                st.info("WAV file download started...")
                            if st.button("📥 MP3", key="dl_mp3"):
                                st.info("MP3 file download started...")
                        
                        with col3:
                            st.markdown("**Actions**")
                            if st.button("🔄 Regenerate", key="regenerate"):
                                st.info("Regenerating with same parameters...")
                            if st.button("💾 Save", key="save_audio"):
                                st.info("Audio saved to your library...")
                        
                        # Show generation details
                        st.markdown("#### 📊 Generation Details")
                        
                        details_col1, details_col2 = st.columns(2)
                        
                        with details_col1:
                            st.markdown("**Voice**: My Professional Voice (VITS)")
                            st.markdown("**Text Length**: 89 characters")
                            st.markdown("**Generation Time**: 2.1 seconds")
                            st.markdown("**Model Version**: v2.1.0")
                        
                        with details_col2:
                            st.markdown("**Emotion**: Professional")
                            st.markdown("**Speed**: 1.0x")
                            st.markdown("**Pitch**: 1.0x")
                            st.markdown("**Quality Score**: 9.2/10")
    
    with tab2:
        st.markdown("### 📊 Generation History")
        
        # Sample generation history
        generation_history = [
            {
                "timestamp": "2 hours ago",
                "voice": "My Professional Voice",
                "text": "Hello, welcome to our meeting today.",
                "duration": "3.2s",
                "format": "WAV",
                "quality": "9.2/10",
                "status": "Completed"
            },
            {
                "timestamp": "5 hours ago",
                "voice": "My Casual Voice",
                "text": "Hey there! How's it going?",
                "duration": "2.8s",
                "format": "MP3",
                "quality": "8.8/10",
                "status": "Completed"
            },
            {
                "timestamp": "1 day ago",
                "voice": "My Storytelling Voice",
                "text": "Once upon a time...",
                "duration": "15.4s",
                "format": "WAV",
                "quality": "9.5/10",
                "status": "Completed"
            }
        ]
        
        # Filter options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            voice_filter = st.selectbox("Filter by Voice", ["All"] + list(set([h["voice"] for h in generation_history])))
        
        with col2:
            format_filter = st.selectbox("Filter by Format", ["All"] + list(set([h["format"] for h in generation_history])))
        
        with col3:
            date_filter = st.selectbox("Filter by Date", ["All", "Today", "This Week", "This Month"])
        
        # Apply filters
        filtered_history = generation_history
        if voice_filter != "All":
            filtered_history = [h for h in filtered_history if h["voice"] == voice_filter]
        if format_filter != "All":
            filtered_history = [h for h in filtered_history if h["format"] == format_filter]
        
        # Display filtered history
        if filtered_history:
            df_history = pd.DataFrame(filtered_history)
            st.dataframe(df_history, use_container_width=True)
            
            # Statistics
            st.markdown("### 📈 Generation Statistics")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                total_generations = len(filtered_history)
                st.metric("Total Generations", total_generations)
            
            with col2:
                avg_quality = sum([float(h["quality"].split("/")[0]) for h in filtered_history]) / len(filtered_history)
                st.metric("Average Quality", f"{avg_quality:.1f}/10")
            
            with col3:
                total_duration = sum([float(h["duration"].replace("s", "")) for h in filtered_history])
                st.metric("Total Duration", f"{total_duration:.1f}s")
            
            # Quality trend chart
            st.markdown("### 📊 Quality Trend")
            
            # Simulate quality data over time
            dates = pd.date_range(start=datetime.now() - timedelta(days=7), periods=7, freq='D')
            qualities = [8.5, 8.8, 9.1, 8.9, 9.2, 9.0, 9.3]
            
            fig_quality = px.line(
                x=dates,
                y=qualities,
                title="Generation Quality Over Time",
                labels={"x": "Date", "y": "Quality Score"}
            )
            fig_quality.update_layout(height=300)
            st.plotly_chart(fig_quality, use_container_width=True)
        else:
            st.info("No generation history found with the selected filters.")
    
    with tab3:
        st.markdown("### ⚙️ Voice Settings & Preferences")
        
        # Default voice parameters
        st.markdown("#### 🎛️ Default Voice Parameters")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Speech Settings**")
            default_emotion = st.selectbox("Default Emotion", ["Neutral", "Happy", "Sad", "Angry", "Calm", "Excited"], index=0)
            default_speed = st.slider("Default Speed", min_value=0.5, max_value=2.0, value=1.0, step=0.1)
            default_pitch = st.slider("Default Pitch", min_value=0.5, max_value=2.0, value=1.0, step=0.1)
        
        with col2:
            st.markdown("**Audio Settings**")
            default_volume = st.slider("Default Volume", min_value=0.1, max_value=2.0, value=1.0, step=0.1)
            default_format = st.selectbox("Default Format", ["WAV", "MP3", "FLAC"], index=0)
            default_sample_rate = st.selectbox("Default Sample Rate", [16000, 22050, 44100], index=2)
        
        # Voice-specific settings
        st.markdown("#### 🎤 Voice-Specific Settings")
        
        voice_settings = st.selectbox("Select Voice for Custom Settings", [v["name"] for v in available_voices])
        
        if voice_settings:
            st.markdown(f"**Custom Settings for {voice_settings}**")
            
            col1, col2 = st.columns(2)
            
            with col1:
                custom_emotion = st.selectbox("Preferred Emotion", ["Auto", "Neutral", "Happy", "Sad", "Angry", "Calm", "Excited"], index=0, key="custom_emotion")
                custom_speed = st.slider("Preferred Speed", min_value=0.5, max_value=2.0, value=1.0, step=0.1, key="custom_speed")
                custom_pitch = st.slider("Preferred Pitch", min_value=0.5, max_value=2.0, value=1.0, step=0.1, key="custom_pitch")
            
            with col2:
                custom_volume = st.slider("Preferred Volume", min_value=0.1, max_value=2.0, value=1.0, step=0.1, key="custom_volume")
                custom_clarity = st.slider("Preferred Clarity", min_value=0.5, max_value=1.0, value=0.8, step=0.05, key="custom_clarity")
                custom_stability = st.slider("Preferred Stability", min_value=0.1, max_value=1.0, value=0.7, step=0.1, key="custom_stability")
        
        # Batch processing settings
        st.markdown("#### 📦 Batch Processing Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            auto_download = st.checkbox("Auto-download generated files", value=False)
            save_to_library = st.checkbox("Auto-save to library", value=True)
            email_notifications = st.checkbox("Email notifications for batch completion", value=False)
        
        with col2:
            max_batch_size = st.number_input("Maximum batch size", min_value=10, max_value=1000, value=100, step=10)
            batch_timeout = st.number_input("Batch timeout (minutes)", min_value=5, max_value=120, value=30, step=5)
            retry_failed = st.checkbox("Retry failed generations", value=True)
        
        # Save settings
        if st.button("💾 Save All Settings", use_container_width=True):
            st.success("Settings saved successfully!")
            st.info("Your preferences will be applied to future voice generations.")