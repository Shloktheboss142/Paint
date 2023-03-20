from __future__ import annotations
from abc import ABC, abstractmethod
from layer_util import Layer
from layer_util import get_layers
import layers
from data_structures.stack_adt import ArrayStack
from data_structures.array_sorted_list import ArraySortedList, ListItem
from data_structures.queue_adt import CircularQueue

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

        self.queue = CircularQueue(len(get_layers()) * 100)

    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        """

        if self.queue.is_full() == False:
            self.queue.append(layer)
            return True
        else:
            return False
        
    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
        """

        if self.queue.is_empty() == False:
            self.queue.serve()
            return True
        return False


    def special(self):
        """
        Special mode. Different for each store implementation.
        """

        temp_stack = ArrayStack(len(get_layers()) * 100)

        for _ in range(self.queue.length):
            temp_stack.push(self.queue.serve())

        for _ in range(temp_stack.length):
            self.queue.append(temp_stack.pop())


        
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        """

        for _ in range(self.queue.length):
            layer_to_apply = self.queue.serve()
            start = layer_to_apply.apply(start, timestamp, x, y)
            self.queue.append(layer_to_apply)

        return start
    
class SequenceLayerStore(LayerStore):

    def __init__(self) -> None:
        valid_layer_count = 0

        for x in get_layers():
            if x != None:
                valid_layer_count += 1

        self.sequence = ArraySortedList(valid_layer_count)
        for x in get_layers():
            if x != None:
                self.sequence.add(ListItem(False, x.index))

    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        """
        if self.sequence[layer.index].value == False:
            self.sequence.delete_at_index(layer.index)
            self.sequence.add(ListItem(True, layer.index))
            return True
        return False

    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
        """
        if self.sequence[layer.index].value == True:
            self.sequence.delete_at_index(layer.index)
            self.sequence.add(ListItem(False, layer.index))
            return True
        return False

    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        """
        for x in range(self.sequence.length):
            if self.sequence[x].value == True:
                start = get_layers()[self.sequence[x].key].apply(start, timestamp, x, y)
        return start

    def special(self):
        """
        Special mode. Different for each store implementation.
        """

        temp_list = ArraySortedList(len(get_layers()))

        for x in range(self.sequence.length):
            if self.sequence[x].value == True:
                temp_list.add(ListItem(get_layers()[self.sequence[x].key], get_layers()[self.sequence[x].key].name))

        if temp_list.length == 0:
            return None
        elif temp_list.length == 1:
            # self.sequence.remove(temp_list[0].value)
            self.erase(temp_list[0].value)
            return 

        if len(temp_list) %2 == 0:
            temp_list.delete_at_index(len(temp_list)-1)

        self.erase(temp_list[len(temp_list) // 2].value)

if __name__=='__main__':
    pass