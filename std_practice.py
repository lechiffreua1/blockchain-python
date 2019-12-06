from random import randint
from datetime import time

first_int = randint(1, 10)
second_int = randint(0, 1)

print('Random (1, 10) - {}'.format(first_int))

print('Random (0, 1) - {}'.format(second_int))

print('Date - {}'.format(time(hour=first_int, minute=second_int)))
