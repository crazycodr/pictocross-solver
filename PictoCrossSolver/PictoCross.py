#######################################################################################
#
# The grid class represents a picto cross grid with hints and values that can be
# in 3 possible states: True, False and None
# 
# The grid class works with scalar object based values so that references from
# other objects persist instead of scalar types that get copied back and forth.
# Other important classes related to a pictocross grid are located in this file.
#
# - Zone: A set of Marks representing a row or column of a pictocross Grid
# - Mark: A single square in the pictocross Grid with 3 possible states
#
# Important terms:
#
# - Hint: A hint is a number that helps the use solve the puzzle, many hint can be
#           presented per Zone and they help solve the puzzle
# - Value: A value is a 3 state number stating what is the state of a square in the
#           grid. These values are represented by Mark objects.
#
# Important organization concepts
#
# - Zones and Marks are predefined and automatically attached together
# - Zones are computed on the fly on Zones. Because Marks change a lot and
#           zones are all about contiguous sets, you should not work with Zones on a
#           static basis but always on a dynamic basis.
#
#######################################################################################

from typing import List

class Mark:

    def __init__(self):
        self._value = None
    
    def isFilled(self) -> bool:
        return self._value == True
    
    def isCrossed(self) -> bool:
        return self._value == False
    
    def isAmbiguous(self) -> bool:
        return self._value == None
    
    def setFilled(self):
        self._value = True
    
    def setCrossed(self):
        self._value = False

    def setAmbiguous(self):
        self._value = None


class Zone:

    def __init__(self):
        self._marks = []
        self._hints = []
    
    def addHint(self, hint: int):
        self._hints.append(hint)
    
    def getHints(self) -> List[int]:
        return self._hints
    
    def addMark(self, mark: Mark):
        self._marks.append(mark)
    
    def getMark(self, index: int) -> Mark:
        return self._marks[index]
    
    def getMarks(self) -> List[Mark]:
        return self._marks


class Grid:

    def __init__(self, rows: int, columns: int):

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
    
    def getRowZones(self) -> list:
        return self._rowZones
    
    def getColumnZones(self) -> list:
        return self._columnZones
    
    def getRowZone(self, index: int) -> Zone:
        return self._rowZones[index]
    
    def getColumnZone(self, index: int) -> Zone:
        return self._columnZones[index]