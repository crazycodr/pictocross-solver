from PictoCrossSolver.Elements import ZoneType, Puzzle, PuzzleChangeAction, PuzzleChange
from PictoCrossSolver.Helpers import ChangeMinimizer
import pytest

def test_minimize_scenario1():
    """
    Tests that the minimize function returns the proper values

    No changes returns no changes
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
    
    changes = []

    assert len(ChangeMinimizer.minimize(puzzle, changes)) == 0

def test_minimize_scenario2():
    """
    Tests that the minimize function returns the proper values

    A change on an empty grid returns the same objects unaffected
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
    
    changes = [PuzzleChange(ZoneType.ROW, 0, slice(0, 4), PuzzleChangeAction.FILL)]
    newChanges = ChangeMinimizer.minimize(puzzle, changes)

    assert len(newChanges) == 1
    assert newChanges[0] is changes[0]

def test_minimize_scenario3():
    """
    Tests that the minimize function returns the proper values

    A change on partially filled grid returns the same objects unaffected because the changes
    don't overlap on existing values
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
    puzzle.getRowZone(1).getMark(0).setFilled()
    puzzle.getRowZone(1).getMark(1).setFilled()
    puzzle.getRowZone(1).getMark(2).setFilled()
    
    changes = [PuzzleChange(ZoneType.ROW, 0, slice(0, 4), PuzzleChangeAction.FILL)]
    newChanges = ChangeMinimizer.minimize(puzzle, changes)

    assert len(newChanges) == 1
    assert newChanges[0] is changes[0]

def test_minimize_scenario4():
    """
    Tests that the minimize function returns the proper values

    A change on an already changed row returns no object if change
    covers all the row and all marks are already set
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
    
    changes = [PuzzleChange(ZoneType.ROW, 0, slice(0, 4), PuzzleChangeAction.FILL)]
    newChanges = ChangeMinimizer.minimize(puzzle, changes)

    assert len(newChanges) == 0

def test_minimize_scenario5():
    """
    Tests that the minimize function returns the proper values

    A change on an already changed row returns a partial slice
    of the original if the slice affects more than what is set.
    Example: 

    Has: OO??
    Wants: OOOO
    Expect: Expects --OO
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
    
    changes = [PuzzleChange(ZoneType.ROW, 0, slice(0, 4), PuzzleChangeAction.FILL)]
    newChanges = ChangeMinimizer.minimize(puzzle, changes)

    assert len(newChanges) == 1
    assert newChanges[0].getZoneSlice() == slice(2, 4)

def test_minimize_scenario6():
    """
    Tests that the minimize function returns the proper values

    A change on an already changed row returns a partial slice
    of the original if the slice affects items within an already 
    set slice in partial way. Example:

    Has: O??O
    Wants: OOOO
    Expect: Expects -OO-
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
    puzzle.getRowZone(0).getMark(3).setFilled()
    
    changes = [PuzzleChange(ZoneType.ROW, 0, slice(0, 4), PuzzleChangeAction.FILL)]
    newChanges = ChangeMinimizer.minimize(puzzle, changes)

    assert len(newChanges) == 1
    assert newChanges[0].getZoneSlice() == slice(1, 3)

def test_minimize_scenario7():
    """
    Tests that the minimize function returns the proper values

    A change on an already changed row returns a partial slice
    of the original if the slice affects items within an already 
    set slice in partial way. Example:

    Has: ??OO
    Wants: OOOO
    Expect: Expects OO--
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
    puzzle.getRowZone(0).getMark(2).setFilled()
    puzzle.getRowZone(0).getMark(3).setFilled()
    
    changes = [PuzzleChange(ZoneType.ROW, 0, slice(0, 4), PuzzleChangeAction.FILL)]
    newChanges = ChangeMinimizer.minimize(puzzle, changes)

    assert len(newChanges) == 1
    assert newChanges[0].getZoneSlice() == slice(0, 2)

def test_minimize_scenario8():
    """
    Tests that the minimize function returns the proper values

    A change on an already changed row returns a partial slice
    of the original if the slice affects items within an already 
    set slice in partial way. Example:

    Has: ?OO?
    Wants: OOOO
    Expect: Expects O--O
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
    puzzle.getRowZone(0).getMark(1).setFilled()
    puzzle.getRowZone(0).getMark(2).setFilled()
    
    changes = [PuzzleChange(ZoneType.ROW, 0, slice(0, 4), PuzzleChangeAction.FILL)]
    newChanges = ChangeMinimizer.minimize(puzzle, changes)

    assert len(newChanges) == 2
    assert newChanges[0].getZoneSlice() == slice(0, 1)
    assert newChanges[1].getZoneSlice() == slice(3, 4)