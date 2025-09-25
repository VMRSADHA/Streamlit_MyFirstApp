import streamlit as st
import random
import time
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="🎮 Rock Paper Scissors",
    page_icon="🎮",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for animations and styling
st.markdown("""
<style>
    .main {
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4, #45B7D1, #96CEB4);
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
        border-radius: 20px;
        margin: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .choice-button {
        padding: 20px;
        margin: 10px;
        border-radius: 15px;
        border: 3px solid;
        font-size: 2rem;
        transition: all 0.3s ease;
        text-align: center;
    }
    
    .choice-button:hover {
        transform: scale(1.1);
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }
    
    .rock-button {
        background-color: #FFD6D6;
        border-color: #FF6B6B;
    }
    
    .paper-button {
        background-color: #D6E5FF;
        border-color: #4ECDC4;
    }
    
    .scissors-button {
        background-color: #D6FFD6;
        border-color: #96CEB4;
    }
    
    .result-box {
        padding: 20px;
        border-radius: 15px;
        margin: 20px 0;
        text-align: center;
        font-size: 1.5rem;
        font-weight: bold;
    }
    
    .win-box {
        background-color: #D4EDDA;
        border: 3px solid #C3E6CB;
        color: #155724;
    }
    
    .lose-box {
        background-color: #F8D7DA;
        border: 3px solid #F5C6CB;
        color: #721C24;
    }
    
    .tie-box {
        background-color: #E2E3E5;
        border: 3px solid #D6D8DB;
        color: #383D41;
    }
    
    .emoji-animation {
        animation: bounce 1s infinite;
        display: inline-block;
    }
    
    @keyframes bounce {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.2); }
    }
    
    .score-board {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

class RockPaperScissorsGame:
    def __init__(self):
        # Initialize session state
        if 'player_score' not in st.session_state:
            st.session_state.player_score = 0
        if 'computer_score' not in st.session_state:
            st.session_state.computer_score = 0
        if 'rounds_played' not in st.session_state:
            st.session_state.rounds_played = 0
        if 'player_choice' not in st.session_state:
            st.session_state.player_choice = None
        if 'computer_choice' not in st.session_state:
            st.session_state.computer_choice = None
        if 'result' not in st.session_state:
            st.session_state.result = None
        if 'game_history' not in st.session_state:
            st.session_state.game_history = []
    
    def get_emoji(self, choice):
        """Return emoji for each choice"""
        emojis = {
            'rock': '🪨',
            'paper': '📄',
            'scissors': '✂️'
        }
        return emojis.get(choice, '❓')
    
    def determine_winner(self, player_choice, computer_choice):
        """Determine the winner of the round"""
        if player_choice == computer_choice:
            return "tie", "It's a tie! 🤝"
        elif (player_choice == "rock" and computer_choice == "scissors") or \
             (player_choice == "paper" and computer_choice == "rock") or \
             (player_choice == "scissors" and computer_choice == "paper"):
            st.session_state.player_score += 1
            return "win", "You win! 🎉"
        else:
            st.session_state.computer_score += 1
            return "lose", "Computer wins! 💻"
    
    def play_round(self, player_choice):
        """Play one round of the game"""
        computer_choice = random.choice(["rock", "paper", "scissors"])
        
        # Store choices
        st.session_state.player_choice = player_choice
        st.session_state.computer_choice = computer_choice
        st.session_state.rounds_played += 1
        
        # Determine result
        result_type, result_message = self.determine_winner(player_choice, computer_choice)
        st.session_state.result = result_message
        
        # Add to history
        st.session_state.game_history.append({
            'round': st.session_state.rounds_played,
            'player_choice': player_choice,
            'computer_choice': computer_choice,
            'result': result_type,
            'timestamp': datetime.now().strftime("%H:%M:%S")
        })
    
    def reset_game(self):
        """Reset the game scores"""
        st.session_state.player_score = 0
        st.session_state.computer_score = 0
        st.session_state.rounds_played = 0
        st.session_state.game_history = []
        st.session_state.result = None
    
    def display_choice_buttons(self):
        """Display the choice selection buttons"""
        st.markdown("### Choose your weapon!")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button(
                f"🪨 Rock", 
                key="rock",
                use_container_width=True,
                help="Rock crushes scissors!"
            ):
                self.play_round("rock")
                st.rerun()
        
        with col2:
            if st.button(
                f"📄 Paper", 
                key="paper",
                use_container_width=True,
                help="Paper covers rock!"
            ):
                self.play_round("paper")
                st.rerun()
        
        with col3:
            if st.button(
                f"✂️ Scissors", 
                key="scissors",
                use_container_width=True,
                help="Scissors cut paper!"
            ):
                self.play_round("scissors")
                st.rerun()
    
    def display_result(self):
        """Display the game result with animations"""
        if st.session_state.result:
            # Determine result box style
            if "win" in st.session_state.result:
                result_class = "win-box"
            elif "lose" in st.session_state.result:
                result_class = "lose-box"
            else:
                result_class = "tie-box"
            
            st.markdown(f'<div class="result-box {result_class}">{st.session_state.result}</div>', 
                       unsafe_allow_html=True)
            
            # Display choices with animations
            col1, col2, col3 = st.columns([2, 1, 2])
            
            with col1:
                st.markdown(f'<div style="text-align: center;"><h2>Your Choice</h2><div class="emoji-animation" style="font-size: 4rem;">{self.get_emoji(st.session_state.player_choice)}</div></div>', 
                           unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div style="text-align: center;"><h2>VS</h2></div>', 
                           unsafe_allow_html=True)
            
            with col3:
                st.markdown(f'<div style="text-align: center;"><h2>Computer</h2><div class="emoji-animation" style="font-size: 4rem;">{self.get_emoji(st.session_state.computer_choice)}</div></div>', 
                           unsafe_allow_html=True)
    
    def display_scoreboard(self):
        """Display the scoreboard"""
        st.markdown(f"""
        <div class="score-board">
            <h3 style="text-align: center; margin: 0;">📊 Scoreboard</h3>
            <div style="display: flex; justify-content: space-around; margin-top: 10px;">
                <div style="text-align: center;">
                    <h4 style="margin: 0;">You</h4>
                    <h2 style="margin: 0; color: #4ECDC4;">{st.session_state.player_score}</h2>
                </div>
                <div style="text-align: center;">
                    <h4 style="margin: 0;">Rounds</h4>
                    <h2 style="margin: 0; color: #FFD166;">{st.session_state.rounds_played}</h2>
                </div>
                <div style="text-align: center;">
                    <h4 style="margin: 0;">Computer</h4>
                    <h2 style="margin: 0; color: #EF476F;">{st.session_state.computer_score}</h2>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    def display_game_history(self):
        """Display game history"""
        if st.session_state.game_history:
            with st.expander("📜 Game History"):
                for game in reversed(st.session_state.game_history[-10:]):  # Show last 10 games
                    result_emoji = "🎉" if game['result'] == "win" else "💻" if game['result'] == "lose" else "🤝"
                    st.write(f"Round {game['round']}: You {self.get_emoji(game['player_choice'])} vs Computer {self.get_emoji(game['computer_choice'])} → {result_emoji} ({game['timestamp']})")
    
    def run(self):
        """Main game loop"""
        # Header
        st.markdown("<h1 style='text-align: center; color: #333;'>🎮 Rock Paper Scissors Game 🎮</h1>", 
                   unsafe_allow_html=True)
        
        # Display scoreboard
        self.display_scoreboard()
        
        # Display choice buttons
        self.display_choice_buttons()
        
        # Display result if available
        self.display_result()
        
        # Game history
        self.display_game_history()
        
        # Reset button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Reset Game", use_container_width=True, type="secondary"):
                self.reset_game()
                st.rerun()
        
        # Game rules
        with st.expander("📖 How to Play"):
            st.markdown("""
            ### Game Rules:
            - **Rock 🪨** crushes **Scissors ✂️**
            - **Scissors ✂️** cut **Paper 📄**  
            - **Paper 📄** covers **Rock 🪨**
            
            ### How to Play:
            1. Click on your choice (Rock, Paper, or Scissors)
            2. The computer will randomly select its choice
            3. See who wins based on the rules above!
            4. Track your score and try to beat the computer!
            
            ### Tips:
            - The computer chooses randomly, so there's no pattern to predict!
            - Best of luck! 🍀
            """)
        
        # Footer
        st.markdown("---")
        st.markdown("<p style='text-align: center; color: #666;'>Built with ❤️ using Streamlit | 🎮 Good luck!</p>", 
                   unsafe_allow_html=True)

# Run the game
if __name__ == "__main__":
    game = RockPaperScissorsGame()
    game.run()