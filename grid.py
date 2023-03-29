from __future__ import annotations
from layer_store import SetLayerStore, AdditiveLayerStore, SequenceLayerStore, LayerStore
from data_structures.referential_array import ArrayR
from layer_util import Layer

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

    def __init__(self, draw_style: DRAW_STYLE_OPTIONS, x: int, y: int) -> None:
        """
        Initialise the grid object and the brush size to the DEFAULT provided as a class variable.

        Args:
        - draw_style:
            The style with which colours will be drawn.
            This draw style determines the LayerStore used on each grid square.
        - x: The length of the grid
            Type: int
        - y: The width of the grid
            Type: int

        Returns:
        - None

        Complexity:
        - Worst case: O(mno), Where m is the length, n is the width and o is the length of the queue to be initialised in the Additive layer store
            Will only occur when the layer store being used is AdditiveLayerStore
        - Best case: O(mn), Where m is the number of rows and n is the number of columns
            Will only occur when the layer store being used is the SetLayerStore or SequenceLayerStore
        """
        self.special_status = False                                         # O(1)
        self.draw_style = draw_style                                        # O(1)
        self.x = x                                                          # O(1)
        self.y = y                                                          # O(1)
        self.brush_size = self.DEFAULT_BRUSH_SIZE                           # O(1)

        self.grid = ArrayR(self.x)                                          # O(n), Where n is the number of rows
        for length in range(self.x):                                        # O(n), Where n is the number of rows
            self.grid[length] = ArrayR(self.y)                              # O(m), Where m is the number of columns
            for width in range(self.y):                                     # O(m), Where m is the number of columns
                if self.draw_style == self.DRAW_STYLE_SET:                  # O(1)
                    self.grid[length][width] = SetLayerStore()              # O(1)
                elif self.draw_style == self.DRAW_STYLE_ADD:                # O(1)
                    self.grid[length][width] = AdditiveLayerStore()         # O(o), Where o is the length of the queue to be initialised
                elif self.draw_style == self.DRAW_STYLE_SEQUENCE:           # O(1)
                    self.grid[length][width] = SequenceLayerStore()         # O(1)

    def increase_brush_size(self) -> None:
        """
        Increases the size of the brush by 1,
        if the brush size is already MAX_BRUSH, then do nothing.

        Returns:
        - None

        Complexity:
        - Worst case: O(1)
            Number of operations is constant and doesnt rely on the size of the input
        - Best case: O(1)
            Number of operations is constant and doesnt rely on the size of the input
        """
        if self.brush_size < self.MAX_BRUSH:                                # O(1)
            self.brush_size += 1                                            # O(1)

    def decrease_brush_size(self) -> None:
        """
        Decreases the size of the brush by 1,
        if the brush size is already MIN.BRUSH, then do nothing.

        Returns:
        - None

        Complexity:
        - Worst case: O(1)
            Number of operations is constant and doesnt rely on the size of the input
        - Best case: O(1)
            Number of operations is constant and doesnt rely on the size of the input
        """
        if self.brush_size > self.MIN_BRUSH:                                # O(1)
            self.brush_size -= 1                                            # O(1)
 
    def special(self) -> None:
        """
        Activate the special affect on all grid squares.

        Returns:
        - None

        Complexity:
        - Worst case: O(mno log p), Where m is the number of rows, n is the number of columns, o is the number of layers in the program and p is the number of layers in the sorted list array
            Will only occur when the layer store being used is the SequenceLayerStore and there is at least one layer in the set
        - Best case: O(mn), Where m is the number of rows and n is the number of columns
            Will only occur when the layer store being used is the SetLayerStore
        """
        for length in range(self.x):                                        # O(n), Where n is the number of rows
            for width in range(self.y):                                     # O(m), Where m is the number of columns
                self.grid[length][width].special()                          # Best Case: O(1) Worst Case (n log m) Where n is number of layers in the program and m is the number of layers in the sorted list array

        return self.add_action(origin = 'special')                          # O(1)
    
    def __getitem__(self, index: int) -> LayerStore: 
        """
        Returns the layerstore at the given index.

        Args:
        - index: The index of the layerstore to be returned
            Type: int

        Returns:
        - LayerStore: The layerstore at the given index
            Type: LayerStore

        Complexity:
        - Worst case: O(1)
            Number of operations is constant and doesnt rely on the size of the input
        - Best case: O(1)
            Number of operations is constant and doesnt rely on the size of the input
        """
        return self.grid[index]                                             # O(1)
    
    def paint(self, layer: Layer, x: int, y: int) -> PaintAction:
        """
        Paint the grid square at (x, y) with the given layer.

        Args:
        - layer: The layer to be painted
            Type: Layer
        - x: The x coordinate of the grid square to be painted
            Type: int
        - y: The y coordinate of the grid square to be painted
            Type: int

        Returns:
        - None

        Complexity:
        - Worst case: O(n^2), Where n is the brush size
            Since duting the loops, the number of operations depends on the brush size
        - Best case: O(n^2), Where n is the brush size
            The worst and best case are both since duting the loops, the number of operations depends on the brush size
        """
        paint_action = self.add_action(origin = 'paint')                                                                        # O(1)
        for length in range(x - self.brush_size, x + self.brush_size + 1):                                                      # O(n) Where n is the brush size
            for width in range(y - self.brush_size, y + self.brush_size + 1):                                                   # O(n) Where n is the brush size
                if 0 <= length < self.x and 0 <= width < self.y and (abs(x - length) + abs(y - width)) <= self.brush_size:      # O(1)
                    if self.grid[length][width].add(layer) == True:                                                             # O(1)
                        paint_action.add_step(self.add_action(length = length, width = width, layer = layer))                   # O(1)

        return paint_action                                                                                                     # O(1)
    
    def add_action(self, origin: str = None, length: int = None, width: int = None, layer: Layer = None) -> None:
        """
        A function to to add either a paint action or a paint step to the paint action list.

        Args:
        - origin: a string that indicates whether to return a paint action/paint step or paint action with special enabled
            Type: string
        - length: the length of the grid square to be painted
            Type: int
        - width: the width of the grid square to be painted
            Type: int
        - layer: the layer to be added on the grid square
            Type: Layer

        Returns:
        - PaintAction: a paint action object
            Type: PaintAction

                OR

        - PaintStep: a paint step object
            Type: PaintStep

        Complexity:
        - Worst case: O(1)
            Number of operations is constant and doesnt rely on the size of the input
        - Best case: O(1)
            Number of operations is constant and doesnt rely on the size of the input
        """
        from action import PaintStep, PaintAction                       # O(1)
        if origin == 'special':                                         # O(1)
            return PaintAction(is_special=True)                         # O(1)
        elif origin == 'paint':                                         # O(1)
            return PaintAction()                                        # O(1)
        else:                                                           # O(1)
            return PaintStep((length, width), layer)                    # O(1)

    

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