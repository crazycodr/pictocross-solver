import itertools
import logging
import os

from PictoCrossSolver.Elements import Grid
from PictoCrossSolver.Renderers import ConsoleRenderer
from PictoCrossSolver.Solvers import *
from PictoCrossSolver.Readers import TextReader
from PictoCrossSolver.Writers import SolutionWriter

# Setup logging
logger = logging.getLogger(None)
consoleLoggingHandler = logging.StreamHandler()
consoleLoggingHandler.setLevel(logging.INFO)
fileLoggingHandler = logging.FileHandler(filename = os.getcwd() + '/run.log', mode = 'w')
fileLoggingHandler.setLevel(logging.DEBUG)
logger.addHandler(consoleLoggingHandler)
logger.addHandler(fileLoggingHandler)
logger.setLevel(logging.DEBUG)

# Load the grid from file
grid = TextReader.load("tests/integration/puzzles/biggest-picture-cross/animals/puzzle-5-2.txt")

# Prepare a console renderer
renderer = ConsoleRenderer(grid)

# Prepare solvers
solvers = []
solvers.append(HintFitsInEstimatedZoneSolver())
solvers.append(CrossAmbiguousZonesInCompletedHintsSolver())
solvers.append(HintExpandsFilledMarksFromEdgeInEstimatedZoneSolver())
solvers.append(CrossMarksOutsideOfSolvedHintZonesSolver())

# Show the initial puzzle empty
logger.info("---------------------------------------------")
logger.info("INITIAL GRID")
logger.info("---------------------------------------------")
renderer.render()
logger.info("---------------------------------------------")

def processSet(setType: str, setIndex: int, zone: Zone) -> bool:

    # Serialize the zone and report it
    logger.info("")
    logger.info(f"Processing {setType} #{setIndex}")
    logger.info("---------------------------------------------")


    # If there are no ambiguous marks left, consider complete and skip
    if len(list((zone for zone in zone.getMarks() if zone.isAmbiguous()))) == 0:
        logger.info(f"Already completed")
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
                logger.info(f"Applying solver {type(solver).__name__}")
                if solver.solve(zone):
                    logger.info(f"Solver made changes:")
                    logger.info("---------------------------------------------")
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


logger.info("---------------------------------------------")
renderer.render()
fileLoggingHandler.close()
consoleLoggingHandler.flush()
consoleLoggingHandler.close()

# Print the solution to solution.txt
SolutionWriter.write(os.getcwd() + '/solution.txt', grid)