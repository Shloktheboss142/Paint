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
        """
        Initlaises active layer to None and special mode status to False

        Returns:
        - None

        Complexity:
        - Worst case and Best case is O(1):
            Number of operations is constant and doesnt rely on the size of the input
        """
        self.active_layer = None                                                                    # O(1)
        self.special_mode_status = False                                                            # O(1)

    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.

        Args:
        - layer: The layer to add to the grid square

        Returns:
        - Boolean value of True is the layer was added to the grid square, False if the layer was not added to the grid square

        Complexity:
        - Worst case and Best case is O(1):
            Number of operations is constant and doesnt rely on the size of the input
        """
        if self.active_layer != layer or self.active_layer == None:                                 # O(1)
            self.active_layer = layer                                                               # O(1)
            return True                                                                             # O(1)
        return False                                                                                # O(1)
    
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Calculating the color that the grid square should display

        Args:
        - start: The color that is currently on the grid square
        - timestamp: Used for layers that change over time (Such as rainbow and sparkle)
        - x: Used for layers that change over time (Such as rainbow and sparkle)
        - y: Used for layers that change over time (Such as rainbow and sparkle)

        Returns:
        - A tuple containing the RGB value that the layer square should display

        Complexity:
        - Worst case: O(n), Where n is the timestamp
            Will only happen if the layer being applied is sparkle
        - Best case: O(1)
            Will occur when there is no active layer and special is not active
        """
        if self.active_layer == None and self.special_mode_status == False:                         # O(1)
            return start                                                                            # O(1)
        elif self.active_layer == None and self.special_mode_status == True:                        # O(1)
            return layers.black.apply(start, timestamp, x, y)                                       # O(1)
        
        if self.special_mode_status == True:                                                        # O(1)
            start = self.active_layer.apply(start, timestamp, x, y)                                 # O(1) / O(n) Where n is the timestamp for the sparkle layer
            return layers.invert.apply(start, timestamp, x, y)                                      # O(1)
        else:                                                                                       # O(1)
            return self.active_layer.apply(start, timestamp, x, y)                                  # O(1) / O(n) Where n is the timestamp for the sparkle layer

    def erase(self, layer: Layer) -> bool:
        """
        Erases the layer that is currently in the grid square

        Args:
        - layer: The layer to be removed from the grid square

        Returns:
        - Boolean value of True is the layer was eaased from the grid square, False if there is no layer in the grid square

        Complexity:
        - Worst case and Best case is O(1):
            Number of operations is constant and doesnt rely on the size of the input
        """
        if self.active_layer != None:                                                               # O(1)
            self.active_layer = None                                                                # O(1)
            return True                                                                             # O(1)
        return False                                                                                # O(1)

    def special(self) -> None:
        """
        Activates the special mode for the grid square

        Returns:
        - None

        Complexity:
        - Worst case and Best case is O(1):
            Number of operations is constant and doesnt rely on the size of the input
        """
        self.special_mode_status = not self.special_mode_status                 # O(1)

