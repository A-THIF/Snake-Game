@echo off
echo Starting Snake Game...
echo.
echo Controls:
echo - Use Arrow Keys or WASD to move
echo - Press Q to quit
echo.
echo Press any key to start...
pause > nul

python snake_game.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Error running the game. Please check if Python is installed.
    echo Run 'python --version' to verify your Python installation.
    pause
)

