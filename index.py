import itertools
import logging
import os
import argparse

from PictoCrossSolver.Readers import TextPuzzleReader
from PictoCrossSolver.Writers import SolutionWriter, InstructionWriter
from PictoCrossSolver.Engines import EventDrivenEngine
from PictoCrossSolver.Renderers import ConsoleRenderer
from PictoCrossSolver.Elements import Puzzle, PuzzleChange
from PictoCrossSolver.Strategies import Strategy, ChangeUsingHintPositionner
from PictoCrossSolver.Helpers import HintPositionner
from PictoCrossSolver.Caches import FileCache, MemoryCache, CacheChain

# Argument parser setup
parser = argparse.ArgumentParser(description='Solves picture cross puzzles using puzzle files')
parser.add_argument('puzzle', help='a puzzle file to solve')
parser.add_argument('--instructions', '-i', default=False, action="store_true", dest="writeInstructions", help='Generate instructions, requires output directory')
parser.add_argument('--solution', '-s', default=False, action="store_true", dest="writeSolution", help='Generate solution, requires output directory')
parser.add_argument('--output-dir', '-o', default=os.getcwd(), dest="outputDirectory", help="Generate output files in this directory")
parser.add_argument('--cache-dir', '-c', default=os.getcwd() + '/cache', dest="cacheDirectory", help="Generate and use cache files using this directory")
parser.add_argument('--verbose', '-v', default=0, dest="verbose", action='count', help="Makes the engine more verbose")
args = parser.parse_args()

# Setup standard logging
logger = logging.getLogger()
consoleLoggingHandler = logging.StreamHandler()
fileLoggingHandler = logging.FileHandler(filename = args.outputDirectory + '/run.log', mode = 'w')
logger.addHandler(consoleLoggingHandler)
logger.addHandler(fileLoggingHandler)
logger.setLevel(logging.ERROR - args.verbose * 10)

# Setup the changes only logging
changesLogger = logging.getLogger("changes")
changesLoggingHandler = logging.FileHandler(filename = args.outputDirectory + '/changes.log', mode = 'w')
changesLoggingHandler.setLevel(logging.DEBUG)
changesLogger.addHandler(changesLoggingHandler)

# Load the puzzle from file
puzzle = TextPuzzleReader.load(args.puzzle)

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
    SolutionWriter.write(args.outputDirectory + '/solution.txt', solvedPuzzle.applyChanges())
if args.writeInstructions:
    InstructionWriter.write(args.outputDirectory + '/instructions.txt', solvedPuzzle)