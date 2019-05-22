from PictoCrossSolver.Elements import Puzzle, PuzzleChange, PuzzleChangeAction, ZoneType
from PictoCrossSolver.Renderers import SolutionRenderer, PuzzleRenderer
from typing import List

class SolutionWriter:
    """
    Used to write the result of a Puzzle to a txt file
    """

    @staticmethod
    def write(file: str, puzzle: Puzzle):
        """
        Loads the file into memory and returns a puzzle

        @param str file to load
        @param Puzzle puzzle to render
        """

        # Get the solution to print
        renderer = SolutionRenderer(puzzle)
        solution = renderer.render()

        # Put the solution in a file
        with open(file, mode = "w") as fileStream:
            fileStream.write("\n".join(solution))

class InstructionWriter:
    """
    Used to write the instruction of a Puzzle to a txt file in a readable format
    """

    @staticmethod
    def write(file: str, puzzle: Puzzle):
        """
        Opens the file and then writes all changes into a readable format

        @param str file to write
        @param List[PuzzleChange] changes to write
        """

        # Render each change as a string
        instructions = []
        for change in puzzle.getChanges():

            # Extract the zone
            zone = puzzle.getZone(change.getZoneType(), change.getZoneIndex())
            hints = "[" + ", ".join(map(lambda a: str(a), zone.getHints())) + "]"
            zoneType = 'row' if zone.getZoneType() == ZoneType.ROW else 'column'
            
            # Extract the action
            action = ""
            if change.getAction() == PuzzleChangeAction.FILL:
                action = "Fill"
            else:
                action = "Cross out"

            # Extract the slice to change
            marks = f"{change.getZoneSlice().start + 1} to {change.getZoneSlice().stop}"

            # Build the instruction
            instructions.append(f"{action} the marks {marks} in {zoneType} #{zone.getZoneIndex() + 1} (with hints: {hints})")

            # Apply the change to the puzzle and render the solution
            puzzle = puzzle.applyChange(change)
            renderer = PuzzleRenderer(puzzle)
            solution = renderer.render()
            instructions.append("")
            for solutionLine in solution:
                instructions.append(solutionLine)
            instructions.append("")

        # Put the instructions in a file
        with open(file, mode = "w") as fileStream:
            fileStream.write("\n".join(instructions))