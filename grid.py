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
        Initialise the grid object.
        - draw_style:
            The style with which colours will be drawn.
            Should be one of DRAW_STYLE_OPTIONS
            This draw style determines the LayerStore used on each grid square.
        - x, y: The dimensions of the grid.

        Should also intialise the brush size to the DEFAULT provided as a class variable.
        """
        
        self.draw_style = draw_style
        self.x = x
        self.y = y
        self.brush_size = self.DEFAULT_BRUSH_SIZE

        self.grid = ArrayR(self.x)
        for i in range(self.x):
            self.grid[i] = ArrayR(self.y)
            for j in range(self.y):
                if self.draw_style == self.DRAW_STYLE_SET:
                    self.grid[i][j] = SetLayerStore()
                elif self.draw_style == self.DRAW_STYLE_ADD:
                    self.grid[i][j] = AdditiveLayerStore()
                elif self.draw_style == self.DRAW_STYLE_SEQUENCE:
                    self.grid[i][j] = SequenceLayerStore()

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

        for i in range(self.x):
            for j in range(self.y):
                self.grid[i][j].special()
    
    def __getitem__(self, index):
            
        return self.grid[index]
    
    def paint(self, layer, x, y):

        for a in range(x - self.brush_size, x + self.brush_size + 1):
            for b in range(y - self.brush_size, y + self.brush_size + 1):
                if abs(x - a) + abs(y - b) <= self.brush_size and a >= 0 and a < self.x and b >= 0 and b < self.y:
                    self.grid[a][b].add(layer)