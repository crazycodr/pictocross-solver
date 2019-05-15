from typing import List
import re
from PictoCrossSolver.Elements import Mark, ZoneType, Zone, Puzzle, PuzzleChange, PuzzleChangeAction
from PictoCrossSolver.Helpers import HintPositionner

class Strategy:

    def apply(self, puzzle: Puzzle) -> List[PuzzleChange]:
        pass


class ChangeUsingHintPositionner(Strategy):
    """
    Searches for hints in the puzzle that can be set without a doubt based on current
    hint setup vs mark status. Uses the HintPositionner helper to figure out where
    each hint can be set without a doubt.
    """
    
    def apply(self, puzzle: Puzzle) -> List[PuzzleChange]:
        """
        Applies the logic and returns changes to apply.
        """
        changes = []

        # Gather the changes
        for zoneIndex, zone in enumerate(puzzle.getRowZones()):
            changes += self.applyOnZone(ZoneType.ROW, zone, zoneIndex)
        for zoneIndex, zone in enumerate(puzzle.getColumnZones()):
            changes += self.applyOnZone(ZoneType.COLUMN, zone, zoneIndex)
        
        # Return the changes
        return changes
    
    def applyOnZone(self, zoneType: ZoneType, zone: Zone, zoneIndex: int) -> List[PuzzleChange]:
        """
        Applies the strategy on a specific zone receiving the type and the zone

        @param ZoneType zoneType of the zone
        @param Zone zone to apply to
        @param int zoneIndex of the zone in the puzzle for that type

        @return List[PuzzleChange] generated for this zone
        """

        # Prepare the indexes to fill and indexes to cross
        indexesToFill = []
        indexesToCross = []
        hintPositions = HintPositionner.position(zone)
        for markIndex, hintPosition in enumerate(hintPositions):

            # If the hintPosition is a number and corresponding mark is ambiguous, add to indexesToFill
            if re.match("\d", hintPosition) and zone.getMark(markIndex).isAmbiguous():
                indexesToFill.append(markIndex)

            # If the hintPosition is a x and corresponding mark is ambiguous, add to indexesToCross
            elif hintPosition == "x" and zone.getMark(markIndex).isAmbiguous():
                indexesToCross.append(markIndex)

        # Generate all the changes
        changes = []

        # Start with indexes to fill
        previousSlice = None
        for index in indexesToFill:

            # If there is a previous slice, the next slice starts at the end of the previous
            if previousSlice != None and previousSlice.stop == index:
                previousSlice = slice(previousSlice.start, index + 1)
            elif previousSlice != None and previousSlice.stop != index:
                changes.append(PuzzleChange(zoneType, zoneIndex, previousSlice, PuzzleChangeAction.FILL))
                previousSlice = slice(index, index + 1)
            else:
                previousSlice = slice(index, index + 1)
        
        # Add the last change as the previousSlice once we are done looping
        if previousSlice != None:
            changes.append(PuzzleChange(zoneType, zoneIndex, previousSlice, PuzzleChangeAction.FILL))

        # Then do indexes to cross
        previousSlice = None
        for index in indexesToCross:

            # If there is a previous slice, the next slice starts at the end of the previous
            if previousSlice != None and previousSlice.stop == index:
                previousSlice = slice(previousSlice.start, index + 1)
            elif previousSlice != None and previousSlice.stop != index:
                changes.append(PuzzleChange(zoneType, zoneIndex, previousSlice, PuzzleChangeAction.CROSS))
                previousSlice = slice(index, index + 1)
            else:
                previousSlice = slice(index, index + 1)
        
        # Add the last change as the previousSlice once we are done looping
        if previousSlice != None:
            changes.append(PuzzleChange(zoneType, zoneIndex, previousSlice, PuzzleChangeAction.CROSS))
        
        return changes