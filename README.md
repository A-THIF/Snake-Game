# Terminal Snake Game

A classic Snake game implementation for Windows terminal using Python. Navigate your snake through the game board, eat food to grow longer, earn points, and avoid collisions with walls and yourself!

## 🎮 Game Preview

```
Score: 70 | High Score: 70
Speed Multiplier: x1.0

################################################################################
#                                                                              #
#                                                                              #
#                                                                              #
#                                                                              #
#                                                                              #
#                                 *                                            #
#                                                                              #
#                                 oooooO                                       #
#                                                                              #
#                                                                              #
#                                                                              #
#                                                                              #
#                                                                              #
#                                                                              #
#                                                                              #
################################################################################

Direction: RIGHT → | Controls: WASD/Arrow Keys | Q to quit
```

## ✨ Features

- **Simple ASCII Interface**: Clean and easy-to-read game elements
- **Dual Controls**: Use either Arrow Keys or WASD
- **Progressive Difficulty**: Snake speeds up as you eat more food
- **Score Multiplier System**: Faster snake = higher points
- **High Score Tracking**: Beat your best score across game sessions
- **Visual Direction Feedback**: Clear indicators when changing direction
- **Smooth Gameplay**: Optimized rendering for a flicker-free experience
- **Windows Terminal Optimized**: Specifically designed for PowerShell/CMD

## 🔧 System Requirements

- **Python**: Version 3.6 or higher
- **Operating System**: Windows (uses Windows-specific keyboard handling via msvcrt)
- **Terminal**: Works best in Windows Terminal, PowerShell, or Command Prompt

## 📥 Installation

1. **Clone the repository** (or download the zip file):
   ```
   git clone https://github.com/yourusername/snake-game.git
   cd Snake-Game
   ```

2. **Verify Python is installed**:
   ```
   python --version
   ```
   Should show Python 3.6 or higher

3. **Run the game**:
   ```
   python snake_game.py
   ```

## 🎯 How to Play

1. **Start the game**: Run the script and press any key when prompted
2. **Control the snake**:
   - Use **Arrow Keys** (↑, ↓, ←, →) or **WASD** keys to change direction
   - The snake continuously moves in the current direction
3. **Eat food**: Guide the snake to eat the food (`*`) that appears randomly
4. **Grow and earn points**: The snake grows longer with each food eaten
5. **Avoid collisions**: Don't hit the walls (`#`) or your own snake body
6. **End game**: Press `Q` at any time to quit

## 🎲 Game Mechanics

### Movement
- The snake moves continuously in the current direction
- You can only change to perpendicular directions (no 180° turns)
- Direction changes take effect immediately

### Scoring System
- **Base points per food**: 10 points
- **Speed-based multipliers**:
  - Normal speed (0.3s delay): x1.0 (10 points)
  - High speed (0.15s - 0.20s delay): x2.0 (20 points)
  - Maximum speed (≤0.15s delay): x3.0 (30 points)

### Game Over Conditions
- Hitting a wall
- Colliding with your own snake body

## 🛠️ Files Included

- **snake_game.py**: Main game script
- **test_keys.py**: Utility for testing keyboard input (useful for troubleshooting)

## 🤝 Contributing

Contributions are welcome! Some ideas for improvements:
- Add sound effects
- Implement obstacles or power-ups
- Create difficulty levels
- Add a graphical interface

## 📜 License

This project is available under the MIT License - feel free to use, modify, and distribute this code.

---

Enjoy the game and happy coding! 🐍
