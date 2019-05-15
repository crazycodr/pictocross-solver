from PictoCrossSolver.Readers import TextPuzzleReader
import os

def test_load_scenario1():
    """
    Tests that scenario1 is loaded properly, 8x8 square, multiple hints
    """

    obj = TextPuzzleReader()
    puzzle = obj.load(os.path.dirname(os.path.abspath(__file__)) + "/scenario1.txt")

    assert len(puzzle.getRowZones()) == 8
    assert len(puzzle.getColumnZones()) == 8

    assert puzzle.getColumnZone(0).getHints() == [1]
    assert puzzle.getColumnZone(1).getHints() == [2, 1]
    assert puzzle.getColumnZone(2).getHints() == [3, 3]
    assert puzzle.getColumnZone(3).getHints() == [3, 4]
    assert puzzle.getColumnZone(4).getHints() == [8]
    assert puzzle.getColumnZone(5).getHints() == [7]
    assert puzzle.getColumnZone(6).getHints() == [7]
    assert puzzle.getColumnZone(7).getHints() == [2, 2]

    assert puzzle.getRowZone(0).getHints() == [8]
    assert puzzle.getRowZone(1).getHints() == [7]
    assert puzzle.getRowZone(2).getHints() == [5]
    assert puzzle.getRowZone(3).getHints() == [3]
    assert puzzle.getRowZone(4).getHints() == [5]
    assert puzzle.getRowZone(5).getHints() == [6]
    assert puzzle.getRowZone(6).getHints() == [6]
    assert puzzle.getRowZone(7).getHints() == [3]

def test_load_scenario2():
    """
    Tests that scenario2 is loaded properly, non square, multiple-hints
    Scenario built from scratch, not necessarily solvable
    """

    obj = TextPuzzleReader()
    puzzle = obj.load(os.path.dirname(os.path.abspath(__file__)) + "/scenario2.txt")

    assert len(puzzle.getRowZones()) == 4
    assert len(puzzle.getColumnZones()) == 7

    assert puzzle.getColumnZone(0).getHints() == [1]
    assert puzzle.getColumnZone(1).getHints() == [4]
    assert puzzle.getColumnZone(2).getHints() == [3, 1]
    assert puzzle.getColumnZone(3).getHints() == [2, 2]
    assert puzzle.getColumnZone(4).getHints() == [4]
    assert puzzle.getColumnZone(5).getHints() == [2]
    assert puzzle.getColumnZone(6).getHints() == [1]

    assert puzzle.getRowZone(0).getHints() == [4]
    assert puzzle.getRowZone(1).getHints() == [7]
    assert puzzle.getRowZone(2).getHints() == [5]
    assert puzzle.getRowZone(3).getHints() == [3]