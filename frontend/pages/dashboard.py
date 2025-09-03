import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
import random

def show():
    st.markdown('<div class="main-header">📊 Dashboard</div>', unsafe_allow_html=True)
    
    # Welcome message
    st.markdown(f"### Welcome back, {st.session_state.user_info['username']}! 👋")
    st.markdown("Here's an overview of your voice cloning activities.")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>🎤 Total Voices</h3>
            <h2>5</h2>
            <p>+2 this month</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>✅ Trained Voices</h3>
            <h2>3</h2>
            <p>2 in progress</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>🎵 Audio Generated</h3>
            <h2>127</h2>
            <p>+23 this week</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>💳 Credits Left</h3>
            <h2>73</h2>
            <p>+25 this month</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Recent activity and charts
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📈 Training Progress")
        
        # Sample training data
        training_data = {
            'Voice': ['My Voice 1', 'My Voice 2', 'My Voice 3', 'My Voice 4', 'My Voice 5'],
            'Progress': [100, 85, 100, 45, 0],
            'Status': ['Completed', 'Training', 'Completed', 'Training', 'Pending'],
            'Model': ['VITS', 'So-VITS-SVC', 'VITS', 'Bark', 'VITS']
        }
        
        df_training = pd.DataFrame(training_data)
        
        # Create progress bars
        for _, row in df_training.iterrows():
            progress_color = "green" if row['Progress'] == 100 else "orange" if row['Progress'] > 0 else "gray"
            st.markdown(f"**{row['Voice']}** ({row['Model']})")
            st.progress(row['Progress'] / 100)
            st.markdown(f"Status: {row['Status']} - {row['Progress']}%")
            st.markdown("---")
    
    with col2:
        st.markdown("### 🎯 Quick Actions")
        
        if st.button("🎤 Create New Voice", use_container_width=True):
            st.info("Navigate to Voice Training to create a new voice")
        
        if st.button("🎵 Generate Speech", use_container_width=True):
            st.info("Navigate to Voice Generation to create audio")
        
        if st.button("📚 Browse Voices", use_container_width=True):
            st.info("Navigate to Voice Library to explore voices")
        
        st.markdown("---")
        
        st.markdown("### 📊 Usage Stats")
        
        # Sample usage data
        usage_data = {
            'Category': ['Voice Training', 'Audio Generation', 'Model Storage'],
            'Usage': [45, 23, 12]
        }
        
        fig_pie = px.pie(
            usage_data, 
            values='Usage', 
            names='Category',
            title="Resource Usage Distribution"
        )
        fig_pie.update_layout(height=300)
        st.plotly_chart(fig_pie, use_container_width=True)
    
    st.markdown("---")
    
    # Recent activity
    st.markdown("### 🔄 Recent Activity")
    
    # Sample activity data
    activities = [
        {"time": "2 hours ago", "action": "Voice training completed", "voice": "My Voice 2", "status": "✅"},
        {"time": "5 hours ago", "action": "Generated audio", "voice": "My Voice 1", "status": "🎵"},
        {"time": "1 day ago", "action": "Voice training started", "voice": "My Voice 4", "status": "🔄"},
        {"time": "2 days ago", "action": "Voice created", "voice": "My Voice 5", "status": "🎤"},
        {"time": "3 days ago", "action": "Audio downloaded", "voice": "My Voice 3", "status": "⬇️"}
    ]
    
    for activity in activities:
        col1, col2, col3, col4 = st.columns([1, 3, 2, 1])
        with col1:
            st.markdown(f"**{activity['time']}**")
        with col2:
            st.markdown(activity['action'])
        with col3:
            st.markdown(f"**{activity['voice']}**")
        with col4:
            st.markdown(activity['status'])
        st.markdown("---")
    
    # Voice quality insights
    st.markdown("### 💡 Voice Quality Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🎯 Training Recommendations**")
        st.markdown("""
        - **My Voice 2**: Consider adding more diverse samples for better emotion control
        - **My Voice 4**: Audio quality is good, training should complete successfully
        - **My Voice 5**: Ready to start training with current sample set
        """)
    
    with col2:
        st.markdown("**📈 Performance Trends**")
        st.markdown("""
        - **Voice Quality**: Improving over time with more training data
        - **Training Speed**: 15% faster than last month
        - **Success Rate**: 95% of voices trained successfully
        """)
    
    # System status
    st.markdown("---")
    st.markdown("### 🖥️ System Status")
    
    status_col1, status_col2, status_col3 = st.columns(3)
    
    with status_col1:
        st.markdown("**API Status**: 🟢 Operational")
        st.markdown("**Response Time**: 45ms avg")
    
    with status_col2:
        st.markdown("**Training Queue**: 🟡 2 pending")
        st.markdown("**GPU Utilization**: 78%")
    
    with status_col3:
        st.markdown("**Storage**: 🟢 23% used")
        st.markdown("**Uptime**: 99.9%")