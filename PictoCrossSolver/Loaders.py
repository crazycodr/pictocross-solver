from PictoCrossSolver.Elements import Grid

class TextLoader:
    """
    Used to load puzzles from text files containing 2 lines
    - First line contains the column definitions
    - Second line contains the row definitions

    All definitions are structure like this:
    - Each column or row definition is separated by a forward slash "/"
    - Each hint in a definition is separated by a comma ","

    Example:
    1/1/2,3 means 3 definitions:
    - Definition 1 has only 1 hint: 1
    - Definition 2 has only 1 hint: 1
    - Definition 3 has 2 hints: 2 and 3
    """    

    @staticmethod
    def load(file: str) -> Grid :
        """
        Loads the file into memory and returns a grid

        @param str file to load

        @return Grid
        """

        # Load the file as a stream
        with open(file, "r+") as handle:
            columnHints = handle.readline().strip().split("/")
            rowHints = handle.readline().strip().split("/")
        
        # Create a grid
        grid = Grid(len(rowHints), len(columnHints))

        # For each rowHint, add the hints
        for rowIndex, rowHint in enumerate(rowHints):
            for hint in rowHint.split(','):
                grid.getRowZone(rowIndex).addHint(int(hint))

        # For each columnHint, add the hints
        for columnIndex, columnHint in enumerate(columnHints):
            for hint in columnHint.split(','):
                grid.getColumnZone(columnIndex).addHint(int(hint))
        
        return grid