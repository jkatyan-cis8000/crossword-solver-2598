"""Puzzle solver service with validation and completion logic."""

from src.types.puzzle import Direction, Puzzle, Word


class PuzzleSolver:
    """Service class for crossword puzzle validation and solving."""

    def __init__(self, puzzle: Puzzle):
        """Initialize the puzzle solver with a puzzle."""
        self._puzzle = puzzle

    def validate_letter(self, row: int, col: int, letter: str) -> bool:
        """Validate if a letter can be placed at the given position.

        Args:
            row: Row index (0-based)
            col: Column index (0-based)
            letter: The letter to validate

        Returns:
            True if the letter is valid at this position, False otherwise
        """
        if not letter or len(letter) != 1:
            return False

        if not letter.isalpha():
            return False

        if row < 0 or row >= self._puzzle.grid_size:
            return False

        if col < 0 or col >= self._puzzle.grid_size:
            return False

        square = self._puzzle.grid[row][col]
        if square.is_black:
            return False

        return True

    def fill_word(self, word_number: int, direction: Direction, answer: str) -> bool:
        """Fill a word into the puzzle.

        Args:
            word_number: The number of the word to fill
            direction: The direction of the word (ACROSS or DOWN)
            answer: The answer string to fill

        Returns:
            True if the word was successfully filled, False otherwise
        """
        word = self._find_word(word_number, direction)
        if word is None:
            return False

        if len(answer) != len(word.answer):
            return False

        if not answer.isalpha():
            return False

        row = word.start_row
        col = word.start_col

        for i, letter in enumerate(answer.upper()):
            if not self.validate_letter(row, col, letter):
                return False

            if self._puzzle.grid[row][col].is_black:
                return False

            if direction == Direction.ACROSS:
                col += 1
            else:
                row += 1

        return True

    def check_completion(self) -> bool:
        """Check if the puzzle is complete.

        Returns:
            True if all words are filled correctly, False otherwise
        """
        for word in self._puzzle.words:
            row = word.start_row
            col = word.start_col

            for i in range(len(word.answer)):
                square = self._puzzle.grid[row][col]

                if square.letter is None:
                    return False

                if square.letter != word.answer[i]:
                    return False

                if word.direction == Direction.ACROSS:
                    col += 1
                else:
                    row += 1

        return True

    def get_word_clue(self, number: int, direction: Direction) -> str | None:
        """Get the clue for a specific word.

        Args:
            number: The word number
            direction: The direction of the word

        Returns:
            The clue string if found, None otherwise
        """
        word = self._find_word(number, direction)
        if word is None:
            return None

        return word.answer

    def _find_word(self, number: int, direction: Direction) -> Word | None:
        """Find a word by number and direction.

        Args:
            number: The word number
            direction: The direction to search

        Returns:
            The Word object if found, None otherwise
        """
        for word in self._puzzle.words:
            if word.number == number and word.direction == direction:
                return word
        return None
