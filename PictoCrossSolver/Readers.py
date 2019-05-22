from typing import List
from PictoCrossSolver.Renderers import ConsoleRenderer
from PictoCrossSolver.Elements import Puzzle, ZoneType, Zone

class TextPuzzleReader:
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
    def load(file: str) -> Puzzle :
        """
        Loads the file into memory and returns a puzzle

        @param str file to load

        @return Puzzle
        """

        # Load the file as a stream
        with open(file, "r+") as handle:
            columnHints = handle.readline().strip().split("/")
            rowHints = handle.readline().strip().split("/")
        
        # Create a puzzle
        puzzle = Puzzle(len(rowHints), len(columnHints))

        # For each rowHint, add the hints
        for rowIndex, rowHint in enumerate(rowHints):
            for hint in rowHint.split(','):
                puzzle.getRowZone(rowIndex).addHint(int(hint))

        # For each columnHint, add the hints
        for columnIndex, columnHint in enumerate(columnHints):
            for hint in columnHint.split(','):
                puzzle.getColumnZone(columnIndex).addHint(int(hint))
        
        return puzzle

class TextSolutionReader:
    """
    Used to load solutions from text files containing a
    pre-rendered puzzle
    """    

    @staticmethod
    def load(file: str) -> List[str] :
        """
        Loads the file into memory and returns a list of strings

        @param str file to load

        @return List[str]
        """

        with open(file, 'r') as solutionStream:
            solution = solutionStream.readlines()
            for index, line in enumerate(solution):
                solution[index] = line.strip()
        
        return solution
    
class PuzzleBuilder:

    def buildFromConsole(self) -> Puzzle:

        # Read from the console until user is satisfied
        # First step is to read all columns, each number entered generates a hint for current column or row
        # If you don't enter anything, we go to next column or row. 
        # If you don't enter any hint, it switches to rows when in columns or ends the puzzle builder

        # First ask for the size and generate the puzzle base
        x = None
        y = None
        while x == None:
            try:
                x = int(input(f'Please enter number of columns: '))
            except:
                print('Invalid number')

        while y == None:
            try:
                y = int(input(f'Please enter number of rows: '))
            except:
                print('Invalid number')

        puzzle = Puzzle(x, y)

        # Next ask for each hints for each zone
        zoneType = ZoneType.COLUMN
        zoneIndex = 0
        building = True
        while building:

            # Get the zone to work with
            currentZone = puzzle.getZone(zoneType, zoneIndex)

            # Ask for next hint, if hint is empty, move to next zone
            try:
                hint = input(f'Please enter next hint for {zoneType.name} #{zoneIndex + 1}: ')
                currentZone.addHint(int(hint))
            except ValueError:
                zoneIndex += 1
                if zoneType == ZoneType.COLUMN and len(puzzle.getColumnZones()) == zoneIndex:
                    zoneType = ZoneType.ROW
                    zoneIndex = 0
                elif zoneType == ZoneType.ROW and len(puzzle.getRowZones()) == zoneIndex:
                    building = False

            # Print the puzzle as it is right now
            renderer = ConsoleRenderer(puzzle)
            renderer.render()

        return puzzle