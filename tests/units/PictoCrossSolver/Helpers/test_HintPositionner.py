from PictoCrossSolver.Elements import ZoneType, Zone, Mark
from PictoCrossSolver.Helpers import HintPositionner
from PictoCrossSolver.Caches import MemoryCache
import pytest

def test_generatePatternsForHint_scenario1():
    """
    Tests that the generatePatternsForHint function returns the proper values

    Single full zone hint returns single pattern
    """

    assert HintPositionner(MemoryCache(), MemoryCache()).generatePatternsForHint([10], 10, 0, "") == ["0000000000"]

def test_generatePatternsForHint_scenario2():
    """
    Tests that the generatePatternsForHint function returns the proper values

    Single partial zone hint returns multiple patterns
    """

    assert set(HintPositionner(MemoryCache(), MemoryCache()).generatePatternsForHint([8], 10, 0, "")) == set(["00000000xx", "x00000000x", "xx00000000"])

def test_generatePatternsForHint_scenario3():
    """
    Tests that the generatePatternsForHint function returns the proper values

    Multi full zone hint returns single pattern
    """

    assert set(HintPositionner(MemoryCache(), MemoryCache()).generatePatternsForHint([3, 3, 2], 10, 0, "")) == set(["000x111x22"])

def test_generatePatternsForHint_scenario4():
    """
    Tests that the generatePatternsForHint function returns the proper values

    Multi partial zone hint returns multiple patterns
    """

    results = set(HintPositionner(MemoryCache(), MemoryCache()).generatePatternsForHint([2,2,2], 10, 0, ""))
    assert results == set(["00x11x22xx", "00x11xx22x", "00x11xxx22", "00xx11x22x", "00xx11xx22", "00xxx11x22", "x00x11x22x", "x00x11xx22", "x00xx11x22", "xx00x11x22"])

def test_patternReducer():
    """
    Tests that the patternReducer function returns the proper values
    """
    assert HintPositionner(MemoryCache(), MemoryCache()).patternReducer("****", "****") == "****"
    assert HintPositionner(MemoryCache(), MemoryCache()).patternReducer("0000", "0000") == "0000"
    assert HintPositionner(MemoryCache(), MemoryCache()).patternReducer("0**1", "0**1") == "0**1"
    assert HintPositionner(MemoryCache(), MemoryCache()).patternReducer("0xx1", "0xx1") == "0xx1"
    assert HintPositionner(MemoryCache(), MemoryCache()).patternReducer("0xx1", "x0x1") == "??x1"
    assert HintPositionner(MemoryCache(), MemoryCache()).patternReducer("0**1", "00x1") == "00x1"

def test_position_scenario1():
    """
    Tests that the position function returns the proper values

    Tests that a full hint returns 0 everywhere
    """
    zone = Zone(ZoneType.ROW, 0)
    zone.addHint(10)
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())

    assert HintPositionner(MemoryCache(), MemoryCache()).position(zone) == ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"]

def test_position_scenario2():
    """
    Tests that the position function returns the proper values

    Tests that multiple hints fully covering full answer
    """
    zone = Zone(ZoneType.ROW, 0)
    zone.addHint(4)
    zone.addHint(5)
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())

    assert HintPositionner(MemoryCache(), MemoryCache()).position(zone) == ["0", "0", "0", "0", "x", "1", "1", "1", "1", "1"]

def test_position_scenario3():
    """
    Tests that the position function returns the proper values

    Tests that one hint partially covering returns ambiguous where expected
    """
    zone = Zone(ZoneType.ROW, 0)
    zone.addHint(8)
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())

    assert HintPositionner(MemoryCache(), MemoryCache()).position(zone) == ["?", "?", "0", "0", "0", "0", "0", "0", "?", "?"]

def test_position_scenario4():
    """
    Tests that the position function returns the proper values

    Tests that a simple multi hint partially covering returns ambiguous where expected
    """
    zone = Zone(ZoneType.ROW, 0)
    zone.addHint(4)
    zone.addHint(4)
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())

    assert HintPositionner(MemoryCache(), MemoryCache()).position(zone) == ["?", "0", "0", "0", "?", "?", "1", "1", "1", "?"]

def test_position_scenario5():
    """
    Tests that the position function returns the proper values

    Tests that a complex multi hint partially covering returns ambiguous where expected
    """
    zone = Zone(ZoneType.ROW, 0)
    zone.addHint(4)
    zone.addHint(1)
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
    zone.addMark(ambiguousMark())

    assert HintPositionner(MemoryCache(), MemoryCache()).position(zone) == ["?", "0", "0", "0", "?", "?", "?", "?", "2", "?"]

def test_position_scenario6():
    """
    Tests that the position function returns the proper values

    Tests that a complex multi hint partially covering returns ambiguous where expected
    when there are already marks set
    """
    zone = Zone(ZoneType.ROW, 0)
    zone.addHint(4)
    zone.addHint(1)
    zone.addHint(2)
    zone.addMark(filledMark())
    zone.addMark(filledMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(filledMark())

    assert HintPositionner(MemoryCache(), MemoryCache()).position(zone) == ["0", "0", "0", "0", "x", "?", "?", "x", "2", "2"]

def test_position_scenario7():
    """
    Tests real life regression
    """
    zone = Zone(ZoneType.ROW, 0)
    zone.addHint(2)
    zone.addHint(2)
    
    zone.addMark(crossedMark())
    zone.addMark(ambiguousMark())
    zone.addMark(filledMark())
    zone.addMark(ambiguousMark())
    zone.addMark(crossedMark())
    zone.addMark(crossedMark())
    zone.addMark(crossedMark())
    zone.addMark(crossedMark())
    zone.addMark(crossedMark())
    zone.addMark(crossedMark())
    zone.addMark(crossedMark())
    zone.addMark(ambiguousMark())
    zone.addMark(filledMark())
    zone.addMark(ambiguousMark())
    zone.addMark(crossedMark())

    assert HintPositionner(MemoryCache(), MemoryCache()).position(zone) == ["x", "?", "0", "?", "x", "x", "x", "x", "x", "x", "x", "?", "1", "?", "x"]

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