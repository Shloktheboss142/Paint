from __future__ import annotations
from action import PaintAction
from grid import Grid
from data_structures.stack_adt import ArrayStack

class UndoTracker:

    def __init__(self):
        self.action_sequence = ArrayStack(10000)
        self.unodSequence = ArrayStack(10000)
        # self.recently_undone = None

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
        if self.action_sequence.is_empty():
            return None
        action_to_undo = self.action_sequence.pop()
        self.unodSequence.push(action_to_undo)
        action_to_undo.undo_apply(grid)
        return action_to_undo

    def redo(self, grid: Grid) -> PaintAction|None:
        """
        Redo an operation that was previously undone.
        If there are no actions to redo, simply do nothing.

        :return: The action that was redone, or None.
        """
        if self.action_sequence.is_empty():
            return None
        action_to_redo = self.unodSequence.pop()
        self.action_sequence.push(action_to_redo)
        action_to_redo.redo_apply(grid)
        return action_to_redo