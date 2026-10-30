# GA Snake, original version (2019 to 2021)

A genetic algorithm that evolves a population of snakes to play Snake. This is the first version, kept as it was before any changes, so you can see where the project started.

It does not get through a generation as written:

- On Python 3.14 it stops with a `TypeError` from `random.randrange`, because `display_width / 10` is a float.
- Once that is fixed, it stops in `choose_parent`, which returns a list where a single snake is expected.

Run it (needs `pygame` and `numpy`):

    python "Main Project/genetic_algorithm.py"

The work on fixing and improving it continues in a separate repository.
