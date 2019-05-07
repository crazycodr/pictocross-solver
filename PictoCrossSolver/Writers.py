from PictoCrossSolver.Elements import Grid
from PictoCrossSolver.Renderers import SolutionRenderer

class SolutionWriter:
    """
    Used to write the result of a Grid to a txt file
    """

    @staticmethod
    def write(file: str, grid: Grid):
        """
        Loads the file into memory and returns a grid

        @param str file to load
        @param Grid grid to render
        """

        # Get the solution to print
        renderer = SolutionRenderer(grid)
        solution = renderer.render()

        # Put the solution in a file
        with open(file, mode = "w") as fileStream:
            fileStream.write("\n".join(solution))