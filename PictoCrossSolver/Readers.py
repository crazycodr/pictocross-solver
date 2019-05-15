from typing import List
from PictoCrossSolver.Elements import Puzzle

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