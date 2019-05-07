from PictoCrossSolver.Loaders import TextLoader
import os

def test_load_scenario1():
    """
    Tests that scenario1 is loaded properly, 8x8 square, multiple hints
    """

    obj = TextLoader()
    grid = obj.load(os.path.dirname(os.path.abspath(__file__)) + "/scenario1.txt")

    assert len(grid.getRowZones()) == 8
    assert len(grid.getColumnZones()) == 8

    assert grid.getColumnZone(0).getHints() == [1]
    assert grid.getColumnZone(1).getHints() == [2, 1]
    assert grid.getColumnZone(2).getHints() == [3, 3]
    assert grid.getColumnZone(3).getHints() == [3, 4]
    assert grid.getColumnZone(4).getHints() == [8]
    assert grid.getColumnZone(5).getHints() == [7]
    assert grid.getColumnZone(6).getHints() == [7]
    assert grid.getColumnZone(7).getHints() == [2, 2]

    assert grid.getRowZone(0).getHints() == [8]
    assert grid.getRowZone(1).getHints() == [7]
    assert grid.getRowZone(2).getHints() == [5]
    assert grid.getRowZone(3).getHints() == [3]
    assert grid.getRowZone(4).getHints() == [5]
    assert grid.getRowZone(5).getHints() == [6]
    assert grid.getRowZone(6).getHints() == [6]
    assert grid.getRowZone(7).getHints() == [3]

def test_load_scenario2():
    """
    Tests that scenario2 is loaded properly, non square, multiple-hints
    Scenario built from scratch, not necessarily solvable
    """

    obj = TextLoader()
    grid = obj.load(os.path.dirname(os.path.abspath(__file__)) + "/scenario2.txt")

    assert len(grid.getRowZones()) == 4
    assert len(grid.getColumnZones()) == 7

    assert grid.getColumnZone(0).getHints() == [1]
    assert grid.getColumnZone(1).getHints() == [4]
    assert grid.getColumnZone(2).getHints() == [3, 1]
    assert grid.getColumnZone(3).getHints() == [2, 2]
    assert grid.getColumnZone(4).getHints() == [4]
    assert grid.getColumnZone(5).getHints() == [2]
    assert grid.getColumnZone(6).getHints() == [1]

    assert grid.getRowZone(0).getHints() == [4]
    assert grid.getRowZone(1).getHints() == [7]
    assert grid.getRowZone(2).getHints() == [5]
    assert grid.getRowZone(3).getHints() == [3]