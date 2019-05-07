import logging
from functools import reduce
from typing import List

from PictoCrossSolver.Elements import Zone, Mark
from PictoCrossSolver.Analyzers import HintCrossoverRegexAnalyzer

class HintFitsInEstimatedZoneSolver:
    """
    Fills marks in the zone that will automatically fit in that zone because the hint
    is long enough to be present from whichever side you can start.
    """

    @staticmethod
    def solve(zone: Zone) -> bool:
        """
        Applies the logic and returns true if something was altered

        @param Zone zone to apply logic to

        @return bool
        """

        for hintIndex, hint in enumerate(zone.getHints()):

            # First get the zones affected by the matcher
            markSlice = HintCrossoverRegexAnalyzer.analyze(zone, hintIndex)
            if markSlice == None:
                return False
            marks = zone.getMarks()[markSlice]

            # If there are no zones, print no change
            if len(marks) == 0:
                logging.getLogger(None).debug(f"No valid zone for hint #{hintIndex}: {hint}")
                continue
            else:
                logging.getLogger(None).debug(f"Found {len(marks)} zones that could be affected by hint #{hintIndex}: {hint}")

            # Calculate the length of the zone
            zoneLength = len(marks)

            # Figure out how many marks are automatically filled and how many must be kept as safe marks
            minimumSafeMarks = zoneLength - hint
            minimumFilledMarks = zoneLength - minimumSafeMarks * 2

            # If the zone has too many values, we can't plot any portion of hint
            if minimumFilledMarks <= 0:
                logging.getLogger(None).debug("Not enough fillable marks to apply")
                continue

            # If the minimumFilledMarks items are already marked, don't alter
            marksAffected = marks[slice(minimumSafeMarks, minimumSafeMarks + minimumFilledMarks)]
            if len(marksAffected) == 0:
                logging.getLogger(None).debug("Not enough marks found")
                continue
            if reduce(lambda x, y: x and y, (mark.isFilled() for mark in marksAffected), True):
                logging.getLogger(None).debug("Marks already filled")
                continue
            
            # Fill all zones
            for zone in marksAffected:
                zone.setFilled()
            
            # return true to break out of the loop, we only want one change to be applied
            return True


class CrossAmbiguousZonesInCompletedHintsSolver:
    """
    Cross cells in the marks that should be crossed because the hint is complete.
    """

    @staticmethod
    def solve(zone: Zone) -> bool:
        """
        Applies the logic and returns true if something was altered

        @param Zone zone to apply logic to

        @return bool
        """

        # Calculate the number of marked zones vs hints
        filledMarks = list((zone for zone in zone.getMarks() if zone.isFilled()))
        totalHintsToFill = reduce(lambda x, y: x + y, zone.getHints())
        ambiguousMarks = list(zone for zone in zone.getMarks() if zone.isAmbiguous())

        # If all marks are there and there are no ambiguous zone, quit
        if len(filledMarks) != totalHintsToFill or len(ambiguousMarks) == 0:
            logging.getLogger(None).debug("No ambiguous marks to cross or hint not complete yet")
            return False

        # Cross all ambiguous marks
        for zone in ambiguousMarks:
            zone.setCrossed()
        
        return True

class HintExpandsFilledMarksFromEdgeInEstimatedZoneSolver:
    """
    Fills marks in the zone that should be filled because there is filled
    mark on the edge of the estimated zone.
    """

    @staticmethod
    def solve(zone: Zone) -> bool:
        """
        Applies the logic and returns true if something was altered

        @param Zone zone to apply logic to

        @return bool
        """

        for hintIndex, hint in enumerate(zone.getHints()):

            # First get the zones affected by the matcher
            markSlice = HintCrossoverRegexAnalyzer.analyze(zone, hintIndex)
            if markSlice == None:
                return False
            marks = zone.getMarks()[markSlice]

            # If there are no zones, print no change
            if len(marks) == 0:
                logging.getLogger(None).debug(f"No valid zone for hint #{hintIndex}: {hint}")
                continue
            else:
                logging.getLogger(None).debug(f"Found {len(marks)} zones that could be affected by hint #{hintIndex}: {hint}")

            # Find out if the there are filled marks in either edges
            if marks[0].isFilled():
                edgeIndex = 0
                endIndex = hint
            elif marks[len(marks) - 1].isFilled():
                edgeIndex = len(marks) - hint
                endIndex = len(marks)
            else:
                logging.getLogger(None).debug(f"No edge detected for hint #{hintIndex}: {hint}")
                continue

            # Fill all marks from the edge to edge + hint
            hasChanges = False
            for mark in marks[slice(edgeIndex, endIndex, 1)]:
                if not mark.isFilled():
                    hasChanges = True
                    mark.setFilled()
            
            return hasChanges

class CrossMarksOutsideOfSolvedHintZonesSolver:
    """
    Crosses marks just outside of a zone that perfectly matched by a hint
    There can be no ambiguity or filled marks beside another hint that is fully compliant
    """

    @staticmethod
    def solve(zone: Zone) -> bool:
        """
        Applies the logic and returns true if something was altered

        @param Zone zone to apply logic to

        @return bool
        """

        for hintIndex, hint in enumerate(zone.getHints()):

            # First get the zones affected by the matcher
            markSlice = HintCrossoverRegexAnalyzer.analyze(zone, hintIndex)
            if markSlice == None:
                return False
            marks = zone.getMarks()[markSlice]

            # If there are no zones, print no change
            if len(marks) == 0:
                logging.getLogger(None).debug(f"No valid zone for hint #{hintIndex}: {hint}")
                continue
            else:
                logging.getLogger(None).debug(f"Found {len(marks)} zones that could be affected by hint #{hintIndex}: {hint}")

            # Extract the filled marks
            filledMarks = list(mark for mark in marks if mark.isFilled())

            # Find out if the hint is fulfilled
            if len(filledMarks) != hint:
                logging.getLogger(None).debug(f"Hint is not fulfilled yet for #{hintIndex}: {hint}")
                continue

            # Find the marks just around this hint and cross them
            previousMark = None
            firstMark = filledMarks[0]
            lastMark = filledMarks[len(filledMarks) - 1]
            nextMark = None
            lastIteratedMark = None
            saveNextMark = False
            for mark in zone.getMarks():
                
                # If we have saveNextMark turned on, save the current mark as the nextMark
                if saveNextMark == True:
                    nextMark = mark
                    break

                # If we found the first or last mark of the zone that matches the hint
                if firstMark is mark:
                    # Save the last iterated mark as the previousMark
                    previousMark = lastIteratedMark

                elif lastMark is mark:
                    # Flag that we must keep the next mark as nextMark
                    saveNextMark = True

                # Keep track of the last mark iterated on in case the next is firstMark
                lastIteratedMark = mark
            
            # Cross the found marks
            hasChanges = False
            if previousMark != None and previousMark.isAmbiguous():
                hasChanges = True
                previousMark.setCrossed()
            if nextMark != None and nextMark.isAmbiguous():
                hasChanges = True
                nextMark.setCrossed()
            
            return hasChanges