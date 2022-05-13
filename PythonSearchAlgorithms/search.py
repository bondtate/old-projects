# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """

    from util import Stack

    # initialize the fringe and closed set
    fringe = Stack()
    fringe.push((problem.getStartState(), 'Start', 0))
    closed = set()

    def pathfinder(path=[]):
        '''
        - Build a path from StartState to GoalState using recursion
        :param path: a list of commands for pacman to follow
        :return: a complete list of commands
        '''

        if fringe.isEmpty():
            return

        node = fringe.pop()

        # if the node is the goal, start building the path
        if problem.isGoalState(node[0]):
            return path.insert(0, node)

        # if the node hasn't been visited loop through it's children
        if node[0] not in closed:

            closed.add(node[0])
            for child_node in problem.getSuccessors(node[0]):
                fringe.push(child_node)
                pathfinder(path)

                if len(path) != 0 and node not in path:
                    path.insert(0, node)
                    break

        return [cmd[1] for cmd in path if cmd[1] != 'Start']

    return pathfinder()


    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""

    from util import Queue

    # initialize the fringe and closed set
    fringe = Queue()
    closed = set()

    # initialize the starting variables
    start_vals = ((problem.getStartState(), 'Start', 0), None)
    fringe.push(start_vals)
    visited = []
    path = []
    short_path = [None for i in range(999999)]

    def buildpath(parent):

        used = []
        # loop through visited nodes to form a path
        while parent != start_vals[0]:
            #print("Parent: {}, Start Vals: {}".format(parent, start_vals))

            for pair in visited:

                if pair[0] == parent:
                    used.insert(0, pair[0][1])
                    parent = pair[1]
                    break
        return used

    # loop through the graph and add nodes to visited list
    while True:

        if fringe.isEmpty():
            return

        vals = fringe.pop()
        node = vals[0]

        if node[1] == 'Found':

            path += buildpath(vals[1])

            node = (node[0], 'Start')
            start_vals = (node, None)

            while not fringe.isEmpty(): fringe.pop()
            fringe.push(start_vals)
            closed = set()
            visited = []

        elif node[1] == 'Reset':
            print(node)

            path += buildpath(vals[1])

            if len(path) < len(short_path):
                short_path = path
            path = []

            node = (problem.getStartState(), 'Start')
            start_vals = (node, None)
            while not fringe.isEmpty(): fringe.pop()
            fringe.push(start_vals)

            closed = set()
            visited = []

        if problem.isGoalState(node[0]):
            parent = vals[1]
            path += buildpath(parent)
            path.append(node[1])
            if len(path) < len(short_path):
                short_path = path
            break

        if node[0] not in closed:

            closed.add(node[0])
            for child_node in problem.getSuccessors(node[0]):
                fringe.push( (child_node, node) )
                visited.append( (child_node, node) )

                if child_node[1] == "Reset" or child_node[1] == "Found":
                    while not fringe.isEmpty(): fringe.pop()
                    fringe.push( (child_node, node) )

    return short_path

    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""

    from util import PriorityQueue

    # initialize the fringe and closed set
    fringe = PriorityQueue()
    closed = set()

    # initialize the starting variables
    start_vals = ((problem.getStartState(), 'Start', 0), None)
    fringe.push(start_vals, start_vals[0][2])
    visited = []
    path = []

    # loop through the graph and add nodes to visited list
    while True:


        if fringe.isEmpty():
            return

        vals = fringe.pop()
        node = vals[0]

        if problem.isGoalState(node[0]):
            parent = vals[1]
            path.insert(0, node[1])
            break

        if node[0] not in closed:

            closed.add(node[0])
            for child_node in problem.getSuccessors(node[0]):

                # update the cost of the node and add to priority queue
                cost = child_node[2] + node[2]
                child_node = (child_node[0], child_node[1], cost)
                fringe.push((child_node, node), cost)
                visited.append((child_node, node))

    # loop through visited nodes to form a path
    while parent != start_vals[0]:

        for pair in visited:

            if pair[0] == parent:
                path.insert(0, pair[0][1])
                parent = pair[1]
                break

    return path

    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """

    return 0

    try:
        xy1 = state
        xy2 = problem.goal
    except AttributeError:
        return 0

    return ((xy2[0] - xy1[0]) ** 2 + (xy2[1] - xy1[1]) ** 2) ** .5

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""

    from util import PriorityQueue

    # initialize the fringe and closed set
    fringe = PriorityQueue()
    closed = set()

    # initialize the starting variables
    start_vals = ((problem.getStartState(), 'Start', 0), None)
    fringe.push(start_vals, start_vals[0][2])
    visited = []
    path = []
    short_path = [None for i in range(999999)]

    def buildpath(parent):

        used = []
        # loop through visited nodes to form a path
        while parent != start_vals[0]:
            #print("Parent: {}, Start Vals: {}".format(parent, start_vals))

            for pair in visited:

                if pair[0] == parent:
                    used.insert(0, pair[0][1])
                    parent = pair[1]
                    break
        return used

    # loop through the graph and add nodes to visited list
    while True:


        if fringe.isEmpty():
            return

        vals = fringe.pop()
        node = vals[0]

        if node[1] == 'Found':

            path += buildpath(vals[1])

            node = (node[0], 'Start', 0)
            start_vals = (node, None)

            while not fringe.isEmpty(): fringe.pop()
            fringe.push(start_vals, start_vals[0][2])
            closed = set()
            visited = []

        elif node[1] == 'Reset':

            path += buildpath(vals[1])

            if len(path) < len(short_path):
                short_path = path
            path = []

            node = (problem.getStartState(), 'Start', 0)
            start_vals = (node, None)
            while not fringe.isEmpty(): fringe.pop()
            fringe.push(start_vals, start_vals[0][2])

            closed = set()
            visited = []

        if problem.isGoalState(node[0]):
            parent = vals[1]
            path += buildpath(parent)
            path.append(node[1])
            if len(path) < len(short_path):
                short_path = path
            break

        if node[0] not in closed:

            closed.add(node[0])
            for child_node in problem.getSuccessors(node[0]):

                # update the cost of the node and add to priority queue
                cost = child_node[2] + node[2]
                child_node = (child_node[0], child_node[1], cost)
                cost += heuristic(child_node[0], problem)

                fringe.push((child_node, node), cost)
                visited.append((child_node, node))

                if child_node[1] == "Reset" or child_node[1] == "Found":
                    while not fringe.isEmpty(): fringe.pop()
                    fringe.push( (child_node, node), cost )

    return short_path

    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
