import streamlit as st
import numpy as np
import random
import time

def initialize_game():
    """Initialize or reset the game state"""
    if 'board' not in st.session_state:
        st.session_state.board = np.full((3, 3), '', dtype=str)
    if 'current_player' not in st.session_state:
        st.session_state.current_player = 'X'
    if 'game_over' not in st.session_state:
        st.session_state.game_over = False
    if 'winner' not in st.session_state:
        st.session_state.winner = None
    if 'scores' not in st.session_state:
        st.session_state.scores = {'X': 0, 'O': 0, 'Draws': 0}
    if 'celebrate' not in st.session_state:
        st.session_state.celebrate = False

def check_winner(board):
    """Check if there's a winner"""
    # Check rows
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != '':
            return board[i][0]
    
    # Check columns
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i] != '':
            return board[0][i]
    
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != '':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != '':
        return board[0][2]
    
    # Check for draw
    if '' not in board:
        return 'Draw'
    
    return None

def make_move(row, col):
    """Handle a player's move"""
    if st.session_state.board[row][col] == '' and not st.session_state.game_over:
        st.session_state.board[row][col] = st.session_state.current_player
        
        # Check for winner
        winner = check_winner(st.session_state.board)
        if winner:
            st.session_state.game_over = True
            st.session_state.winner = winner
            if winner != 'Draw':
                st.session_state.scores[winner] += 1
                st.session_state.celebrate = True
            else:
                st.session_state.scores['Draws'] += 1
        else:
            # Switch player
            st.session_state.current_player = 'O' if st.session_state.current_player == 'X' else 'X'

def reset_game():
    """Reset the game state"""
    st.session_state.board = np.full((3, 3), '', dtype=str)
    st.session_state.current_player = 'X'
    st.session_state.game_over = False
    st.session_state.winner = None
    st.session_state.celebrate = False

def get_rainbow_color(index):
    """Generate rainbow colors"""
    colors = [
        '#FF6B6B', '#FF9E6B', '#FFD56B', '#C5FF6B', 
        '#6BFF8E', '#6BFFD5', '#6BC5FF', '#6B8EFF', 
        '#8E6BFF', '#D56BFF', '#FF6BD5', '#FF6B8E'
    ]
    return colors[index % len(colors)]

