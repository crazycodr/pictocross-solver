import PictoCrossSolver.Solvers
import PictoCrossSolver.PictoCross

def test_solve_scenario1():
    """
    Tests that both marks preceding and following a zone are crossed when fulfilled
    3 => aaammmaa => aaxmmmxa
    """

    obj = PictoCrossSolver.Solvers.CrossMarksOutsideOfSolvedHintZonesSolver()

    zone = PictoCrossSolver.PictoCross.Zone()
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

    obj = PictoCrossSolver.Solvers.CrossMarksOutsideOfSolvedHintZonesSolver()

    zone = PictoCrossSolver.PictoCross.Zone()
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

    obj = PictoCrossSolver.Solvers.CrossMarksOutsideOfSolvedHintZonesSolver()

    zone = PictoCrossSolver.PictoCross.Zone()
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

    obj = PictoCrossSolver.Solvers.CrossMarksOutsideOfSolvedHintZonesSolver()

    zone = PictoCrossSolver.PictoCross.Zone()
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