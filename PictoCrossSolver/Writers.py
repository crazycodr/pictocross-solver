from PictoCrossSolver.Elements import Puzzle
from PictoCrossSolver.Renderers import SolutionRenderer

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