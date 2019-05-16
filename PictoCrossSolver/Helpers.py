from typing import List
from functools import reduce
import re
from PictoCrossSolver.Elements import Puzzle, PuzzleChange, Zone

class HintPositionner:

    def __init__(self):
        self._generatedPatternCache = {}
        self._applicablePatternCache = {}
        self._reducedPatternCache = {}
    
    def position(self, zone: Zone) -> []:
        """
        Positions the hints using a forward generation algorithm
        that create all potential positions for each hint using the zone.
        
        Then, it serializes the zone into a regular expression and applies
        it to all positions to find which match the current zone setup.

        Finaly, it summarizes the valid hint positions into potential
        marks that you could turn on or bar. Each mark of the zone is returned
        in a list using either a number that matches the hint that can be set
        there or a "X" meaning nothing can go here or "?" meaning this is
        still ambiguous.
        """
        patterns = self.generatePatternsForHint(zone.getHints(), len(zone.getMarks()), 0, self.getApplicablePatternExpression(zone))
        return self.reducePatterns(zone, patterns)
    
    def reducePatterns(self, zone: Zone, patterns: List[str]) -> []:
        """
        Reduce the patterns to a single pattern and return the final pattern as a list
        """
        # Return the cached version
        reducedPatternHash = hash(frozenset({
            "size": len(zone.getMarks()),
            "hints": tuple(zone.getHints()),
            "patterns": tuple(patterns)
        }.items()))
        if reducedPatternHash in self._reducedPatternCache:
            return self._reducedPatternCache[reducedPatternHash]

        # Save the results to the cache
        self._reducedPatternCache[reducedPatternHash] = list(reduce(self.patternReducer, patterns, "*" * len(zone.getMarks())))
        return self._reducedPatternCache[reducedPatternHash]
    
    def getApplicablePatternExpression(self, zone: Zone) -> str:
        """
        Creates a filter pattern to be used against patterns to exclude
        invalid patterns off the bat.
        """
        # Generate regular expression from zone status
        regularExpression = ""
        for mark in zone.getMarks():
            if mark.isFilled():
                regularExpression += "[0-9]"
            elif mark.isCrossed():
                regularExpression += "x"
            else:
                regularExpression += "."
        
        return regularExpression
    
    def patternReducer(self, a: str, b: str) -> str:
        """
        Reduces pattern a and pattern b into one final pattern.
        Each letter in the pattern is compared with the letter of the other pattern to 
        find the proper output char.

        * vs Anything = Anything (* is the initial unset char)
        ? vs Anything = ? (? means ambiguous by nature)
        Same vs Same = Same (Same here can be a number, X, ? or *)
        Diff vs Diff = ? (Different chars yield ambiguity except if one of the char is *)
        """
        r = list("*" * len(a))
        for charIndex in range(0, len(a)):

            charA = a[charIndex]
            charB = b[charIndex]
            
            # If both chars are the same, results in same
            if charA == charB:
                r[charIndex] = charA
            
            # If charA or charB is unset, use the other
            elif charA == "*":
                r[charIndex] = charB
            elif charB == "*":
                r[charIndex] = charA
            
            # If charA or charB is ambiguous, use ambiguous
            elif charA == "?" or charB == "?":
                r[charIndex] = "?"
            
            # If charA and charB are not the same, use ambiguous
            else:
                r[charIndex] = "?"

        return "".join(r)
        
    def generatePatternsForHint(self, hints: List[int], space: int, hintIndex: int, filteringPattern: str) -> List[str]:
        """
        Used to generate all patterns for a hint and generate all subpatterns
        of following hints calling the same method in a recursive way.

        Example 1:
        zone = (4,4) on 10 marks
        Level 0 call (zone, 0, "")
            "0000x" -> Level 1 call (zone, 1, "0000x")
                returns ["0000x0000x", "0000xx0000"]
            "x0000x" -> Level 1 call (zone, 1, "x0000x")
                returns ["x0000x0000"]
            returns ["0000x0000x", "0000xx0000", "x0000x0000"]

        Example 2:
        zone = (2,2,2) on 10 marks
        Level 0 call (zone, 0, "")
            "00x" -> Level 1 call (zone, 1, "00x")
                "00x00x" -> Level 2 call (zone, 2, "00x00x")
                    returns ["00x00x00xx", "00x00xx00x", "00x00xxx00"]
                "00x00xx" -> Level 2 call (zone, 2, "00x00xx")
                    returns ["00x00xx00x", "00x00xxx00"]
                "00x00xxx" -> Level 2 call (zone, 2, "00x00xxx")
                    returns ["00x00xxx00"]
                returns ["00x00x00xx", "00x00xx00x", "00x00xxx00", "00x00xx00x", "00x00xxx00", "00x00xxx00"]
            "x00x" -> Level 1 call (zone, 1, "x00x")
                "x00x00x" -> Level 2 call (zone, 2, "x00x00x")
                    returns ["x00x00x00x", "x00x00xx00"]
                "x00x00xx" -> Level 2 call (zone, 2, "x00x00xx")
                    returns ["x00x00xx00"]
                returns ["x00x00x00x", "x00x00xx00", "x00x00xx00"]
            "xx00x" -> Level 1 call (zone, 1, "xx00x")
                "xx00x00x" -> Level 2 call (zone, 2, "xx00x00x")
                    returns ["xx00x00x00"]
                returns ["xx00x00x00"]
            returns ["00x00x00xx", "00x00xx00x", "00x00xxx00", "00x00xx00x", "00x00xxx00", "00x00xxx00", "x00x00x00x", "x00x00xx00", "x00x00xx00", "xx00x00x00"]
        """
        # Return the cached version of all patterns
        zoneCacheHash = hash(frozenset({
            "space": space,
            "hints": tuple(hints),
            "hintIndex": hintIndex
        }.items()))
        zoneCacheFilteredHash = hash(frozenset({
            "space": space,
            "hints": tuple(hints),
            "hintIndex": hintIndex,
            "filterPattern": filteringPattern
        }.items()))
        if zoneCacheFilteredHash in self._generatedPatternCache:
            return self._generatedPatternCache[zoneCacheFilteredHash]
        if zoneCacheHash in self._generatedPatternCache:

            # Filter the patterns then update the cache
            patterns = self._generatedPatternCache[zoneCacheHash]
            newPatterns = list(filter(lambda a: re.match(filteringPattern, a), patterns))
            if len(patterns) != len(newPatterns):
                self._generatedPatternCache[zoneCacheFilteredHash] = newPatterns
            return newPatterns

        # Get the hint and next hints and calculate the space needed so this iteration does not push over
        hint = hints[0]
        nextHints = hints[slice(1, len(hints))]
        nextHintSpace = max(0, reduce(lambda a, b: a + 1 + b, nextHints, 0) - 1)
        spaceAvailable = space - nextHintSpace
        spaceNeeded = hint + (1 if len(nextHints) > 0 else 0)

        # Generate the current patterns
        results = []
        for spacers in range(0, spaceAvailable - spaceNeeded + 1):

            # Create the current pattern
            currentPattern = "x" * spacers
            currentPattern += str(hintIndex) * hint
            currentPattern += "x" if len(nextHints) > 0 else "x" * (spaceAvailable - spaceNeeded - spacers)

            # Generate all sub patterns from it
            if len(nextHints) > 0:
                for generatedSubPattern in self.generatePatternsForHint(nextHints, space - len(currentPattern), hintIndex + 1, ""):
                    results.append(currentPattern + generatedSubPattern)
            else:
                results.append(currentPattern)

        # Cache and return unique patterns using a set
        patterns = newPatterns = list(set(results))
        self._generatedPatternCache[zoneCacheHash] = newPatterns
        if filteringPattern != "":
            newPatterns = list(filter(lambda a: re.match(filteringPattern, a), patterns))
            if len(patterns) != len(newPatterns):
                self._generatedPatternCache[zoneCacheFilteredHash] = newPatterns

        # Return the patterns
        return newPatterns