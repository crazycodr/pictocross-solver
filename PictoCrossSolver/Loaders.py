import PictoCrossSolver.PictoCross

class TextLoader:

    @staticmethod
    def load(file: str) -> PictoCrossSolver.PictoCross.Grid :

        # Load the file as a stream
        with open(file, "r+") as handle:
            columnHints = handle.readline().strip().split("/")
            rowHints = handle.readline().strip().split("/")
        
        # Create a grid
        grid = PictoCrossSolver.PictoCross.Grid(len(rowHints), len(columnHints))

        # For each rowHint, add the hints
        for rowIndex, rowHint in enumerate(rowHints):
            for hint in rowHint.split(','):
                grid.getRowZone(rowIndex).addHint(int(hint))

        # For each columnHint, add the hints
        for columnIndex, columnHint in enumerate(columnHints):
            for hint in columnHint.split(','):
                grid.getColumnZone(columnIndex).addHint(int(hint))
        
        return grid