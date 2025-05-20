import os
import sys
import time
import random
import msvcrt
import traceback

# Debug mode - writes to a log file for diagnostics
DEBUG = True

# Game dimensions
WIDTH, HEIGHT = 30, 15  # Larger size for more playing space

# Game characters - simple ASCII only
SNAKE_HEAD = 'O'  # Snake head
SNAKE_BODY = 'o'  # Snake body
FOOD_CHAR = '*'   # Food
WALL_CHAR = '#'   # Wall
EMPTY_CHAR = ' '  # Empty space

# Direction constants
UP, RIGHT, DOWN, LEFT = 0, 1, 2, 3

# Key codes for Windows
KEY_W, KEY_A, KEY_S, KEY_D = ord('w'), ord('a'), ord('s'), ord('d')
KEY_W_UP, KEY_A_UP, KEY_S_UP, KEY_D_UP = ord('W'), ord('A'), ord('S'), ord('D')
KEY_Q, KEY_Q_UP = ord('q'), ord('Q')
KEY_ESC = 27

# Arrow key codes (after extended key prefix 224 or 0)
KEY_UP = 72
KEY_DOWN = 80
KEY_LEFT = 75
KEY_RIGHT = 77

# Speed parameters (seconds delay)
BASE_DELAY = 0.3   # Moderate base speed for better gameplay
MIN_DELAY = 0.15   # Minimum delay for maximum difficulty
SPEED_STEP = 0.01  # Smaller steps when speeding up

# Score multiplier based on speed
def get_score_multiplier(delay):
    """Return score multiplier based on speed (faster = higher score)"""
    if delay <= MIN_DELAY:
        return 3.0  # Triple points at maximum speed
    elif delay <= MIN_DELAY + 0.05:
        return 2.0  # Double points at high speed
    else:
        return 1.0  # Normal points at regular speed

# High score tracking
HIGH_SCORE = 0
# Simple debug function for logging issues

def debug_print(msg):
    """Print debug messages to log file"""
    if DEBUG:
        with open('snake_debug.log', 'a') as f:
            f.write(f"{time.strftime('%H:%M:%S')} - {msg}\n")
def clear_screen():
    """Clear the console screen using simple cls command"""
    os.system('cls')
    debug_print("Screen cleared")
class GameBoard:
    def __init__(self):
        """Initialize the game board"""
        self.width, self.height = WIDTH, HEIGHT
        self.buffer = []
        self.init_board()
        debug_print(f"Game board initialized: {WIDTH}x{HEIGHT}")

    def init_board(self):
        """Initialize the game board with walls"""
        self.buffer = [[WALL_CHAR if x in (0, self.width+1) or y in (0, self.height+1) else EMPTY_CHAR
                        for x in range(self.width+2)]
                       for y in range(self.height+2)]
        debug_print("Game board with walls created")

    def clear_inner(self):
        """Clear the inner area of the board (not walls)"""
        for y in range(1, self.height+1):
            for x in range(1, self.width+1):
                self.buffer[y][x] = EMPTY_CHAR
        debug_print("Game board interior cleared")

    def set_cell(self, x, y, ch):
        """Set a cell on the board to a specific character"""
        if 0 <= x < self.width+2 and 0 <= y < self.height+2:
            self.buffer[y][x] = ch

    def render(self, score, direction, high_score=0, direction_changed=False):
        """Render the game board to console using simple print statements"""
        # Clear screen first
        clear_screen()
        
        # Print score information
        print(f"Score: {score} | High Score: {high_score}")
        
        # Show multiplier if score is above 0
        if score > 0:
            multiplier = get_score_multiplier(BASE_DELAY)
            print(f"Speed Multiplier: x{multiplier:.1f}")
        
        # Print game board
        for row in self.buffer:
            print(''.join(row))
        
        # Print controls and direction
        dir_name = {UP: "UP ↑", RIGHT: "RIGHT →", DOWN: "DOWN ↓", LEFT: "LEFT ←"}.get(direction, "NONE")
        
        # Visual feedback when direction changes
        if direction_changed:
            print(f"Direction: << {dir_name} >> | Controls: WASD/Arrow Keys | Q to quit")
        else:
            print(f"Direction: {dir_name} | Controls: WASD/Arrow Keys | Q to quit")
        
        # Force output to display immediately
        sys.stdout.flush()


