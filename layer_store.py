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

        self.active_layer = None
        self.special_mode_status = False

    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        """

        if self.active_layer != layer or self.active_layer == None:
            self.active_layer = layer
            return True
        return False
    
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        """

        if self.active_layer == None and self.special_mode_status == False:
            return start
        elif self.active_layer == None and self.special_mode_status == True:
            return layers.black.apply(start, timestamp, x, y)
        
        if self.special_mode_status == True:
            start = self.active_layer.apply(start, timestamp, x, y)
            return layers.invert.apply(start, timestamp, x, y)
        else:
            return self.active_layer.apply(start, timestamp, x, y)

    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
        """

        if self.active_layer != None:
            self.active_layer = None
            return True
        return False

    def special(self):
        """
        Special mode. Different for each store implementation.
        """

        self.special_mode_status = not self.special_mode_status

class AdditiveLayerStore(LayerStore):
    """
    Additive layer store. Each added layer applies after all previous ones.
    - add: Add a new layer to be added last.
    - erase: Remove the first layer that was added. Ignore what is currently selected.
    - special: Reverse the order of current layers (first becomes last, etc.)
    """

    def __init__(self) -> None:

        self.layer_sequence = CircularQueue(len(get_layers()) * 100)

    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        """

        if self.layer_sequence.is_full() == False:
            self.layer_sequence.append(layer)
            return True
        else:
            return False
        
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        """

        for _ in range(self.layer_sequence.length):
            layer_to_apply = self.layer_sequence.serve()
            start = layer_to_apply.apply(start, timestamp, x, y)
            self.layer_sequence.append(layer_to_apply)

        return start
        
    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
        """

        if self.layer_sequence.is_empty() == False:
            self.layer_sequence.serve()
            return True
        return False

    def special(self):
        """
        Special mode. Different for each store implementation.
        """

        temp_layer_stack = ArrayStack(len(get_layers()) * 100)

        for _ in range(self.layer_sequence.length):
            temp_layer_stack.push(self.layer_sequence.serve())

        for _ in range(temp_layer_stack.length):
            self.layer_sequence.append(temp_layer_stack.pop())
    
class SequenceLayerStore(LayerStore):
    """
    Sequence layer store. Layers are either 'enabled' or 'disabled'.
    - add: 'Enables' the layer.
    - erase: 'Disables' the layer.
    - special: Order all the active layers lexiographically and 'disable' the centre one.
    """

    def __init__(self) -> None:

        valid_layer_count = 0

        for number_of_layers in get_layers():
            if number_of_layers != None:
                valid_layer_count += 1

        self.layer_list = ArraySortedList(valid_layer_count)
        
        for layer in get_layers():
            if layer != None:
                self.layer_list.add(ListItem(False, layer.index))

    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerS\tore was actually changed.
        """
        
        if self.layer_list[layer.index].value == False:
            self.layer_list.delete_at_index(layer.index)
            self.layer_list.add(ListItem(True, layer.index))
            return True
        return False
    
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        """

        for index in range(self.layer_list.length):
            if self.layer_list[index].value == True:
                start = get_layers()[self.layer_list[index].key].apply(start, timestamp, x, y)
        return start

    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
        """

        if self.layer_list[layer.index].value == True:
            self.layer_list.delete_at_index(layer.index)
            self.layer_list.add(ListItem(False, layer.index))
            return True
        return False

    def special(self):
        """
        Special mode. Different for each store implementation.
        """

        temp_list = ArraySortedList(len(get_layers()))

        for index in range(self.layer_list.length):
            if self.layer_list[index].value == True:
                item_key = get_layers()[self.layer_list[index].key]
                item_name = get_layers()[self.layer_list[index].key].name
                temp_list.add(ListItem(item_key, item_name))

        if temp_list.length == 0:
            return None
        elif temp_list.length == 1:
            self.erase(temp_list[0].value)
            return None

        if temp_list.length % 2 == 0:
            temp_list.delete_at_index(temp_list.length - 1)

        self.erase(temp_list[temp_list.length // 2].value)