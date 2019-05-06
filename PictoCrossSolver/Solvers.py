import math
from functools import reduce
from typing import List

from PictoCrossSolver.PictoCross import Zone, Mark
import PictoCrossSolver.Analyzers

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
            regularExpression = PictoCrossSolver.Analyzers.RegexBuilder.getRegularExpressions(zone.getHints())[hintIndex]
            serializedZone = PictoCrossSolver.Analyzers.ZoneSerializer.serialize(zone)
            marks = zone.getMarks()[PictoCrossSolver.Analyzers.ZoneAnalyzer.analyze(serializedZone, regularExpression, hintIndex)]

            # If there are no zones, print no change
            if len(marks) == 0:
                print(f"No valid zone for hint #{hintIndex}: {hint}")
                continue
            else:
                print(f"Found {len(marks)} zones that could be affected by hint #{hintIndex}: {hint} in {serializedZone}")

            # Calculate the length of the zone
            zoneLength = len(marks)

            # Figure out how many marks are automatically filled and how many must be kept as safe marks
            minimumSafeMarks = zoneLength - hint
            minimumFilledMarks = zoneLength - minimumSafeMarks * 2

            # If the zone has too many values, we can't plot any portion of hint
            if minimumFilledMarks <= 0:
                print("Not enough fillable marks to apply")
                continue

            # If the minimumFilledMarks items are already marked, don't alter
            marksAffected = marks[slice(minimumSafeMarks, minimumSafeMarks + minimumFilledMarks)]
            if len(marksAffected) == 0:
                print("Not enough marks found")
                continue
            if reduce(lambda x, y: x and y.isFilled(), marksAffected):
                print("Marks already filled")
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
            print("No ambiguous marks to cross or hint not complete yet")
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
            regularExpression = PictoCrossSolver.Analyzers.RegexBuilder.getRegularExpressions(zone.getHints())[hintIndex]
            serializedZone = PictoCrossSolver.Analyzers.ZoneSerializer.serialize(zone)
            marks = zone.getMarks()[PictoCrossSolver.Analyzers.ZoneAnalyzer.analyze(serializedZone, regularExpression, hintIndex)]

            # If there are no zones, print no change
            if len(marks) == 0:
                print(f"No valid zone for hint #{hintIndex}: {hint}")
                continue
            else:
                print(f"Found {len(marks)} zones that could be affected by hint #{hintIndex}: {hint} in {serializedZone}")

            # Find out if the there are filled marks in either edges
            if marks[0].isFilled():
                edgeIndex = 0
                endIndex = hint
            elif marks[len(marks) - 1].isFilled():
                edgeIndex = len(marks) - hint
                endIndex = len(marks)
            else:
                print(f"No edge detected for hint #{hintIndex}: {hint} in {serializedZone}")
                continue

            # Fill all marks from the edge to edge + hint
            hasChanges = False
            for mark in marks[slice(edgeIndex, endIndex, 1)]:
                if not mark.isFilled():
                    hasChanges = True
                    mark.setFilled()
            
            # If there are changes return
            if hasChanges:
                return True