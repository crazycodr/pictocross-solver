from PictoCrossSolver.Solvers import HintExpandsFilledMarksFromEdgeInEstimatedZoneSolver
from PictoCrossSolver.Elements import Zone, Mark

def test_solve_scenario1():
    """
    Tests that an edge mark expands properly when at the start of a zone
    xmmaaxxa => xmmmaxxa
    """

    obj = HintExpandsFilledMarksFromEdgeInEstimatedZoneSolver()

    zone = Zone()
    zone.addHint(3)
    zone.addMark(crossedMark())
    zone.addMark(filledMark())
    zone.addMark(filledMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(crossedMark())
    zone.addMark(crossedMark())
    zone.addMark(ambiguousMark())

    obj.solve(zone)
    
    assert zone.getMark(0).isCrossed()
    assert zone.getMark(1).isFilled()
    assert zone.getMark(2).isFilled()
    assert zone.getMark(3).isFilled()
    assert zone.getMark(4).isAmbiguous()
    assert zone.getMark(5).isCrossed()
    assert zone.getMark(6).isCrossed()
    assert zone.getMark(7).isAmbiguous()

def test_solve_scenario2():
    """
    Tests that an edge mark that is set expands when at the end of a zone
    xaammxxa => xammmxxa
    """

    obj = HintExpandsFilledMarksFromEdgeInEstimatedZoneSolver()

    zone = Zone()
    zone.addHint(3)
    zone.addMark(crossedMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(filledMark())
    zone.addMark(filledMark())
    zone.addMark(crossedMark())
    zone.addMark(crossedMark())
    zone.addMark(ambiguousMark())

    obj.solve(zone)
    
    assert zone.getMark(0).isCrossed()
    assert zone.getMark(1).isAmbiguous()
    assert zone.getMark(2).isFilled()
    assert zone.getMark(3).isFilled()
    assert zone.getMark(4).isFilled()
    assert zone.getMark(5).isCrossed()
    assert zone.getMark(6).isCrossed()
    assert zone.getMark(7).isAmbiguous()

def test_solve_scenario3():
    """
    Tests that an edge mark that is set expands when at the end of a zone
    when the space is limited to just what is available
    xammmmmx => xmmmmmmx
    """

    zone = Zone()
    zone.addHint(6)
    zone.addMark(crossedMark())
    zone.addMark(ambiguousMark())
    zone.addMark(filledMark())
    zone.addMark(filledMark())
    zone.addMark(filledMark())
    zone.addMark(filledMark())
    zone.addMark(filledMark())
    zone.addMark(crossedMark())

    HintExpandsFilledMarksFromEdgeInEstimatedZoneSolver.solve(zone)
    
    assert zone.getMark(0).isCrossed()
    assert zone.getMark(1).isFilled()
    assert zone.getMark(2).isFilled()
    assert zone.getMark(3).isFilled()
    assert zone.getMark(4).isFilled()
    assert zone.getMark(5).isFilled()
    assert zone.getMark(6).isFilled()
    assert zone.getMark(7).isCrossed()


def test_analyze_scenario4():
    """
    Tests a scenario that currently returns wrong zones for a hint.

    Row 2 currently thinks that mark in column 12 is part of hint #2
    but it is in fact part of hint #3.

    Nothing should change.
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
    zone.addHint(1)
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(filledMark())
    zone.addMark(filledMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(crossedMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(filledMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())

    HintExpandsFilledMarksFromEdgeInEstimatedZoneSolver.solve(zone)
    
    assert zone.getMark(0).isAmbiguous()
    assert zone.getMark(1).isAmbiguous()
    assert zone.getMark(2).isFilled()
    assert zone.getMark(3).isFilled()
    assert zone.getMark(4).isAmbiguous()
    assert zone.getMark(5).isAmbiguous()
    assert zone.getMark(6).isCrossed()
    assert zone.getMark(7).isAmbiguous()
    assert zone.getMark(8).isAmbiguous()
    assert zone.getMark(9).isAmbiguous()
    assert zone.getMark(10).isAmbiguous()
    assert zone.getMark(11).isAmbiguous()
    assert zone.getMark(12).isFilled()
    assert zone.getMark(13).isAmbiguous()
    assert zone.getMark(14).isAmbiguous()


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