def main():
    st.set_page_config(
        page_title="🌈 Tic-Tac-Toe Game",
        page_icon="🎮",
        layout="centered"
    )
    
    # Add custom CSS for rainbow background and animations
    st.markdown("""
    <style>
    .main {
        background: linear-gradient(45deg, #FF6B6B, #FF9E6B, #FFD56B, #C5FF6B, #6BFF8E, #6BFFD5, #6BC5FF, #6B8EFF, #8E6BFF, #D56BFF, #FF6BD5, #FF6B8E);
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
        padding: 20px;
        margin: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .celebrate {
        animation: celebrate 2s ease-in-out;
    }
    
    @keyframes celebrate {
        0% { transform: scale(1); }
        25% { transform: scale(1.2); }
        50% { transform: scale(0.9); }
        75% { transform: scale(1.1); }
        100% { transform: scale(1); }
    }
    
    .rainbow-text {
        background: linear-gradient(45deg, #FF6B6B, #FF9E6B, #FFD56B, #C5FF6B, #6BFF8E, #6BFFD5, #6BC5FF, #6B8EFF, #8E6BFF, #D56BFF, #FF6BD5, #FF6B8E);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: gradient 3s ease infinite;
    }
    
    .cell-x {
        background: linear-gradient(45deg, #ff6b6b, #ff4757);
        color: white !important;
        font-weight: bold;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.4);
    }
    
    .cell-o {
        background: linear-gradient(45deg, #48dbfb, #0abde3);
        color: white !important;
        font-weight: bold;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(72, 219, 251, 0.4);
    }
    
    .empty-cell {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    .empty-cell:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
        background: rgba(255, 255, 255, 1);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize game state
    initialize_game()
    
    # Title with rainbow effect
    st.markdown("<h1 class='rainbow-text' style='text-align: center;'>🌈🎮 Tic-Tac-Toe Game 🎮🌈</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Score display
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("❌ Player X", st.session_state.scores['X'])
    with col2:
        st.metric("🤝 Draws", st.session_state.scores['Draws'])
    with col3:
        st.metric("⭕ Player O", st.session_state.scores['O'])
    
    st.markdown("---")
    
    # Display current player or winner with emojis
    if st.session_state.game_over:
        if st.session_state.winner == 'Draw':
            st.markdown(f"<h2 class='celebrate' style='text-align: center; color: #ff9f43;'>🤝 It's a Draw! 🎉</h2>", unsafe_allow_html=True)
            st.balloons()
        else:
            winner_emoji = "❌" if st.session_state.winner == 'X' else "⭕"
            st.markdown(f"<h2 class='celebrate' style='text-align: center; color: #ff9f43;'>🎊 {winner_emoji} Player {st.session_state.winner} wins! 🎊</h2>", unsafe_allow_html=True)
            st.balloons()
            if st.session_state.celebrate:
                st.snow()
                st.session_state.celebrate = False
    else:
        player_emoji = "❌" if st.session_state.current_player == 'X' else "⭕"
        st.markdown(f"<h3 style='text-align: center;'>Current Player: {player_emoji} <strong>{st.session_state.current_player}</strong></h3>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Create the game board
    st.markdown("<h3 style='text-align: center;'>🎯 Game Board 🎯</h3>", unsafe_allow_html=True)
    
    # Display the board with buttons
    for i in range(3):
        cols = st.columns([1, 1, 1], gap="medium")
        for j in range(3):
            with cols[j]:
                cell_value = st.session_state.board[i][j]
                cell_emoji = "❌" if cell_value == 'X' else "⭕" if cell_value == 'O' else "🎯"
                
                if cell_value != '':
                    cell_class = "cell-x" if cell_value == 'X' else "cell-o"
                    st.markdown(
                        f"<div class='{cell_class}' style='height: 100px; display: flex; "
                        f"justify-content: center; align-items: center; border-radius: 15px;'>"
                        f"<h1 style='margin: 0;'>{cell_emoji}</h1></div>",
                        unsafe_allow_html=True
                    )
                else:
                    if st.button(
                        f"🎯", 
                        key=f"btn_{i}_{j}", 
                        use_container_width=True,
                        disabled=st.session_state.game_over
                    ):
                        make_move(i, j)
                        st.rerun()
    
    st.markdown("---")
    
    # Action buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 Restart Game", use_container_width=True, type="primary"):
            reset_game()
            st.rerun()
        
        if st.button("🎲 Random Move", use_container_width=True, disabled=st.session_state.game_over):
            empty_cells = [(i, j) for i in range(3) for j in range(3) if st.session_state.board[i][j] == '']
            if empty_cells:
                row, col = random.choice(empty_cells)
                make_move(row, col)
                st.rerun()
    
    # Fun emoji section
    st.markdown("---")
    st.markdown("<h3 style='text-align: center;'>🎪 Game Fun Zone 🎪</h3>", unsafe_allow_html=True)
    
    emoji_cols = st.columns(5)
    fun_emojis = ["🎮", "🎯", "🎨", "🤹", "🎪"]
    for i, col in enumerate(emoji_cols):
        with col:
            st.markdown(f"<h2 style='text-align: center;'>{fun_emojis[i]}</h2>", unsafe_allow_html=True)
    
    # Instructions with emojis
    with st.expander("📖 How to Play & Rules"):
        st.markdown("""
        ## 🎯 How to Play:
        
        1. **Players take turns** placing their marks (❌ for X, ⭕ for O)
        2. **Click on an empty spot** to place your mark
        3. **Get 3 in a row** (horizontal, vertical, or diagonal) to win!
        4. **Fill all spots** without a winner = Draw! 🤝
        
        ## 🏆 Winning Patterns:
        - Horizontal: 🎯🎯🎯
        - Vertical:   🎯  
                     🎯  
                     🎯  
        - Diagonal:  🎯    
                       🎯  
                         🎯
        
        ## 🎮 Features:
        - **Rainbow background** 🌈
        - **Animated celebrations** 🎊
        - **Score tracking** 📊
        - **Random move generator** 🎲
        - **Fun emojis everywhere!** 😄
        
        ## 💡 Pro Tip:
        The center spot is the most powerful position! 🎯
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("<p style='text-align: center; color: #666;'>Made with ❤️ using Streamlit | 🌈 Enjoy the game! 🎮</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()