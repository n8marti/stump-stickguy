#!/usr/bin/env python3

import math
import sys

from os import system
from random import randint

def set_guess_range(lowest, highest):
    quarter1 = int((highest + 1 - lowest) / 4)
    quarter3 = 3 * quarter1
    guess_min = lowest + quarter1
    guess_max = lowest + quarter3
    return(guess_min, guess_max)


highest = int(input("Guessing a number between 1 and: "))
lowest = 1
max_guesses = int(round(math.log2(highest)) + round(math.log(highest, 1000)))
num_guesses = 1

playing = True
while playing:
    system('clear')
    rem_choices = highest + 1 - lowest
    rem_guesses = max_guesses - num_guesses + 1
    p = round(1 / rem_choices ** (1 / rem_guesses)
, 2) * 100
    text = "guesses" if rem_guesses > 1 else "guess"
    print(f"{rem_guesses} {text} left.")
    print(f"(my confidence level: {int(p)}%)\n")
    guess_min, guess_max = set_guess_range(
        lowest,
        highest
    )
    guess = randint(guess_min, guess_max)
    response = input(f"Is it {guess}? [yes/higher/lower]: ")
    response = response[0].lower()
    if response == 'y':
        print("I win!")
        playing = False
        continue
    elif response == 'h':
        highest = highest
        lowest = guess + 1
    elif response == 'l':
        highest = guess - 1
        lowest = lowest
    else:
        print("Please enter 'y', 'h', or 'l'.")
        continue
    if lowest > highest:
        print(f"Impossible! Did you forget your number?")
        playing = False
    if num_guesses >= max_guesses:
        print("You win!")
        playing = False
        continue
    num_guesses += 1
