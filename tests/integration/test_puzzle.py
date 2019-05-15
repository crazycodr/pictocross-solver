import pytest
import re
from PictoCrossSolver.Engines import EventDrivenEngine
from PictoCrossSolver.Renderers import SolutionRenderer
from PictoCrossSolver.Readers import TextPuzzleReader, TextSolutionReader
from PictoCrossSolver.Strategies import ChangeUsingHintPositionner

import os

def getPuzzlesAndSolutions() -> []:

    # Scan for puzzle files
    testablePuzzles = []
    for root, subdirs, files in os.walk(os.path.dirname(__file__) + '/puzzles'):
        for file in files:
            if re.match('puzzle-.*\\.txt', file):
                solution = 'solution-' + re.search('puzzle-(?P<puzzle>\d+-\d+)\.txt', file).groupdict()['puzzle'] + '.txt'
                if os.path.exists(root + '/' + solution):
                    testablePuzzles.append((root + '/' + file, root + '/' + solution))
    
    return testablePuzzles

@pytest.mark.parametrize("puzzle,solution", getPuzzlesAndSolutions())
def test_eventDrivenEngine(puzzle: str, solution: str):
    """
    Integration test for specific puzzle in Biggest Picture Cross - Animals - Puzzle 1,2
    """
    
    # Load the puzzle and solution in memory
    puzzle = TextPuzzleReader.load(puzzle)
    solution = TextSolutionReader.load(solution)
    
    # Solve the puzzle
    engine = EventDrivenEngine()
    engine.addStrategy(ChangeUsingHintPositionner())
    solvedPuzzle = engine.solve(puzzle)

    # Get the solution representation in memory and compare with loaded solution
    solutionRenderer = SolutionRenderer(solvedPuzzle.applyChanges())
    liveSolution = solutionRenderer.render()
    assert liveSolution == solution