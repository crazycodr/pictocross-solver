import itertools
import logging
import os

from PictoCrossSolver.Readers import TextPuzzleReader
from PictoCrossSolver.Writers import SolutionWriter
from PictoCrossSolver.Engines import EventDrivenEngine
from PictoCrossSolver.Renderers import ConsoleRenderer
from PictoCrossSolver.Elements import Puzzle, PuzzleChange
from PictoCrossSolver.Strategies import Strategy, ChangeUsingHintPositionner

# Setup standard logging
logger = logging.getLogger()
consoleLoggingHandler = logging.StreamHandler()
consoleLoggingHandler.setLevel(logging.INFO)
fileLoggingHandler = logging.FileHandler(filename = os.getcwd() + '/run.log', mode = 'w')
fileLoggingHandler.setLevel(logging.DEBUG)
logger.addHandler(consoleLoggingHandler)
logger.addHandler(fileLoggingHandler)
logger.setLevel(logging.DEBUG)

# Setup the changes only logging
changesLogger = logging.getLogger("changes")
changesLoggingHandler = logging.FileHandler(filename = os.getcwd() + '/changes.log', mode = 'w')
changesLoggingHandler.setLevel(logging.DEBUG)
changesLogger.addHandler(changesLoggingHandler)

# Load the puzzle from file
puzzle = TextPuzzleReader.load("tests/integration/puzzles/books/sport-cerebral/logimage/103/puzzle-48.txt")

# Change applied watcher
def changeAppliedWatcher(puzzle: Puzzle, strategy: Strategy):
    renderer = ConsoleRenderer(puzzle.applyChanges())
    renderer.render()

# Prepare the engine and ask it to solve the puzzle
engine = EventDrivenEngine()
engine.addStrategy(ChangeUsingHintPositionner())
engine.onChangesApplied(changeAppliedWatcher)
solvedPuzzle = engine.solve(puzzle)

# Print the solution to solution.txt
SolutionWriter.write(os.getcwd() + '/solution.txt', solvedPuzzle.applyChanges())