'''
PROJECT 7 - Hash Tables
Name: Tate Bond
PID: A55032302
'''

class HashNode:
    """
    DO NOT EDIT
    """
    __slots__ = ["key", "value", "deleted"]

    def __init__(self, key, value, deleted=False):
        self.key = key
        self.value = value
        self.deleted = deleted

    def __repr__(self):
        return f"HashNode({self.key}, {self.value})"

    def __eq__(self, other):
        return self.key == other.key and self.value == other.value


class HashTable:
    """
    Hash Table Class
    """
    __slots__ = ['capacity', 'size', 'table', 'collisions', 'prime_index']

    primes = (
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83,
        89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179,
        181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277,
        281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389,
        397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499,
        503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617,
        619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739,
        743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859,
        863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991,
        997)

    def __init__(self, capacity=8):
        """
        DO NOT EDIT
        Initializes hash table
        :param capacity: capacity of the hash table
        """
        self.capacity = capacity
        self.size = 0
        self.table = [None] * capacity

        i = 0
        while HashTable.primes[i] <= self.capacity:
            i += 1
        self.prime_index = i - 1

    def __eq__(self, other):
        """
        DO NOT EDIT
        Equality operator
        :param other: other hash table we are comparing with this one
        :return: bool if equal or not
        """
        if self.capacity != other.capacity or self.size != other.size:
            return False
        for i in range(self.capacity):
            if self.table[i] != other.table[i]:
                return False
        return True

    def __repr__(self):
        """
        DO NOT EDIT
        Represents the table as a string
        :return: string representation of the hash table
        """
        represent = ""
        bin_no = 0
        for item in self.table:
            represent += "[" + str(bin_no) + "]: " + str(item) + '\n'
            bin_no += 1
        return represent

    def __setitem__(self, key, value):
        """
        DO NOT EDIT
        Allows for the use of the set operator to insert into table
        :param key: string key to insert
        :param value: value to insert
        :return: None
        """
        return self.insert(key=key, value=value)

    def __getitem__(self, item):
        """
        DO NOT EDIT
        Allows get operator to retrieve a value from the table
        :param item: string key of item to retrieve from tabkle
        :return: HashNode
        """
        return self.get(item)

    def __contains__(self, item):
        """
        DO NOT EDIT
        Checks whether a given key exists in the table
        :param item: string key of item to retrieve
        :return: Bool
        """
        if self.get(item) is not None:
            return True
        return False

    def _hash_1(self, key):
        """
        ---DO NOT EDIT---
        Converts a string x into a bin number for our hash table
        :param x: key to be hashed
        :return: bin number to insert hash item at in our table, -1 if x is an empty string
        """
        if not key:
            return None
        hashed_value = 0

        for char in key:
            hashed_value = 181 * hashed_value + ord(char)
        return hashed_value % self.capacity

    def _hash_2(self, key):
        """
        ---DO NOT EDIT---
        Converts a string x into a hash
        :param x: key to be hashed
        :return: a hashed value
        """
        if not key:
            return None
        hashed_value = 0

        for char in key:
            hashed_value = 181 * hashed_value + ord(char)

        prime = HashTable.primes[self.prime_index]

        hashed_value = prime - (hashed_value % prime)
        if hashed_value % 2 == 0:
            hashed_value += 1
        return hashed_value

    """ **************** Student Section Below ******************************"""

    def hash(self, key, inserting=False):
        '''
        - Use a given string key to either find a given value
          or find the next available index
        :param key: string: key to find
        :param inserting: if the hash function is being used for insertion
        :return: either the current value or next available location
        '''

        hash_1 = self._hash_1(key)
        if hash_1 is None or hash_1 == -1:
            return
        else:
            buckets_probed = 0
            bucket = hash_1
            if inserting is False:

                # loop through table until empty since start or size is reached
                while self.table[bucket] is not None and self.table[bucket].key != key:

                    # set next bucket value using second hash function
                    buckets_probed += 1
                    bucket = (hash_1 + buckets_probed * self._hash_2(key)) % self.capacity

                return bucket

            else:

                # stop loop on empty-since-start or deleted bucket
                while self.table[bucket] is not None and self.table[bucket].deleted is False:

                    if self.table[bucket].key == key:
                        break
                    # set next bucket value using second hash function
                    buckets_probed += 1
                    bucket = (hash_1 + buckets_probed * self._hash_2(key)) % self.capacity

                return bucket

    def insert(self, key, value):
        '''
        - Insert a given key value pair into the table
        :param key: location in table
        :param value: value contained in key
        :return: Void
        '''

        loc = self.hash(key, True)
        new_node = HashNode(key, value)
        if loc is None:
            return
        if self.table[loc] is not None and self.table[loc].deleted is False:
            self.table[loc].value = value
        else:
            self.table[loc] = new_node
            self.size += 1

        if self.size / self.capacity >= .5:
            self.grow()

    def get(self, key):
        '''
        - Find the HashNode with the given key in the table
        :param key: key to search for
        :return: either the found HashNode or None
        '''

        loc = self.hash(key)
        if loc is None:
            return
        elif self.table[loc] is None or self.table[loc].deleted is True:
            return
        else:
            return self.table[loc]

    def delete(self, key):
        '''
        - Find the HashNode with the given key in the table for deletion
        :param key: key to search for
        :return: None
        '''
        loc = self.hash(key)
        if loc is None:
            return
        if self.table[loc] is None or self.table[loc].deleted is True:
            return
        else:
            self.table[loc].key = None
            self.table[loc].value = None
            self.table[loc].deleted = True
            self.size -= 1


    def grow(self):
        '''
        - double the capacity of the table
        - rehash existing nodes
        - no rehashing of deleted nodes
        :return: Void
        '''

        # double the capacity
        cap = self.capacity * 2
        new_table = HashTable(cap)

        # set the new prime_index
        prime = 0
        for index in range(len(HashTable.primes)):
            if HashTable.primes[index] < new_table.capacity:
                prime = index
        new_table.prime_index = prime

        # loop through current table and re-hash to new_table
        for node in self.table:
            if node is not None and node.deleted is False:
                new_table.insert(node.key, node.value)

        # reset current table with new elements
        self.table = new_table.table
        self.size = new_table.size
        self.prime_index = new_table.prime_index
        self.capacity = new_table.capacity

