from PictoCrossSolver.Analyzers import HintCrossoverRegexAnalyzer
from PictoCrossSolver.PictoCross import Zone, Mark

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
    The pattern is "aaaaaaaaabmm"
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