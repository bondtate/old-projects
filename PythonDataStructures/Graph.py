'''
PROJECT 8 - Graphs
Name: Tate Bond
PID: A55032302
'''

import random

def Generate_edges(size, connectedness):
    """
    DO NOT EDIT THIS FUNCTION
    Generates directed edges between vertices to form a DAG
    :return: A generator object that returns a tuple of the form (source ID, destination ID)
    used to construct an edge
    """

    assert connectedness <= 1
    random.seed(10)
    for i in range(size):
        for j in range(i + 1, size):
            if random.randrange(0, 100) <= connectedness * 100:
                yield f'{i} {j}'


# Custom Graph error
class GraphError(Exception): pass


class Vertex:
    """
    Class representing a Vertex in the Graph
    """
    __slots__ = ['ID', 'index', 'visited']

    def __init__(self, ID, index):
        """
        Class representing a vertex in the graph
        :param ID : Unique ID of this vertex
        :param index : Index of vertex edges in adjacency matrix
        """
        self.ID = ID
        self.index = index  # The index that this vertex is in the matrix
        self.visited = False

    def __repr__(self):
        return f"Vertex: {self.ID}"

    __str__ = __repr__

    def __eq__(self, other):
        """
        DO NOT EDIT THIS METHOD
        :param other: Vertex to compare
        :return: Bool, True if same, otherwise False
        """
        return self.ID == other.ID and self.index == other.index

    def out_degree(self, adj_matrix):
        '''
        - given the adj_matrix find the number of outgoing edges
        :param adj_matrix: edge matrix
        :return: int: number of edges
        '''
        if adj_matrix is None or self.index >= len(adj_matrix) or self.index < 0:
            return
        else:
            count = 0
            for i in range(len(adj_matrix)):
                if adj_matrix[self.index][i] is not None:
                    count += 1

        return count

    def in_degree(self, adj_matrix):
        '''
        - given the adj_matrix find the number of incoming edges
        :param adj_matrix: edge matrix
        :return: int: number of edges
        '''
        if adj_matrix is None or self.index >= len(adj_matrix) or self.index < 0:
            return
        else:
            count = 0
            for i in range(len(adj_matrix)):
                if adj_matrix[i][self.index] is not None:
                    count += 1

        return count

    def visit(self):
        self.visited = True


class Graph:
    """
    Graph Class ADT
    """

    def __init__(self, iterable=None):
        """
        DO NOT EDIT THIS METHOD
        Construct a random Directed Graph
        :param size: Number of vertices
        :param: iterable: iterable containing edges to use to construct the graph.
        """
        self.id_map = {}
        self.size = 0
        self.matrix = []
        self.iterable = iterable
        self.construct_graph()
        if hasattr(iterable, 'close'):
            iterable.close()

    def __eq__(self, other):
        """
        DO NOT EDIT THIS METHOD
        Determines if 2 graphs are Identical
        :param other: Graph Object
        :return: Bool, True if Graph objects are equal
        """
        return self.id_map == other.id_map and self.matrix == other.matrix and self.size == other.size

    def get_vertex(self, ID):
        '''
        -given an ID return the Vertex object
        :param ID: Vertex ID
        :return: Vertex object
        '''
        if ID in self.id_map:
            return self.id_map[ID]
        else:
            return

    def get_edges(self, ID):
        '''
        - return a tuple of outgoing edges from a given id
        :param ID: ID to find edges for
        :return: tuple of edges
        '''
        outgoing_edges = set()
        index = self.id_map[ID].index
        for i in range(len(self.matrix)):
            if self.matrix[index][i] is not None:
                outgoing_edges.add(self.matrix[index][i])

        return outgoing_edges

    def construct_graph(self):
        '''
        - loop through iterable and create edge matrix
        - caatch non-iterable objects
        :return: None
        '''

        # check for non-iterable
        try:

            # loop through generator checking for vertices on each line
            for i in self.iterable:
                temp = i.split()
                source_index = 0
                destination_index = 1
                while destination_index < len(temp):
                    source = int(temp[source_index])
                    destination = int(temp[destination_index])
                    self.insert_edge(source, destination)
                    source_index += 2
                    destination_index += 2

        except TypeError:
            raise GraphError(TypeError)

    def insert_edge(self, source, destination):
        '''
        - if source or destination are not in id_map create
          new vertex object and add
        - add edge in self.matrix
        :param source: where the edge is coming from
        :param destination: where the edge ends
        :return: None
        '''

        # check id_map for source and destination then update size
        if source not in self.id_map.keys() and destination not in self.id_map.keys():
            self.id_map[source] = Vertex(source, len(self.id_map))
            for i in range(0, len(self.id_map)-1):
                self.matrix[i].append(None)
                self.matrix[i].append(None)
            self.matrix.append([None for i in range(len(self.id_map) + 1)])
            self.id_map[destination] = Vertex(destination, len(self.id_map))
            self.matrix.append([None for i in range(len(self.id_map))])
            self.size += 2

        elif destination not in self.id_map.keys():
            self.id_map[destination] = Vertex(destination, len(self.id_map))
            for i in range(0, len(self.id_map) -1):
                self.matrix[i].append(None)
            self.matrix.append([None for i in range(len(self.id_map))])
            self.size += 1


        elif source not in self.id_map.keys():
            self.id_map[source] = Vertex(source, len(self.id_map))
            for i in range(0, len(self.id_map)-1):
                self.matrix[i].append(None)
            self.matrix.append([None for i in range(len(self.id_map))])
            self.size += 1

        # find destination and add its ID to self.matrix
        source_index = self.id_map[source].index
        destination_index = self.id_map[destination].index
        self.matrix[source_index][destination_index] = destination

    def bfs(self, start, target, path=None):
        '''
        - find a path from start to target
        - if no path return empty list
        - use breadth first traversal
        - path must = empty list
        :param start: starting vertex
        :param target: ending vertex
        :param path: list for recursive calls
        :return: list containing the path of vertex.ID
        '''

        # check for start and finish in graph
        if start not in self.id_map:
            return []
        if target not in self.id_map:
            return []
        if path is None:
            path = []

        # get the next vertices and check if current = target
        self.id_map[start].visit()
        next_vertices = self.get_edges(start)
        if start == target:
            return path.insert(0, start)

        # loop through each next_vertices and check for valid path
        for vert in next_vertices:
            self.bfs(vert, target, path)
            if len(path) != 0:
                path.insert(0, start)
                break

        return path

    def dfs(self, start, target, path=None):
        '''
        - find a path from start to target
        - if no path return empty list
        - use depth first traversal
        - path must = empty list
        :param start: starting vertex
        :param target: ending vertex
        :param path: list for recursive calls
        :return: list containing the path of vertex.ID
        '''

        # check for start and finish in graph and path exists
        if start not in self.id_map:
            return []
        if target not in self.id_map:
            return []
        if path is None:
            path = []

        # get the next vertices and check if current = target
        self.id_map[start].visit()
        next_vertices = self.get_edges(start)
        if start == target:
            return path.insert(0, start)

        # loop through each next_vertices and check for valid path
        for vert in next_vertices:
            if self.id_map[vert].visited is False:
                self.bfs(vert, target, path)
            if len(path) != 0:
                path.insert(0, start)
                break

        return path

