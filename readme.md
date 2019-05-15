# PictoCross Solver

To learn Python, i decided to do more than just a simple HelloWorld example. I decided to mix one of my active passions PictureCross Puzzles with this learning experience and thus i created the PictoCross Solver.

# Components

The PictoCrossSolver module provides several sub modules below:

| Component | Description |
| --------- | ----------- |
| Elements  | All elements composing the puzzle and puzzle |
| Analyzers | The analyzers are used to figure out marks to touch based on hints |
| Solvers   | The solvers are used to apply certain logic based on analyzers |
| Readers   | The Readers load puzzles from files |

# Requirements

- [python3](https://www.python.org) and [venv](https://docs.python.org/3/library/venv.html)
- [poetry](https://github.com/sdispater/poetry)

# Setup the environment

To use the solver, you need to create an environment. I used the traditional `venv` module:

    python3 -m venv create .env

Then activate the environment:

    source .env/bin/activate

Then install the requirements using poetry:

    poetry install

# Using the solver

Just run the solver using the python environment, there are no parameters for now and the puzzles is hardcoded into the index.py. I'll add a loading facility later, for now, i'm focusing on solving more complex puzzles.

    python index.py

# Output

The solver will print a lot of things to the console and to a log file called `run.log`. It doesn't produce a solution into some kind of file yet.

The end result will render the puzzle to the console or file. If you still have ambiguities, it means the solver doesn't have all required algorithms to finish this puzzle. Submit your puzzle and i'll try to add the necessary missing pieces.

> You can also contribute! Remember to follow the code style and create tests for your new solver.