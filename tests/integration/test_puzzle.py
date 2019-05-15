# from PictoCrossSolver.Engines import FirstEngine
# from PictoCrossSolver.Renderers import SolutionRenderer
# from PictoCrossSolver.Solvers import *
# from PictoCrossSolver.Readers import TextPuzzleReader

# import os

# def test_bpc_animals_1_2():
#     """
#     Integration test for specific puzzle in Biggest Picture Cross - Animals - Puzzle 1,2
#     """
    
#     # Load the puzzle and solution in memory
#     puzzle = TextPuzzleReader.load(os.path.dirname(__file__) + '/puzzles/biggest-picture-cross/animals/puzzle-1-2.txt')
#     with open(os.path.dirname(__file__) + '/puzzles/biggest-picture-cross/animals/solution-1-2.txt', 'r') as solutionStream:
#         solution = solutionStream.readlines()
#         for index, line in enumerate(solution):
#             solution[index] = line.strip()
    
#     # Solve the puzzle
#     puzzle = FirstEngine.solve(puzzle)

#     # Get the solution representation in memory and compare with loaded solution
#     solutionRenderer = SolutionRenderer(puzzle)
#     liveSolution = solutionRenderer.render()
#     assert liveSolution == solution

# def test_bpc_animals_3_1():
#     """
#     Integration test for specific puzzle in Biggest Picture Cross - Animals - Puzzle 3,1
#     """
    
#     # Load the puzzle and solution in memory
#     puzzle = TextPuzzleReader.load(os.path.dirname(__file__) + '/puzzles/biggest-picture-cross/animals/puzzle-3-1.txt')
#     with open(os.path.dirname(__file__) + '/puzzles/biggest-picture-cross/animals/solution-3-1.txt', 'r') as solutionStream:
#         solution = solutionStream.readlines()
#         for index, line in enumerate(solution):
#             solution[index] = line.strip()
    
#     # Solve the puzzle
#     puzzle = FirstEngine.solve(puzzle)

#     # Get the solution representation in memory and compare with loaded solution
#     solutionRenderer = SolutionRenderer(puzzle)
#     liveSolution = solutionRenderer.render()
#     assert liveSolution == solution

# def test_bpc_animals_4_3():
#     """Puzzle
#     Integration test for specific puzzle in Biggest Picture Cross - Animals - Puzzle 4,3
#     """
    
#     # Load the puzzle and solution in memory
#     puzzle = TextPuzzleReader.load(os.path.dirname(__file__) + '/puzzles/biggest-picture-cross/animals/puzzle-4-3.txt')
#     with open(os.path.dirname(__file__) + '/puzzles/biggest-picture-cross/animals/solution-4-3.txt', 'r') as solutionStream:
#         solution = solutionStream.readlines()
#         for index, line in enumerate(solution):
#             solution[index] = line.strip()
    
#     # Solve the puzzle
#     puzzle = FirstEngine.solve(puzzle)

#     # Get the solution representation in memory and compare with loaded solution
#     solutionRenderer = SolutionRenderer(puzzle)
#     liveSolution = solutionRenderer.render()
#     assert liveSolution == solution

# def test_bpc_animals_5_2():
#     """
#     Integration test for specific puzzle in Biggest Picture Cross - Animals - Puzzle 5,2
#     """
    
#     # Load the puzzle and solution in memory
#     puzzle = TextPuzzleReader.load(os.path.dirname(__file__) + '/puzzles/biggest-picture-cross/animals/puzzle-5-2.txt')
#     with open(os.path.dirname(__file__) + '/puzzles/biggest-picture-cross/animals/solution-5-2.txt', 'r') as solutionStream:
#         solution = solutionStream.readlines()
#         for index, line in enumerate(solution):
#             solution[index] = line.strip()
    
#     # Solve the puzzle
#     puzzle = FirstEngine.solve(puzzle)

#     #Puzzle the solution representation in memory and compare with loaded solution
#     solutionRenderer = SolutionRenderer(puzzle)
#     liveSolution = solutionRenderer.render()
#     assert liveSolution == solutionPuzzle