import PictoCrossSolver.Solvers
import PictoCrossSolver.PictoCross

def test_solve_scenario1():
    """
    Tests that a real life scenario regression

    """

    obj = PictoCrossSolver.Solvers.HintFitsInEstimatedZoneSolver()

    zone = PictoCrossSolver.PictoCross.Zone()
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
    mark = PictoCrossSolver.PictoCross.Mark()
    mark.setCrossed()
    return mark

def filledMark():
    mark = PictoCrossSolver.PictoCross.Mark()
    mark.setFilled()
    return mark

def ambiguousMark():
    mark = PictoCrossSolver.PictoCross.Mark()
    mark.setAmbiguous()
    return mark