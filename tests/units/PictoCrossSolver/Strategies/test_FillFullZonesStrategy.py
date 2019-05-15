from PictoCrossSolver.Strategies import FillFullZonesStrategy
from PictoCrossSolver.Elements import Puzzle, Zone, Mark, PuzzleChangeAction

def test_apply_scenario1():
    """
    Tests that a zone with single full hint returns a change that fills that zone.

    This scenario sets a 4x4 to return 2 changes
    """

    # Build a simple puzzle
    puzzle = Puzzle(4, 4)
    puzzle.getRowZone(0).addHint(4)
    puzzle.getRowZone(1).addHint(3)
    puzzle.getRowZone(2).addHint(2)
    puzzle.getRowZone(3).addHint(1)
    puzzle.getColumnZone(0).addHint(4)
    puzzle.getColumnZone(1).addHint(3)
    puzzle.getColumnZone(2).addHint(2)
    puzzle.getColumnZone(3).addHint(1)
    
    # Apply the strategy
    strategy = FillFullZonesStrategy()
    changes = strategy.apply(puzzle)

    # There should be 2 changes
    assert len(changes) == 2

    # Both changes should be a single slice of 0, 4
    assert changes[0].getAction() == PuzzleChangeAction.FILL
    assert changes[0].getZoneSlice() == slice(0, 4)
    assert changes[1].getAction() == PuzzleChangeAction.FILL
    assert changes[1].getZoneSlice() == slice(0, 4)

def test_apply_scenario2():
    """
    Tests that a zone with enough hints to fill a zone returns
    those zones with changes.

    This scenario sets a 4x4 with this layout

      2
      1 3 2 1
    4 O O O O
    3 O O O X
    1 X O X X
    1 O X X X

    And it should return 1 (4) + 3 (2+x+1) changes!
    """

    # Build a simple puzzle
    puzzle = Puzzle(4, 4)
    puzzle.getRowZone(0).addHint(4)
    puzzle.getRowZone(1).addHint(3)
    puzzle.getRowZone(2).addHint(1)
    puzzle.getRowZone(3).addHint(1)
    puzzle.getColumnZone(0).addHint(2)
    puzzle.getColumnZone(0).addHint(1)
    puzzle.getColumnZone(1).addHint(3)
    puzzle.getColumnZone(2).addHint(2)
    puzzle.getColumnZone(3).addHint(1)
    
    # Apply the strategy
    strategy = FillFullZonesStrategy()
    changes = strategy.apply(puzzle)

    # There should be 11 changes, 3 for the main column and 1 for each row
    assert len(changes) == 4

    # Change 0 should be the 4 marks on row 0
    assert changes[0].getAction() == PuzzleChangeAction.FILL
    assert changes[0].getZoneSlice() == slice(0, 4)

    # Changes 1 to 3 should be 2 + x + 1 fills of column 0
    assert changes[1].getAction() == PuzzleChangeAction.FILL
    assert changes[1].getZoneSlice() == slice(0, 2)
    assert changes[2].getAction() == PuzzleChangeAction.CROSS
    assert changes[2].getZoneSlice() == slice(2, 3)
    assert changes[3].getAction() == PuzzleChangeAction.FILL
    assert changes[3].getZoneSlice() == slice(3, 4)