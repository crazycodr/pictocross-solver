from PictoCrossSolver.Analyzers import HintUnionRegexAnalyzer
from PictoCrossSolver.Elements import Zone, Mark

def test_analyze_scenario1():
    """
    Tests that a real life problem where the CrossMarksUnreachableByAnyHint
    doesn't find the proper marks to cross because HintUnionRegexAnalyzer
    returns the improper slice when there is a filled mark in the analyzed
    zone.

    In this scenario, row 9 (5,3) should receive crosses
    on columns 10 and 11 because the hint #2 (3) cannot
    reach past column 9 (from 7 to 9).

    This means that HintUnionRegexAnalyzer should return
    a slice of 6 to 9 instead of 6 to 12.
    ---------------------------------------------
                    1  1                         
                    1  1                         
                 3  1  1              1  1       
                 3  1  1  1        3  1  1       
                 1  1  1  1        1  1  1  3  1 
              5  1  1  1  5  3  5  1  1  1  5  1 
    ---------------------------------------------
      1 1 2 | X     X  X  X     X  X             
            |
        5 1 | X  █  █  █  █  █  X  X  X  X  █  X 
            |
      1 1 2 | X  █  X  X  X  █  X  X        █    
            |
        3 3 | X     █  █           █             
            |
        2 1 | X  X  X  X           █  X  X       
            |
        3 5 | X  █  █  █  X  X  █  █  █  █  █  X 
            |
    2 1 1 1 | █  █  X  X  █  X  █  X  X  X  █  X 
            |
        5 5 | █  █  █  █  █  X  █  █  █  █  █  X 
            |
    1 1 1 1 | █  X  X  X  █  X  █  X  X  X  █  X 
            |
        5 3 | █  █  █  █  █  X     █             
            |
        1 1 | █  X  X  X  █  X  X  X  X  X  X  X 
            |
          3 | X  █  █  █  X  X  X  X  X  X  X  X 
            |
    """

    zone = Zone()
    zone.addHint(5)
    zone.addHint(3)
    zone.addMark(filledMark())
    zone.addMark(filledMark())
    zone.addMark(filledMark())
    zone.addMark(filledMark())
    zone.addMark(filledMark())
    zone.addMark(crossedMark())
    zone.addMark(ambiguousMark())
    zone.addMark(filledMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())

    assert HintUnionRegexAnalyzer.analyze(zone, 1) == slice(6, 10)
    

def test_analyze_scenario2():
    """
    Tests that a real life problem where the CrossMarksUnreachableByAnyHint
    doesn't find the proper marks to cross because HintUnionRegexAnalyzer
    returns the improper slice when there is a filled mark in the analyzed
    zone.

    In this scenario, column 7 (3,1,1) should not receive crosses
    on rows 10 and 11 because the hint #3 (1) can be in any of those squares.

    This means that HintUnionRegexAnalyzer should return a full range in this
    case.
    ---------------------------------------------
                    1  1                         
                    1  1                         
                 3  1  1              1  1       
                 3  1  1  1        3  1  1       
                 1  1  1  1        1  1  1  3  1 
              5  1  1  1  5  3  5  1  1  1  5  1 
    ---------------------------------------------
      1 1 2 |                                    
            |
        5 1 |    █                               
            |
      1 1 2 |    █                               
            |
        3 3 |                                    
            |
        2 1 |    X                               
            |
        3 5 |    █                 █  █          
            |
    2 1 1 1 |    █  X  X                         
            |
        5 5 |    █  █  █  █        █  █  █  █    
            |
    1 1 1 1 |    X  X  X  █                      
            |
        5 3 |    █  █  █  █                      
            |
        1 1 |    X  X  X                         
            |
          3 |    █  █  █                         
            |
    """

    zone = Zone()
    zone.addHint(3)
    zone.addHint(1)
    zone.addHint(1)
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(filledMark())
    zone.addMark(ambiguousMark())
    zone.addMark(filledMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())

    assert HintUnionRegexAnalyzer.analyze(zone, 2) == slice(7, 12)
    

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