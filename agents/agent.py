import abc
from copy import deepcopy

class Agent:

    def __init__(self) -> None:
        self.reset()

    @abc.abstractmethod
    def guess(self, words) -> list[str]:
        ...

    def solve(self, puzzle):
        """
        Given a puzzle, this function calls 'solve' until either the puzzle
        is solved or the number of guesses is exhausted.
        """
        all_colors_solved = []
        while not puzzle.finished:
            words = puzzle.get_remaining_words()
            next_guess = self.guess(words)
            colors_solved, one_away = puzzle.guess(next_guess)
            all_colors_solved += colors_solved
            self.guesses[tuple(next_guess)] = (colors_solved, one_away)
        
        win_state = puzzle.get_win_state()
        guesses = deepcopy(self.guesses)
        self.reset()
        return guesses, win_state

    def reset(self):
        self.guesses = {}