def find_k_away(K, iterable, start):
    '''
    - given a starting vertex find all vertices
      that are K away from start
    :param K: distance from starting vertex
    :param iterable: graph iterable
    :param start: starting node
    :return: a set of vertex.IDs
    '''
    # create a directed graph from iterable
    graph = Graph(iterable)
    r_set = set()

    if K == 0:
        r_set.add(start)
        return r_set

    if graph.get_vertex(start) is None or graph.get_vertex(start).out_degree == 0:
        return r_set

    else:
        distance_traveled = 0
        frontier = {start : distance_traveled}
        discovered = {start : distance_traveled}

        while len(frontier) != 0 and distance_traveled < K:
            for key in frontier.keys():
                current = key
                break
            distance_traveled = frontier[current]
            del frontier[current]
            '''current_item = frontier.popitem()
            current = current_item[0]
            distance_traveled = current_item[1]'''

            for vert in graph.get_edges(current):
                if vert != start:
                    frontier[vert] = distance_traveled + 1
                    discovered[vert] = distance_traveled + 1

        for key in discovered.keys():
            if discovered[key] == K:
                r_set.add(key)

        return r_set

def main():
    gen = open("/Users/Tate/Downloads/cse_331/Project8/test_search_simple.txt")
    assert find_k_away(0, gen, 7) == {7}
    gen = ["1 2",
           "2 5",
           "2 4",
           "4 5",
           "5 1",
           "5 6",
           "6 1"
           ]

    for i, j in enumerate([{1}, {2}, {4, 5}, {5, 6}, {6}, set()]):
        assert (find_k_away(i, gen, 1) == j)

    assert (find_k_away(3, gen, -1) == set())

    '''gen = [
        "100 99 ",
        "99  98 ",
        "98  97 ",
        "99  20 ",
        "100 97",
        "97  1",
        "97  98",
        "98  100"
    ]
    assert find_k_away(2, gen, 100) == {1, 98, 20}

    gen = open("/Users/Tate/Downloads/cse_331/Project8/test_search_simple.txt")
    print(find_k_away(3, gen, 3))
    gen = open("/Users/Tate/Downloads/cse_331/Project8/test_search_simple.txt")
    assert find_k_away(3, gen, 3) == {26, 59, 4, 47}'''



if __name__ == '__main__':
    main()
