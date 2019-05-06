import itertools
import logging

from PictoCrossSolver.PictoCross import Grid
from PictoCrossSolver.Renderers import ConsoleRenderer
from PictoCrossSolver.Solvers import *
from PictoCrossSolver.Loaders import TextLoader

# Load the grid from file
grid = TextLoader.load("puzzles/super-easy-2.txt")

# Prepare a console renderer
renderer = ConsoleRenderer(grid)

# Prepare solvers
solvers = []
solvers.append(HintFitsInEstimatedZoneSolver())
solvers.append(CrossAmbiguousZonesInCompletedHintsSolver())
solvers.append(HintExpandsFilledMarksFromEdgeInEstimatedZoneSolver())
solvers.append(CrossMarksOutsideOfSolvedHintZonesSolver())

# Print the initial grid
print("---------------------------------------------")
print("INITIAL GRID")
print("---------------------------------------------")
renderer.render()
print("---------------------------------------------")

logging.basicConfig(level = logging.DEBUG)

def processSet(setType: str, setIndex: int, zone: Zone) -> bool:

    # Serialize the zone and report it
    print()
    print(f"Processing {setType} #{setIndex}")
    print("---------------------------------------------")


    # If there are no ambiguous marks left, consider complete and skip
    if len(list((zone for zone in zone.getMarks() if zone.isAmbiguous()))) == 0:
        print(f"Already completed")
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
                print(f"Applying solver {type(solver).__name__}")
                if solver.solve(zone):
                    print(f"Solver made changes:")
                    print("---------------------------------------------")
                    renderer.render()
                    hasChanges = hadChanges = True

    return hadChanges

# Run our solvers until no change at all between two full loops
hasChanges = True
hadChanges = False
while hasChanges:
    hasChanges = False

    for rowIndex, rowSet in enumerate(grid.getRowZones()):
        hadChanges = processSet("row", rowIndex, rowSet)
        hasChanges = hasChanges or hadChanges

    for columnIndex, columnSet in enumerate(grid.getColumnZones()):
        hadChanges = processSet("column", columnIndex, columnSet)
        hasChanges = hasChanges or hadChanges


print("---------------------------------------------")
renderer.render()