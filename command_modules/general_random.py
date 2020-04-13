import random
from commands import *

commands = []


def coin_flip(message):
    return "It's {}!".format(random.choice(['heads', 'tails']))


commands.append(Command('flipcoin', 'flips a coin', ['Luuk'], coin_flip))


candidate_list = Argument('candidates', 'space separated list of candidates for the lotto')


def lotto(message):
    options = message.content.split()
    return random.choice(options)


commands.append(Command('lotto',
                        'picks a random name from the provided list of names',
                        ['Marco'],
                        lotto, arguments=[candidate_list]))

sides_argument = Argument('sides',
                          'positive integer representing the amount of sides the die should have',
                          optional=True)


def roll(message):
    sides = 6

    if message.content:
        try:
            sides = int(message.content)
        except ValueError:
            raise WrongArgumentError(sides_argument, 'Must be an integer!')

    if sides > 0:
        random_side = random.randint(1, int(sides))
        return "Rolling {}-sided die: {}".format(sides, random_side)
    else:
        raise WrongArgumentError(sides_argument, 'Must be positive!')


commands.append(Command('roll',
                        'roll an N-sided die of your choice',
                        ['Luuk'],
                        roll, arguments=[sides_argument]))


def add_commands(main_module):
    for command in commands:
        main_module.add_command(command)
