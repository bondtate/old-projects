"""
PROJECT 4 - QUEUES
Name: Tate Bond
PID: A55032302
"""

import math


class CircularQueue:
    """
    Circular Queue Class
    """
    # DO NOT MODIFY THESE METHODS
    def __init__(self, capacity=4):
        """
        DO NOT MODIFY.
        Initialize the queue with an initial capacity
        :param capacity: the initial capacity of the queue
        """
        self.capacity = capacity
        self.size = 0
        self.data = [None] * capacity
        self.head = 0
        self.tail = 0


    def __eq__(self, other):
        """
        DO NOT MODIFY.
        Defines equality for two queues
        :return: true if two queues are equal, false otherwise
        """
        if self.capacity != other.capacity:
            return False
        for i in range(self.capacity):
            if self.data[i] != other.data[i]:
                return False
        return self.head == other.head and self.tail == other.tail and self.size == other.size

    def __str__(self):
        """
        DO NOT MODIFY.
        String representation of the queue
        :return: the queue as a string
        """
        if self.is_empty():
            return "Empty queue"
        result = ""
        str_list = [str(self.data[(self.head + i)%self.capacity]) for i in range(self.size)]
        return "Queue: " + (", ").join(str_list)

    # -----------MODIFY BELOW--------------
    def __len__(self):
        '''
        -get the length of the list
        :return: int: length of the list
        '''
        return self.size

    def is_empty(self):
        '''
        -check if the queue is emtpy
        :return: bool: true if empty false otherwise
        '''
        if self.size == 0:
            return True
        else:
            return False

    def head_element(self):
        '''
        -return the data at the head of the queue
        :return: head element of queue
        '''
        return self.data[self.head]

    def tail_element(self):
        '''
        -return the data at the tail of the queue
        :return: tail element of queue
        '''
        return self.data[self.tail - 1]

    def enqueue(self, val):
        '''
        -add an element to the back of the queue
        :param val: value to add
        :return: None
        '''

        if self.size == 0:
            self.data[self.head] = val
            self.size += 1
            self.tail += 1

        #if not empty or full list
        else:
            self.tail = (self.tail + 1) % self.capacity
            self.data[self.tail - 1] = val
            self.size += 1

            #grow immediately if capacity is reached
            if self.size == self.capacity:
                self.grow()

    def dequeue(self):
        '''
        -remove an element from the front of the queue
        -return the removed item and move head up one element
        :return: the removed element, if empty None
        '''

        if self.is_empty() is True:
            return None
        else:

            return_val = self.data[self.head]
            self.data[self.head] = None
            self.head = (self.head + 1) % self.capacity
            self.size -= 1

            #shrink immediately if size is 1/4 of capacity
            self.shrink()

            return return_val


    def tail_dequeue(self):
        '''
        -remove an element from the back of the queue
        -return removed value and change tail -1
        :return: the removed element, if empty None
        '''

        if self.is_empty() is True:
            self.head = 0
            self.tail = 0
            return
        else:
            return_val = self.data[self.tail - 1]
            self.data[self.tail - 1] = None
            self.tail -= 1
            self.size -= 1

            # shrink immediately if size is 1/4 of capacity
            self.shrink()
            return return_val

    def grow(self):
        '''
        -double the capacity of the queue
        :return: None
        '''

        self.capacity = self.capacity * 2
        new_data = [None] * self.capacity

        loc = 0
        for i in range(self.head, len(self.data)):
            new_data[loc] = self.data[i]
            loc += 1

        if self.head <= self.tail:
            for i in range(0, self.tail):
                new_data[loc] = self.data[i]
                loc += 1

        self.head = 0
        self.tail = self.size
        self.data = new_data
        del new_data

    def shrink(self):
        '''
        -shrink the capacity by half
        :return: None
        '''

        if self.capacity > 7 and self.capacity // 4 == self.size:
            self.capacity = self.capacity // 2
            new_data = [None] * self.capacity

            for i in range(0, len(new_data)):
                new_data[i] = self.data[i + self.head]

            self.head = 0
            self.tail = self.size
            self.data = new_data
            del new_data


def compare_val(val1, val2):
    '''
    -compare two given values
    -return the greater of the two
    :param val1: input value
    :param val2: input value
    :return: return the greater value
    '''

    if val1 > val2:
        return val1
    else:
        return val2


def greatest_val(w, values):
    '''
    -find the greatest value for each broken down list of size w
    -store all greatest values in a list and return it
    :param w: breakdown array size
    :param values: starting queue
    :return: a list of greatest values for each queue breakdown
    '''

    if len(values) == 0 is True or w <= 0:
        return []

    else:
        return_list = []
        greatest = values[0]
        temp_queue = CircularQueue()

        #loop along the outside of the list until pos = len(values) - w
        pos = 0
        while pos <= len(values) - w:

            for i in range(pos, pos + w):
                temp_queue.enqueue(values[i])

            greatest = temp_queue.head_element()
            for i in range(temp_queue.size):
                greatest = compare_val(greatest, temp_queue.dequeue())

            return_list.append(greatest)
            pos += 1

        del temp_queue
        return return_list



def main():

    q = CircularQueue()

    for i in range(1, 10):
        q.enqueue(i)
    print(q.data)
    for i in range(1, 4):
        q.tail_dequeue()
    print(q.data)
    for i in range(1, 5):
        q.dequeue()
    print(q.data)
    for i in range(1,3):
        q.enqueue(i)
    print(q.data)


    v = [1.4 , -2.9, 3.6]
    print(v)
    print(greatest_val(2, v))
    print(v)



if __name__ == '__main__':
    main()