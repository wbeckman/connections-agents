import pandas as pd
import connections
from pprint import pprint
import connections.connections

def assert_val_exists_and_valid_value(val_name, dictionary):
    key_present = val_name in dictionary
    if not key_present:
        print(f'ERROR: Record exists without key \'{val_name}\'\n')
        pprint(record)
    valid_value = dictionary[val_name] is not None and dictionary[val_name] != ''
    if not valid_value:
        print(f'ERROR: key {val_name} has an invalid value.\n')
        print(f'\tVALUE: {dictionary[val_name]}')

    return key_present and valid_value

# Data scraped from here: https://tryhardguides.com/nyt-connections-answers/

if __name__ == '__main__':
    with open('previous_puzzles.txt', 'r') as f:
        txt = f.readlines()
    stripped_lines = []
    for line in txt:
        stripped_lines.append(line.strip())
    idx = 0
    processed_data = []
    record = {}
    column_names = ['puzzle_num', 'date', 'cat1_name', 'cat2_name', 'cat3_name', 'cat4_name', 'cat1_words', 'cat2_words', 'cat3_words', 'cat4_words']
    for line in stripped_lines:
        if line.lower().startswith('nyt connections '):
            idx = 0
            if record: processed_data.append(record)
            record = {}
            line = line[16:]
            puzzle_num, date = [l.strip() for l in line.split('-')]
            record['puzzle_num'] = puzzle_num
            record['date'] = date
        else:
            category = [l.strip() for l in line.split('-')][0]
            words = ''.join([l.strip() for l in line.split('-')][1:]) 
            all_words = words.split(', ')
            if idx == 1:
                record['color'] = 'yellow'
            if idx == 2:
                record['color'] = 'green'
            if idx == 3:
                record['color'] = 'blue'
            if idx == 4:
                record['color'] = 'purple'
            record[f'{record["color"]}_solution'] = category
            record[f'{record["color"]}_words'] = all_words

        idx += 1
    processed_data.append(record)

    for record in processed_data:
        for field in record:
            assert(assert_val_exists_and_valid_value('date', record))
            assert(assert_val_exists_and_valid_value('puzzle_num', record))
            assert(assert_val_exists_and_valid_value('yellow_solution', record))
            assert(assert_val_exists_and_valid_value('green_solution', record))
            assert(assert_val_exists_and_valid_value('blue_solution', record))
            assert(assert_val_exists_and_valid_value('purple_solution', record))
            assert(assert_val_exists_and_valid_value('yellow_words', record))
            assert(assert_val_exists_and_valid_value('green_words', record))
            assert(assert_val_exists_and_valid_value('blue_words', record))
            assert(assert_val_exists_and_valid_value('purple_words', record))
            assert(len(record['yellow_words']) == 4)
            assert(len(record['green_words']) == 4)
            assert(len(record['blue_words']) == 4)
            assert(len(record['purple_words']) == 4)
    

    def parse_record(record):
        categories = {}
        category_words = {}
        for color in ['yellow', 'green', 'blue', 'purple']:
            categories[color] = record[f'{color}_solution'].lower()
            category_words[color] = record[f'{color}_words']
        return categories, category_words

            

    puzzle = connections.connections.Connections(*parse_record(processed_data[0]))
    puzzle.guess(['chiffon', 'satin', 'velvet', 'land'])
    puzzle.guess(['CHIFFON', 'SATIN', 'SILK', 'VELVET'])
    

    print(puzzle)
    print(puzzle.categories)