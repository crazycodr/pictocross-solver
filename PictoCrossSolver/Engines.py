import logging
from typing import Callable, List

from PictoCrossSolver.Elements import Puzzle, PuzzleChange, PuzzleChangeAction
from PictoCrossSolver.Renderers import ConsoleRenderer
from PictoCrossSolver.Solvers import *
from PictoCrossSolver.Strategies import Strategy

class EventDrivenEngine:
    """
    This engine operates using an even driven pattern instead of a cyclic pattern that loops zones
    endlessly until it cannot find anything to do. This engine is more optimized although less
    predictible.

    The approach of this engine is through strategies instead of analyzers and solvers. Strategies
    are a combined, more complex object that will do both at the same time but using very precise
    algorithms instead of using wild guesses that we fix over runs.
    """

    def __init__(self):
        self._onApplyStrategy = None
        self._onAcceptChange = None
        self._onStrategyApplied = None
        self._onChangesApplied = None
        self._strategies = []

    def addStrategy(self, strategy: Strategy):
        """
        Adds a strategy to the engine. Strategies are the first level of solver guiding the whole
        solving process.
        """
        self._strategies.append(strategy)
    
    def onApplyStrategy(self, callback: Callable[[Puzzle, Strategy], bool]):
        """
        Saves the callback to use when the engine applies a strategy

        @param Callable[[Puzzle, Strategy], bool] callback to save
        """
        self._onApplyStrategy = callback
    
    def onAcceptChange(self, callback: Callable[[Puzzle, Strategy, PuzzleChange], bool]):
        """
        Saves the callback to use when approving a change

        @param Callable[[Puzzle, Strategy, PuzzleChange], bool] callback to save
        """
        self._onAcceptChange = callback
    
    def onStrategyApplied(self, callback: Callable[[Puzzle, Strategy, List[PuzzleChange]], bool]):
        """
        Saves the callback to use when validating if strategy should continue to be applied

        @param Callable[[Puzzle, Strategy, List[PuzzleChange]], bool] callback to save
        """
        self._onStrategyApplied = callback
    
    def onChangesApplied(self, callback: Callable[[Puzzle, Strategy], None]):
        """
        Saves the callback to use when changes have been applied by a strategy. Use this
        to generate viewable puzzle results. Remember to apply the changes before rendering!

        @param Callable[[Puzzle, Strategy], None] callback to save
        """
        self._onChangesApplied = callback
    
    def solve(self, puzzle: Puzzle) -> Puzzle :
        """
        Attempts to solve the puzzle by running various solvers on the puzzle

        @param Puzzle puzzle to solve

        @return Puzzle that was solved
        """

        # As long as we have strategies to run, run them in a loop
        while len(self._strategies) > 0:
        
            # Run each strategy one by one
            for strategy in self._strategies:

                # Apply the strategy on the puzzle with changes applied
                hasNewChanges = False
                for change in self.applyStrategy(puzzle.applyChanges(), strategy):
                    hasNewChanges = True
                    puzzle.addChange(change)
                
                # Notify that changes were applied
                if self._onChangesApplied and hasNewChanges:
                    self._onChangesApplied(puzzle, strategy)
        
        return puzzle

    def applyStrategy(self, puzzle: Puzzle, strategy: Strategy) -> List[PuzzleChange]:
        """
        Applies a strategy on a puzzle and returns the changes to add to the puzzle.
        
        This calls different callback events if set such as:
            - onApplyStrategy: Return True to allow strategy to run
            - onAcceptChange: Return True to accept a change to be applied to puzzle
            - onStrategyApplied: Return True to disable strategy from now on
        
        If there are no handlers, the code assumes True.
        
        If there are no accepted changes, the strategy is automatically disabled. You
        can override this by setting a "onStrategyApplied" handler instead which receives
        the puzzle and the changes.

        @param Puzzle puzzle to apply strategy to
        @param Strategy strategy to apply

        @return List[PuzzleChange] that strategy generated and handler approved
        """

        # Notify usage of strategy and exist if False
        if self._onApplyStrategy and not self._onApplyStrategy(puzzle, strategy):
            return []

        # Apply strategy and validate the changes
        acceptedChanges = []
        for change in strategy.apply(puzzle):

            # Validate the change is accepted and add it
            if self._onAcceptChange and not self._onAcceptChange(puzzle, strategy, change):
                continue
            acceptedChanges.append(change)

        # Notify usage of strategy and disable
        if self._onStrategyApplied and self._onStrategyApplied(puzzle, strategy, acceptedChanges):
            self.disableStrategy(strategy)
        elif len(acceptedChanges) == 0:
            self.disableStrategy(strategy)
        
        return acceptedChanges
    
    def disableStrategy(self, strategy: Strategy):
        """
        Disables strategy from engine so it doesn't get executed again.
        """
        self._strategies.remove(strategy)