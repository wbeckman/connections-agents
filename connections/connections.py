"""
Class to define a connections puzzle. A connections
puzzle has four logical categories (given as strings),
with four words per category (also given as strings).

"""

from connections import util

class Connections:

    """
    Defines a connections puzzle. Categories and corresponding
    words need to be listed in order of difficulty matching
    'difficulty_order' parameter
    """
    @util.upper_input
    def __init__(self, categories, category_words) -> None:
        if len(categories) != len(category_words):
            raise ValueError(
                'Number of categories must match number of category word lists provided (number '
                f' of categories: {len(categories)}; number of category word lists: '
                f'{len(category_words)})'
            )
        
        self.categories = categories
        self.category_words = category_words
        self.finished = False
        self.incorrect_guesses_before_loss = 4
        self.num_incorrect_guesses = 0
        self.guesses = []
        
        self.remaining_words = []
        for word_list in self.category_words.values():
            for word in word_list:
                print(word)
                self.remaining_words.append(word)

        self.emoji_guesses = []
        self.emoji_map = {'YELLOW': '🟨', 'GREEN': '🟩', 'BLUE': '🟦', 'PURPLE': '🟪',}

    def __str__(self):
        remaining_grid = self.remaining_word_grid()
        repr_str = 'CONNECTIONS' + remaining_grid
        print(f'Remaining guesses: {self.incorrect_guesses_before_loss - self.num_incorrect_guesses}')
        return repr_str

    @classmethod
    def from_category_dict(cls, category_dict):
        """
        Converts category dictionary 
        e.g. 
        {
            'yellow': ('PARTS OF A RIVER', ['BANK', 'BED', 'DELTA' 'MOUTH'}),
            'green': ('SOMETHING EASY TO DO', ['BREEZE', 'CINCH', 'PICNIC', 'SNAP']),
            ...
        }
        into a Connections puzzle object for that particular puzzle.

        a category_dict should have exactly four 
        """
        categories = []
        category_words = []
        for category, words in category_dict.items():
            categories.append(category)
            category_words.append(words)
        return cls(categories, category_words)
    
    def remaining_word_grid(self):
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
        one_away = False
        is_solution = False
        guess_repr = ''
        for (color,s) in self.category_words.items():
            similar_count = 0
            for g in guess:
                if g in s:
                    similar_count += 1
                    guess_repr += self.emoji_map[color]
            if similar_count == 4:
                is_solution = True
            if similar_count == 3:
                one_away = True
        return (is_solution, one_away, guess_repr)

    @util.upper_input
    def guess(self, guess):
        """
        Takes a guess of four words in the puzzle. If those words
        are a group, it will display what the group is 
        """
        self._valid_guess(guess)
        is_solution, one_away, guess_repr = self._check_solution(guess)
        self.emoji_guesses.append(guess_repr)
        if not is_solution:
            self.num_incorrect_guesses += 1
            if self.num_incorrect_guesses == 4:
                self.finished = True
        else:
            for word in guess:
                self.remaining_words.remove(word)
        self.guesses.append(sorted(guess))
        return is_solution, one_away


    def reset(self):
        self.num_incorrect_guesses = 0
        self.finished = False
        self.emoji_guesses = []


