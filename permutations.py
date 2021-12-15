import itertools
import re

words = []


def read_words(file):
    with open(file, 'r') as f:
        return f.read().splitlines()


input_file = 'all_words3.txt'
output_file = 'all_possibilities3.txt'

words += read_words(input_file)

print('Num words', len(words))


def all_combinations(it):
    all_combos = []
    for f in range(1, len(it) + 1):
        for x in itertools.combinations(it, f):
            all_combos.append(x)
    return all_combos


def capitalise_first_letter(word):
    return [word[0].upper() + word[1:]]


def capitalise_all_letters(word):
    word_upper = word.upper()
    if word_upper != word:
        return [word.upper()]
    return []


def append_digit(word):
    return [word + str(n) for n in range(0, 10)]


def append_symbol(word):
    return [word + sym for sym in ['&', '*', '$', '%', '!']]

# This creates too many possibilities and seems unlikely to produce a hit
# def insert_symbol_or_digit(word):
#     new_words = []
#     for i in range(1, len(word)):
#         for sym in ['@', '&', '$', '3', '0', '5']:
#             new_words.append(word[0:i] + sym + word[i:])
#     return new_words


def replace_char(char, repl):
    def replace(word):
        replacements = []
        indexes = [m.start() for m in re.finditer(char, word)]
        for combo in all_combinations(indexes):
            new_word = word
            for index in combo:
                new_word = new_word[0:index] + repl + new_word[index+1:]
            replacements.append(new_word)
        return replacements
    return replace


substitutions = [replace_char('a', '@'), replace_char('a', '&'), replace_char('e', '3'), replace_char('o', '0'), replace_char('s', '5'), replace_char('s', '$')]
all_functions = [capitalise_first_letter] + substitutions + [capitalise_all_letters, append_symbol, append_digit]

combinations = all_combinations(all_functions)

all_words = []


def flatten(l):
    flattened_list = []
    for nested_list in l:
        flattened_list += nested_list
    return flattened_list


for word in words:
    all_words.append(word)
    for combo in combinations:
        # Apply all the functions in combination
        buffer = [word]
        for f in combo:
            buffer = flatten([f(cw) for cw in buffer])
        all_words += buffer

print(f'Generated {len(all_words)} words')
with open(output_file, 'w') as f:
    for word in all_words:
        f.write(f'{word}\n')