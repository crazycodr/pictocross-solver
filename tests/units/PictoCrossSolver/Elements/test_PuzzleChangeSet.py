from PictoCrossSolver.Elements import PuzzleChangeAction, PuzzleChange
import pytest

def test_happy_paths():
    """
    Tests that the definition of a change set keeps the values we pass it
    """

    zoneType = 1
    zoneIndex = 7

    changeSet = PuzzleChange(zoneType, zoneIndex, slice(0, 2), PuzzleChangeAction.FILL)

    assert changeSet.getZoneType() == zoneType
    assert changeSet.getZoneIndex() == zoneIndex
    assert changeSet.getZoneSlice() == slice(0, 2)
    assert changeSet.getAction() == PuzzleChangeAction.FILL