import streamlit as st
import random
import time
import numpy as np

# Page configuration
st.set_page_config(
    page_title="🐍 Snake Game",
    page_icon="🐍",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for game styling
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
    }
    
    .stApp {
        background: rgba(0, 0, 0, 0.9);
        border-radius: 20px;
        margin: 20px;
        box-shadow: 0 0 50px rgba(0, 255, 0, 0.3);
    }
    
    .game-header {
        background: linear-gradient(135deg, #00b09b 0%, #96c93d 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin: 10px 0;
        border: 3px solid #00ff00;
    }
    
    .game-board {
        background-color: #001100;
        border: 3px solid #00ff00;
        border-radius: 10px;
        padding: 10px;
        margin: 10px auto;
    }
    
    .score-board {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin: 10px 0;
        font-weight: bold;
        font-size: 1.2em;
    }
    
    .control-button {
        border-radius: 10px !important;
        border: 2px solid !important;
        font-weight: bold !important;
        padding: 10px 20px !important;
        margin: 5px !important;
        transition: all 0.3s ease !important;
    }
    
    .control-button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(0, 255, 0, 0.3);
    }
    
    .game-over {
        background: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%);
        color: white;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        margin: 20px 0;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .cell {
        width: 20px;
        height: 20px;
        display: inline-block;
        margin: 1px;
        border-radius: 3px;
        transition: all 0.2s ease;
    }
    
    .snake-cell {
        background: linear-gradient(135deg, #00ff00 0%, #00cc00 100%);
        box-shadow: 0 0 10px #00ff00;
    }
    
    .food-cell {
        background: linear-gradient(135deg, #ff0000 0%, #cc0000 100%);
        box-shadow: 0 0 15px #ff0000;
        animation: blink 1s infinite;
        border-radius: 50%;
    }
    
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    .empty-cell {
        background-color: #002200;
    }
    
    .wall-cell {
        background-color: #333333;
    }
</style>
""", unsafe_allow_html=True)

class SnakeGame:
    def __init__(self, grid_size=20):
        self.grid_size = grid_size
        self.reset_game()
    
    def reset_game(self):
        """Initialize or reset the game state"""
        # Initialize snake in the center
        center = self.grid_size // 2
        self.snake = [(center, center), (center, center-1), (center, center-2)]
        self.direction = "RIGHT"
        self.next_direction = "RIGHT"
        self.food = self.generate_food()
        self.score = 0
        self.game_over = False
        self.game_speed = 0.2  # seconds per move
        self.last_move_time = time.time()
    
    def generate_food(self):
        """Generate food at a random position not occupied by snake"""
        while True:
            food = (random.randint(0, self.grid_size-1), random.randint(0, self.grid_size-1))
            if food not in self.snake:
                return food
    
    def change_direction(self, new_direction):
        """Change snake direction (prevent 180-degree turns)"""
        opposite_directions = {
            "UP": "DOWN", "DOWN": "UP", 
            "LEFT": "RIGHT", "RIGHT": "LEFT"
        }
        if new_direction != opposite_directions.get(self.direction):
            self.next_direction = new_direction
    
    def move_snake(self):
        """Move the snake in the current direction"""
        if self.game_over:
            return
        
        current_time = time.time()
        if current_time - self.last_move_time < self.game_speed:
            return False  # Not time to move yet
        
        self.last_move_time = current_time
        self.direction = self.next_direction
        
        # Get current head position
        head_x, head_y = self.snake[0]
        
        # Calculate new head position based on direction
        if self.direction == "UP":
            new_head = (head_x - 1, head_y)
        elif self.direction == "DOWN":
            new_head = (head_x + 1, head_y)
        elif self.direction == "LEFT":
            new_head = (head_x, head_y - 1)
        elif self.direction == "RIGHT":
            new_head = (head_x, head_y + 1)
        
        # Check for collisions
        if (new_head[0] < 0 or new_head[0] >= self.grid_size or 
            new_head[1] < 0 or new_head[1] >= self.grid_size or
            new_head in self.snake):
            self.game_over = True
            return True
        
        # Move snake
        self.snake.insert(0, new_head)
        
        # Check if food is eaten
        if new_head == self.food:
            self.score += 10
            self.food = self.generate_food()
            # Increase speed slightly as score increases
            self.game_speed = max(0.05, 0.2 - (self.score / 500))
        else:
            # Remove tail if no food eaten
            self.snake.pop()
        
        return True
    
    def render_board(self):
        """Render the game board as HTML"""
        board_html = '<div class="game-board">'
        
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                cell_type = "empty"
                
                if (i, j) == self.food:
                    cell_type = "food"
                elif (i, j) in self.snake:
                    if (i, j) == self.snake[0]:  # Snake head
                        cell_type = "snake-head"
                    else:
                        cell_type = "snake"
                elif i == 0 or i == self.grid_size-1 or j == 0 or j == self.grid_size-1:
                    cell_type = "wall"
                
                cell_class = {
                    "empty": "empty-cell",
                    "food": "food-cell",
                    "snake": "snake-cell",
                    "snake-head": "snake-cell",
                    "wall": "wall-cell"
                }.get(cell_type, "empty-cell")
                
                board_html += f'<div class="cell {cell_class}"></div>'
            board_html += '<br>'
        
        board_html += '</div>'
        return board_html

def main():
    # Initialize game in session state
    if 'game' not in st.session_state:
        st.session_state.game = SnakeGame()
    
    game = st.session_state.game
    
    # Header
    st.markdown("""
    <div class="game-header">
        <h1>🐍 Classic Snake Game</h1>
        <h3>Eat the red food and avoid collisions!</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Score board
    st.markdown(f"""
    <div class="score-board">
        🏆 Score: {game.score} | 🐍 Length: {len(game.snake)} | ⚡ Speed: {max(1, int(0.2/game.game_speed))}x
    </div>
    """, unsafe_allow_html=True)
    
    # Game board
    st.markdown(game.render_board(), unsafe_allow_html=True)
    
    # Control buttons
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
    
    with col1:
        if st.button("🔼 Up", key="up", use_container_width=True, 
                    disabled=game.game_over):
            game.change_direction("UP")
    
    with col2:
        if st.button("◀️ Left", key="left", use_container_width=True,
                    disabled=game.game_over):
            game.change_direction("LEFT")
    
    with col3:
        if st.button("⏹️ Pause", key="pause", use_container_width=True):
            st.info("Game paused. Click direction buttons to resume.")
    
    with col4:
        if st.button("▶️ Right", key="right", use_container_width=True,
                    disabled=game.game_over):
            game.change_direction("RIGHT")
    
    with col5:
        if st.button("🔽 Down", key="down", use_container_width=True,
                    disabled=game.game_over):
            game.change_direction("DOWN")
    
    # Game over display
    if game.game_over:
        st.markdown(f"""
        <div class="game-over">
            <h2>💀 Game Over!</h2>
            <h3>Final Score: {game.score}</h3>
            <p>Snake length: {len(game.snake)}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Restart button
        if st.button("🔄 Restart Game", key="restart", use_container_width=True, type="primary"):
            game.reset_game()
            st.rerun()
    
    # Game instructions
    with st.expander("🎮 How to Play"):
        st.markdown("""
        ### Game Rules:
        1. **Control the snake** using direction buttons
        2. **Eat the red food** 🍎 to grow longer and increase score
        3. **Avoid collisions** with walls and yourself
        4. **Game ends** when snake hits wall or itself
        
        ### Controls:
        - **Up/Down/Left/Right buttons**: Change snake direction
        - **Pause button**: Temporarily stop the game
        - **Restart button**: Start a new game after game over
        
        ### Tips:
        - The snake moves faster as your score increases
        - Plan your moves to avoid getting trapped
        - Use the entire game area strategically
        """)
    
    # Keyboard controls info
    st.markdown("""
    **⌨️ Keyboard Shortcuts (Click buttons above or use):**
    - **W/Up Arrow**: Move Up
    - **A/Left Arrow**: Move Left  
    - **S/Down Arrow**: Move Down
    - **D/Right Arrow**: Move Right
    - **Space**: Pause/Resume
    - **R**: Restart Game
    """)
    
    # Auto-refresh for continuous movement
    if not game.game_over:
        if game.move_snake():
            time.sleep(0.01)  # Small delay for smooth animation
            st.rerun()

if __name__ == "__main__":
    main()