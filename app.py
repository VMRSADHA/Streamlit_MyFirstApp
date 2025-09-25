import streamlit as st
import time
import datetime
from PIL import Image
import os

# Page configuration
st.set_page_config(
    page_title="🏋️ Fitness Stopwatch",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with fitness theme
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #ff6b6b 0%, #4ecdc4 50%, #45b7d1 100%);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .stApp {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 25px;
        margin: 15px;
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
        border: 3px solid #4ecdc4;
    }
    
    .fitness-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        margin: 10px 0;
        border: 4px solid #ffd93d;
    }
    
    .stopwatch-display {
        font-family: 'Courier New', monospace;
        font-size: 5rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4, #45B7D1, #FFD93D);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        padding: 30px;
        margin: 20px 0;
        border: 4px solid;
        border-image: linear-gradient(45deg, #FF6B6B, #4ECDC4, #45B7D1) 1;
        border-radius: 15px;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    
    .fitness-button {
        border-radius: 15px !important;
        border: 3px solid !important;
        font-weight: bold !important;
        padding: 15px 25px !important;
        font-size: 1.2rem !important;
        transition: all 0.3s ease !important;
        margin: 5px !important;
    }
    
    .start-button {
        background: linear-gradient(135deg, #4CAF50, #45a049) !important;
        color: white !important;
        border-color: #388E3C !important;
    }
    
    .stop-button {
        background: linear-gradient(135deg, #f44336, #d32f2f) !important;
        color: white !important;
        border-color: #c62828 !important;
    }
    
    .reset-button {
        background: linear-gradient(135deg, #2196F3, #1976D2) !important;
        color: white !important;
        border-color: #1565C0 !important;
    }
    
    .lap-button {
        background: linear-gradient(135deg, #FF9800, #F57C00) !important;
        color: white !important;
        border-color: #EF6C00 !important;
    }
    
    .exercise-card {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        border: 2px solid #ffd93d;
        text-align: center;
    }
    
    .stats-card {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        margin: 10px;
        text-align: center;
        border: 2px solid #ff6b6b;
    }
    
    .lap-time {
        background: linear-gradient(135deg, #d4fc79 0%, #96e6a1 100%);
        border-left: 5px solid #4ecdc4;
        padding: 15px;
        margin: 8px 0;
        border-radius: 10px;
        font-family: 'Courier New', monospace;
        font-weight: bold;
    }
    
    .emoji-bar {
        display: flex;
        justify-content: space-around;
        font-size: 2rem;
        padding: 15px;
        background: rgba(255, 255, 255, 0.8);
        border-radius: 15px;
        margin: 15px 0;
        border: 2px dashed #4ecdc4;
    }
    
    .gif-container {
        text-align: center;
        padding: 10px;
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        margin: 10px 0;
        border: 2px solid #ffd93d;
    }
</style>
""", unsafe_allow_html=True)

class FitnessStopwatch:
    def __init__(self):
        # Initialize session state variables
        if 'running' not in st.session_state:
            st.session_state.running = False
        if 'start_time' not in st.session_state:
            st.session_state.start_time = None
        if 'elapsed_time' not in st.session_state:
            st.session_state.elapsed_time = 0
        if 'lap_times' not in st.session_state:
            st.session_state.lap_times = []
        if 'last_update' not in st.session_state:
            st.session_state.last_update = time.time()
        if 'current_exercise' not in st.session_state:
            st.session_state.current_exercise = "Warm-up"
        if 'calories_burned' not in st.session_state:
            st.session_state.calories_burned = 0
    
    def start(self):
        if not st.session_state.running:
            st.session_state.running = True
            if st.session_state.start_time is None:
                st.session_state.start_time = time.time() - st.session_state.elapsed_time
            st.session_state.last_update = time.time()
    
    def stop(self):
        if st.session_state.running:
            st.session_state.running = False
            current_time = time.time()
            st.session_state.elapsed_time += current_time - st.session_state.last_update
            # Update calories when stopping
            self.update_calories()
    
    def reset(self):
        st.session_state.running = False
        st.session_state.start_time = None
        st.session_state.elapsed_time = 0
        st.session_state.lap_times = []
        st.session_state.last_update = time.time()
        st.session_state.calories_burned = 0
        st.session_state.current_exercise = "Warm-up"
    
    def lap(self):
        if st.session_state.running:
            current_time = time.time()
            lap_time = current_time - st.session_state.start_time
            exercise_type = self.get_exercise_for_lap(len(st.session_state.lap_times) + 1)
            
            st.session_state.lap_times.append({
                'lap_number': len(st.session_state.lap_times) + 1,
                'time': lap_time,
                'timestamp': datetime.datetime.now().strftime("%H:%M:%S"),
                'exercise': exercise_type
            })
            st.session_state.current_exercise = exercise_type
    
    def get_elapsed_time(self):
        if st.session_state.running:
            current_time = time.time()
            return st.session_state.elapsed_time + (current_time - st.session_state.last_update)
        else:
            return st.session_state.elapsed_time
    
    def format_time(self, seconds):
        """Convert seconds to HH:MM:SS.mmm format"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds_remaining = seconds % 60
        milliseconds = int((seconds_remaining - int(seconds_remaining)) * 1000)
        
        return f"{hours:02d}:{minutes:02d}:{int(seconds_remaining):02d}.{milliseconds:03d}"
    
    def get_exercise_for_lap(self, lap_number):
        """Assign different exercises based on lap number"""
        exercises = [
            "🏃‍♂️ Running", "🤸‍♂️ Jumping Jacks", "💪 Push-ups", 
            "🦵 Squats", "🧘‍♂️ Stretching", "🤸‍♀️ Burpees",
            "🚴‍♂️ Cycling", "🏊‍♂️ Swimming", "🥊 Boxing"
        ]
        return exercises[(lap_number - 1) % len(exercises)]
    
    def update_calories(self):
        """Estimate calories burned based on exercise time"""
        # Rough estimate: 5 calories per minute of moderate exercise
        minutes = st.session_state.elapsed_time / 60
        st.session_state.calories_burned = round(minutes * 5, 1)
    
    def get_current_gif(self):
        """Get the appropriate exercise GIF based on current exercise"""
        exercise_gifs = {
            "🏃‍♂️ Running": "assets/running.gif",
            "🤸‍♂️ Jumping Jacks": "assets/jumping_jacks.gif",
            "💪 Push-ups": "assets/pushups.gif",
            "🦵 Squats": "assets/squats.gif",
            "🧘‍♂️ Stretching": "assets/stretching.gif",
            "Warm-up": "assets/stretching.gif"
        }
        return exercise_gifs.get(st.session_state.current_exercise, "assets/running.gif")

def load_gif(gif_path):
    """Load and display GIF"""
    try:
        if os.path.exists(gif_path):
            return st.image(gif_path, use_column_width=True)
        else:
            # Fallback emoji if GIF not found
            return st.markdown(f"<div style='text-align: center; font-size: 4rem;'>🎯</div>", unsafe_allow_html=True)
    except:
        return st.markdown(f"<div style='text-align: center; font-size: 4rem;'>⚡</div>", unsafe_allow_html=True)

def main():
    # Fitness-themed header
    st.markdown("""
    <div class="fitness-header">
        <h1>🏋️ FITNESS STOPWATCH ⏱️</h1>
        <h3>Track Your Workout Like a Pro! 💪</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize stopwatch
    stopwatch = FitnessStopwatch()
    
    # Create columns for layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Emoji bar
        st.markdown("""
        <div class="emoji-bar">
            <span>💪</span><span>🔥</span><span>⚡</span><span>🎯</span><span>🏆</span>
            <span>🚀</span><span>🌟</span><span>💥</span><span>🌈</span><span>🎉</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Stopwatch display
        current_time = stopwatch.get_elapsed_time()
        formatted_time = stopwatch.format_time(current_time)
        
        st.markdown(f'<div class="stopwatch-display">{formatted_time}</div>', unsafe_allow_html=True)
        
        # Control buttons
        button_col1, button_col2, button_col3, button_col4 = st.columns(4)
        
        with button_col1:
            if st.button("▶️ START WORKOUT", key="start", use_container_width=True, 
                        help="Begin your fitness session"):
                stopwatch.start()
                st.rerun()
        
        with button_col2:
            if st.button("⏸️ PAUSE", key="stop", use_container_width=True,
                        help="Pause your workout"):
                stopwatch.stop()
                st.rerun()
        
        with button_col3:
            if st.button("⏹️ RESET", key="reset", use_container_width=True,
                        help="Reset everything and start fresh"):
                stopwatch.reset()
                st.rerun()
        
        with button_col4:
            if st.button("⏱️ NEXT EXERCISE", key="lap", use_container_width=True,
                        disabled=not st.session_state.running,
                        help="Record current time and move to next exercise"):
                stopwatch.lap()
                st.rerun()
        
        # Exercise GIF display
        st.markdown("### 🎬 Current Exercise Demo")
        gif_path = stopwatch.get_current_gif()
        load_gif(gif_path)
    
    with col2:
        # Fitness statistics
        st.markdown("### 📊 Workout Stats")
        
        col_stat1, col_stat2 = st.columns(2)
        
        with col_stat1:
            st.markdown(f"""
            <div class="stats-card">
                <h4>🔥 Calories Burned</h4>
                <h2>{st.session_state.calories_burned}</h2>
                <p>kcal</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="stats-card">
                <h4>⏱️ Current Exercise</h4>
                <h3>{st.session_state.current_exercise}</h3>
            </div>
            """, unsafe_allow_html=True)
        
        with col_stat2:
            status_emoji = "🟢" if st.session_state.running else "🔴"
            status_text = "ACTIVE" if st.session_state.running else "PAUSED"
            
            st.markdown(f"""
            <div class="stats-card">
                <h4>📈 Status</h4>
                <h2>{status_emoji} {status_text}</h2>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="stats-card">
                <h4>🎯 Exercises Completed</h4>
                <h2>{len(st.session_state.lap_times)}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        # Quick exercise guide
        st.markdown("### 💡 Exercise Tips")
        exercises = [
            ("🏃‍♂️ Running", "Keep good posture, land mid-foot"),
            ("🤸‍♂️ Jumping Jacks", "Engage core, soft knee landing"),
            ("💪 Push-ups", "Keep body straight, full range"),
            ("🦵 Squats", "Knees behind toes, chest up")
        ]
        
        for exercise, tip in exercises:
            with st.expander(f"{exercise}"):
                st.write(f"**Tip:** {tip}")
    
    # Lap times section
    st.markdown("---")
    st.markdown("### 📝 Exercise History")
    
    if st.session_state.lap_times:
        # Display exercise history
        for lap in reversed(st.session_state.lap_times[-8:]):  # Show last 8 exercises
            lap_formatted = stopwatch.format_time(lap['time'])
            st.markdown(
                f'<div class="lap-time">'
                f'<strong>Exercise {lap["lap_number"]}: {lap["exercise"]}</strong><br>'
                f'Time: {lap_formatted} | Completed at: {lap["timestamp"]}'
                f'</div>', 
                unsafe_allow_html=True
            )
    else:
        st.info("🏁 No exercises recorded yet. Start your workout and click 'Next Exercise' to record your progress!")
    
    # Workout plans
    with st.expander("🏋️‍♂️ Sample Workout Plans"):
        tab1, tab2, tab3 = st.tabs(["🔥 Beginner", "💪 Intermediate", "⚡ Advanced"])
        
        with tab1:
            st.markdown("""
            **20-Minute Beginner Circuit:**
            - 3 min 🏃‍♂️ Warm-up (jogging in place)
            - 1 min 🤸‍♂️ Jumping Jacks
            - 1 min 💪 Push-ups (knee push-ups ok)
            - 1 min 🦵 Squats
            - 1 min 🧘‍♂️ Rest
            - Repeat 3 times
            """)
        
        with tab2:
            st.markdown("""
            **30-Minute Intermediate Circuit:**
            - 5 min 🏃‍♂️ Running
            - 2 min 🤸‍♂️ Burpees
            - 2 min 💪 Push-ups
            - 2 min 🦵 Squats
            - 1 min 🧘‍♂️ Rest
            - Repeat 4 times
            """)
        
        with tab3:
            st.markdown("""
            **45-Minute Advanced HIIT:**
            - 5 min 🏃‍♂️ Sprint intervals
            - 3 min 🤸‍♂️ Burpees with push-up
            - 3 min 💪 Decline push-ups
            - 3 min 🦵 Jump squats
            - 1 min 🧘‍♂️ Active rest
            - Repeat 5 times
            """)
    
    # Auto-refresh when running
    if st.session_state.running:
        time.sleep(0.01)
        st.rerun()

if __name__ == "__main__":
    main()