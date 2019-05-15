from PictoCrossSolver.Elements import ZoneType, Puzzle, PuzzleChangeAction, PuzzleChange
import pytest

def test_applyChanges_scenario1():
    """
    Tests that the applyChanges yields the proper result.

    No marks set, copy should yield a different object with same config.
    """
    puzzle = Puzzle(4, 4)
    puzzle.getRowZone(0).addHint(4)
    puzzle.getRowZone(1).addHint(3)
    puzzle.getRowZone(2).addHint(2)
    puzzle.getRowZone(3).addHint(1)
    puzzle.getColumnZone(0).addHint(4)
    puzzle.getColumnZone(1).addHint(3)
    puzzle.getColumnZone(2).addHint(2)
    puzzle.getColumnZone(3).addHint(1)

    copy = puzzle.applyChanges()

    assert not puzzle is copy
    assert not puzzle.getRowZone(0) is copy.getRowZone(0)
    assert not puzzle.getRowZone(1) is copy.getRowZone(1)
    assert not puzzle.getRowZone(2) is copy.getRowZone(2)
    assert not puzzle.getRowZone(3) is copy.getRowZone(3)
    assert not puzzle.getColumnZone(0) is copy.getColumnZone(0)
    assert not puzzle.getColumnZone(1) is copy.getColumnZone(1)
    assert not puzzle.getColumnZone(2) is copy.getColumnZone(2)
    assert not puzzle.getColumnZone(3) is copy.getColumnZone(3)

    assert len(copy.getRowZones()) == 4
    assert len(copy.getColumnZones()) == 4

    assert copy.getRowZone(0).getHints() == [4]
    assert copy.getRowZone(1).getHints() == [3]
    assert copy.getRowZone(2).getHints() == [2]
    assert copy.getRowZone(3).getHints() == [1]
    assert copy.getColumnZone(0).getHints() == [4]
    assert copy.getColumnZone(1).getHints() == [3]
    assert copy.getColumnZone(2).getHints() == [2]
    assert copy.getColumnZone(3).getHints() == [1]

def test_applyChanges_scenario2():
    """
    Tests that the applyChanges yields the proper result.

    Marks are set, they should copy over
    """
    puzzle = Puzzle(4, 4)
    puzzle.getRowZone(0).addHint(4)
    puzzle.getRowZone(1).addHint(3)
    puzzle.getRowZone(2).addHint(2)
    puzzle.getRowZone(3).addHint(1)
    puzzle.getColumnZone(0).addHint(4)
    puzzle.getColumnZone(1).addHint(3)
    puzzle.getColumnZone(2).addHint(2)
    puzzle.getColumnZone(3).addHint(1)
    puzzle.getRowZone(0).getMark(0).setFilled()
    puzzle.getRowZone(0).getMark(1).setFilled()
    puzzle.getRowZone(0).getMark(2).setFilled()
    puzzle.getRowZone(0).getMark(3).setFilled()

    copy = puzzle.applyChanges()

    assert copy.getRowZone(0).getMark(0).isFilled()
    assert copy.getRowZone(0).getMark(1).isFilled()
    assert copy.getRowZone(0).getMark(2).isFilled()
    assert copy.getRowZone(0).getMark(3).isFilled()
    assert copy.getRowZone(1).getMark(0).isAmbiguous()
    assert copy.getRowZone(1).getMark(1).isAmbiguous()
    assert copy.getRowZone(1).getMark(2).isAmbiguous()
    assert copy.getRowZone(1).getMark(3).isAmbiguous()
    assert copy.getRowZone(2).getMark(0).isAmbiguous()
    assert copy.getRowZone(2).getMark(1).isAmbiguous()
    assert copy.getRowZone(2).getMark(2).isAmbiguous()
    assert copy.getRowZone(2).getMark(3).isAmbiguous()
    assert copy.getRowZone(3).getMark(0).isAmbiguous()
    assert copy.getRowZone(3).getMark(1).isAmbiguous()
    assert copy.getRowZone(3).getMark(2).isAmbiguous()
    assert copy.getRowZone(3).getMark(3).isAmbiguous()

def test_applyChanges_scenario3():
    """
    Tests that the applyChanges yields the proper result.

    There are changes attached to puzzle, ensure they are commited
    """
    puzzle = Puzzle(4, 4)
    puzzle.getRowZone(0).addHint(4)
    puzzle.getRowZone(1).addHint(3)
    puzzle.getRowZone(2).addHint(2)
    puzzle.getRowZone(3).addHint(1)
    puzzle.getColumnZone(0).addHint(4)
    puzzle.getColumnZone(1).addHint(3)
    puzzle.getColumnZone(2).addHint(2)
    puzzle.getColumnZone(3).addHint(1)
    puzzle.addChange(PuzzleChange(ZoneType.ROW, 0, slice(0, 4), PuzzleChangeAction.FILL))

    copy = puzzle.applyChanges()

    assert copy.getRowZone(0).getMark(0).isFilled()
    assert copy.getRowZone(0).getMark(1).isFilled()
    assert copy.getRowZone(0).getMark(2).isFilled()
    assert copy.getRowZone(0).getMark(3).isFilled()
    assert copy.getRowZone(1).getMark(0).isAmbiguous()
    assert copy.getRowZone(1).getMark(1).isAmbiguous()
    assert copy.getRowZone(1).getMark(2).isAmbiguous()
    assert copy.getRowZone(1).getMark(3).isAmbiguous()
    assert copy.getRowZone(2).getMark(0).isAmbiguous()
    assert copy.getRowZone(2).getMark(1).isAmbiguous()
    assert copy.getRowZone(2).getMark(2).isAmbiguous()
    assert copy.getRowZone(2).getMark(3).isAmbiguous()
    assert copy.getRowZone(3).getMark(0).isAmbiguous()
    assert copy.getRowZone(3).getMark(1).isAmbiguous()
    assert copy.getRowZone(3).getMark(2).isAmbiguous()
    assert copy.getRowZone(3).getMark(3).isAmbiguous()