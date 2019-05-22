from typing import List
from functools import reduce
from enum import Enum


class Mark:
    """
    Defines a square that can be filled, crossed or ambiguous to the user.
    Solvers will lookup and change marks to solve the puzzle
    """

    def __init__(self):
        self._value = PuzzleChangeAction.AMBIGUOUS
    
    def getStatus(self) -> 'PuzzleChangeAction':
        """
        Returns the status of the mark
        """
        return self._value
    
    def setStatus(self, newStatus: 'PuzzleChangeAction') -> 'PuzzleChangeAction':
        """
        Sets the status of the mark
        """
        self._value = newStatus
    
    def isFilled(self) -> bool:
        """
        Returns if the mark is filled or not

        @return bool
        """
        return self._value == PuzzleChangeAction.FILL
    
    def isCrossed(self) -> bool:
        """
        Returns if the mark is crossed or not

        @return bool
        """
        return self._value == PuzzleChangeAction.CROSS
    
    def isAmbiguous(self) -> bool:
        """
        Returns if the mark is ambiguous or not

        @return bool
        """
        return self._value == PuzzleChangeAction.AMBIGUOUS
    
    def setFilled(self):
        """
        Sets the mark to a filled state

        @return bool
        """
        self._value = PuzzleChangeAction.FILL
    
    def setCrossed(self):
        """
        Sets the mark to a crossed state

        @return bool
        """
        self._value = PuzzleChangeAction.CROSS

    def setAmbiguous(self):
        """
        Sets the mark to an ambiguous state

        @return bool
        """
        self._value = PuzzleChangeAction.AMBIGUOUS


class ZoneType(Enum):
    ROW = 0
    COLUMN = 1
    

class Zone:
    """
    Defines a list of squares that can be filled, crossed or ambiguous to the user.
    Zones contain hints and marks. Zones can contain marks from other zones such as
    when a zone crosses another zone (column vs row).
    Solvers will mostly work off a zone.
    """

    def __init__(self, zoneType: ZoneType, zoneIndex: int):
        self._marks = []
        self._hints = []
        self._zoneType = zoneType
        self._zoneIndex = zoneIndex
    
    def getZoneType(self) -> ZoneType:
        """
        Returns the zone type of the zone

        @return ZoneType
        """
        return self._zoneType
    
    def getZoneIndex(self) -> int:
        """
        Returns the zone index of the zone

        @return int
        """
        return self._zoneIndex
    
    def addHint(self, hint: int):
        """
        Adds a hint to the Zone

        @param int hint to add
        """
        self._hints.append(hint)
    
    def getHints(self) -> List[int]:
        """
        Returns a list of marks

        @return List[int]
        """
        return self._hints
    
    def addMark(self, mark: Mark):
        """
        Adds a mark to the zone

        @param Mark mark to add to the zone
        """
        self._marks.append(mark)
    
    def getMark(self, index: int) -> Mark:
        """
        Returns a specific mark from the zone based on index

        @param int index to return

        @return Mark
        """
        return self._marks[index]
    
    def getMarks(self) -> List[Mark]:
        """
        Returns a list of marks from the zone

        @return List[Mark]
        """
        return self._marks
    
    def isComplete(self) -> bool:
        """
        Checks if all marks are filled or crossed.

        @return bool
        """
        return reduce(lambda a, b: a and b, map(lambda a: not a.isAmbiguous(), self.getMarks()), True)


class PuzzleChangeAction(Enum):
    AMBIGUOUS = None
    FILL = True
    CROSS = False


class PuzzleChange:
    """
    Defines a change set in a puzzle. Used for replayability but also for 
    better validation. ChangeSets are indicators of zones and slices of
    zones and actions such as "fill" or "cross"
    """

    def __init__(self, zoneType: int, zoneIndex: int, zoneSlice: slice, action: PuzzleChangeAction):
        self._zoneType = zoneType
        self._zoneIndex = zoneIndex
        self._zoneSlice = zoneSlice
        self._action = action
    
    def getZoneType(self) -> int:
        return self._zoneType
    
    def getZoneIndex(self) -> int:
        return self._zoneIndex
    
    def getZoneSlice(self) -> slice:
        return self._zoneSlice
    
    def getAction(self) -> PuzzleChangeAction:
        return self._action


