import itertools
import logging
import os
import argparse

from PictoCrossSolver.Readers import TextPuzzleReader, PuzzleBuilder
from PictoCrossSolver.Writers import SolutionWriter, InstructionWriter, PuzzleWriter
from PictoCrossSolver.Engines import EventDrivenEngine
from PictoCrossSolver.Renderers import ConsoleRenderer
from PictoCrossSolver.Elements import Puzzle, PuzzleChange
from PictoCrossSolver.Strategies import Strategy, ChangeUsingHintPositionner
from PictoCrossSolver.Helpers import HintPositionner
from PictoCrossSolver.Caches import FileCache, MemoryCache, CacheChain

# Argument parser setup
parser = argparse.ArgumentParser(description='Solves picture cross puzzles using puzzle files')
parser.add_argument('puzzle', nargs="?", default=None, help='a puzzle file to solve')
parser.add_argument('--write-instructions', default=False, action="store_true", dest="writeInstructions", help='Generate instructions')
parser.add_argument('--write-solution', default=False, action="store_true", dest="writeSolution", help='Generate solution')
parser.add_argument('--output-dir', '-o', default=os.getcwd(), dest="outputDirectory", help="Generate output files in this directory")
parser.add_argument('--cache-dir', '-c', default=os.getcwd() + '/cache', dest="cacheDirectory", help="Generate and use cache files using this directory")
parser.add_argument('--write-puzzle', default=False, action="store_true", dest="writePuzzle", help="Generate puzzle")
parser.add_argument('--puzzle-suffix', default="", dest="puzzleSuffix", help="dSuffix of the written files")
parser.add_argument('--verbose', '-v', default=0, dest="verbose", action='count', help="Makes the engine more verbose")
args = parser.parse_args()

# Setup standard logging
logger = logging.getLogger()
consoleLoggingHandler = logging.StreamHandler()
fileLoggingHandler = logging.FileHandler(filename = args.outputDirectory + f'/run{args.puzzleSuffix}.log', mode = 'w')
logger.addHandler(consoleLoggingHandler)
logger.addHandler(fileLoggingHandler)
logger.setLevel(logging.ERROR - args.verbose * 10)

# Setup the changes only logging
changesLogger = logging.getLogger("changes")
changesLoggingHandler = logging.FileHandler(filename = args.outputDirectory + f'/changes{args.puzzleSuffix}.log', mode = 'w')
changesLoggingHandler.setLevel(logging.DEBUG)
changesLogger.addHandler(changesLoggingHandler)

# Load the puzzle from file if puzzle is set in args
if args.puzzle:
    puzzle = TextPuzzleReader.load(args.puzzle)
else:
    puzzle = PuzzleBuilder().buildFromConsole()

# Change applied watcher
def changeAppliedWatcher(puzzle: Puzzle, strategy: Strategy):
    renderer = ConsoleRenderer(puzzle.applyChanges())
    renderer.render()

# Prepare the engine and ask it to solve the puzzle
engine = EventDrivenEngine()
cacheChain = CacheChain()
memoryCache = MemoryCache()
cacheChain.addCache(memoryCache)
cacheChain.addCache(FileCache(args.cacheDirectory))
engine.addStrategy(ChangeUsingHintPositionner(HintPositionner(cacheChain, memoryCache)))
engine.onChangesApplied(changeAppliedWatcher)
solvedPuzzle = engine.solve(puzzle)

# Print the solution to solution.txt
if args.writeSolution:
    SolutionWriter.write(args.outputDirectory + f'/solution{args.puzzleSuffix}.txt', solvedPuzzle.applyChanges())
if args.writeInstructions:
    InstructionWriter.write(args.outputDirectory + f'/instructions{args.puzzleSuffix}.txt', solvedPuzzle)
if args.writePuzzle:
    PuzzleWriter.write(args.outputDirectory + f'/puzzle{args.puzzleSuffix}.txt', solvedPuzzle)