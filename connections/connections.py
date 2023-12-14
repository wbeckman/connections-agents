"""
Class to define a connections puzzle. A connections
puzzle has four logical categories (given as strings),
with four words per category (also given as strings).
"""

import random
from connections import util
from connections.colors import Colors

class Connections:

    """
    Defines a connections puzzle. A connections puzzle has four categories
    associated with the colors [yellow, green, blue, purple]. Those colors
    are sorted in order of increasing difficulty. It also takes four 
    groups of four words, which are associated with a category of the same
    color. 

    The idea is that the four words share a common theme (i.e. a connection),
    but are presented in a grid format with the player having to guess what
    the words within each group are. Often, there are red herrings to
    intentionally confuse.

    categories is given as:

    {
        'yellow': 'CATEGORY 1',
        'green': 'CATEGORY 2',
        ...
    }

    category_words is given as:
    {
        'yellow': ['word1', 'word2', ...],
        'green': ['other_word1', 'other_word2', ...],
        ...
    }
    """
    num_incorrect_guesses_allowed = 4
    emoji_map = {
        Colors.YELLOW: '🟨',
        Colors.GREEN: '🟩',
        Colors.BLUE: '🟦',
        Colors.PURPLE: '🟪'
    }
    color_map = {
        'YELLOW': Colors.YELLOW,
        'GREEN': Colors.GREEN,
        'BLUE': Colors.BLUE,
        'PURPLE': Colors.PURPLE
    }

    @util.upper_input
    def __init__(self, categories, category_words, puzzle_num=None, date=None) -> None:
        if len(categories) != 4:
            raise ValueError(
                f'There must be exactly four categories ({len(categories)} provided)'
            )
        if len(categories) != len(category_words):
            raise ValueError(
                'Number of categories must match number of category word lists provided'
                f'(number of categories: {len(categories)}; number of category word lists: '
                f'{len(category_words)})'
            )

        new_categories = Connections._convert_dict_keys_to_colors(categories)
        new_category_words = Connections._convert_dict_keys_to_colors(category_words)
        self.puzzle_num = puzzle_num
        self.date = date
        self.categories = new_categories
        self.category_words = new_category_words
        self.reset()

    @staticmethod
    def _convert_dict_keys_to_colors(dct):
        keys_are_strings = any([isinstance(k, str) for k in dct.keys()])
        keys_dont_match_string_colors = sorted(dct.keys()) != sorted(Connections.color_map.keys())
        colors = [Colors.YELLOW, Colors.GREEN, Colors.BLUE, Colors.PURPLE]
        keys_dont_match_colors = sorted(dct.keys()) != colors
        string_invalid = keys_are_strings and keys_dont_match_string_colors
        enum_invalid =  not keys_are_strings and keys_dont_match_colors
        exactly_four_colors = len(dct.keys()) == 4
        if string_invalid or enum_invalid and exactly_four_colors:
            keys_str = '\n\t'.join(dct.keys())
            error_msg = ('The keys in the input dictionaries must match ["YELLOW", '
                '"GREEN", "BLUE", "PURPLE"]. The keys you provided are:\n\t'
                f'{keys_str}.')
            raise ValueError(error_msg)

        new_dct = {}
        for k, v in dct.items():
            if isinstance(k, str):
                new_dct[Connections.color_map[k]] = v
            else:
                new_dct[k] = v
        return new_dct

    def __str__(self):
        remaining_grid = self._remaining_word_grid_representation()
        repr_str = (f'CONNECTIONS {remaining_grid}'
        f'\nRemaining guesses: {self.get_num_remaining_guesses()}')
        return repr_str

    def _remaining_word_grid_representation(self):
        output = '\t'
        for idx, word in enumerate(self.remaining_words):
            if idx % 4  == 0:
                output += '\n\t'
            output += word
            output += '\t'
        return output

    def _valid_guess(self, guess):
        sorted_guess = sorted(guess)
        if len(guess) != 4:
            raise ValueError('Guess must be exactly four words')

        word_not_in_word_list = False
        invalid_words = []
        for word in guess:
            if word not in self.remaining_words:
                word_not_in_word_list = True
                invalid_words.append(word)
                
        if word_not_in_word_list:
            raise ValueError('All guess words must be in remaining word list. '
                             'Invalid words: \n\t' + '\n\t'.join(invalid_words))
        
        if sorted_guess in self.guesses:
            raise ValueError(f'[{", ".join(sorted_guess)}] has already been guessed!')

    def _check_solution(self, guess):
        """
        Checks if 'guess' is a solution. If it is, is_solution is
        set to True. Otherwise, if there are three correct words,
        one_away is set to True.

        A visual representation of the guess is also returned.

        returns: (solution: bool; one_away: bool, guess_repr: str)
        """
        colors_solved = []
        guess_repr = []
        max_similar_count = 0
        for (color,s) in self.category_words.items():
            similar_count = 0
            for g in guess:
                if g in s:
                    similar_count += 1
                    guess_repr.append(color)
            if similar_count == 4:
                colors_solved.append(color)
            max_similar_count = max(max_similar_count, similar_count)
        self.guess_representations.append(guess_repr)

        return max_similar_count, colors_solved

    @util.upper_input
    def guess(self, guess):
        """
        Takes a guess of four words in the puzzle. If those words
        are a group, it will display what the group is.
        """
        one_away = False
        self._valid_guess(guess)
        similar_count, colors_solved = self._check_solution(guess)

        if colors_solved:
            for word in guess:
                self.remaining_words.remove(word)
            for color in colors_solved:
                self.remaining_colors.remove(color)

            # By default, if someone has solved the second
            # to last clue, they have solved the puzzle.
            if len(self.remaining_colors) == 1:
                colors_solved += self.remaining_colors
                self.finished = True
                self.win = True
        else:
            if similar_count == 3:
                one_away = True
            self.num_incorrect_guesses += 1
            if self.num_incorrect_guesses == 4:
                self.finished = True
            
        self.guesses.append(sorted(guess))

        return colors_solved, one_away

    def get_num_remaining_guesses(self):
        """Gets guesses remaining"""
        return Connections.num_incorrect_guesses_allowed - self.num_incorrect_guesses
    
    def get_num_incorrect_guesses(self):
        """Gets number of incorrect guesses"""
        return self.num_incorrect_guesses
    
    def get_remaining_words(self):
        """Gets words remaining in puzzle"""
        return self.remaining_words
    
    def get_win_state(self):
        """
        Returns whether or not puzzle is in win state (no categories remaining)
        """
        return self.win

    def reset(self):
        """
        Resets current game to its original state
        """
        self.finished = False
        self.win = False
        self.num_incorrect_guesses = 0
        self.guesses = []
        self.guess_representations = []
        self.remaining_words = []
        for word_list in self.category_words.values():
            for word in word_list:
                self.remaining_words.append(word)
        self.remaining_colors = [Colors.YELLOW, Colors.GREEN, Colors.BLUE, Colors.PURPLE]
        random.shuffle(self.remaining_words)
