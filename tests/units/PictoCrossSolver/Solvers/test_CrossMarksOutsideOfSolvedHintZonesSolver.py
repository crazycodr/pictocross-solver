from PictoCrossSolver.Solvers import CrossMarksOutsideOfSolvedHintZonesSolver
from PictoCrossSolver.Elements import Zone, Mark

def test_solve_scenario1():
    """
    Tests that both marks preceding and following a zone are crossed when fulfilled
    3 => aaammmaa => aaxmmmxa
    """

    obj = CrossMarksOutsideOfSolvedHintZonesSolver()

    zone = Zone()
    zone.addHint(3)
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(filledMark())
    zone.addMark(filledMark())
    zone.addMark(filledMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())

    obj.solve(zone)
    
    assert zone.getMark(0).isAmbiguous()
    assert zone.getMark(1).isAmbiguous()
    assert zone.getMark(2).isCrossed()
    assert zone.getMark(3).isFilled()
    assert zone.getMark(4).isFilled()
    assert zone.getMark(5).isFilled()
    assert zone.getMark(6).isCrossed()
    assert zone.getMark(7).isAmbiguous()

def test_solve_scenario2():
    """
    Tests that previous mark only is changed because zone is on edge of grid
    3 => aaaaammm => aaaaxmmm
    """

    obj = CrossMarksOutsideOfSolvedHintZonesSolver()

    zone = Zone()
    zone.addHint(3)
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(filledMark())
    zone.addMark(filledMark())
    zone.addMark(filledMark())

    obj.solve(zone)
    
    assert zone.getMark(0).isAmbiguous()
    assert zone.getMark(1).isAmbiguous()
    assert zone.getMark(2).isAmbiguous()
    assert zone.getMark(3).isAmbiguous()
    assert zone.getMark(4).isCrossed()
    assert zone.getMark(5).isFilled()
    assert zone.getMark(6).isFilled()
    assert zone.getMark(7).isFilled()

def test_solve_scenario3():
    """
    Tests that next mark only is changed because zone is on edge of grid
    3 => mmmaaaaa => mmmxaaaa
    """

    obj = CrossMarksOutsideOfSolvedHintZonesSolver()

    zone = Zone()
    zone.addHint(3)
    zone.addMark(filledMark())
    zone.addMark(filledMark())
    zone.addMark(filledMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())

    obj.solve(zone)
    
    assert zone.getMark(0).isFilled()
    assert zone.getMark(1).isFilled()
    assert zone.getMark(2).isFilled()
    assert zone.getMark(3).isCrossed()
    assert zone.getMark(4).isAmbiguous()
    assert zone.getMark(5).isAmbiguous()
    assert zone.getMark(6).isAmbiguous()
    assert zone.getMark(7).isAmbiguous()

def test_solve_scenario4():
    """
    Tests that unfulfilled hints have no previous or next marks crossed
    3 => aaammaaa => aaammaaa
    """

    obj = CrossMarksOutsideOfSolvedHintZonesSolver()

    zone = Zone()
    zone.addHint(3)
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(filledMark())
    zone.addMark(filledMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())

    obj.solve(zone)
    
    assert zone.getMark(0).isAmbiguous()
    assert zone.getMark(1).isAmbiguous()
    assert zone.getMark(2).isAmbiguous()
    assert zone.getMark(3).isFilled()
    assert zone.getMark(4).isFilled()
    assert zone.getMark(5).isAmbiguous()
    assert zone.getMark(6).isAmbiguous()
    assert zone.getMark(7).isAmbiguous()

