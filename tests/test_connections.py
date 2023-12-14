# Test invalid input
# Test incorrect guess
# test init with both types of initialization



import pytest
from connections.connections import Connections

@pytest.fixture
def puzzle():
    categories = {
        'yellow': 'luxurious fabrics',
        'green': 'come down to rest',
        'blue': 'shoe parts',
        'purple': 'things that are delivered',
    }
    category_words = {
        'yellow': ['chiffon', 'satin', 'silk', 'velvet'],
        'green': ['perch', 'roost', 'settle', 'land'],
        'blue': ['eyelet', 'lace', 'sole', 'tongue'],
        'purple': ['baby', 'blow', 'package', 'speech'],
    }

    return Connections(categories, category_words)

def test_capitalize_category_words(puzzle):
    """Ensures category words are capitalized when passed as input"""
    for k,v in puzzle.category_words.items():
        assert(k == k.upper())
        for word in v:
            assert(word == word.upper())

def test_capitalize_categories(puzzle):
    """Ensures categories are capitalized when passed as input"""
    for k,v in puzzle.categories.items():
        assert(k == k.upper())
        assert(v == v.upper())


def test_invalid_input_not_in_vocab(puzzle):
    invalid = ['fff', 'ddd', 'ggg', 'ppp']
    with pytest.raises(ValueError):
        puzzle.guess(invalid)
