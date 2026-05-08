# ARCHITECTURE.md

Written by team-lead before spawning teammates. This is the shared blueprint —
teammates read it to understand what they are building and how their module fits.
Update it when the structure changes; do not let it drift from the actual code.

## Module Structure

- src/types/puzzle.py: Puzzle, GridSquare, Word, Direction types
- src/types/__init__.py: Public exports from types layer
- src/config/__init__.py: Configuration constants (grid size, default puzzle)
- src/service/__init__.py: Public exports from service layer
- src/service/puzzle_solver.py: PuzzleSolver class with validation and completion logic
- src/ui/__init__.py: Public exports from ui layer
- src/ui/cli.py: CLIPuzzleUI class for terminal interaction
- src/runtime/__init__.py: Main entry point wiring
- src/runtime/main.py: Application entry point, orchestrates puzzle game loop

## Interfaces

### types/puzzle.py
- `class Direction(Enum)`: ACROSS = "across", DOWN = "down"
- `class GridSquare: letter: str | None, is_black: bool`
- `class Word: number: int, direction: Direction, start_row: int, start_col: int, answer: str`
- `class Puzzle: grid_size: int, words: list[Word], grid: list[list[GridSquare]]`

### service/puzzle_solver.py
- `class PuzzleSolver:`
  - `validate_letter(row: int, col: int, letter: str) -> bool`
  - `fill_word(word_number: int, direction: Direction, answer: str) -> bool`
  - `check_completion() -> bool`
  - `get_word_clue(number: int, direction: Direction) -> str | None`

### ui/cli.py
- `class CLIPuzzleUI:`
  - `display_puzzle(puzzle: Puzzle) -> None`
  - `get_user_input() -> tuple[int, str, str] | None` (clue_number, direction, answer)
  - `show_message(message: str) -> None`

### runtime/main.py
- `def main() -> None`: Entry point, initializes puzzle and runs game loop

## Shared Data Structures

### Puzzle State
- Grid represented as 2D list of GridSquare
- Words list with number, direction, start position, and answer
- Black squares marked with is_black=True and letter=None

### Direction Enum
- ACROSS: horizontal words
- DOWN: vertical words

### Input Format
- User provides: clue number (int), direction ("across" or "down"), answer (str)

## External Dependencies

No external dependencies required. Pure Python standard library.
