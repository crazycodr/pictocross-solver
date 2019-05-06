import itertools
import logging

from PictoCrossSolver.PictoCross import Grid
from PictoCrossSolver.Renderers import ConsoleRenderer
from PictoCrossSolver.Solvers import *

# Create a 8,8 grid with a simple scenario taken from world's biggest picture cross
grid = Grid(8, 8)
grid.getRowZone(0).addHint(8)
grid.getRowZone(1).addHint(7)
grid.getRowZone(2).addHint(5)
grid.getRowZone(3).addHint(3)
grid.getRowZone(4).addHint(5)
grid.getRowZone(5).addHint(6)
grid.getRowZone(6).addHint(6)
grid.getRowZone(7).addHint(3)
grid.getColumnZone(0).addHint(1)
grid.getColumnZone(1).addHint(2)
grid.getColumnZone(1).addHint(1)
grid.getColumnZone(2).addHint(3)
grid.getColumnZone(2).addHint(3)
grid.getColumnZone(3).addHint(3)
grid.getColumnZone(3).addHint(4)
grid.getColumnZone(4).addHint(8)
grid.getColumnZone(5).addHint(7)
grid.getColumnZone(6).addHint(7)
grid.getColumnZone(7).addHint(2)
grid.getColumnZone(7).addHint(2)

# Prepare a console renderer
renderer = ConsoleRenderer(grid)

# Prepare solvers
solvers = []
solvers.append(HintFitsInEstimatedZoneSolver())
solvers.append(CrossAmbiguousZonesInCompletedHintsSolver())
solvers.append(HintExpandsFilledMarksFromEdgeInEstimatedZoneSolver())

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
                    input("Press a key to continue")

    return hadChanges

# Run our solvers until no change at all between two full loops
hasChanges = True
while hasChanges:
    hasChanges = False

    for rowIndex, rowSet in enumerate(grid.getRowZones()):
        hasChanges = hasChanges or processSet("row", rowIndex, rowSet)

    for columnIndex, columnSet in enumerate(grid.getColumnZones()):
        hasChanges = hasChanges or processSet("column", columnIndex, columnSet)


print("---------------------------------------------")
renderer.render()