class Puzzle:
    """
    Defines the complete puzzle that must be solved.
    Contains a list of zones that act as columns and rows.
    Puzzles cannot be changed once they are created. They are automatically 
    initialized to a certain size of rows and columns and all marks are
    set to ambiguous.
    """

    def __init__(self, rows: int, columns: int):
        """
        Creates a puzzle

        @param int rows in the puzzle
        @param int columns in the puzzle
        """

        # Create the initial zones and marks
        self._rowZones = []
        self._columnZones = []
        self._puzzleChanges = []

        # Fill the zones
        for x in range(0, rows):
            self._rowZones.append(Zone(ZoneType.ROW, x))

        for y in range(0, columns):
            self._columnZones.append(Zone(ZoneType.COLUMN, y))
        
        # Fill the marks
        for x in range(0, rows):
            rowZone = self._rowZones[x]
            for y in range(0, columns):
                columnZone = self._columnZones[y]
                mark = Mark()
                rowZone.addMark(mark)
                columnZone.addMark(mark)
    
    def getRowZones(self) -> List[Zone]:
        """
        Returns the row zones of the puzzle

        @return List[Zone]
        """
        return self._rowZones
    
    def getColumnZones(self) -> List[Zone]:
        """
        Returns the column zones of the puzzle

        @return List[Zone]
        """
        return self._columnZones
    
    def getRowZone(self, index: int) -> Zone:
        """
        Returns a specific row zone based on index

        @param int index of the row to return

        @return Zone
        """
        return self._rowZones[index]
    
    def getColumnZone(self, index: int) -> Zone:
        """
        Returns a specific column zone based on index

        @param int index of the column to return

        @return Zone
        """
        return self._columnZones[index]
    
    def getZones(self) -> List[Zone]:
        """
        Returns all zones, rows or columns

        @return List[Zone]
        """
        return self._columnZones + self._rowZones
    
    def getZone(self, zoneType: ZoneType, zoneIndex: int) -> Zone:
        """
        Returns a specific zone, row or column

        @param ZoneType zonetype to return
        @param int zoneIndex to return

        @return Zone
        """
        if zoneType == zoneType.ROW:
            return self.getRowZone(zoneIndex)
        else:
            return self.getColumnZone(zoneIndex)
    
    def addChange(self, change: PuzzleChange):
        """
        Adds a new change to the puzzle

        @param PuzzleChange change to add to puzzle
        """
        self._puzzleChanges.append(change)
    
    def getChanges(self) -> List[PuzzleChange]:
        """
        Returns all changes

        @return List[PuzzleChange]
        """
        return self._puzzleChanges

    def applyChanges(self) -> 'Puzzle':
        """
        Returns a copy of this Puzzle with changes applied to the marks and no changes
        in store in the Puzzle.
        """

        # Create a copy of self
        puzzleCopy = self.__class__(len(self.getRowZones()), len(self.getColumnZones()))

        # Update the copy's columns by setting the hints
        for columnIndex, columnZone in enumerate(self.getColumnZones()):
            columnZoneCopy = puzzleCopy.getColumnZone(columnIndex)
            for hint in columnZone.getHints():
                columnZoneCopy.addHint(hint)

        # Update the copy's rows by setting the hints
        for rowIndex, rowZone in enumerate(self.getRowZones()):
            rowZoneCopy = puzzleCopy.getRowZone(rowIndex)
            for hint in rowZone.getHints():
                rowZoneCopy.addHint(hint)
            for markIndex, mark in enumerate(rowZone.getMarks()):
                rowZoneCopy.getMark(markIndex).setStatus(mark.getStatus())
        
        # Update the copy's zones by setting the status of marks
        for change in self.getChanges():
            zoneCopy = puzzleCopy.getZone(change.getZoneType(), change.getZoneIndex())
            for mark in zoneCopy.getMarks()[change.getZoneSlice()]:
                mark.setStatus(change.getAction())

        # Return the copy
        return puzzleCopy

    def applyChange(self, change: PuzzleChange) -> 'Puzzle':
        """
        Returns a copy of this Puzzle with changes applied to the marks and no changes
        in store in the Puzzle.
        """

        # Create a copy of self
        puzzleCopy = self.__class__(len(self.getRowZones()), len(self.getColumnZones()))

        # Update the copy's columns by setting the hints
        for columnIndex, columnZone in enumerate(self.getColumnZones()):
            columnZoneCopy = puzzleCopy.getColumnZone(columnIndex)
            for hint in columnZone.getHints():
                columnZoneCopy.addHint(hint)

        # Update the copy's rows by setting the hints
        for rowIndex, rowZone in enumerate(self.getRowZones()):
            rowZoneCopy = puzzleCopy.getRowZone(rowIndex)
            for hint in rowZone.getHints():
                rowZoneCopy.addHint(hint)
            for markIndex, mark in enumerate(rowZone.getMarks()):
                rowZoneCopy.getMark(markIndex).setStatus(mark.getStatus())
        
        # Update the copy's zones by setting the status of marks
        zoneCopy = puzzleCopy.getZone(change.getZoneType(), change.getZoneIndex())
        for mark in zoneCopy.getMarks()[change.getZoneSlice()]:
            mark.setStatus(change.getAction())

        # Return the copy
        return puzzleCopy