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
    
    assert zone.getMark(0).isCrossed() == True
    assert zone.getMark(1).isFilled() == True
    assert zone.getMark(2).isFilled() == True
    assert zone.getMark(3).isFilled() == True
    assert zone.getMark(4).isAmbiguous() == True
    assert zone.getMark(5).isCrossed() == True
    assert zone.getMark(6).isCrossed() == True
    assert zone.getMark(7).isAmbiguous() == True

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
    
    assert zone.getMark(0).isCrossed() == True
    assert zone.getMark(1).isAmbiguous() == True
    assert zone.getMark(2).isFilled() == True
    assert zone.getMark(3).isFilled() == True
    assert zone.getMark(4).isFilled() == True
    assert zone.getMark(5).isCrossed() == True
    assert zone.getMark(6).isCrossed() == True
    assert zone.getMark(7).isAmbiguous() == True

def test_solve_scenario3():
    """
    Tests that an edge mark that is set expands when at the end of a zone
    when the space is limited to just what is available
    xammmmmx => xmmmmmmx
    """

    obj = HintExpandsFilledMarksFromEdgeInEstimatedZoneSolver()

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

    obj.solve(zone)
    
    assert zone.getMark(0).isCrossed() == True
    assert zone.getMark(1).isFilled() == True
    assert zone.getMark(2).isFilled() == True
    assert zone.getMark(3).isFilled() == True
    assert zone.getMark(4).isFilled() == True
    assert zone.getMark(5).isFilled() == True
    assert zone.getMark(6).isFilled() == True
    assert zone.getMark(7).isCrossed() == True

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