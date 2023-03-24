from __future__ import annotations
from action import PaintAction
from grid import Grid
from data_structures.stack_adt import ArrayStack

class UndoTracker:

    def __init__(self):
        self.action_sequence = ArrayStack(10000)
        self.undo_sequence = ArrayStack(10000)

    def add_action(self, action: PaintAction) -> None:
        """
        Adds an action to the undo tracker.

        If your collection is already full,
        feel free to exit early and not add the action.
        """
        if self.action_sequence.is_full() == False:
            self.action_sequence.push(action)

    def undo(self, grid: Grid) -> PaintAction|None:
        """
        Undo an operation, and apply the relevant action to the grid.
        If there are no actions to undo, simply do nothing.

        :return: The action that was undone, or None.
        """
        if self.action_sequence.is_empty() == True:
            return None
        else:
            operation = self.action_sequence.pop()
            self.undo_sequence.push(operation)
            operation.undo_apply(grid)
            return operation

    def redo(self, grid: Grid) -> PaintAction|None:
        """
        Redo an operation that was previously undone.
        If there are no actions to redo, simply do nothing.

        :return: The action that was redone, or None.
        """
        if self.undo_sequence.is_empty() == True:
            return None
        else:
            operation = self.undo_sequence.pop()
            self.action_sequence.push(operation)
            operation.redo_apply(grid)
            return operation