class SnakeGame:
    def __init__(self):
        """Initialize the snake game"""
        self.board = GameBoard()
        # Initialize snake in the middle of the board
        mid_y, mid_x = HEIGHT//2, WIDTH//4
        self.snake = [[mid_y, mid_x], [mid_y, mid_x-1], [mid_y, mid_x-2]]
        self.dir = RIGHT  # Start moving right
        self.food = None
        self.score = 0
        self.over = False
        self.last_key = None
        self.delay = BASE_DELAY
        self.direction_changed = False  # Track direction changes for visual feedback
        self.spawn_food()
        debug_print("Game initialized")

    def spawn_food(self):
        """Spawn food at a random position not occupied by the snake"""
        debug_print("Spawning food")
        # Try to find a spot for food
        for _ in range(100):  # Limit attempts
            x = random.randint(1, WIDTH)
            y = random.randint(1, HEIGHT)
            if [y, x] not in self.snake:
                self.food = [y, x]
                debug_print(f"Food spawned at {x},{y}")
                return
        # If no spot found, game is won (snake filled the board)
        debug_print("No space for food - game won!")
        self.over = True

    def process_input(self):
        """Process keyboard input"""
        try:
            if msvcrt.kbhit():
                key = ord(msvcrt.getch())
                self.last_key = key
                debug_print(f"Key pressed: {key}")
                
                # Check for quit keys
                if key in (KEY_Q, KEY_Q_UP, KEY_ESC):
                    debug_print("Quit signal received")
                    self.over = True
                    return
                
                # Check for WASD keys
                if key in (KEY_W, KEY_W_UP) and self.dir != DOWN:
                    self.dir = UP
                    self.direction_changed = True
                    debug_print("Direction changed to UP")
                elif key in (KEY_S, KEY_S_UP) and self.dir != UP:
                    self.dir = DOWN
                    self.direction_changed = True
                    debug_print("Direction changed to DOWN")
                elif key in (KEY_A, KEY_A_UP) and self.dir != RIGHT:
                    self.dir = LEFT
                    self.direction_changed = True
                    debug_print("Direction changed to LEFT")
                elif key in (KEY_D, KEY_D_UP) and self.dir != LEFT:
                    self.dir = RIGHT
                    self.direction_changed = True
                    debug_print("Direction changed to RIGHT")
                # Check for extended keys (arrow keys)
                elif key in (0, 224):  # Extended key prefix
                    try:
                        ext_key = ord(msvcrt.getch())
                        debug_print(f"Extended key: {ext_key}")
                        if ext_key == KEY_UP and self.dir != DOWN:
                            self.dir = UP
                            self.direction_changed = True
                            debug_print("Direction changed to UP (arrow)")
                        elif ext_key == KEY_DOWN and self.dir != UP:
                            self.dir = DOWN
                            self.direction_changed = True
                            debug_print("Direction changed to DOWN (arrow)")
                        elif ext_key == KEY_LEFT and self.dir != RIGHT:
                            self.dir = LEFT
                            self.direction_changed = True
                            debug_print("Direction changed to LEFT (arrow)")
                        elif ext_key == KEY_RIGHT and self.dir != LEFT:
                            self.dir = RIGHT
                            self.direction_changed = True
                            debug_print("Direction changed to RIGHT (arrow)")
                    except Exception as e:
                        debug_print(f"Error reading extended key: {e}")
        except Exception as e:
            debug_print(f"Input processing error: {e}")

    def update(self):
        """Update the game state"""
        debug_print("Updating game state")
        # Get current head position
        head = self.snake[0].copy()
        
        # Calculate new head position based on direction
        if self.dir == UP:
            head[0] -= 1
        elif self.dir == DOWN:
            head[0] += 1
        elif self.dir == LEFT:
            head[1] -= 1
        elif self.dir == RIGHT:
            head[1] += 1
        
        # Check for collisions with walls
        if head[0] == 0 or head[0] == HEIGHT+1 or head[1] == 0 or head[1] == WIDTH+1:
            debug_print(f"Wall collision at {head[1]},{head[0]}")
            self.over = True
            return
        
        # Check for collision with self
        if head in self.snake:
            debug_print(f"Self collision at {head[1]},{head[0]}")
            self.over = True
            return
        
        # Move the snake by adding new head
        self.snake.insert(0, head)
        
        # Check if snake ate the food
        if head == self.food:
            debug_print(f"Food eaten at {self.food[1]},{self.food[0]}")
            
            # Apply score multiplier based on current speed
            multiplier = get_score_multiplier(self.delay)
            points = int(10 * multiplier)
            self.score += points
            debug_print(f"Added {points} points with multiplier x{multiplier:.1f}")
            
            # Speed up the game a bit
            self.delay = max(MIN_DELAY, self.delay - SPEED_STEP)
            
            # Create new food
            self.spawn_food()
            
            # Update high score if needed
            global HIGH_SCORE
            if self.score > HIGH_SCORE:
                HIGH_SCORE = self.score
                debug_print(f"New high score: {HIGH_SCORE}")
        else:
            # Remove the tail if no food was eaten
            self.snake.pop()

    def render(self):
        """Render the current game state"""
        # Clear the board (except walls)
        self.board.clear_inner()
        
        # Draw food
        if self.food:
            y, x = self.food
            self.board.set_cell(x, y, FOOD_CHAR)
        
        # Draw snake
        for i, (y, x) in enumerate(self.snake):
            ch = SNAKE_HEAD if i == 0 else SNAKE_BODY
            self.board.set_cell(x, y, ch)
        
        # Render the board with high score and direction change feedback
        self.board.render(self.score, self.dir, HIGH_SCORE, self.direction_changed)
        
        # Reset direction changed flag after rendering
        self.direction_changed = False

    def run(self):
        """Simple main game loop"""
        # Show welcome screen
        clear_screen()
        print("\n" + "="*50)
        print("SNAKE GAME")
        print("="*50)
        print("\nControls:")
        print("• Arrow keys or WASD to control the snake")
        print(f"• Eat the food ({FOOD_CHAR}) to grow and earn points")
        print("• Don't hit the walls or yourself!")
        print("• Press Q to quit anytime")
        print("\nPress any key to start...")
        msvcrt.getch()  # Wait for key press
        
        # Clear the screen once before starting the game
        clear_screen()
        
        # Main game loop with simple timing
        debug_print("Entering main game loop")
        start_time = time.time()
        
        while not self.over:
            # Process input (check for key presses)
            self.process_input()
            
            # Update game state
            self.update()
            
            # Render the game
            self.render()
            
            # Control game speed with simple delay
            time.sleep(self.delay)
            
            # Occasionally log game state
            if int(time.time() - start_time) % 5 == 0:  # Every ~5 seconds
                elapsed = time.time() - start_time
                debug_print(f"Game running for {elapsed:.1f}s, Score: {self.score}")
        
        # Game over screen
        clear_screen()
        print("\n" + "="*50)
        print("GAME OVER")
        print("="*50)
        print(f"\nFinal Score: {self.score}")
        
        # Show high score information
        if self.score >= HIGH_SCORE:
            print(f"NEW HIGH SCORE: {self.score}!")
        else:
            print(f"High Score: {HIGH_SCORE}")
            
        print(f"Time played: {time.time() - start_time:.1f} seconds")
        print("\nPress any key to exit...")
        msvcrt.getch()


def main():
    """Main function"""
    try:
        # Initialize debug log
        if DEBUG:
            with open('snake_debug.log', 'w') as f:
                f.write(f"Snake Game Debug Log - {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("-" * 50 + "\n")
        
        debug_print("Starting game")
        
        # Create and run the game
        game = SnakeGame()
        game.run()
        
    except Exception as e:
        # Handle any unexpected errors
        clear_screen()
        print(f"An error occurred: {e}")
        debug_print(f"Critical error: {e}")
        debug_print(traceback.format_exc())
        print("\nCheck snake_debug.log for details")
        input("Press Enter to exit...")


if __name__ == "__main__":
    main()
