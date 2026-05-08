"""CLI user interface for crossword puzzle."""

from src.types.puzzle import Direction, Puzzle


class CLIPuzzleUI:
    """CLI user interface for the crossword puzzle game."""

    def display_puzzle(self, puzzle: Puzzle) -> None:
        """Display the current state of the puzzle grid.

        Args:
            puzzle: The puzzle to display
        """
        print("\n+---+" + "---+" * (puzzle.grid_size - 1))
        for row in range(puzzle.grid_size):
            line = "|"
            for col in range(puzzle.grid_size):
                square = puzzle.grid[row][col]
                if square.is_black:
                    cell = "   "
                elif square.letter is None:
                    cell = "   "
                else:
                    cell = f" {square.letter} "
                line += cell + "|"
            print(line)
            print("+---+" + "---+" * (puzzle.grid_size - 1))
        print()

    def get_user_input(self) -> tuple[int, str, str] | None:
        """Get user input for filling a word.

        Returns:
            Tuple of (clue_number, direction, answer) or None if user wants to quit
        """
        try:
            user_input = input(
                "Enter clue number, direction (across/down), and answer (e.g., '1 across ANSWER') or 'q' to quit: "
            ).strip()
            if user_input.lower() == "q":
                return None
            parts = user_input.split()
            if len(parts) < 3:
                print("Invalid input. Format: <number> <direction> <answer>")
                return None
            clue_number = int(parts[0])
            direction = parts[1].lower()
            answer = parts[2].upper()
            if direction not in ("across", "down"):
                print("Direction must be 'across' or 'down'")
                return None
            return (clue_number, direction, answer)
        except ValueError:
            print("Invalid clue number")
            return None

    def show_message(self, message: str) -> None:
        """Display a message to the user.

        Args:
            message: The message to display
        """
        print(message)
