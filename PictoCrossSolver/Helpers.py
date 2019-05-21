from typing import List
from functools import reduce
import re
from PictoCrossSolver.Elements import Puzzle, PuzzleChange, ZoneType, Zone
from PictoCrossSolver.Caches import Cache
import hashlib
import logging
from json import JSONDecodeError

class HintPositionner:

    def __init__(self, persistentCache: Cache, volatileCache: Cache):
        self._generatedPatternCache = {}
        self._applicablePatternCache = {}
        self._reducedPatternCache = {}
        self._persistentCache = persistentCache
        self._volatileCache = volatileCache
        self._reductionFullPattern = None
    
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
        patterns = self.generatePatternsForHint(zone.getHints(), len(zone.getMarks()), 0, zone)
        return self.reducePatterns(zone, patterns)
    
    def reducePatterns(self, zone: Zone, patterns: List[str]) -> []:
        """
        Reduce the patterns to a single pattern and return the final pattern as a list
        """
        # Return the cached version
        reducedPatternHash = hash((zone.getZoneType().value, zone.getZoneIndex(), tuple(self.hashString(self.getApplicablePatternExpression(zone)))))
        if self._volatileCache.hasKey(reducedPatternHash):
            return self._volatileCache.retrieve(reducedPatternHash)

        # Generate the reduced pattern
        self._reductionFullPattern = "?" * len(zone.getMarks())
        logging.debug(f'Reducing {len(patterns):,d} patterns into 1 pattern')
        reducedPattern = list(reduce(self.patternReducer, patterns, "*" * len(zone.getMarks())))
        
        # Save the results to the cache
        self._volatileCache.save(reducedPatternHash, reducedPattern)
        return self._volatileCache.retrieve(reducedPatternHash)
    
    def getApplicablePatternExpression(self, zone: Zone) -> str:
        """
        Creates a filter pattern to be used against patterns to exclude
        invalid patterns off the bat.
        """
        # Generate regular expression from zone status
        regularExpression = ""
        for mark in zone.getMarks():
            if mark.isFilled():
                regularExpression += "[0-9A-F]"
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
        if a == self._reductionFullPattern or b == self._reductionFullPattern:
            return self._reductionFullPattern
            
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
        
    def generatePatternsForHint(self, hints: List[int], space: int, hintIndex: int, zone: Zone) -> List[str]:
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
        # Prepare the filtering pattern
        filteringPattern = self.getApplicablePatternExpression(zone)

        # Return the cached version of all patterns
        zoneCacheHash = hash((space, tuple(hints), hintIndex))
        lastZoneCacheHash = hash((zone.getZoneType().value, zone.getZoneIndex(), tuple(self.hashString('filters'))))

        # Load from volative cache which contains the latest patterns filtered and saved in memory
        # Those patterns are kept for specific zone indexes and types so that nothing can collide
        patterns = []
        if hintIndex == 0 and self._volatileCache.hasKey(lastZoneCacheHash):
            patterns = self._volatileCache.retrieve(lastZoneCacheHash)
            if len(hints) > 4 or hintIndex == 0:
                logging.debug(f'Loaded {len(patterns):,d} patterns from volatile cache for {hints} with {space} spaces for hintIndex {hintIndex}')

        # If no patterns, load from unfiltered cache
        # Load from cache but catch errors in case file has issues
        if len(patterns) == 0 and self._persistentCache.hasKey(zoneCacheHash):
            try:
                patterns = self._persistentCache.retrieve(zoneCacheHash)
                if len(hints) > 4 or hintIndex == 0:
                    logging.debug(f'Loaded {len(patterns):,d} from cache for {hints} with {space} spaces for hintIndex {hintIndex}')
            except JSONDecodeError:
                logging.debug(f'Failed to load patterns from file, file is corrupt')
                patterns = []
        
        # If no patterns, generate them
        if len(patterns) == 0:

            if len(hints) > 4 or hintIndex == 0:
                logging.debug(f'Generating patterns for {hints} with {space} spaces for hintIndex {hintIndex}')

            # Get the hint and next hints and calculate the space needed so this iteration does not push over
            hint = hints[0]
            nextHints = hints[slice(1, len(hints))]
            nextHintSpace = max(0, reduce(lambda a, b: a + 1 + b, nextHints, 0) - 1)
            spaceAvailable = space - nextHintSpace
            spaceNeeded = hint + (1 if len(nextHints) > 0 else 0)

            # Generate the current patterns
            results = []
            spacers = range(0, spaceAvailable - spaceNeeded + 1)
            for spaces in spacers:

                # Create the current pattern
                currentPattern = "x" * spaces
                currentPattern += (hex(hintIndex).replace('0x', '').upper()) * hint
                currentPattern += "x" if len(nextHints) > 0 else "x" * (spaceAvailable - spaceNeeded - spaces)

                # Report progress
                if len(hints) > 4 or hintIndex == 0:
                    logging.debug(f"Loop {spaces}/{spacers.stop}")

                # Generate all sub patterns from it
                if len(nextHints) > 0:
                    subpatterns = self.generatePatternsForHint(nextHints, space - len(currentPattern), hintIndex + 1, zone)
                    for generatedSubPattern in subpatterns:
                        results.append(currentPattern + generatedSubPattern)
                else:
                    results.append(currentPattern)

            # Cache unique patterns using a set
            patterns = list(set(results))

            # Cache only we are at hintIndex 0 or if we have at least 4 levels of hint to generate, 
            # we do not want to cache all permutations of all hints and spaces, it generates
            # way too much data that is probably not reusable that much
            if len(hints) > 4 or hintIndex == 0:
                logging.debug(f'Saving {len(patterns):,d} patterns to cache')
                self._persistentCache.save(zoneCacheHash, patterns)

        # Filter the patterns and return
        if hintIndex == 0 and filteringPattern != "" and filteringPattern != "." * space:
            logging.debug(f'Filtering {len(patterns):,d} patterns using {filteringPattern}')
            patterns = list(filter(lambda a: re.match(filteringPattern, a), patterns))
            logging.debug(f'Saving {len(patterns):,d} patterns to volatile cache')
            self._volatileCache.save(lastZoneCacheHash, patterns)
        
        # Return the patterns
        if len(hints) > 4 or hintIndex == 0:
            logging.debug(f'Generated {len(patterns):,d} patterns')
        return patterns
    
    def hashString(self, data: str) -> bytes:
        hasher = hashlib.sha256()
        hasher.update(bytes(data, 'utf-8'))
        return hasher.digest()