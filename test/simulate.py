"""
Simulate the game a bazillion times to evaluate Stickguy's performance.
"""

import csv
import os
import sys
import time

from pathlib import Path
from random import randint

# Add project to Python path.
test_dir = Path(__file__).parents[0]
sys.path.append(str(test_dir.parents[0]))

import guesser

def play_game(max_number, user_number, gamedata):
    # print(f"User number: {user_number}")
    playing = True
    range_limits = (1, max_number)
    lo = range_limits[0]
    hi = range_limits[1]
    num_rem_guesses = guesser.get_max_guesses(max_number)
    gamedata['guesses-allowed'] = num_rem_guesses
    winner = None
    while playing:
        guess_limits = guesser.set_guess_range(lo, hi)
        guess = guesser.get_guess(guess_limits[0], guess_limits[1])
        num_rem_guesses -= 1
        gamedata['guesses-made'] = gamedata['guesses-allowed'] - num_rem_guesses
        gamedata['guesses'].append(guess)
        if num_rem_guesses == 0:
            # User wins.
            playing = False
            winner = 'user'
        elif guess == user_number:
            # Stickguy wins.
            playing = False
            winner = 'stickguy'
        elif user_number > guess:
            lo = guess
        elif guess > user_number:
            hi = guess
        gamedata['winner'] = winner
    return gamedata


data = []
runs = 1
args = sys.argv[:]
verbose = False
if len(args) > 1:
    if '-v' in args:
        args.remove('-v')
        verbose = True
    runs = int(args[1])

# Ensure that outfile exists.
outfile = test_dir / 'simulations.csv'
outfile.touch()

# Run simulations.
for i in range(runs):
    max = randint(2, 10000)
    user_max = randint(1, max)
    gamedata = {
        'game-id': time.time(),
        'max-num': max,
        'user-num': user_max,
        'guesses-allowed': 0,
        'guesses-made': 0,
        'guesses': [],
        'winner': '',
    }
    gamedata = play_game(max, user_max, gamedata)
    data.append(gamedata)

# Ensure that header row exists.
if not outfile.read_text():
    with open(outfile, 'w', newline='') as f:
        w = csv.writer(f, delimiter=',')
        w.writerow(gamedata.keys())

# Write data to CSV file.
for gamedata in data:
    if verbose:
        for k, v in gamedata.items():
            print(f"{k}: {v}")
        print()
    guesses_list = [str(i) for i in gamedata['guesses']]
    gamedata['guesses'] = ', '.join(guesses_list)
    with open(outfile, 'a', newline='') as f:
        w = csv.writer(f, delimiter=',')
        w.writerow(gamedata.values())
