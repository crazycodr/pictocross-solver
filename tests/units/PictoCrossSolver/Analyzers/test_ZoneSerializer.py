from PictoCrossSolver.Analyzers import ZoneSerializer
from PictoCrossSolver.Elements import Zone, Mark

def test_serialize_scenario1():
    """
    Tests that serializer returns proper result
    """

    obj = ZoneSerializer()

    zone = Zone()
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    zone.addMark(ambiguousMark())
    
    assert obj.serialize(zone) == 'aaaaaa'


def test_serialize_scenario2():
    """
    Tests that serializer returns proper result
    """

    obj = ZoneSerializer()

    zone = Zone()
    zone.addMark(filledMark())
    zone.addMark(filledMark())
    zone.addMark(filledMark())
    zone.addMark(filledMark())
    zone.addMark(filledMark())
    zone.addMark(filledMark())
    
    assert obj.serialize(zone) == 'mmmmmm'


def test_serialize_scenario3():
    """
    Tests that serializer returns proper result
    """

    obj = ZoneSerializer()

    zone = Zone()
    zone.addMark(crossedMark())
    zone.addMark(crossedMark())
    zone.addMark(crossedMark())
    zone.addMark(crossedMark())
    zone.addMark(crossedMark())
    zone.addMark(crossedMark())
    
    assert obj.serialize(zone) == 'bbbbbb'


def test_serialize_scenario4():
    """
    Tests that serializer returns proper result
    """

    obj = ZoneSerializer()

    zone = Zone()
    zone.addMark(crossedMark())
    zone.addMark(filledMark())
    zone.addMark(filledMark())
    zone.addMark(ambiguousMark())
    zone.addMark(crossedMark())
    zone.addMark(ambiguousMark())
    
    assert obj.serialize(zone) == 'bmmaba'


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