from __future__ import annotations
from action import PaintAction
from grid import Grid
from data_structures.queue_adt import CircularQueue
from undo import UndoTracker

class ReplayTracker:

    def __init__(self):
        """
        Initlaises a queue to store the replay sequence.

        Returns:
        - None

        Complexity:
        - Worst case: O(1), Since the length of the CircularQueue to be initialised is constant
            Number of operations is constant and doesnt rely on the size of the input
        - Best case: O(1), Since the length of the CircularQueue to be initialised is constant
            Number of operations is constant and doesnt rely on the size of the input

        Both best and worst happen when the queue is initialised since there is no other option
        """
        self.replay_sequence = CircularQueue(10000)                                 # O(1), Since the length of the CircularQueue to be initialised is constant

    def start_replay(self) -> None:

        """-------------NOT USED-------------"""

        pass

    def add_action(self, action: PaintAction, is_undo: bool = False) -> None:
        """
        Adds an action to the replay. If the action is an undo action, it will be added to the undo sequence.

        Args:
        - action: A PaintAction object to be added to the replay
            - Type: PaintAction
        - is_undo: A boolean that specifies whether the action is an undo action or not
            - Type: bool

        Returns:
        - None

        Complexity:
        - Worst case: O(1)
            Number of operations is constant and doesnt rely on the size of the input
        - Best case: O(1)
            Number of operations is constant and doesnt rely on the size of the input
        
        Both best and worst happen when either the queue is full or not full and hence the action is added or not added
        """
        if is_undo == True:                                                         # O(1)
            undo_tracker = UndoTracker()                                            # O(1)
            undo_tracker.add_action(action)                                         # O(1)
            self.replay_sequence.append(undo_tracker)                               # O(1)
        else:                                                                       # O(1)
            self.replay_sequence.append(action)                                     # O(1)

    def play_next_action(self, grid: Grid) -> bool:
        """
        Plays the next replay action in the queue on the grid.

        Args:
        - grid: The grid object to be modified
            - Type: Grid

        Returns:
        - Boolean value that specifies whether there were no more actions to play or not
            A return value of True means that there were no more actions to play
            - Type: bool

        Complexity:
        - Worst case: O(mno log p), Where m is the length of the grid, n is the width of the grid, o is the number of layers in the grid and p is the number of steps in the action
            Will only occur if the stack is not empty and the layer is SequenceLayerStore, since the complexity of the undo_apply method is O(mno log p) for the SequenceLayerStore
        - Best case: O(1)
            Will only occur if the queue is empty
        """
        if self.replay_sequence.is_empty() == False:                                # O(1)
            replay_action = self.replay_sequence.serve()                            # O(1)
            if isinstance(replay_action, UndoTracker) == True:                      # O(1)
                replay_action.action_sequence.pop().undo_apply(grid)                # O(mno log p)
                return False                                                        # O(1)
            else:                                                                   # O(1)
                if isinstance(replay_action, PaintAction) == True:                  # O(1)
                    replay_action.redo_apply(grid)                                  # O(mno log p)
                    return False                                                    # O(1)
        else:                                                                       # O(1)
            return True                                                             # O(1)

if __name__ == "__main__":
    action1 = PaintAction([], is_special=True)
    action2 = PaintAction([])

    g = Grid(Grid.DRAW_STYLE_SET, 5, 5)

    r = ReplayTracker()
    # add all actions
    r.add_action(action1)
    r.add_action(action2)
    r.add_action(action2, is_undo=True)
    # Start the replay.
    r.start_replay()
    f1 = r.play_next_action(g) # action 1, special
    f2 = r.play_next_action(g) # action 2, draw
    f3 = r.play_next_action(g) # action 2, undo
    t = r.play_next_action(g)  # True, nothing to do.
    assert (f1, f2, f3, t) == (False, False, False, True)

