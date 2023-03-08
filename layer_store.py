from __future__ import annotations
from abc import ABC, abstractmethod
from layer_util import Layer
import layers
from data_structures.stack_adt import ArrayStack
from data_structures.abstract_list import List

class LayerStore(ABC):

    def __init__(self) -> None:
        pass

    @abstractmethod
    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        """
        pass

    @abstractmethod
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        """
        pass

    @abstractmethod
    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
        """
        pass

    @abstractmethod
    def special(self):
        """
        Special mode. Different for each store implementation.
        """
        pass

class SetLayerStore(LayerStore):
    """
    Set layer store. A single layer can be stored at a time (or nothing at all)
    - add: Set the single layer.
    - erase: Remove the single layer. Ignore what is currently selected.
    - special: Invert the colour output.
    """

    def __init__(self) -> None:
        self.layer = None
        self.special_mode = False

    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        """
        if layer != self.layer:
            self.layer = layer
            return True
        return False

    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
        """
        if layer != None:
            self.layer = None
            return True
        return False

    def special(self):
        """
        Special mode. Different for each store implementation.
        """
        self.special_mode = not self.special_mode
        # self.grid.bg_color = (255, 255, 255) if self.special_mode else (0, 0, 0)
        
        
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        """
        if self.layer == None and self.special_mode == False:
            return start
        elif self.layer == None and self.special_mode == True:
            return layers.black.apply(start, timestamp, x, y)
        
        if self.special_mode == True:
            start = self.layer.apply(start, timestamp, x, y)
            return layers.invert.apply(start, timestamp, x, y)
        else:
            return self.layer.apply(start, timestamp, x, y)

class AdditiveLayerStore(LayerStore):
    """
    Additive layer store. Each added layer applies after all previous ones.
    - add: Add a new layer to be added last.
    - erase: Remove the first layer that was added. Ignore what is currently selected.
    - special: Reverse the order of current layers (first becomes last, etc.)
    """

    def __init__(self) -> None:
        self.stack = ArrayStack(100)
        self.special_mode = False

    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        """
        if self.stack.is_full() == False:
            self.stack.push(layer)
            return True
        else:
            return False
        
    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
        """
        temp_stack = ArrayStack(100)
        
        while self.stack.is_empty() == False:
            temp = self.stack.pop()
            temp_stack.push(temp)

        temp_stack.pop()

        while temp_stack.is_empty() == False:
            temp = temp_stack.pop()
            self.stack.push(temp)


    def special(self):
        """
        Special mode. Different for each store implementation.
        """
        tmp1 = ArrayStack(100)
        tmp2 = ArrayStack(100)

        while not self.stack.is_empty():
            tmp1.push(self.stack.pop())
        while not tmp1.is_empty():
            tmp2.push(tmp1.pop())
        while not tmp2.is_empty():
            self.stack.push(tmp2.pop())
        
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        """
        if self.stack.is_empty() == True:
            return start

        temp_stack = ArrayStack(100)
        
        while self.stack.is_empty() == False:
            temp = self.stack.pop()
            temp_stack.push(temp)

        while temp_stack.is_empty() == False:
            temp = temp_stack.pop()
            start = temp.apply(start, timestamp, x, y)
            self.stack.push(temp)

        return start

class SequenceLayerStore(LayerStore):
    """
    Sequential layer store. Each layer type is either applied / not applied, and is applied in order of index.
    - add: Ensure this layer type is applied.
    - erase: Ensure this layer type is not applied.
    - special:
        Of all currently applied layers, remove the one with median `name`.
        In the event of two layers being the median names, pick the lexicographically smaller one.
    """

    def __init__(self) -> None:
        self.layer = None
        self.specials = False

    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        """
        if layer != self.layer:
            self.layer = layer
            return True
        return False

    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
        """
        if layer != None:
            self.layer = None
            return True
        return False

    def special(self):
        """
        Special mode. Different for each store implementation.
        """
        self.specials = not self.specials
        # self.grid.bg_color = (255, 255, 255) if self.specials else (0, 0, 0)
        
        
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        """
        if self.layer == None:
            return start
        
        if self.specials == True:
            start = self.layer.apply(start, timestamp, x, y)
            return layers.invert.apply(start, timestamp, x, y)
        else:
            return self.layer.apply(start, timestamp, x, y)

if __name__ == "__main__":
    # s = AdditiveLayerStore()
    # s.add(layers.lighten)
    # s.add(layers.rainbow)
    # s.add(layers.black)
    # print(s.get_color((100, 100, 100), 0, 0, 0), (0, 0, 0))
    # s.special()
    # print(s.get_color((100, 100, 100), 7, 0, 0), (131, 254, 144))
    # s.erase(layers.lighten)
    # s.add(layers.lighten)
    # print(s.get_color((100, 100, 100), 7, 0, 0), (171, 255, 184))
    # s.special()
    # print(s.get_color((100, 100, 100), 7, 0, 0), (91, 214, 104))
    pass