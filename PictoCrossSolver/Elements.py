from typing import List

class Mark:
    """
    Defines a square that can be filled, crossed or ambiguous to the user.
    Solvers will lookup and change marks to solve the puzzle
    """

    def __init__(self):
        self._value = None
    
    def isFilled(self) -> bool:
        """
        Returns if the mark is filled or not

        @return bool
        """

        return self._value == True
    
    def isCrossed(self) -> bool:
        """
        Returns if the mark is crossed or not

        @return bool
        """

        return self._value == False
    
    def isAmbiguous(self) -> bool:
        """
        Returns if the mark is ambiguous or not

        @return bool
        """

        return self._value == None
    
    def setFilled(self):
        """
        Sets the mark to a filled state

        @return bool
        """

        self._value = True
    
    def setCrossed(self):
        """
        Sets the mark to a crossed state

        @return bool
        """
        
        self._value = False

    def setAmbiguous(self):
        """
        Sets the mark to an ambiguous state

        @return bool
        """
        
        self._value = None


class Zone:
    """
    Defines a list of squares that can be filled, crossed or ambiguous to the user.
    Zones contain hints and marks. Zones can contain marks from other zones such as
    when a zone crosses another zone (column vs row).
    Solvers will mostly work off a zone.
    """

    def __init__(self):
        self._marks = []
        self._hints = []
    
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


class Grid:
    """
    Defines the complete puzzle that must be solved.
    Contains a list of zones that act as columns and rows.
    Grids cannot be changed once they are created. They are automatically 
    initialized to a certain size of rows and columns and all marks are
    set to ambiguous.
    """

    def __init__(self, rows: int, columns: int):
        """
        Creates a grid

        @param int rows in the grid
        @param int columns in the grid
        """

        # Create the initial zones and marks
        self._rowZones = []
        self._columnZones = []

        # Fill the zones
        for x in range(0, rows):
            self._rowZones.append(Zone())

        for y in range(0, columns):
            self._columnZones.append(Zone())
        
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
        Returns the row zones of the grid

        @return List[Zone]
        """

        return self._rowZones
    
    def getColumnZones(self) -> List[Zone]:
        """
        Returns the column zones of the grid

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