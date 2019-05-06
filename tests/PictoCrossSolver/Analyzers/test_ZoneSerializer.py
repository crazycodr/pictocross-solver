import PictoCrossSolver.Analyzers
import PictoCrossSolver.PictoCross

def test_serialize_scenario1():
    """
    Tests that serializer returns proper result
    """

    obj = PictoCrossSolver.Analyzers.ZoneSerializer()

    zone = PictoCrossSolver.PictoCross.Zone()
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

    obj = PictoCrossSolver.Analyzers.ZoneSerializer()

    zone = PictoCrossSolver.PictoCross.Zone()
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

    obj = PictoCrossSolver.Analyzers.ZoneSerializer()

    zone = PictoCrossSolver.PictoCross.Zone()
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

    obj = PictoCrossSolver.Analyzers.ZoneSerializer()

    zone = PictoCrossSolver.PictoCross.Zone()
    zone.addMark(crossedMark())
    zone.addMark(filledMark())
    zone.addMark(filledMark())
    zone.addMark(ambiguousMark())
    zone.addMark(crossedMark())
    zone.addMark(ambiguousMark())
    
    assert obj.serialize(zone) == 'bmmaba'


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