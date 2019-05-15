from PictoCrossSolver.Renderers import SolutionRenderer
from PictoCrossSolver.Elements import Puzzle, Zone, Mark

def test_render_scenario1():
    """
    Tests that the rendering to a list of strings behaves as expected
    """

    puzzle = Puzzle(4, 4)

    puzzle.getRowZone(0).getMark(0).setFilled()
    puzzle.getRowZone(0).getMark(1).setAmbiguous()
    puzzle.getRowZone(0).getMark(2).setAmbiguous()
    puzzle.getRowZone(0).getMark(3).setFilled()

    puzzle.getRowZone(1).getMark(0).setAmbiguous()
    puzzle.getRowZone(1).getMark(1).setCrossed()
    puzzle.getRowZone(1).getMark(2).setCrossed()
    puzzle.getRowZone(1).getMark(3).setAmbiguous()

    puzzle.getRowZone(2).getMark(0).setFilled()
    puzzle.getRowZone(2).getMark(1).setAmbiguous()
    puzzle.getRowZone(2).getMark(2).setFilled()
    puzzle.getRowZone(2).getMark(3).setAmbiguous()

    puzzle.getRowZone(3).getMark(0).setAmbiguous()
    puzzle.getRowZone(3).getMark(1).setCrossed()
    puzzle.getRowZone(3).getMark(2).setAmbiguous()
    puzzle.getRowZone(3).getMark(3).setCrossed()

    renderer = SolutionRenderer(puzzle)
    
    assert renderer.render() == [
        '█  █',
        ' XX ',
        '█ █ ',
        ' X X'
    ]