class AdditiveLayerStore(LayerStore):
    """
    Additive layer store. Each added layer applies after all previous ones.
    - add: Add a new layer to be added last.
    - erase: Remove the first layer that was added. Ignore what is currently selected.
    - special: Reverse the order of current layers (first becomes last, etc.)
    """

    def __init__(self) -> None:
        """
        Initialises a queue to store the layers added

        Returns:
        - None

        Complexity:
        - Worst case and Best case is O(n):
            Where n is the length of the queue
        """
        self.layer_sequence = CircularQueue(len(get_layers()) * 100)                                # O(n) Where n is the length of the queue

    def add(self, layer: Layer) -> bool:
        """
        Adds a layer to the layers queue

        Args:
        - layer: The layer to be added to the queue

        Returns:
        - Boolean value of True is the layer was added to the queue, False if the layer was not added to the queue due to the queue being full

        Complexity:
        - Worst case and Best case is O(1):
            Where n is the length of the queue
        """
        if self.layer_sequence.is_full() == False:                                                  # O(1)
            self.layer_sequence.append(layer)                                                       # O(1)
            return True                                                                             # O(1)
        else:                                                                                       # O(1)
            return False                                                                            # O(1)
        
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.

        Args:
        - start: The color that is currently on the grid square
        - timestamp: Used for layers that change over time (Such as rainbow and sparkle)
        - x: Used for layers that change over time (Such as rainbow and sparkle)
        - y: Used for layers that change over time (Such as rainbow and sparkle)

        Returns:
        - A tuple containing the RGB value that the layer square should display

        Complexity:
        - Worst case and Best case: O(nm), Where n is the length of the layer sequence, and n is the timestamp
            Since the 
        """
        for _ in range(len(self.layer_sequence)):                                                   # O(n) Where n is the length of the layer sequence
            layer_to_apply = self.layer_sequence.serve()                                            # O(1)
            start = layer_to_apply.apply(start, timestamp, x, y)                                    # O(1) / O(m) Where m is the timestamp for the sparkle layer
            self.layer_sequence.append(layer_to_apply)                                              # O(1)

        return start                                                                                # O(1)
        
    def erase(self, layer: Layer) -> bool:
        """
        Erases the first layer that was addede to the layer sequence queue

        Args:
        - layer: The layer to be removed from the grid square

        Returns:
        - Boolean value of True is the layer was eaased from the grid square, False if there is no layer in the grid square

        Complexity:
        - Worst case and Best case is O(1):
            Number of operations is constant and doesnt rely on the size of the input
        """

        if self.layer_sequence.is_empty() == False:                                                 # O(1)
            self.layer_sequence.serve()                                                             # O(1)
            return True                                                                             # O(1)
        return False                                                                                # O(1)

    def special(self) -> None:
        """
        Special mode. Different for each store implementation.
        """
        """
        Reverses the order of layers in the layer sequence queue

        Returns:
        - None

        Complexity:
        - Worst case: O(nm), Where n is the number of layers in the program and m is the number of layers in the layer sequence queue
            Happens when there is at least one layer in the layer sequence queue
        - Best case: O(n), Where n is the number of layers in the program
            Happens when there are no layers in the layer sequence queue
        """
        temp_layer_stack = ArrayStack(len(get_layers()) * 100)                                      # O(n) Where n is the number of layers in the program

        for _ in range(len(self.layer_sequence)):                                                   # O(m) Where m is the number of layers in the layer sequence queue
            temp_layer_stack.push(self.layer_sequence.serve())                                      # O(1)

        for _ in range(len(temp_layer_stack)):                                                      # O(m) Where m is the number of layers in the layer sequence queue
            self.layer_sequence.append(temp_layer_stack.pop())                                      # O(1)
    
class SequenceLayerStore(LayerStore):
    """
    Sequence layer store. Layers are either 'enabled' or 'disabled'.
    - add: 'Enables' the layer.
    - erase: 'Disables' the layer.
    - special: Order all the active layers lexiographically and 'disable' the centre one.
    """

    def __init__(self) -> None:
        """
        Initialises a sorted list to store the layers added

        Returns:
        - None

        Complexity:
        - Worst case: O(log n), Where n is the 
            where log(n) occurs when a layer is added into the array sorted list, 
            and the position of the index is to be found using the function _index_to_add, which iterates 
            logarithmically, because it involves halving the number of elements in an array
        - Best case: O(1), which occurs when the value of the layer is already True, which means it is 
            already "applying", in this case, nothing is changed and False is returned immediately
        """
        valid_layer_count = 0                                                                       # O(1)

        for number_of_layers in get_layers():                                                       # O(n) Where n is the number of layers in the program
            if number_of_layers != None:                                                            # O(1)
                valid_layer_count += 1                                                              # O(1)

        self.layer_list = ArraySortedList(valid_layer_count)                                        # O(m) Where n is the number of layers in the program
        
        for layer in get_layers():                                                                  # O(n) Where n is the number of layers in the program
            if layer != None:                                                                       # O(1)
                self.layer_list.add(ListItem(False, layer.index))                                   # O(log n) Where n is the length of the sorted list

    def add(self, layer: Layer) -> bool:
        """
        Enables the given layer

        Args:
        - layer: The layer to be enabled

        Returns:
        - Boolean value of True is the layer was enables, False if the layer already enabled

        Complexity:
        - Worst case: O(n), Where n is the length of the sorted list array
            Happens when the layer trying to be added is not yet enabled
        - Best case: O(1)
            Happens when the layer trying to be added is already enabled
        """
        if self.layer_list[layer.index].value == False:                                             # O(1)
            self.layer_list.delete_at_index(layer.index)                                            # O(n)
            self.layer_list.add(ListItem(True, layer.index))                                        # O(log n)
            return True                                                                             # O(1)
        return False                                                                                # O(1)
    
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current enabled layers.

        Args:
        - start: The color that is currently on the grid square
        - timestamp: Used for layers that change over time (Such as rainbow and sparkle)
        - x: Used for layers that change over time (Such as rainbow and sparkle)
        - y: Used for layers that change over time (Such as rainbow and sparkle)

        Returns:
        - A tuple containing the RGB value that the layer square should display

        Complexity:
        - Worst case and Best case: O(nm), Where n is the length of the layer sequence, and n is the timestamp
            Since the 
        """
        for index in range(len(self.layer_list)):                                                   # O(n) Where n is the length of the sorted list array
            if self.layer_list[index].value == True:                                                # O(1)
                start = get_layers()[self.layer_list[index].key].apply(start, timestamp, x, y)      # O(1) / O(m) Where m is the timestamp for the sparkle layer
        return start                                                                                # O(1)

    def erase(self, layer: Layer) -> bool:
        """
        Disables the given layer

        Args:
        - layer: The layer to be disabled

        Returns:
        - Boolean value of True is the layer was enables, False if the layer already enabled

        Complexity:
        - Worst case: O(n), Where n is the length of the sorted list array
            Happens when the layer trying to be diabled is hasn't been disabled yet
        - Best case: O(1)
            Happens when the layer trying to be disabled is already disabled
        """
        if self.layer_list[layer.index].value == True:                                              # O(1)
            self.layer_list.delete_at_index(layer.index)                                            # O(n)
            self.layer_list.add(ListItem(False, layer.index))                                       # O(log n)
            return True                                                                             # O(1)
        return False                                                                                # O(1)

    def special(self) -> None:
        """
        Arranges the enabled layers lexigraphically and disables the middle layer

        Returns:
        - None

        Complexity:
        - Worst case: O(n), Where n is the length of the sorted list array
            Happens when the layer trying to be diabled is hasn't been disabled yet
        - Best case: O(1)
            Happens when the layer trying to be disabled is already disabled
        """
        temp_list = ArraySortedList(len(self.layer_list))                                           # O(n) Where n is the number of layers

        for index in range(len(self.layer_list)):                                                   # O(n) Where n is the length of the layer list
            if self.layer_list[index].value == True:                                                # O(1)
                item_key = get_layers()[self.layer_list[index].key]                                 # O(1)
                item_name = get_layers()[self.layer_list[index].key].name                           # O(1)
                temp_list.add(ListItem(item_key, item_name))                                        # O(log m) Where m is the length of the temp list

        if temp_list.is_empty() == True:                                                            # O(1)
            return None                                                                             # O(1)
        elif len(temp_list) == 1:                                                                   # O(1)
            self.erase(temp_list[0].value)                                                          # O(n), Where n is the number of layers
            return None                                                                             # O(1)

        if len(temp_list) % 2 == 0:                                                                 # O(1)
            temp_list.delete_at_index(len(temp_list) - 1)                                           # O(n)

        self.erase(temp_list[len(temp_list) // 2].value)                                            # O(n)