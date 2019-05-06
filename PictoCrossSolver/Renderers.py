import sys

from PictoCrossSolver.PictoCross import Grid

#######################################################################################
#
# The renderers attach to a grid and allows a grid to be printed. Only a
# ConsoleRenderer exists for now.
#
#######################################################################################

class ConsoleRenderer:

    def __init__(self, grid: Grid):

        # Save the grid for later use
        self._grid = grid

        # Pre-render hints as they would never change
        # x hints are for each row Zone or range(0, len(grid.getRowZones())
        self._rowHints = []
        for Zone in grid.getRowZones():
            self._rowHints.append(" ".join(str(hint) for hint in Zone.getHints()))

        # Pre-render hints as they would never change
        # Column hints are for each line of hints or range(0, max(len(Zone.getHints) for Zone in grid.getColumnZones()))
        self._columnHints = []
        maxColumnHints = max(len(Zone.getHints()) for Zone in grid.getColumnZones())
        for columnRow in range(0, maxColumnHints):
            columnHint = ""
            for Zone in grid.getColumnZones():
                
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

        # Render each _yHint
        for hintRow in self._columnHints:
            print(hintRow)
        
        # Print the separator
        print(max(len(hint) for hint in self._columnHints) * "-")
        
        # Render each _xHint and corresponding zone
        for index, hintRow in enumerate(self._rowHints):
            sys.stdout.write(hintRow)
            zone = self._grid.getRowZone(index)
            for mark in zone.getMarks():
                if mark.isFilled():
                    sys.stdout.write(" " + u'\u2588' + " ")
                elif mark.isCrossed():
                    sys.stdout.write(" X ")
                else:
                    sys.stdout.write(" ? ")
            print("")
            print(self._pipeOnlySpacer)