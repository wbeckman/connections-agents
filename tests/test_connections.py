# Test invalid input
# Test incorrect guess
# test init with both types of initialization


import pytest
from connections.connections import Connections
from connections.colors import Colors

@pytest.fixture
def puzzle():
    categories = {
        'yellow': 'luxurious fabrics',
        'green': 'come down to rest',
        'blue': 'shoe parts',
        'purple': 'things that are delivered',
    }
    category_words = {
        Colors.YELLOW: ['chiffon', 'satin', 'silk', 'velvet'],
        Colors.GREEN: ['perch', 'roost', 'settle', 'land'],
        Colors.BLUE: ['eyelet', 'lace', 'sole', 'tongue'],
        Colors.PURPLE: ['baby', 'blow', 'package', 'speech'],
    }

    return Connections(categories, category_words)

def test_bad_puzzle_creation_bad_colors_string():
    categories = {
        'yello': 'luxurious fabrics',
        'green': 'come down to rest',
        'blue': 'shoe parts',
        'purple': 'things that are delivered',
    }
    category_words = {
        Colors.YELLOW: ['chiffon', 'satin', 'silk', 'velvet'],
        Colors.GREEN: ['perch', 'roost', 'settle', 'land'],
        Colors.BLUE: ['eyelet', 'lace', 'sole', 'tongue'],
        Colors.PURPLE: ['baby', 'blow', 'package', 'speech'],
    }
    with pytest.raises(ValueError):
        Connections(categories, category_words)


def test_bad_puzzle_creation_bad_colors_enum():
    categories = {
        'yellow': 'luxurious fabrics',
        'green': 'come down to rest',
        'blue': 'shoe parts',
        'purple': 'things that are delivered',
    }
    category_words = {
        Colors.GREEN: ['perch', 'roost', 'settle', 'land'],
        Colors.BLUE: ['eyelet', 'lace', 'sole', 'tongue'],
        Colors.PURPLE: ['baby', 'blow', 'package', 'speech']
    }
    with pytest.raises(ValueError):
        Connections(categories, category_words)

def test_bad_puzzle_creation_lt_4_categories():
    categories = {
        'yellow': 'luxurious fabrics',
    }
    category_words = {
        Colors.GREEN: ['perch', 'roost', 'settle', 'land'],
        Colors.BLUE: ['eyelet', 'lace', 'sole', 'tongue'],
        Colors.PURPLE: ['baby', 'blow', 'package', 'speech']
    }
    with pytest.raises(ValueError):
        Connections(categories, category_words)

def test_capitalize_category_words(puzzle):
    """Ensures category words are capitalized when passed as input"""
    for k,v in puzzle.category_words.items():
        for word in v:
            assert(word == word.upper())

def test_capitalize_categories(puzzle):
    """Ensures categories are capitalized when passed as input"""
    for k,v in puzzle.categories.items():
        assert(v == v.upper())

def test_invalid_input_more_than_four_words(puzzle):
    invalid = ['chiffon', 'satin', 'silk', 'velvet', 'roost']
    with pytest.raises(ValueError):
        puzzle.guess(invalid)

def test_invalid_input_not_in_vocab(puzzle):
    invalid = ['fff', 'ddd', 'ggg', 'ppp']
    with pytest.raises(ValueError):
        puzzle.guess(invalid)

def test_invalid_input_already_guessed(puzzle):
    invalid_if_guessed_twice = ['chiffon', 'satin', 'silk', 'velvet']
    puzzle.guess(invalid_if_guessed_twice)
    with pytest.raises(ValueError):
        puzzle.guess(invalid_if_guessed_twice)

def test_str(puzzle):
    pass


