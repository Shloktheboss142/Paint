from __future__ import annotations
from layer_store import SetLayerStore,AdditiveLayerStore,SequenceLayerStore
from data_structures.referential_array import ArrayR

class Grid:
    DRAW_STYLE_SET = "SET"
    DRAW_STYLE_ADD = "ADD"
    DRAW_STYLE_SEQUENCE = "SEQUENCE"
    DRAW_STYLE_OPTIONS = (
        DRAW_STYLE_SET,
        DRAW_STYLE_ADD,
        DRAW_STYLE_SEQUENCE
    )

    DEFAULT_BRUSH_SIZE = 2
    MAX_BRUSH = 5
    MIN_BRUSH = 0

    def __init__(self, draw_style, x, y) -> None:
        """
        Initialise the grid object and the brush size to the DEFAULT provided as a class variable.

        Args:
        - draw_style:
            The style with which colours will be drawn.
            This draw style determines the LayerStore used on each grid square.
        - x, y: 
            The width and height of the grid, respectively.

        Returns:
        - None

        Complexity:
        - Worst case: O(mno), Where m is the length, n is the width and o is the length of the queue or sorted list initialised in the layer store
            Will only occur when the layer store being used is the SequenceLayerStore and AdditiveLayerStore
        - Best case: O(mn), Where m is the number of rows and n is the number of columns
            Will only occur when the layer store being used is the SetLayerStore
        """
        self.special_status = False                                         # O(1)
        self.draw_style = draw_style                                        # O(1)
        self.x = x                                                          # O(1)
        self.y = y                                                          # O(1)
        self.brush_size = self.DEFAULT_BRUSH_SIZE                           # O(1)

        self.grid = ArrayR(self.x) 
        for length in range(self.x):
            self.grid[length] = ArrayR(self.y)
            for width in range(self.y):
                if self.draw_style == self.DRAW_STYLE_SET:
                    self.grid[length][width] = SetLayerStore()
                elif self.draw_style == self.DRAW_STYLE_ADD:
                    self.grid[length][width] = AdditiveLayerStore()
                elif self.draw_style == self.DRAW_STYLE_SEQUENCE:
                    self.grid[length][width] = SequenceLayerStore()

    def increase_brush_size(self) -> None:
        """
        Increases the size of the brush by 1,
        if the brush size is already MAX_BRUSH, then do nothing.

        Returns:
        - None

        Complexity:
        - Worst case and Best case is O(1)
            Number of operations is constant and doesnt rely on the size of the input
        """
        if self.brush_size < self.MAX_BRUSH:
            self.brush_size += 1

    def decrease_brush_size(self) -> None:
        """
        Decreases the size of the brush by 1,
        if the brush size is already MIN.BRUSH, then do nothing.

        Returns:
        - None

        Complexity:
        - Worst case and Best case is O(1)
            Number of operations is constant and doesnt rely on the size of the input
        """
        if self.brush_size > self.MIN_BRUSH:
            self.brush_size -= 1

    def special(self) -> None:
        """
        Activate the special affect on all grid squares.
        """
        for length in range(self.x):
            for width in range(self.y):
                self.grid[length][width].special()
        return self.add_action(origin = 'special')
    
    def __getitem__(self, index): 
        return self.grid[index]
    
    def paint(self, layer, x, y):
        """
        Paint the grid square at (x, y) with the given layer.
        Returns a PaintAction object.
        O Complexity = O(brush_size^2)
        """
        """
        Paint the grid square at (x, y) with the given layer.
        if the brush size is already MAX_BRUSH, then do nothing.

        Returns:
        - None

        Complexity:
        - Worst case and best case is O(1)
            Number of operations is constant and doesnt rely on the size of the input
        """
        paint_action = self.add_action(origin = 'paint')
        for length in range(x - self.brush_size, x + self.brush_size + 1):
            for width in range(y - self.brush_size, y + self.brush_size + 1):
                if 0 <= length < self.x and 0 <= width < self.y and (abs(x - length) + abs(y - width)) <= self.brush_size:
                    if self.grid[length][width].add(layer) == True:
                        paint_action.add_step(self.add_action(length = length, width = width, layer = layer))
        return paint_action
    
    def add_action(self, origin = None, length = None, width = None, layer = None) -> None:
        """
        Add the given action to the grid.
        """
        from action import PaintStep, PaintAction
        if origin == 'special':
            return PaintAction(is_special=True)
        elif origin == 'paint':
            return PaintAction()
        else:
            return PaintStep((length, width), layer)

    

    """
    Multiply all the numbers in a list together.

    Args:
    - lst: a list of integers or floats

    Raises:
    - TypeError: if lst is not a list
    - ValueError: if lst is empty or contains non-numeric values

    Returns:
    - result: the product of all the numbers in the list, as a float

    Complexity:
    - Worst case: O(n), where n is the length of the list
    - Best case: O(n), same as worst case since we need to iterate over all the elements in the list
    """