def mod_table(key, command, table):
    '''
    - Helper function for word_frequency
    - Edit table with the given key
    :param key: key to add or modify withen table
    :param command: string: add, or new
    :param table: HashTable to edit
    :return: Void
    '''

    node = table.get(key)
    if command == 'new':
        table.insert(key, 0)
    elif command == 'add':
        if node is None:
            table.insert(key, 1)
            node = table.get(key)
        node.value += 1
        table.insert(node.key, node.value)

def word_frequency(string, lexicon, table):
    '''
    - Create and return a hashtable with word frequency
      from a given string
    - string contains no whitespace
    :param string: string to parse
    :param lexicon: list of words to find
    :param table: HashTable containing word frequency
    :return: HashTable: table(string, int)
    '''

    back = ''
    front = ''
    temp_string = ''
    found = False
    current_index = 1
    index = 1
    while index < len(string):
        back = string[index:]
        front = string[:index]

        if back in lexicon and front not in lexicon:
            cur_size = table.size
            new_size = word_frequency(front, lexicon, table).size
            if cur_size != new_size:
                #mod_table(back, "add", table)
                temp_string = back
                index += 1
            else:
                return table
        elif back in lexicon and front in lexicon:
            mod_table(back, "add", table)
            mod_table(front, "add", table)
            word_frequency(back, lexicon, table)
            string = front
        elif front in lexicon:
            mod_table(front, "new", table)
            index += 1
        else:
            index += 1

    return table






def main():
    table = HashTable()

    print(word_frequency('chefallfall',['chef', 'fall', 'all', 'a'], table))







if __name__ == '__main__':
    main()