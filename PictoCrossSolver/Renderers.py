import sys
import logging
from typing import List

from PictoCrossSolver.Elements import Puzzle

class PuzzleRenderer:
    """
    The renderers attach to a puzzle and allows a puzzle to be printed to strings.
    """

    def __init__(self, puzzle: Puzzle):

        # Save the puzzle for later use
        self._puzzle = puzzle

        # Pre-render hints as they would never change
        # x hints are for each row Zone or range(0, len(puzzle.getRowZones())
        self._rowHints = []
        for Zone in puzzle.getRowZones():
            self._rowHints.append(" ".join(str(hint) for hint in Zone.getHints()))

        # Pre-render hints as they would never change
        # Column hints are for each line of hints or range(0, max(len(Zone.getHints) for Zone in puzzle.getColumnZones()))
        self._columnHints = []
        maxColumnHints = max(len(Zone.getHints()) for Zone in puzzle.getColumnZones())
        for columnRow in range(0, maxColumnHints):
            columnHint = ""
            for Zone in puzzle.getColumnZones():
                
                # Only print hints that match the row, they should be printed in ascending padding like
                # 1
                # 1 2 2
                # 2 3 3
                if maxColumnHints - len(Zone.getHints()) <= columnRow:
                    columnHint += str(Zone.getHints()[len(Zone.getHints()) + columnRow - maxColumnHints]).center(3)
                else:
                    columnHint += "   "
            self._columnHints.append(columnHint)
        
        # Pad the xhints and yhints with proper spacing based on largest xHints
        maxRowHintSize = max([max(len(hint) for hint in self._rowHints), 5])
        for index, hint in enumerate(self._rowHints):
            self._rowHints[index] = hint.rjust(maxRowHintSize) + " |"
        
        # Prepare a pipe only spacer
        self._pipeOnlySpacer = maxRowHintSize * " " + " |"
        
        # Recalculate because we added the pipe
        maxRowHintSize = max([max(len(hint) for hint in self._rowHints), 5])
        for index, hint in enumerate(self._columnHints):
            self._columnHints[index] = maxRowHintSize * " " + hint

    
    def render(self) -> List[str]:
        """
        Renders the currently attached puzzle to strings
        """

        results = []

        # Render each _yHint
        for hintRow in self._columnHints:
            results.append(hintRow)
        
        # Print the separator
        results.append(max(len(hint) for hint in self._columnHints) * "-")
        
        # Render each _xHint and corresponding zone
        for index, hintRow in enumerate(self._rowHints):
            render = hintRow
            zone = self._puzzle.getRowZone(index)
            for mark in zone.getMarks():
                if mark.isFilled():
                    render += " " + u'\u2588' + " "
                elif mark.isCrossed():
                    render += " X "
                else:
                    render += "   "
            results.append(render)
            results.append(self._pipeOnlySpacer)
        
        return results

class ConsoleRenderer:
    """
    The renderers attach to a puzzle and allows a puzzle to be printed. Only a 
    ConsoleRenderer exists for now.
    """

    def __init__(self, puzzle: Puzzle):

        # Save the puzzle for later use
        self._puzzle = puzzle

        # Pre-render hints as they would never change
        # x hints are for each row Zone or range(0, len(puzzle.getRowZones())
        self._rowHints = []
        for Zone in puzzle.getRowZones():
            self._rowHints.append(" ".join(str(hint) for hint in Zone.getHints()))

        # Pre-render hints as they would never change
        # Column hints are for each line of hints or range(0, max(len(Zone.getHints) for Zone in puzzle.getColumnZones()))
        self._columnHints = []
        maxColumnHints = max(len(Zone.getHints()) for Zone in puzzle.getColumnZones())
        for columnRow in range(0, maxColumnHints):
            columnHint = ""
            for Zone in puzzle.getColumnZones():
                
                # Only print hints that match the row, they should be printed in ascending padding like
                # 1
                # 1 2 2
                # 2 3 3
                if maxColumnHints - len(Zone.getHints()) <= columnRow:
                    columnHint += str(Zone.getHints()[len(Zone.getHints()) + columnRow - maxColumnHints]).center(3)
                else:
                    columnHint += "   "
            self._columnHints.append(columnHint)
        
        # Pad the xhints and yhints with proper spacing based on largest xHints
        maxRowHintSize = max([max(len(hint) for hint in self._rowHints), 5])
        for index, hint in enumerate(self._rowHints):
            self._rowHints[index] = hint.rjust(maxRowHintSize) + " |"
        
        # Prepare a pipe only spacer
        self._pipeOnlySpacer = maxRowHintSize * " " + " |"
        
        # Recalculate because we added the pipe
        maxRowHintSize = max([max(len(hint) for hint in self._rowHints), 5])
        for index, hint in enumerate(self._columnHints):
            self._columnHints[index] = maxRowHintSize * " " + hint

    
    def render(self):
        """
        Renders the currently attached puzzle to the logger
        """

        # Render each _yHint
        for hintRow in self._columnHints:
            logging.getLogger("changes").info(hintRow)
        
        # Print the separator
        logging.getLogger("changes").info(max(len(hint) for hint in self._columnHints) * "-")
        
        # Render each _xHint and corresponding zone
        for index, hintRow in enumerate(self._rowHints):
            render = hintRow
            zone = self._puzzle.getRowZone(index)
            for mark in zone.getMarks():
                if mark.isFilled():
                    render += " " + u'\u2588' + " "
                elif mark.isCrossed():
                    render += " X "
                else:
                    render += "   "
            logging.getLogger("changes").info(render)
            logging.getLogger("changes").info(self._pipeOnlySpacer)

class SolutionRenderer:
    """
    This renderer transforms a Puzzle into a list of strings with each
    mark represented by a single character
    """

    def __init__(self, puzzle: Puzzle):

        # Save the puzzle for later use
        self._puzzle = puzzle

    
    def render(self) -> List[str]:
        """
        Renders the currently attached puzzle to the logger

        @param TextIOWrapper file to output the puzzle solution to
        """

        # Render each row mark by mark
        results = []
        for rowZone in self._puzzle.getRowZones():
            rowStr = ""
            for mark in rowZone.getMarks():
                if mark.isFilled():
                    rowStr += u'\u2588'
                elif mark.isCrossed():
                    rowStr += "X"
                else:
                    rowStr += " "
            results.append(rowStr)
        
        return results