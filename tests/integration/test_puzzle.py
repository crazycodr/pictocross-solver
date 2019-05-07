from PictoCrossSolver.Elements import Grid
from PictoCrossSolver.Renderers import SolutionRenderer
from PictoCrossSolver.Solvers import *
from PictoCrossSolver.Readers import TextReader

import os
import re

def test_puzzle_fixtures():
    """
    Tests that the solving still works properly by using
    predefined real-world scenarios.

    If any solver was to change and solve the puzzles incorrectly,
    this would allow us to know pre-emptively.
    """

    # Scan for puzzle files
    puzzles = []
    for root, subdirs, files in os.walk(os.path.dirname(__file__) + '/puzzles'):
        for file in files:
            if re.match('puzzle-.*\\.txt', file):
                puzzles.append(root + '/' + file)
    
    # Test each puzzle
    for puzzleFile in puzzles:

        # Ensure there is a solution
        solutionFile = puzzleFile.replace('puzzle-', 'solution-')
        if not os.path.exists(solutionFile):
            continue

        # Report
        print(f"Testing solution for puzzle {puzzleFile} still works")
        
        # Load the puzzle and solution in memory
        grid = TextReader.load(puzzleFile)
        with open(solutionFile, 'r') as solutionStream:
            solution = solutionStream.readlines()
            for index, line in enumerate(solution):
                solution[index] = line.strip()
        
        # Prepare solvers
        solvers = []
        solvers.append(HintFitsInEstimatedZoneSolver())
        solvers.append(CrossAmbiguousZonesInCompletedHintsSolver())
        solvers.append(HintExpandsFilledMarksFromEdgeInEstimatedZoneSolver())
        solvers.append(CrossMarksOutsideOfSolvedHintZonesSolver())

        # Run our solvers until no change at all between two full loops
        hasChanges = True
        hadChanges = False
        while hasChanges:
            hasChanges = False

            for rowIndex, rowSet in enumerate(grid.getRowZones()):
                hadChanges = processSet("row", rowIndex, rowSet, solvers)
                hasChanges = hasChanges or hadChanges

            for columnIndex, columnSet in enumerate(grid.getColumnZones()):
                hadChanges = processSet("column", columnIndex, columnSet, solvers)
                hasChanges = hasChanges or hadChanges

    # Get the solution representation in memory and compare with loaded solution
    solutionRenderer = SolutionRenderer(grid)
    liveSolution = solutionRenderer.render()
    assert liveSolution == solution
    

def processSet(setType: str, setIndex: int, zone: Zone, solvers: list) -> bool:

    # If there are no ambiguous marks left, consider complete and skip
    if len(list((zone for zone in zone.getMarks() if zone.isAmbiguous()))) == 0:
        return False

    # As long as we have changes, apply the solvers again
    hasChanges = True
    hadChanges = False
    while hasChanges:
        hasChanges = False

        # For each hint, find a potential set of Marks that match and then apply a list of
        # different solvers to change the zone if applicable
        for hintIndex, hint in enumerate(zone.getHints()):
            
            # Apply the solvers
            for solver in solvers:
                if solver.solve(zone):
                    hasChanges = hadChanges = True

    return hadChanges