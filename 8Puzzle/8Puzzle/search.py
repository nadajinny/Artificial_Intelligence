# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.


import inspect
import sys
import random
import heapq
from collections import deque

def raiseNotDefined():
    fileName = inspect.stack()[1][1]
    line = inspect.stack()[1][2]
    method = inspect.stack()[1][3]

    print("*** Method not implemented: %s at line %s of %s" % (method, line, fileName))
    sys.exit(1)


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
        pass

    def isGoalState(self, state):
        """
        state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        pass

    def getSuccessors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        pass

    def getCostOfActions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        pass


def random_search(problem):
    """
    Search the nodes in the search tree randomly.

    Your search algorithm needs to return a list of actions that reaches the goal.
    Make sure to implement a graph search algorithm.

    This random_search function is just example not a solution.
    You can write your code by examining this function
    """
    start = problem.getStartState()
    node = [(start, "", 0)]   # class is better
    frontier = [node]

    explored = set()
    while frontier:
        node = random.choice(frontier)
        state = node[-1][0]
        if problem.isGoalState(state):
            return [x[1] for x in node][1:]

        if state not in explored:
            explored.add(state)

            for successor in problem.getSuccessors(state):
                if successor[0] not in explored:
                    parent = node[:]
                    parent.append(successor)
                    frontier.append(parent)

    return []


def depth_first_search(problem):
    start = problem.getStartState()
    node = [(start, "", 0)]
    frontier = [node]
    explored = set()

    while frontier: 
        node = frontier.pop()
        state = node[-1][0]
        if problem.isGoalState(state): 
            return [x[1] for x in node][1:]
        if state not in explored: 
            explored.add(state)
            for successor in problem.getSuccessors(state): 
                if successor[0] not in explored: 
                    new = node[:]
                    new.append(successor)
                    frontier.append(new)
    return []

def breadth_first_search(problem):
    start = problem.getStartState()
    node = [(start, "", 0)] 
    frontier = deque([node])
    explored = set()

    while frontier: 
        node = frontier.popleft()
        state = node[-1][0]
        if problem.isGoalState(state): 
            return [x[1] for x in node][1:]
        if state not in explored: 
            explored.add(state)
            for successor in problem.getSuccessors(state): 
                if successor[0] not in explored: 
                    new = node[:]
                    new.append(successor)
                    frontier.append(new)
    return []

def uniform_cost_search(problem):
    start = problem.getStartState()
    node = [(start, "", 0)]
    frontier = []
    breaker = 0
    heapq.heappush(frontier, (0, breaker, node))

    explored = {}

    while frontier: 
        cost, unuse , node = heapq.heappop(frontier)
        state = node[-1][0]
        if problem.isGoalState(state):
            return [x[1] for x in node][1:]
        if state not in explored or explored[state] > cost : 
            explored[state] = cost 
            for successor in problem.getSuccessors(state):
                unuse2, unuse3, next_cost = successor
                breaker += 1
                new = node[:]
                new.append(successor)
                print(next_cost)
                heapq.heappush(frontier, (cost + next_cost, breaker,  new))
    return []

def heuristic(state, problem=None):
    cnt = 0
    if state.cells[0][0] != 1: cnt += 1
    if state.cells[0][1] != 2: cnt += 1
    if state.cells[0][2] != 3: cnt += 1
    if state.cells[1][0] != 4: cnt += 1
    if state.cells[1][1] != 5: cnt += 1
    if state.cells[1][2] != 6: cnt += 1
    if state.cells[2][0] != 7: cnt += 1
    if state.cells[2][1] != 8: cnt += 1
    if state.cells[2][2] != 0: cnt += 1
    return cnt


def aStar_search(problem, heuristic=heuristic):
    start = problem.getStartState()
    node = [(start, "", 0)]
    frontier = []
    breaker = 0

    heuristic_g = 0
    heuristic_f = heuristic_g + heuristic(start,problem)
    heapq.heappush(frontier, (heuristic_f, heuristic_g, breaker, node))
    explored = {}

    while frontier: 
        cost_f, cost_g , unuse , node = heapq.heappop(frontier)
        state = node[-1][0]
        if problem.isGoalState(state):
            return [x[1] for x in node][1:]
        if state not in explored or explored[state] > cost_g : 
            explored[state] = cost_g 
            for successor in problem.getSuccessors(state):
                unuse2, unuse3, next_cost = successor
                new_g = cost_g + next_cost
                new_h = heuristic(unuse2, problem)
                new_f = new_g + new_h

                breaker += 1
                new = node[:]
                new.append(successor)
                heapq.heappush(frontier, (new_f, new_g, breaker,  new))
    return []



# Abbreviations
rand = random_search
bfs = breadth_first_search
dfs = depth_first_search
astar = aStar_search
ucs = uniform_cost_search