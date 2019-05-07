from PictoCrossSolver.Renderers import SolutionRenderer
from PictoCrossSolver.Elements import Grid, Zone, Mark

def test_render_scenario1():
    """
    Tests that the rendering to a list of strings behaves as expected
    """

    grid = Grid(4, 4)

    grid.getRowZone(0).getMark(0).setFilled()
    grid.getRowZone(0).getMark(1).setAmbiguous()
    grid.getRowZone(0).getMark(2).setAmbiguous()
    grid.getRowZone(0).getMark(3).setFilled()

    grid.getRowZone(1).getMark(0).setAmbiguous()
    grid.getRowZone(1).getMark(1).setCrossed()
    grid.getRowZone(1).getMark(2).setCrossed()
    grid.getRowZone(1).getMark(3).setAmbiguous()

    grid.getRowZone(2).getMark(0).setFilled()
    grid.getRowZone(2).getMark(1).setAmbiguous()
    grid.getRowZone(2).getMark(2).setFilled()
    grid.getRowZone(2).getMark(3).setAmbiguous()

    grid.getRowZone(3).getMark(0).setAmbiguous()
    grid.getRowZone(3).getMark(1).setCrossed()
    grid.getRowZone(3).getMark(2).setAmbiguous()
    grid.getRowZone(3).getMark(3).setCrossed()

    renderer = SolutionRenderer(grid)
    
    assert renderer.render() == [
        '█  █',
        ' XX ',
        '█ █ ',
        ' X X'
    ]