def test_solve_scenario5():
    """
    Tests that fulfilled hints of 1 gets their crosses when at an edge.
    
    Here, column index 7 and 8 should have a cross after running.
    ---------------------------------------------
                     3              1  1     2          
                  6  2  1  1  1  1  1  1  1  2  6       
            6  11 6  6  7  7  7  8  8  8  8  6  6  11 6 
    ----------------------------------------------------
        9 | ?  ?  ?  ?  ?  ?  █  █  █  ?  ?  ?  ?  ?  ? 
          |
      2 2 | ?  ?  ?  █  ?  ?  X  ?  ?  ?  ?  ?  ?  ?  ? 
          |
    2 2 1 | ?  ?  █  █  ?  ?  X  ?  ?  ?  ?  ?  ?  ?  ? 
          |
      2 2 | ?  ?  █  ?  ?  ?  X  ?  ?  ?  ?  ?  ?  ?  ? 
          |
    2 4 2 | ?  █  █  X  ?  X  X  ?  ?  ?  ?  ?  ?  ?  ? 
          |
       13 | ?  █  █  █  █  █  █  █  █  █  █  █  █  ?  ? 
          |
       15 | █  █  █  █  █  █  █  █  █  █  █  █  █  █  █ 
          |
    2 7 2 | ?  █  ?  X  ?  █  █  █  █  █  ?  ?  ?  ?  ? 
          |
    2 9 2 | █  █  X  █  █  █  █  █  █  █  █  █  X  █  █ 
          |
       15 | █  █  █  █  █  █  █  █  █  █  █  █  █  █  █ 
          |
       15 | █  █  █  █  █  █  █  █  █  █  █  █  █  █  █ 
          |
       15 | █  █  █  █  █  █  █  █  █  █  █  █  █  █  █ 
          |
      3 3 | ?  ?  █  █  ?  X  X  ?  ?  ?  ?  ?  ?  ?  ? 
          |
      3 3 | ?  ?  █  █  ?  ?  X  ?  ?  ?  ?  ?  ?  ?  ? 
          |
      1 1 | ?  ?  █  ?  ?  ?  X  ?  ?  ?  ?  ?  ?  ?  ? 
          |
    """

    obj = CrossMarksOutsideOfSolvedHintZonesSolver()

    zone = Zone()
    zone.addHint(1)
    zone.addHint(8)
    zone.addMark(filledMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(filledMark())
    zone.addMark(filledMark())
    zone.addMark(filledMark())
    zone.addMark(filledMark())
    zone.addMark(filledMark())
    zone.addMark(filledMark())
    zone.addMark(filledMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())

    obj.solve(zone)
    
    assert zone.getMark(0).isFilled()
    assert zone.getMark(1).isCrossed()
    assert zone.getMark(2).isAmbiguous()
    assert zone.getMark(3).isAmbiguous()
    assert zone.getMark(4).isAmbiguous()
    assert zone.getMark(5).isFilled()
    assert zone.getMark(6).isFilled()
    assert zone.getMark(7).isFilled()
    assert zone.getMark(8).isFilled()
    assert zone.getMark(9).isFilled()
    assert zone.getMark(10).isFilled()
    assert zone.getMark(11).isFilled()
    assert zone.getMark(12).isAmbiguous()
    assert zone.getMark(13).isAmbiguous()
    assert zone.getMark(14).isAmbiguous()


def test_solve_scenario6():
    """
    Tests that fulfilled hints are still processed. The following
    scenario is not letting this solver cross the last mark of column 11.

    ---------------------------------------------
                     3              1  1     2          
                  6  2  1  1  1  1  1  1  1  2  6       
            6  11 6  6  7  7  7  8  8  8  8  6  6  11 6 
    ----------------------------------------------------
        9 | ?  ?  ?  ?  ?  ?  █  █  █  ?  ?  ?  ?  ?  ? 
          |
      2 2 | ?  ?  ?  █  ?  ?  X  X  X  ?  ?  ?  ?  ?  ? 
          |
    2 2 1 | ?  ?  █  █  ?  ?  X  ?  ?  ?  ?  ?  ?  ?  ? 
          |
      2 2 | ?  ?  █  ?  ?  ?  X  ?  ?  ?  ?  ?  ?  ?  ? 
          |
    2 4 2 | ?  █  █  X  ?  X  X  ?  ?  ?  ?  X  ?  ?  ? 
          |
       13 | ?  █  █  █  █  █  █  █  █  █  █  █  █  ?  ? 
          |
       15 | █  █  █  █  █  █  █  █  █  █  █  █  █  █  █ 
          |
    2 7 2 | ?  █  ?  X  ?  █  █  █  █  █  █  X  ?  ?  ? 
          |
    2 9 2 | █  █  X  █  █  █  █  █  █  █  █  █  X  █  █ 
          |
       15 | █  █  █  █  █  █  █  █  █  █  █  █  █  █  █ 
          |
       15 | █  █  █  █  █  █  █  █  █  █  █  █  █  █  █ 
          |
       15 | █  █  █  █  █  █  █  █  █  █  █  █  █  █  █ 
          |
      3 3 | ?  ?  █  █  ?  X  X  ?  ?  ?  ?  █  ?  ?  ? 
          |
      3 3 | ?  ?  █  █  ?  ?  X  ?  ?  ?  ?  █  ?  ?  ? 
          |
      1 1 | ?  ?  █  ?  ?  ?  X  ?  ?  ?  ?  ?  ?  ?  ? 
          |
    """

    obj = CrossMarksOutsideOfSolvedHintZonesSolver()

    zone = Zone()
    zone.addHint(2)
    zone.addHint(2)
    zone.addHint(6)
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(crossedMark())
    zone.addMark(filledMark())
    zone.addMark(filledMark())
    zone.addMark(crossedMark())
    zone.addMark(filledMark())
    zone.addMark(filledMark())
    zone.addMark(filledMark())
    zone.addMark(filledMark())
    zone.addMark(filledMark())
    zone.addMark(filledMark())
    zone.addMark(ambiguousMark())

    obj.solve(zone)
    
    assert zone.getMark(0).isAmbiguous()
    assert zone.getMark(1).isAmbiguous()
    assert zone.getMark(2).isAmbiguous()
    assert zone.getMark(3).isAmbiguous()
    assert zone.getMark(4).isCrossed()
    assert zone.getMark(5).isFilled()
    assert zone.getMark(6).isFilled()
    assert zone.getMark(7).isCrossed()
    assert zone.getMark(8).isFilled()
    assert zone.getMark(9).isFilled()
    assert zone.getMark(10).isFilled()
    assert zone.getMark(11).isFilled()
    assert zone.getMark(12).isFilled()
    assert zone.getMark(13).isFilled()
    assert zone.getMark(14).isCrossed()


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