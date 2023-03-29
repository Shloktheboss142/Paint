from __future__ import annotations
from abc import ABC, abstractmethod
from layer_util import Layer
from layer_util import get_layers
import layers
from data_structures.stack_adt import ArrayStack
from data_structures.array_sorted_list import ArraySortedList, ListItem
from data_structures.queue_adt import CircularQueue
from data_structures.bset import BSet

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
        - Worst case: O(1)
            Number of operations is constant and doesnt rely on the size of the input
        - Best case: O(1)
            Number of operations is constant and doesnt rely on the size of the input
        """
        self.active_layer = None                                                                    # O(1)
        self.special_mode_status = False                                                            # O(1)

    def add(self, layer: Layer) -> bool:
        """
        Adds a layer to the grid square

        Args:
        - layer: The layer to add to the grid square
            Type: Layer Oblject

        Returns:
        - Boolean value of True if the layer was added to the grid square, False if the current layer is unchanged
            Type: Boolean

        Complexity:
        - Worst case: O(1)
            Number of operations is constant and doesnt rely on the size of the input
        - Best case: O(1)
            Number of operations is constant and doesnt rely on the size of the input
        """
        if self.active_layer != layer or self.active_layer == None:                                 # O(1)
            self.active_layer = layer                                                               # O(1)
            return True                                                                             # O(1)
        return False                                                                                # O(1)
    
    def get_color(self, start: tuple[int, int, int], timestamp: int, x: int, y: int) -> tuple[int, int, int]:
        """
        Calculating the color that the grid square should display

        Args:
        - start: The color that is currently on the grid square
            Type: Tuple of 3 integers
        - timestamp: Used for layers that change over time (Such as rainbow and sparkle)
            Type: Integer
        - x: Used for layers that change over time (Such as rainbow and sparkle)
            Type: Integer
        - y: Used for layers that change over time (Such as rainbow and sparkle)
            Type: Integer

        Returns:
        - A tuple containing the RGB value that the layer square should display
            Type: Tuple of 3 integers

        Complexity:
        - Worst case: O(n), Where n is the timestamp
            Will only happen if the layer being applied is sparkle.
        - Best case: O(1)
            Will occur when there is no active layer and special is not active. In which case the start color is returned.
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
        Erases the layer that is currently in the grid square and sets the active layer to None

        Args:
        - layer: The layer to be removed from the grid square
            Type: Layer Object
            (Not used in this function)

        Returns:
        - Boolean value of True is the layer was eaased from the grid square, False if there was no active layer in the grid square
            Type: Boolean

        Complexity:
        - Worst case: O(1)
            Number of operations is constant and doesnt rely on the size of the input
        - Best case: O(1)
            Number of operations is constant and doesnt rely on the size of the input
        """
        if self.active_layer != None:                                                               # O(1)
            self.active_layer = None                                                                # O(1)
            return True                                                                             # O(1)
        return False                                                                                # O(1)

    def special(self) -> None:
        """
        Activates the special mode for the current grid square

        Returns:
        - None

        Complexity:
        - Worst case: O(1)
            Number of operations is constant and doesnt rely on the size of the input
        - Best case: O(1)
            Number of operations is constant and doesnt rely on the size of the input
        """
        self.special_mode_status = not self.special_mode_status                                     # O(1)

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
        - Worst case: O(n) Where n is the length of the queue to be initialised
        - Best case: O(n) Where n is the length of the queue to be initialised            
        """
        self.layer_sequence = CircularQueue(len(get_layers()) * 100)                                # O(n) Where n is the length of the queue

    def add(self, layer: Layer) -> bool:
        """
        Adds a layer to the layers queue

        Args:
        - layer: The layer to be added to the queue
            Type: Layer Object

        Returns:
        - Boolean value of True is the layer was added to the queue, False if the layer was not added to the queue due to the queue being full
            Type: Boolean

        Complexity:
        - Worst case: O(1)
            Number of operations is constant and doesnt rely on the size of the input
        - Best case: O(1)
            Number of operations is constant and doesnt rely on the size of the input
        """
        if self.layer_sequence.is_full() == False:                                                  # O(1)
            self.layer_sequence.append(layer)                                                       # O(1)
            return True                                                                             # O(1)
        else:                                                                                       # O(1)
            return False                                                                            # O(1)
        
    def get_color(self, start: tuple[int, int, int], timestamp: int, x: int, y: int) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.

        Args:
        - start: The color that is currently on the grid square
            Type: Tuple of 3 integers
        - timestamp: Used for layers that change over time (Such as rainbow and sparkle)
            Type: Integer
        - x: Used for layers that change over time (Such as rainbow and sparkle)
            Type: Integer
        - y: Used for layers that change over time (Such as rainbow and sparkle)
            Type: Integer

        Returns:
        - A tuple containing the RGB value that the layer square should display
            Type: Tuple of 3 integers

        Complexity:
        - Worst case: O(mn), Where n is the length of the layer sequence, and m is the timestamp of the sparkle layer
            Will only happen if one of the layers being applied is sparkle.
        - Best case: O(n), Where n is the length of the layer sequence
            Will only occur when the sparkle layer is not present in the layer sequence
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
            Type: Layer Object

        Returns:
        - Boolean value of True is the layer was eaased from the grid square, False if there are no layers in the grid square
            Type: Boolean

        Complexity:
        - Worst case: O(1)
            Number of operations is constant and doesnt rely on the size of the input
        - Best case: O(1)
            Number of operations is constant and doesnt rely on the size of the input
        """
        if self.layer_sequence.is_empty() == False:                                                 # O(1)
            self.layer_sequence.serve()                                                             # O(1)
            return True                                                                             # O(1)
        return False                                                                                # O(1)

    def special(self) -> None:
        """
        Reverses the order of layers in the layer sequence queue so that the layer are applied backwards

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
        Initialises a set to store the layers added

        Returns:
        - None

        Complexity:
        - Worst case: O(1)
            Number of operations is constant and doesnt rely on the size of the input
        - Best case: O(1)
            Number of operations is constant and doesnt rely on the size of the input
        """
        self.set = BSet()                                                                           # O(1)

    def add(self, layer: Layer) -> bool:
        """
        Enables the given layer

        Args:
        - layer: The layer to be added to the queue
            Type: Layer Object

        Returns:
        - Boolean value of True is the layer was added to the queue, False if the layer was not added to the queue due to the queue being full
            Type: Boolean

        Complexity:
        - Worst case: O(1)
            Number of operations is constant and doesnt rely on the size of the input
        - Best case: O(1)
            Number of operations is constant and doesnt rely on the size of the input
        """
        if layer.index + 1 in self.set:                                                             # O(1)
            return False                                                                            # O(1)
        self.set.add(layer.index + 1)                                                               # O(1)
        return True                                                                                 # O(1)
    
    def get_color(self, start: tuple[int, int, int], timestamp: int, x: int, y: int) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.

        Args:
        - start: The color that is currently on the grid square
            Type: Tuple of 3 integers
        - timestamp: Used for layers that change over time (Such as rainbow and sparkle)
            Type: Integer
        - x: Used for layers that change over time (Such as rainbow and sparkle)
            Type: Integer
        - y: Used for layers that change over time (Such as rainbow and sparkle)
            Type: Integer

        Returns:
        - A tuple containing the RGB value that the layer square should display
            Type: Tuple of 3 integers

        Complexity:
        - Worst case: O(mn), Where n is the length of the layer sequence, and m is the timestamp of the sparkle layer
            Will only happen if one of the layers being applied is sparkle.
        - Best case: O(n), Where n is the length of the layer sequence
            Will only occur when the sparkle layer is not present in the layer sequence
        """
        for layer in get_layers():                                                                  # O(n) Where n is the number of layers in the program
            if layer != None:                                                                       # O(1)
                if (layer.index + 1) in self.set:                                                   # O(1)
                    start = layer.apply(start, timestamp, x, y)                                     # Best case: O(1) Worst case: O(m) Where m is the timestamp for the sparkle layer

        return start                                                                                # O(1)

    def erase(self, layer: Layer) -> bool:
        """
        Disables the given layer

        Args:
        - layer: The layer to be removed from the grid square
            Type: Layer Object

        Returns:
        - Boolean value of True is the layer was eaased from the grid square, False if there are no layers in the grid square
            Type: Boolean

        Complexity:
        - Worst case: O(1)
            Number of operations is constant and doesnt rely on the size of the input
        - Best case: O(1)
            Number of operations is constant and doesnt rely on the size of the input
        """
        if (layer.index + 1) not in self.set:                                                       # O(1)
            return False                                                                            # O(1)
        self.set.remove(layer.index + 1)                                                            # O(1)
        return True                                                                                 # O(1)

    def special(self) -> None:
        """
        Arranges the enabled layers lexigraphically and disables the middle layer

        Returns:
        - None

        Complexity:
        - Worst case: O(n log m), Where n is number of layers in the program and m is the number of layers in the sorted list array
            Happens when at least one layer is enabled
        - Best case: O(n), Where n is the length of the sorted list array
            Happens when there are no layers enabled
        """
        temp_list = ArraySortedList(len(get_layers()))                                              # O(n) Where n is the number of layers

        for layer in get_layers():                                                                  # O(n) Where n is the number of layers in the program
            if layer != None:                                                                       # O(1)
                if (layer.index + 1) in self.set:                                                   # O(1)
                    temp_list.add(ListItem(layer, layer.name))                                      # O(log m) Where n is the length of the sorted list array

        if temp_list.is_empty() == True:                                                            # O(1)
            return None                                                                             # O(1)
        elif len(temp_list) == 1:                                                                   # O(1)
            self.erase(temp_list[0].value)                                                          # O(1)
            return None                                                                             # O(1)
        
        if len(temp_list) % 2 == 0:                                                                 # O(1)
            temp_list.delete_at_index(len(temp_list) - 1)                                           # O(m) Where n is the length of the sorted list array

        self.erase(temp_list[len(temp_list) // 2].value)                                            # O(1)