from __future__ import annotations
from abc import ABC, abstractmethod
from layer_util import Layer
from layer_util import get_layers
import layers
from data_structures.stack_adt import ArrayStack
from data_structures.abstract_list import List
from data_structures.array_sorted_list import ArraySortedList

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

        self.stack = ArrayStack(len(get_layers()) * 100)

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

        temp_stack = ArrayStack(len(get_layers()) * 100)
        
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

        Temp_1 = ArrayStack(len(get_layers()) * 100)
        Temp_2 = ArrayStack(len(get_layers()) * 100)

        while self.stack.is_empty() == False:
            Temp_1.push(self.stack.pop())

        while Temp_1.is_empty() == False:
            Temp_2.push(Temp_1.pop())

        while Temp_2.is_empty() == False:
            self.stack.push(Temp_2.pop())
        
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        """

        if self.stack.is_empty() == True:
            return start

        temp_stack = ArrayStack(len(get_layers()) * 100)
        
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

        valid_layer_count = 0

        for x in get_layers():
            if x != None:
                valid_layer_count += 1

        self.sequence = ArraySortedList(valid_layer_count)
        for x in get_layers():
            if x != None:
                x.key = x.index
                x.applied_status = False
                self.sequence.add(x)


    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        """

        if self.sequence[layer.key].applied_status == False:
            self.sequence[layer.key].applied_status = True
            return True
        else:
            return False

    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
        """

        if self.sequence[layer.key].applied_status == True:
            self.sequence[layer.key].applied_status = False
            return True
        else:
            return False

    def special(self):
        """
        Special mode. Different for each store implementation.
        """

        temp_list = ArraySortedList(len(get_layers()))
        for x in self.sequence:
            if x.applied_status == True:
                x.key = x.name
                temp_list.add(x)

        if len(temp_list) %2 == 0:
            temp_list.delete_at_index(len(temp_list)-1)

        while len(temp_list) != 1:
            temp_list.delete_at_index(0)
            temp_list.delete_at_index(len(temp_list)-1)
        
        temp_list[0].applied_status = False

        for x in self.sequence:
            x.key = x.index
        
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        """

        for a in self.sequence:
            if a.applied_status == True:
                start = a.apply(start, timestamp, x, y)
        return start

