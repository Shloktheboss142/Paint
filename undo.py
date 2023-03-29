from __future__ import annotations
from action import PaintAction
from grid import Grid
from data_structures.stack_adt import ArrayStack

class UndoTracker:

    def __init__(self):
        """
        Initlaises two stacks, one for the action sequence and one for the undo sequence.

        Returns:
        - None

        Complexity:
        - Worst case: O(1), Since the length of the ArrayStack to be initialised is constant
            Number of operations is constant and doesnt rely on the size of the input
        - Best case: O(1), Since the length of the ArrayStack to be initialised is constant
            Number of operations is constant and doesnt rely on the size of the input

        Both best and worst happen when the stacks are initialised since there is no other option
        """
        self.action_sequence = ArrayStack(10000)                                # O(1)
        self.undo_sequence = ArrayStack(10000)                                  # O(1)

    def add_action(self, action: PaintAction) -> None:
        """
        Adds an action to the undo tracker.

        Args:
        - action: A PaintAction object to be added to the undo tracker
            - Type: PaintAction

        Returns:
        - None

        Complexity:
        - Worst case: O(1)
            Number of operations is constant and doesnt rely on the size of the input
        - Best case: O(1)
            Number of operations is constant and doesnt rely on the size of the input

        Both best and worst happen when either the stack is full or not full and hence the action is added or not added
        """
        if self.action_sequence.is_full() == False:                             # O(1)
            self.action_sequence.push(action)                                   # O(1)

    def undo(self, grid: Grid) -> PaintAction|None:
        """
        Undo's an action and adds it to the undo sequence.

        Args:
        - grid: The grid object to be modified
            - Type: Grid

        Returns:
        - None

                 OR 

        - PaintAction: The action that was undone
            - Type: PaintAction

        Complexity:
        - Worst case: O(mno log p), Where m is the length of the grid, n is the width of the grid, o is the number of layers in the grid and p is the number of steps in the action sequence
            Will only occur if the stack is not empty and the layer is SequenceLayerStore, since the complexity of the undo_apply method is O(mno log p) for the SequenceLayerStore
        - Best case: O(1)
            Will only occur if the stack is empty
        """
        if self.action_sequence.is_empty() == True:                             # O(1)
            return None                                                         # O(1)
        else:                                                                   # O(1)
            operation = self.action_sequence.pop()                              # O(1)
            self.undo_sequence.push(operation)                                  # O(1)
            operation.undo_apply(grid)                                          # O(mno log p)
            return operation                                                    # O(1)

    def redo(self, grid: Grid) -> PaintAction|None:
        """
        Redo's an action and adds it back to the action sequence.

        Args:
        - grid: The grid object to be modified
            - Type: Grid

        Returns:
        - None

                 OR 

        - PaintAction: The action that was redone
            - Type: PaintAction

        Complexity:
        - Worst case: O(mno log p), Where m is the length of the grid, n is the width of the grid, o is the number of layers in the grid and p is the number of steps in the action sequence
            Will only occur if the stack is not empty and the layer is SequenceLayerStore, since the complexity of the undo_apply method is O(mno log p) for the SequenceLayerStore
        - Best case: O(1)
            Will only occur if the stack is empty
        """
        if self.undo_sequence.is_empty() == True:                               # O(1)
            return None                                                         # O(1)
        else:                                                                   # O(1)
            operation = self.undo_sequence.pop()                                # O(1)
            self.action_sequence.push(operation)                                # O(1)
            operation.redo_apply(grid)                                          # O(mno log p)
            return operation                                                    # O(1)