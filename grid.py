from __future__ import annotations
from layer_store import SetLayerStore,AdditiveLayerStore,SequenceLayerStore
from data_structures.referential_array import ArrayR
import layers


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
        Initialise the grid object.
        - draw_style:
            The style with which colours will be drawn.
            Should be one of DRAW_STYLE_OPTIONS
            This draw style determines the LayerStore used on each grid square.
        - x, y: The dimensions of the grid.

        Should also intialise the brush size to the DEFAULT provided as a class variable.
        """
        self.special_status = False
        self.draw_style = draw_style
        self.x = x
        self.y = y
        self.brush_size = self.DEFAULT_BRUSH_SIZE

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

    def increase_brush_size(self):
        """
        Increases the size of the brush by 1,
        if the brush size is already MAX_BRUSH,
        then do nothing.
        """
        if self.brush_size < self.MAX_BRUSH:
            self.brush_size += 1

    def decrease_brush_size(self):
        """
        Decreases the size of the brush by 1,
        if the brush size is already MIN_BRUSH,
        then do nothing.
        """
        if self.brush_size > self.MIN_BRUSH:
            self.brush_size -= 1

    def special(self):
        """
        Activate the special affect on all grid squares.
        """
        self.special_status = not self.special_status
        for length in range(self.x):
            for width in range(self.y):
                self.grid[length][width].special()
    
    def __getitem__(self, index): 
        return self.grid[index]
    
    def paint(self, layer, x, y):
        """
        Paint the grid square at (x, y) with the given layer.
        Returns a PaintAction object.
        O Complexity = O(brush_size^2)
        """
        from action import PaintStep, PaintAction
        paint_action = PaintAction(is_special=self.special_status)
        for length in range(x - self.brush_size, x + self.brush_size + 1):
            for width in range(y - self.brush_size, y + self.brush_size + 1):
                if 0 <= length < self.x and 0 <= width < self.y and (abs(x - length) + abs(y - width)) <= self.brush_size:
                    if self.grid[length][width].add(layer) == True:
                        paint_action.add_step(PaintStep((length, width), layer))
        return paint_action
    
if __name__ == "__main__":
    from doctest import testmod
    testmod()