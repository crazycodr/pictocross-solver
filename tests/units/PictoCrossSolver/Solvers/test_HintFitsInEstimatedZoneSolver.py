from PictoCrossSolver.Solvers import HintFitsInEstimatedZoneSolver
from PictoCrossSolver.Elements import Zone, Mark


def test_solve_scenario1():
    """
    Tests that a real life scenario regression

    """

    obj = HintFitsInEstimatedZoneSolver()

    zone = Zone()
    zone.addHint(1)
    zone.addHint(10)
    zone.addMark(ambiguousMark())
    zone.addMark(crossedMark())
    zone.addMark(filledMark())
    zone.addMark(filledMark())
    zone.addMark(filledMark())
    zone.addMark(filledMark())
    zone.addMark(filledMark())
    zone.addMark(filledMark())
    zone.addMark(filledMark())
    zone.addMark(filledMark())
    zone.addMark(filledMark())
    zone.addMark(filledMark())

    obj.solve(zone)
    
    assert zone.getMark(0).isFilled()
    assert zone.getMark(1).isCrossed()
    assert zone.getMark(2).isFilled()
    assert zone.getMark(3).isFilled()
    assert zone.getMark(4).isFilled()
    assert zone.getMark(5).isFilled()
    assert zone.getMark(6).isFilled()
    assert zone.getMark(7).isFilled()
    assert zone.getMark(8).isFilled()
    assert zone.getMark(9).isFilled()
    assert zone.getMark(10).isFilled()
    assert zone.getMark(11).isFilled()


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