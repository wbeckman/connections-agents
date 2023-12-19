import pickle
import functools
from connections.connections import Connections
from bots.bot import Bot

PUZZLES_PATH = 'assess/puzzles.pkl'


def load_puzzles():
    """Load existing puzzles from pre-fixed puzzle path"""
    with open(PUZZLES_PATH, 'rb') as handle:
        puzzles = pickle.load(handle)
    return puzzles

def detailed_stat_overview(stats, just_solutions=False, just_any_category=False):
    """
    Gives detailed overview for all stats (what the guesses were
    per game, what each game results were, etc.).

    'just_solutions' prints stats for puzzles that were solved.
    'just_any_category' prints stats for puzzles where at least one category was solved.
    """
    print_flag = True
    for puzzle_num, stat in stats.items():
        if just_solutions and stat['win_state'] == False:
            print_flag = False
        all_colors_solved = [c for _,(c, _)  in stat['guesses'].items()]
        all_colors_solved_flat = functools.reduce(lambda x,y:x+y, all_colors_solved)
        if just_any_category and len(all_colors_solved_flat) == 0:
            print_flag = False

        if print_flag:
            print(f"PUZZLE NUMBER {puzzle_num}")
            print(f"Number of guesses: {len(stat['guesses'])}")
            print('Guesses:\n')
            for guess_words, (_, one_away) in stat['guesses'].items():
                print(f'\tGUESS: {guess_words} | colors solved: {all_colors_solved_flat} | One away?: {one_away}')
            print(f'Puzzle won?: {stat["win_state"]}')


def stat_summary(stats):
    """
    Prints just the highlights for summary stats
    """
    print('**STAT SUMMARY**')
    n_guesses_solve = 0
    n_wins = 0
    n_categories_sum = 0
    max_categories = 0
    for _, stat in stats.items():
        if stat['win_state'] == True:
            n_wins += 1
            n_guesses_solve += len(stat['guesses']) - 4

        colors_solved = 0
        for guess_words, (colors_solved, _) in stat['guesses'].items():
            if len(colors_solved) >0:
                print(guess_words)
            n_categories_sum += len(colors_solved)
            max_categories = max(len(colors_solved), max_categories)

    n_categories_avg = n_categories_sum / len(stats)
    print(f'Number of puzzles successfully completed: {n_wins}')
    print(f'Number of categories solved per puzzle on average: {round(n_categories_avg,4)} / 4')
    print(f'Most categories solved from a single puzzle: {max_categories}')
    num_guesses_avg_solve = "NaN" if n_wins==0 else str(round(n_guesses_solve / n_wins), 2)
    print(f'Number of incorrect guesses on SOLVED puzzles (on average): {num_guesses_avg_solve}')


def assess_all(bot: Bot) -> dict:
    """
    Assesses performance of a bot on all previous connections puzzles
    (prior to December 11th, 2023) Returns which colors were guessed
    correctly, what the incorrect guesses were, whether the puzzle was
    solved or not.
    """
    puzzles = [Connections(*p) for p in load_puzzles()]
    results = {}
    for puzzle in puzzles:
        guesses, win_state = bot.solve(puzzle)
        results[puzzle.puzzle_num] = {
            'guesses': guesses,
            'win_state': win_state
        }
    return results
    
