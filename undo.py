from __future__ import annotations
from action import PaintAction
from grid import Grid
from data_structures.stack_adt import ArrayStack

class UndoTracker:

    def __init__(self):
        self.action_sequence = ArrayStack(10000)
        self.unodSequence = ArrayStack(10000)

    def add_action(self, action: PaintAction) -> None:
        """
        Adds an action to the undo tracker.

        If your collection is already full,
        feel free to exit early and not add the action.
        """
        self.action_sequence.push(action)

    def undo(self, grid: Grid) -> PaintAction|None:
        """
        Undo an operation, and apply the relevant action to the grid.
        If there are no actions to undo, simply do nothing.

        :return: The action that was undone, or None.
        """
        if self.action_sequence.is_empty():
            return None
        self.unodSequence.push(self.action_sequence.pop())
        self.unodSequence.peek().undo_apply(grid)
        return self.unodSequence.peek()

    def redo(self, grid: Grid) -> PaintAction|None:
        """
        Redo an operation that was previously undone.
        If there are no actions to redo, simply do nothing.

        :return: The action that was redone, or None.
        """
        if self.unodSequence.is_empty():
            return None
        self.action_sequence.push(self.unodSequence.pop())
        self.action_sequence.peek().redo_apply(grid)
        return self.action_sequence.peek()