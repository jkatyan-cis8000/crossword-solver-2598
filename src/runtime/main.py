"""Main entry point for the crossword puzzle game."""

import sys

from src.config import GRID_SIZE
from src.service import PuzzleSolver
from src.types import Direction, GridSquare, Puzzle, Word
from src.ui import CLIPuzzleUI


def create_sample_puzzle() -> Puzzle:
    """Create a sample 5x5 crossword puzzle.

    Returns:
        A 5x5 puzzle with sample words
    """
    grid_size = GRID_SIZE

    words = [
        Word(
            number=1,
            direction=Direction.ACROSS,
            start_row=0,
            start_col=0,
            answer="HELLO",
        ),
        Word(
            number=2,
            direction=Direction.DOWN,
            start_row=0,
            start_col=0,
            answer="HOUSE",
        ),
        Word(
            number=3,
            direction=Direction.ACROSS,
            start_row=2,
            start_col=0,
            answer="APPLE",
        ),
        Word(
            number=4,
            direction=Direction.DOWN,
            start_row=0,
            start_col=4,
            answer="LOOSE",
        ),
    ]

    grid = [
        [
            GridSquare(letter=None, is_black=False) for _ in range(grid_size)
        ]
        for _ in range(grid_size)
    ]

    for word in words:
        row = word.start_row
        col = word.start_col
        for i in range(len(word.answer)):
            grid[row][col] = GridSquare(letter=None, is_black=False)
            if word.direction == Direction.ACROSS:
                col += 1
            else:
                row += 1

    return Puzzle(grid_size=grid_size, words=words, grid=grid)


def main() -> None:
    """Entry point for the crossword puzzle game."""
    puzzle = create_sample_puzzle()
    solver = PuzzleSolver(puzzle)
    ui = CLIPuzzleUI()

    ui.show_message("Welcome to Crossword Solver!")
    ui.display_puzzle(puzzle)

    while True:
        user_input = ui.get_user_input()
        if user_input is None:
            ui.show_message("Goodbye!")
            break

        clue_number, direction_str, answer = user_input

        if direction_str == "across":
            direction = Direction.ACROSS
        else:
            direction = Direction.DOWN

        success = solver.fill_word(clue_number, direction, answer)
        if success:
            ui.show_message(f"Word {clue_number} {direction_str} filled!")
            ui.display_puzzle(puzzle)

            if solver.check_completion():
                ui.show_message("Congratulations! Puzzle complete!")
                break
        else:
            ui.show_message("Invalid move. Try again.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGoodbye!")
        sys.exit(0)
