import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

def show():
    st.markdown('<div class="main-header">📚 Voice Library</div>', unsafe_allow_html=True)
    
    # Page description
    st.markdown("""
    ### Browse and Manage Your Voice Collection
    
    Explore your trained voices, discover public voices, and manage your voice models.
    """)
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs(["🎤 My Voices", "🌍 Public Voices", "📊 Voice Analytics", "⚙️ Voice Management"])
    
    with tab1:
        st.markdown("### 🎤 My Voice Collection")
        
        # Sample user voices
        my_voices = [
            {
                "name": "My Professional Voice",
                "model": "VITS",
                "status": "Trained",
                "quality": 9.2,
                "created": "2 days ago",
                "last_used": "2 hours ago",
                "usage_count": 127,
                "is_public": False,
                "language": "en",
                "gender": "Male",
                "age_group": "Adult"
            },
            {
                "name": "My Casual Voice",
                "model": "So-VITS-SVC",
                "status": "Trained",
                "quality": 8.8,
                "created": "1 week ago",
                "last_used": "5 hours ago",
                "usage_count": 89,
                "is_public": False,
                "language": "en",
                "gender": "Male",
                "age_group": "Adult"
            },
            {
                "name": "My Storytelling Voice",
                "model": "Bark",
                "status": "Trained",
                "quality": 9.5,
                "created": "3 days ago",
                "last_used": "1 day ago",
                "usage_count": 45,
                "is_public": True,
                "language": "en",
                "gender": "Male",
                "age_group": "Adult"
            },
            {
                "name": "My Singing Voice",
                "model": "VITS",
                "status": "Training",
                "quality": None,
                "created": "1 day ago",
                "last_used": "Never",
                "usage_count": 0,
                "is_public": False,
                "language": "en",
                "gender": "Male",
                "age_group": "Adult"
            }
        ]
        
        # Filter options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            status_filter = st.selectbox("Filter by Status", ["All", "Trained", "Training", "Pending"])
        
        with col2:
            model_filter = st.selectbox("Filter by Model", ["All", "VITS", "So-VITS-SVC", "Bark"])
        
        with col3:
            language_filter = st.selectbox("Filter by Language", ["All", "en", "es", "fr", "de", "it", "ja", "ko", "zh"])
        
        # Apply filters
        filtered_voices = my_voices
        if status_filter != "All":
            filtered_voices = [v for v in filtered_voices if v["status"] == status_filter]
        if model_filter != "All":
            filtered_voices = [v for v in filtered_voices if v["model"] == model_filter]
        if language_filter != "All":
            filtered_voices = [v for v in filtered_voices if v["language"] == language_filter]
        
        # Display voices
        if filtered_voices:
            for voice in filtered_voices:
                with st.expander(f"🎤 {voice['name']} ({voice['model']})", expanded=True):
                    col1, col2, col3 = st.columns([2, 1, 1])
                    
                    with col1:
                        st.markdown(f"**Status**: {voice['status']}")
                        st.markdown(f"**Quality**: {voice['quality']}/10" if voice['quality'] else "**Quality**: Training...")
                        st.markdown(f"**Created**: {voice['created']}")
                        st.markdown(f"**Last Used**: {voice['last_used']}")
                        st.markdown(f"**Usage Count**: {voice['usage_count']}")
                        
                        # Quality indicator
                        if voice['quality']:
                            if voice['quality'] >= 9.0:
                                st.markdown("🟢 Excellent Quality")
                            elif voice['quality'] >= 8.0:
                                st.markdown("🟡 Good Quality")
                            else:
                                st.markdown("🔴 Needs Improvement")
                    
                    with col2:
                        st.markdown("**Characteristics**")
                        st.markdown(f"Language: {voice['language'].upper()}")
                        st.markdown(f"Gender: {voice['gender']}")
                        st.markdown(f"Age: {voice['age_group']}")
                        st.markdown(f"Public: {'Yes' if voice['is_public'] else 'No'}")
                        
                        # Model info
                        st.markdown("**Model Info**")
                        if voice['model'] == "VITS":
                            st.markdown("🎯 Fast & Efficient")
                        elif voice['model'] == "So-VITS-SVC":
                            st.markdown("🎵 High Quality")
                        elif voice['model'] == "Bark":
                            st.markdown("🎭 Creative Control")
                    
                    with col3:
                        st.markdown("**Actions**")
                        
                        if voice['status'] == "Trained":
                            if st.button("🎵 Generate", key=f"gen_{voice['name']}"):
                                st.info("Navigate to Voice Generation to use this voice")
                            
                            if st.button("📊 Analytics", key=f"analytics_{voice['name']}"):
                                st.info("View detailed analytics for this voice")
                            
                            if st.button("📥 Download", key=f"download_{voice['name']}"):
                                st.info("Download model files started...")
                            
                            if st.button("🔗 Share", key=f"share_{voice['name']}"):
                                if voice['is_public']:
                                    st.success("Voice is already public!")
                                else:
                                    st.info("Make voice public to share with others")
                        
                        elif voice['status'] == "Training":
                            st.markdown("⏳ Training in progress...")
                            if st.button("📊 Monitor", key=f"monitor_{voice['name']}"):
                                st.info("Navigate to Voice Training to monitor progress")
                        
                        # Toggle public status
                        if voice['status'] == "Trained":
                            if voice['is_public']:
                                if st.button("🔒 Make Private", key=f"private_{voice['name']}"):
                                    st.success("Voice is now private")
                            else:
                                if st.button("🌍 Make Public", key=f"public_{voice['name']}"):
                                    st.success("Voice is now public!")
                        
                        # Delete voice
                        if st.button("🗑️ Delete", key=f"delete_{voice['name']}", type="secondary"):
                            st.warning("Are you sure you want to delete this voice?")
                            if st.button("✅ Confirm Delete", key=f"confirm_delete_{voice['name']}"):
                                st.success("Voice deleted successfully!")
        else:
            st.info("No voices found with the selected filters.")
        
        # Voice statistics
        st.markdown("---")
        st.markdown("### 📊 My Voice Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_voices = len([v for v in my_voices if v["status"] == "Trained"])
            st.metric("Total Trained Voices", total_voices)
        
        with col2:
            avg_quality = sum([v["quality"] for v in my_voices if v["quality"]]) / len([v for v in my_voices if v["quality"]])
            st.metric("Average Quality", f"{avg_quality:.1f}/10")
        
        with col3:
            total_usage = sum([v["usage_count"] for v in my_voices])
            st.metric("Total Usage", total_usage)
        
        with col4:
            public_voices = len([v for v in my_voices if v["is_public"]])
            st.metric("Public Voices", public_voices)
    
    with tab2:
        st.markdown("### 🌍 Public Voice Library")
        
        # Sample public voices
        public_voices = [
            {
                "name": "Professional Narrator",
                "creator": "VoiceMaster",
                "model": "VITS",
                "quality": 9.4,
                "language": "en",
                "gender": "Female",
                "age_group": "Adult",
                "downloads": 1247,
                "rating": 4.8,
                "tags": ["professional", "narrator", "clear"]
            },
            {
                "name": "Casual Friend",
                "creator": "VoiceArtist",
                "model": "So-VITS-SVC",
                "quality": 9.1,
                "language": "en",
                "gender": "Male",
                "age_group": "Young",
                "downloads": 892,
                "rating": 4.6,
                "tags": ["casual", "friendly", "natural"]
            },
            {
                "name": "Storyteller",
                "creator": "VoiceCraft",
                "model": "Bark",
                "quality": 9.6,
                "language": "en",
                "gender": "Female",
                "age_group": "Adult",
                "downloads": 2156,
                "rating": 4.9,
                "tags": ["storytelling", "expressive", "creative"]
            }
        ]
        
        # Search and filter
        col1, col2 = st.columns([2, 1])
        
        with col1:
            search_query = st.text_input("Search voices", placeholder="Search by name, creator, or tags...")
        
        with col2:
            sort_by = st.selectbox("Sort by", ["Popularity", "Quality", "Rating", "Downloads", "Newest"])
        
        # Apply search filter
        if search_query:
            filtered_public = [v for v in public_voices if 
                             search_query.lower() in v["name"].lower() or
                             search_query.lower() in v["creator"].lower() or
                             any(search_query.lower() in tag.lower() for tag in v["tags"])]
        else:
            filtered_public = public_voices
        
        # Sort voices
        if sort_by == "Popularity":
            filtered_public.sort(key=lambda x: x["downloads"], reverse=True)
        elif sort_by == "Quality":
            filtered_public.sort(key=lambda x: x["quality"], reverse=True)
        elif sort_by == "Rating":
            filtered_public.sort(key=lambda x: x["rating"], reverse=True)
        elif sort_by == "Downloads":
            filtered_public.sort(key=lambda x: x["downloads"], reverse=True)
        
        # Display public voices
        if filtered_public:
            for voice in filtered_public:
                with st.expander(f"🌍 {voice['name']} by {voice['creator']} ({voice['model']})", expanded=True):
                    col1, col2, col3 = st.columns([2, 1, 1])
                    
                    with col1:
                        st.markdown(f"**Quality**: {voice['quality']}/10")
                        st.markdown(f"**Language**: {voice['language'].upper()}")
                        st.markdown(f"**Gender**: {voice['gender']}")
                        st.markdown(f"**Age Group**: {voice['age_group']}")
                        st.markdown(f"**Downloads**: {voice['downloads']:,}")
                        st.markdown(f"**Rating**: {voice['rating']}/5 ⭐")
                        
                        # Tags
                        tags_text = " ".join([f"`{tag}`" for tag in voice["tags"]])
                        st.markdown(f"**Tags**: {tags_text}")
                    
                    with col2:
                        st.markdown("**Model Info**")
                        if voice['model'] == "VITS":
                            st.markdown("🎯 Fast & Efficient")
                        elif voice['model'] == "So-VITS-SVC":
                            st.markdown("🎵 High Quality")
                        elif voice['model'] == "Bark":
                            st.markdown("🎭 Creative Control")
                        
                        st.markdown("**Creator**: " + voice['creator'])
                    
                    with col3:
                        st.markdown("**Actions**")
                        
                        if st.button("🎵 Try Voice", key=f"try_{voice['name']}"):
                            st.info("Navigate to Voice Generation to test this voice")
                        
                        if st.button("📥 Download", key=f"download_public_{voice['name']}"):
                            st.success("Voice downloaded successfully!")
                        
                        if st.button("⭐ Rate", key=f"rate_{voice['name']}"):
                            rating = st.slider("Your Rating", 1, 5, 3, key=f"rating_{voice['name']}")
                            if st.button("Submit Rating", key=f"submit_rating_{voice['name']}"):
                                st.success(f"Thank you for rating this voice {rating}/5!")
                        
                        if st.button("🔖 Bookmark", key=f"bookmark_{voice['name']}"):
                            st.success("Voice bookmarked!")
        else:
            st.info("No public voices found matching your search criteria.")
    
    with tab3:
        st.markdown("### 📊 Voice Analytics & Insights")
        
        # Voice usage analytics
        st.markdown("#### 📈 Usage Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Usage over time chart
            dates = pd.date_range(start=datetime.now() - timedelta(days=30), periods=30, freq='D')
            usage_data = [random.randint(5, 25) for _ in range(30)]
            
            fig_usage = px.line(
                x=dates,
                y=usage_data,
                title="Voice Usage Over Time",
                labels={"x": "Date", "y": "Usage Count"}
            )
            fig_usage.update_layout(height=300)
            st.plotly_chart(fig_usage, use_container_width=True)
        
        with col2:
            # Voice quality distribution
            quality_data = [9.2, 8.8, 9.5, 8.5, 9.1, 8.9, 9.3]
            
            fig_quality = px.histogram(
                x=quality_data,
                title="Voice Quality Distribution",
                labels={"x": "Quality Score", "y": "Count"},
                nbins=10
            )
            fig_quality.update_layout(height=300)
            st.plotly_chart(fig_quality, use_container_width=True)
        
        # Performance metrics
        st.markdown("#### 🎯 Performance Metrics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Average Generation Time", "2.1s", "-0.3s")
        
        with col2:
            st.metric("Success Rate", "98.5%", "+1.2%")
        
        with col3:
            st.metric("User Satisfaction", "4.7/5", "+0.2")
        
        with col4:
            st.metric("Model Efficiency", "87%", "+5%")
        
        # Voice comparison
        st.markdown("#### 🔍 Voice Comparison")
        
        comparison_data = {
            "Voice": ["My Professional", "My Casual", "My Storytelling"],
            "Quality": [9.2, 8.8, 9.5],
            "Usage": [127, 89, 45],
            "Rating": [4.8, 4.6, 4.9],
            "Efficiency": [92, 88, 95]
        }
        
        df_comparison = pd.DataFrame(comparison_data)
        st.dataframe(df_comparison, use_container_width=True)
        
        # Quality vs Usage scatter plot
        fig_scatter = px.scatter(
            df_comparison,
            x="Quality",
            y="Usage",
            size="Rating",
            color="Voice",
            title="Quality vs Usage Analysis",
            labels={"Quality": "Quality Score", "Usage": "Usage Count"}
        )
        fig_scatter.update_layout(height=400)
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    with tab4:
        st.markdown("### ⚙️ Voice Management & Settings")
        
        # Voice organization
        st.markdown("#### 📁 Voice Organization")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Create Voice Categories**")
            new_category = st.text_input("New Category Name", placeholder="e.g., Professional, Personal, Creative")
            if st.button("➕ Add Category"):
                if new_category:
                    st.success(f"Category '{new_category}' created!")
                else:
                    st.error("Please enter a category name")
            
            st.markdown("**Existing Categories**")
            categories = ["Professional", "Personal", "Creative", "Experimental"]
            for cat in categories:
                col_a, col_b = st.columns([3, 1])
                with col_a:
                    st.markdown(f"📁 {cat}")
                with col_b:
                    if st.button("🗑️", key=f"del_cat_{cat}"):
                        st.success(f"Category '{cat}' deleted!")
        
        with col2:
            st.markdown("**Voice Permissions**")
            st.markdown("**Default Privacy**: Private")
            st.markdown("**Auto-Share**: Disabled")
            st.markdown("**Download Protection**: Enabled")
            
            if st.button("🔒 Manage Permissions"):
                st.info("Permission management panel opened")
        
        # Backup and restore
        st.markdown("#### 💾 Backup & Restore")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Backup Options**")
            backup_frequency = st.selectbox("Backup Frequency", ["Daily", "Weekly", "Monthly", "Manual"])
            include_models = st.checkbox("Include Model Files", value=True)
            include_samples = st.checkbox("Include Audio Samples", value=True)
            
            if st.button("💾 Create Backup"):
                st.success("Backup created successfully!")
        
        with col2:
            st.markdown("**Restore Options**")
            backup_files = st.file_uploader("Select Backup File", type=["zip", "tar.gz"])
            if backup_files:
                st.success(f"Backup file selected: {backup_files.name}")
                if st.button("🔄 Restore from Backup"):
                    st.info("Restore process started...")
        
        # Voice optimization
        st.markdown("#### 🚀 Voice Optimization")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Quality Improvement**")
            auto_retrain = st.checkbox("Auto-retrain low-quality voices", value=False)
            quality_threshold = st.slider("Quality Threshold", 7.0, 10.0, 8.0, 0.1)
            retrain_interval = st.selectbox("Retrain Interval", ["Weekly", "Monthly", "Quarterly", "Never"])
        
        with col2:
            st.markdown("**Performance Tuning**")
            model_compression = st.checkbox("Enable Model Compression", value=True)
            cache_models = st.checkbox("Cache Frequently Used Models", value=True)
            parallel_processing = st.checkbox("Enable Parallel Processing", value=False)
        
        # Save all settings
        if st.button("💾 Save All Settings", use_container_width=True):
            st.success("All settings saved successfully!")
            st.info("Your voice management preferences have been updated.")