'''
PROJECT 6 - Heaps
Name: Tate Bond
PID: A55032302
'''

class Node:
    """
    Class definition shouldn't be modified in anyway
    """
    __slots__ = ('_key', '_val')

    def __init__(self, key, val):
        self._key = key
        self._val = val

    def __lt__(self, other):
        return self._key < other._key or (self._key == other._key and self._val < other._val)

    def __gt__(self, other):
        return self._key > other._key or (self._key == other._key and self._val > other._val)

    def __eq__(self, other):
        return self._key == other._key and self._val == other._val

    def __str__(self):
        return '(k: {0} v: {1})'.format(self._key, self._val)

    __repr__ = __str__

    @property
    def val(self):
        """
        :return: underlying value of node
        """
        return self._val


class Heap:
    """
    Class definition is partially completed.
    Method signatures and provided methods may not be edited in any way.
    """
    __slots__ = ('_size', '_capacity', '_data')

    def __init__(self, capacity):
        self._size = 0
        self._capacity = capacity + 1  # additional element space for push
        self._data = [None for _ in range(self._capacity)]

    def __str__(self):
        return ', '.join(str(el) for el in self._data if el is not None)

    __repr__ = __str__

    def __len__(self):  # allows for use of len(my_heap_object)
        return self._size

#    DO NOT MODIFY ANYTHING ABOVE THIS LINE
#    Start of Student Modifications

    def _swap(self, index1, index2):
        '''
        - swap the value in self._data at the two index's
        :param index1: index to be swapped
        :param index2: index to be swapped
        :return: Void
        '''

        temp_val = self._data[index1]
        self._data[index1] = self._data[index2]
        self._data[index2] = temp_val


    def _percolate_up(self):
        '''
        - percolate the node up the array until in the right location
        :return: Void
        '''
        if self._size == 1:
            return
        else:
            node_index = self._size - 1
            while node_index > 0:
                parent_index = (node_index - 1) // 2
                if self._data[node_index] > self._data[parent_index]\
                        or self._data[node_index] == self._data[parent_index]:
                    return
                else:
                    self._swap(node_index, parent_index)
                    node_index = parent_index


    def _percolate_down(self):
        '''
        - percolate the node down the array until in the right location
        :return: void
        '''
        if self._size == 1:
            return
        else:
            node_index = 0
            child_index = 2 * node_index + 1
            key = self._data[node_index]

            while child_index < self._size - 1:
                # Find the max among the node and all the node's children
                min_value = key
                min_index = -1
                for i in range(2):
                    if i + child_index >= self._size - 1:
                        break
                    elif self._data[i + child_index] < min_value:
                        min_value = self._data[i + child_index]
                        min_index = i + child_index

                if min_value == key:
                    return

                else:
                    self._swap(node_index, min_index)
                    node_index = min_index
                    child_index = 2 * node_index + 1

    def _min_child(self, i):
        '''
        - return the index of the minimum child of the index i
        - if no children return -1
        :param i: index to find children of
        :return: int: child index
        '''

        if self._size == 0 or self._capacity == 0:
            return -1
        else:
            child_index = 2 * i + 1
            if child_index < self._size:
                child_val1 = self._data[child_index]
                if child_index + 1 < self._size:
                    child_val2 = self._data[child_index + 1]
                    if child_val1 is None and child_val2 is None:
                        return -1
                    elif child_val1 is None:
                        return child_index + 1
                    elif child_val2 is None:
                        return child_index
                    elif child_val1 < child_val2:
                        return child_index
                    else:
                        return child_index + 1
                else:
                    return child_index
            else:
                return -1




    def push(self, key, val):
        '''
        - add a new node to the end of the array
        - percolate_up until Node is in the right loaction
        :param key: key value of the new node
        :param val: value of the new node
        :return: void
        '''

        if val is None or self._capacity == 0:
            return
        else:
            new_node = Node(key, val)
            self._data[self._size] = new_node
            self._size += 1
            self._percolate_up()

            if self._size == self._capacity:
                self.pop()



    def pop(self):
        '''
        - remove the largest node from the array
        - percolate down until the node is in the right location
        :return: value of smallest node
        '''

        if self._size == 0 or self._capacity == 0:
            return

        elif self._size == 1:
            r_val = self._data[0]
            self._data[0] = None

        else:
            r_val = self._data[0]
            self._data[0] = self._data[self._size - 1]
            self._data[self._size - 1] = None
            self._percolate_down()

        self._size -= 1
        return r_val.val



    @property  # do not remove
    def empty(self):
        '''
        - check for an empty heap
        :return: boolean true if empty false if not
        '''
        if self._size == 0:
            return True
        else:
            return False

    @property  # do not remove
    def top(self):
        '''
        - return the root of the node
        :return: root node value or none if not possible
        '''

        if self._data[0] is None:
            return
        else:
            return self._data[0].val

    @property  # do not remove
    def levels(self):
        '''
        - create a list and fill with each level of the heap
        - add these lists to another list and return
        :return: list of levels
        '''

        r_list = []
        if self._data[0] is None:
            return r_list
        else:
            index = 1
            count = 2
            help_list = []
            r_list.append([self._data[0]])
            while index < self._size:
                if self._data[index] is None:
                    break
                elif len(help_list) < count:
                    help_list.append(self._data[index])
                else:
                    r_list.append(help_list)
                    count *= 2
                    help_list = [self._data[index]]
                index += 1

            if len(help_list) != 0:
                r_list.append(help_list)

            return r_list


def most_x_common(vals, X):
    '''
    - find the X most recurring elements in list of vals
    - x cannot be greater than len(vals)
    :param vals: list of strings
    :param X: amount of recurring elements
    :return: set('string') of recurring elements
    '''
    if len(vals) == 0:
        return
    else:
        count_track = {}
        heap = Heap(X)
        r_set = set()
        
        # loop through list and create dictionary
        # string as key frequency count as value
        for val in vals:
            if val not in count_track:
                count_track[val] = 1
            else:
                count_track[val] += 1

        # push the elements into a heap of size X
        for key, val in count_track.items():
            heap.push(val, key)

        # loop through heap and add elements to return set
        while heap.empty is False:
            r_set.add(heap.pop())

        return r_set

