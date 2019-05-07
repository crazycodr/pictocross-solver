from PictoCrossSolver.Analyzers import HintCrossoverRegexAnalyzer
from PictoCrossSolver.Elements import Zone, Mark

def test_analyze_scenario1():
    """
    Tests that the analysis yields the proper result
    In this scenario the pattern is fully open "aaaaaa"
    Only 1 hint
    Every direction should yield 6 possible marks so the slice will be (0, 6)
    """

    zone = Zone()
    zone.addHint(2)
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    
    assert HintCrossoverRegexAnalyzer.analyze(zone, 0) == slice(0, 6, None)

def test_analyze_scenario2():
    """
    Tests that the analysis yields the proper result
    In this scenario the pattern is fully open "aaaaaa"
    There are 2 hints of 2 and 2
    In hint 0 detection
    For hint 0:
        Forward direction should yield the marks 0-3
        Backward direction should yield the marks 0-3
        Result should be 0-3
    In hint 1 detection
    For hint 1:
        Forward direction should yield the marks 3-6
        Backward direction should yield the marks 3-6
        Result should be 3-6
    """

    zone = Zone()
    zone.addHint(2)
    zone.addHint(2)
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    
    assert HintCrossoverRegexAnalyzer.analyze(zone, 0) == slice(0, 3, None)
    assert HintCrossoverRegexAnalyzer.analyze(zone, 1) == slice(3, 6, None)

def test_analyze_scenario3():
    """
    Tests that the analysis yields the proper result
    In this scenario the pattern is complex an features barred zones
    that would normally result in incorrect slice lookup if using only forward lookups.
    This comes from a real world scenario 
    The pattern is "aaaaaaaaacff"
    There are 2 hints of 4 and 2
    For hint 0:
        Forward direction should yield the marks 0-9
        Backward direction should yield the marks 0-9
        Result should be 0-9
    For hint 1:
        Forward direction should yield the marks 6-9
        Backward direction should yield the marks 10-12
        Result should be 10-12
    """

    zone = Zone()
    zone.addHint(4)
    zone.addHint(2)
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(crossedMark())
    zone.addMark(filledMark())
    zone.addMark(filledMark())
    
    assert HintCrossoverRegexAnalyzer.analyze(zone, 0) == slice(0, 9, None)
    assert HintCrossoverRegexAnalyzer.analyze(zone, 1) == slice(10, 12, None)

def test_analyze_scenario4():
    """
    Tests that the analysis yields the proper result
    Regression test for following scenario:
    
    hints: [7]
    pattern: caaaafffccaa
    expected: 1-8

    Currently getting error due to None being returned
    """

    zone = Zone()
    zone.addHint(7)
    zone.addMark(crossedMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(filledMark())
    zone.addMark(filledMark())
    zone.addMark(filledMark())
    zone.addMark(crossedMark())
    zone.addMark(crossedMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    
    assert HintCrossoverRegexAnalyzer.analyze(zone, 0) == slice(1, 8, None)

def test_analyze_scenario5():
    """
    Tests that the analysis yields the proper result
    Regression test for following scenario:
    
    hints: [4]
    pattern: caaaacccaaaa
    expected: None

    Currently getting error due to None being returned
    """

    zone = Zone()
    zone.addHint(4)
    zone.addMark(crossedMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(crossedMark())
    zone.addMark(crossedMark())
    zone.addMark(crossedMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    
    assert HintCrossoverRegexAnalyzer.analyze(zone, 0) == None

def test_analyze_scenario6():
    """
    Tests a scenario that currently returns wrong zones for a hint.

    Row 1 currently changes hint #2 and adds a mark at column 4 which is
    wrong because hint #2 could very well be on the other side of the puzzle.

    The problem here is that it is assumed that row 1 setup forces hint #1 to
    resolve to the 2 first ambiguous squares and hint #2 to the squares 3-5.
    ---------------------------------------------
                     3              1  1     2          
                  6  2  1  1  1  1  1  1  1  2  6       
            6  11 6  6  7  7  7  8  8  8  8  6  6  11 6 
    ----------------------------------------------------
        9 | ?  ?  ?  ?  ?  ?  █  █  █  ?  ?  ?  ?  ?  ? 
          |
      2 2 | ?  ?  ?  █  ?  ?  X  X  X  ?  ?  ?  ?  ?  ? 
          |
    2 2 1 | ?  ?  █  █  ?  ?  X  ?  ?  ?  ?  ?  █  ?  ? 
          |
      2 2 | ?  ?  █  ?  ?  ?  X  ?  ?  ?  ?  ?  █  ?  ? 
          |
    2 4 2 | ?  █  █  X  ?  X  X  ?  ?  ?  ?  X  █  █  ? 
          |
       13 | ?  █  █  █  █  █  █  █  █  █  █  █  █  █  ? 
          |
       15 | █  █  █  █  █  █  █  █  █  █  █  █  █  █  █ 
          |
    2 7 2 | ?  █  ?  X  ?  █  █  █  █  █  █  X  ?  █  ? 
          |
    2 9 2 | █  █  X  █  █  █  █  █  █  █  █  █  X  █  █ 
          |
       15 | █  █  █  █  █  █  █  █  █  █  █  █  █  █  █ 
          |
       15 | █  █  █  █  █  █  █  █  █  █  █  █  █  █  █ 
          |
       15 | █  █  █  █  █  █  █  █  █  █  █  █  █  █  █ 
          |
      3 3 | ?  ?  █  █  ?  X  X  ?  ?  ?  ?  █  █  ?  ? 
          |
      3 3 | ?  ?  █  █  ?  ?  X  ?  ?  ?  ?  █  █  ?  ? 
          |
      1 1 | ?  ?  █  X  ?  ?  X  ?  ?  ?  ?  X  █  ?  ? 
          |
    """

    zone = Zone()
    zone.addHint(2)
    zone.addHint(2)
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(filledMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(crossedMark())
    zone.addMark(crossedMark())
    zone.addMark(crossedMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    
    assert HintCrossoverRegexAnalyzer.analyze(zone, 1) == None
    

def crossedMark():
    mark = Mark()
    mark.setCrossed()
    return mark


def filledMark():
    mark = Mark()
    mark.setFilled()
    return mark


def ambiguousMark():
    mark = Mark()
    mark.setAmbiguous()
    return mark