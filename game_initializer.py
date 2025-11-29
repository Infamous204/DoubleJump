import subprocess
import sys
from sys import exit

class GameInitializer:
    def __init__(self):
        pass  # No setup needed

    def run(self):

        #Runs checkers_game.py as a subprocess.
        try:
            # Run the original checkers_game.py script
            result = subprocess.call([sys.executable, 'checkers_game.py'])
            print(f"checkers_game.py exited with code: {result}")  # Debug: 0=normal quit
            return "quit"  # Match original
        except FileNotFoundError:
            print("Error: checkers_game.py not found in current directory.")
            return "error"
        except Exception as e:
            print(f"Error running checkers_game.py: {e}")
            return "error"

# test
if __name__ == "__main__":
    game_init = GameInitializer()
    result = game_init.run()
    print(f"Ended with: {result}")