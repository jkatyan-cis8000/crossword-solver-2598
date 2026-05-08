"""Puzzle domain types for the crossword solver."""

from enum import Enum
from typing import NamedTuple


class Direction(Enum):
    """Direction of a word in the crossword grid."""

    ACROSS = "across"
    DOWN = "down"


class GridSquare(NamedTuple):
    """A single square in the crossword grid."""

    letter: str | None
    is_black: bool


class Word(NamedTuple):
    """A word in the crossword puzzle."""

    number: int
    direction: Direction
    start_row: int
    start_col: int
    answer: str


class Puzzle(NamedTuple):
    """A complete crossword puzzle."""

    grid_size: int
    words: list[Word]
    grid: list[list[GridSquare]]
