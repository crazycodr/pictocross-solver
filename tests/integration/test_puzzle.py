import pytest
import re
from PictoCrossSolver.Engines import EventDrivenEngine
from PictoCrossSolver.Renderers import SolutionRenderer
from PictoCrossSolver.Readers import TextPuzzleReader, TextSolutionReader
from PictoCrossSolver.Strategies import ChangeUsingHintPositionner
from PictoCrossSolver.Helpers import HintPositionner
from PictoCrossSolver.Caches import MemoryCache

import os

def getPuzzlesAndSolutions() -> []:

    # Scan for puzzle files
    testablePuzzles = []
    for root, subdirs, files in os.walk(os.path.dirname(__file__) + '/puzzles'):
        for file in files:
            if re.match('puzzle-.*\\.txt', file):
                matches = re.search('puzzle-(?P<puzzle>\d+-\d+)\.txt', file)
                if matches == None:
                    continue
                solution = 'solution-' + matches.groupdict()['puzzle'] + '.txt'
                if os.path.exists(root + '/' + solution):
                    testablePuzzles.append((root + '/' + file, root + '/' + solution))
    
    return testablePuzzles

@pytest.mark.parametrize("puzzle,solution", getPuzzlesAndSolutions())
def test_eventDrivenEngine(puzzle: str, solution: str):
    """
    Integration test for specific puzzle in integration tests
    """
    
    # Load the puzzle and solution in memory
    puzzle = TextPuzzleReader.load(puzzle)
    preparedSolution = TextSolutionReader.load(solution)
    
    # Solve the puzzle
    engine = EventDrivenEngine()
    engine.addStrategy(ChangeUsingHintPositionner(HintPositionner(MemoryCache(), MemoryCache())))
    solvedPuzzle = engine.solve(puzzle)

    # Get the solution representation in memory and compare with loaded solution
    solutionRenderer = SolutionRenderer(solvedPuzzle.applyChanges())
    liveSolution = solutionRenderer.render()
    print(f"LIVE SOLUTION: {puzzle}")
    print("--------------------------")
    print("\n".join(liveSolution))
    print("--------------------------")
    print(f"PREPARED SOLUTION: {solution}")
    print("--------------------------")
    print("\n".join(preparedSolution))
    print("--------------------------")
    assert liveSolution == preparedSolution