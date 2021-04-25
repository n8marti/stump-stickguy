# Simulate the game a bazillion times to evaluate Stickguy's performance.

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from random import randint

import guesser

def play_game(max_number, user_number, counts):
    # print(f"User number: {user_number}")
    playing = True
    range_limits = (1, max_number)
    lo = range_limits[0]
    hi = range_limits[1]
    num_rem_guesses = guesser.get_max_guesses(max_number)
    while playing:
        # print(f"Guesses left: {num_rem_guesses}")
        guess_limits = guesser.set_guess_range(lo, hi)
        guess = guesser.get_guess(guess_limits[0], guess_limits[1])
        # print(f"Guess: {guess}")
        num_rem_guesses -= 1
        if num_rem_guesses == 0:
            # print("User wins.")
            counts['user'] += 1
            playing = False
        elif guess == user_number:
            # print("Stickguy wins!")
            counts['stickguy'] += 1
            playing = False
        elif user_number > guess:
            lo = guess
            # print(f"New low: {lo}")
        elif guess > user_number:
            hi = guess
            # print(f"New high: {hi}")
        # print()


counts = {
    'user': 0,
    'stickguy': 0,
}

runs = 10000
for i in range(runs):
    max = randint(1, 10000)
    play_game(max, randint(1, max), counts)

print(f"User: {counts['user']/runs}\tStickguy: {counts['stickguy']/runs}")
