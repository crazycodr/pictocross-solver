from PictoCrossSolver.Solvers import CrossMarksUnreachableByAnyHint
from PictoCrossSolver.Elements import Zone, Mark

def test_solve_scenario1():
    """
    Tests that a real life problem where the CrossMarksUnreachableByAnyHint
    doesn't find the proper marks to cross.

    In this scenario, row 9 (5,3) should receive crosses
    on columns 10 and 11 because the hint #2 (3) cannot
    reach past column 9 (from 7 to 9).
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

    CrossMarksUnreachableByAnyHint.solve(zone)
    
    assert zone.getMark(0).isFilled()
    assert zone.getMark(1).isFilled()
    assert zone.getMark(2).isFilled()
    assert zone.getMark(3).isFilled()
    assert zone.getMark(4).isFilled()
    assert zone.getMark(5).isCrossed()
    assert zone.getMark(6).isAmbiguous()
    assert zone.getMark(7).isFilled()
    assert zone.getMark(8).isAmbiguous()
    assert zone.getMark(9).isAmbiguous()
    assert zone.getMark(10).isCrossed()
    assert zone.getMark(11).isCrossed()
    

def test_solve_scenario2():
    """
    Tests that a real life problem where the CrossMarksUnreachableByAnyHint
    doesn't find the proper marks to cross.

    In this scenario, column 7 (3,1,1) should not receive crosses
    on rows 10 and 11 because the hint #3 (1) can be in any of those squares.
    
    The recent addition of contiguous filled marks messed this all up because
    hint #2 and #3 can overlap the same filled marks.
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
    zone.addHint(5)
    zone.addHint(3)
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

    CrossMarksUnreachableByAnyHint.solve(zone)
    
    assert zone.getMark(0).isAmbiguous()
    assert zone.getMark(1).isAmbiguous()
    assert zone.getMark(2).isAmbiguous()
    assert zone.getMark(3).isAmbiguous()
    assert zone.getMark(4).isAmbiguous()
    assert zone.getMark(5).isFilled()
    assert zone.getMark(6).isAmbiguous()
    assert zone.getMark(7).isFilled()
    assert zone.getMark(8).isAmbiguous()
    assert zone.getMark(9).isAmbiguous()
    assert zone.getMark(10).isAmbiguous()
    assert zone.getMark(11).isAmbiguous()


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