import math

from random import randint


def set_guess_range(lowest, highest):
    quarter1 = int((highest + 1 - lowest) / 4)
    quarter3 = 3 * quarter1
    guess_min = lowest + quarter1
    guess_max = lowest + quarter3
    # Special treatment for small ranges.
    if highest < 8:
        guess_min = lowest
        guess_max = highest
    return guess_min, guess_max

def get_confidence(rem_possibilities, rem_guesses):
    confidence = round(1 / rem_possibilities ** (1 / rem_guesses), 2) * 100
    return confidence

def get_guess(guess_min, guess_max):
    guess = randint(guess_min, guess_max)
    return guess

def get_max_guesses(max_number):
    max_guesses = int(round(math.log2(max_number)) + round(math.log(max_number, 1000)))
    return max_guesses
