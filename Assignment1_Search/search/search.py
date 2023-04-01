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
        Returns the start current for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, current):
        """
          current: Search current

        Returns True if and only if the current is a valid goal current.
        """
        util.raiseNotDefined()

    def getSuccessors(self, current):
        """
          current: Search current

        For a given current, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        current, 'action' is the action required to get there, and 'stepCost' is
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
    # Start: (5, 5)
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    # False
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    # Start's successors: [((5, 4), 'South', 1), ((4, 5), 'West', 1)]
    """
    # getCostofActions:  <bound method PositionSearchProblem.getCostOfActions of <searchAgents.PositionSearchProblem object at 0x1016f1308>>
    "*** YOUR CODE HERE ***"
    stk = util.Stack() #((5, 4), 'South', 1))
    path = [] #['South', ]
    visited = [] #[(5, 5), ]
    current_path = dict() #{((5, 4), 'South', 1): ((5, 5), None, None), }

    start = (problem.getStartState(), None, None)
    stk.push(start)

    while stk.isEmpty != 0:
        current = stk.pop()
        if(current[0] in visited): continue
        visited.append(current[0])

        # goal state를 찾은 경우
        if problem.isGoalState(current[0]):
            while current[0] != start[0]:
                path.append(current[1])
                current = current_path[current]

            path.reverse()
            return path
        
        # goal state를 찾지 못한 경우
        for succ in problem.getSuccessors(current[0]):
            if succ[0] not in visited:
                stk.push(succ)
                current_path[succ] = current

    return None
    # util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    q = util.Queue()
    visited = []
    current_path = dict()
    path = []

    start = (problem.getStartState(), None, None)
    q.push(start)
    
    while q.isEmpty != 0:
        current = q.pop()
        if(current[0] in visited): continue

        visited.append(current[0])

        if problem.isGoalState(current[0]):
            while current[0] != start[0]:
                path.append(current[1])
                current = current_path[current]

            path.reverse()
            return path
        
        for succ in problem.getSuccessors(current[0]):
            if succ[0] not in visited:
                q.push(succ)
                current_path[succ] = current

    return None
    # util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    # print(problem.getCostOfActions(['South', 'West']))
    pq = util.PriorityQueue() # [(priority, self.count, ((5,5), None, None)), ]
    visited = []

    start = (problem.getStartState(), []) # [((5, 5), [])]
    pq.push(start, 0)

    while pq.isEmpty != 0:
        current = pq.pop()
        if(current[0] in visited): continue
        visited.append(current[0])

        if problem.isGoalState(current[0]):
            return current[1]
        
        for succ in problem.getSuccessors(current[0]):
            pq.push((succ[0], current[1] + [succ[1]]), problem.getCostOfActions(current[1]) + succ[2])

    return None
    # util.raiseNotDefined()

def nullHeuristic(current, problem=None):
    """
    A heuristic function estimates the cost from the current current to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    print(heuristic)
    # pq = util.PriorityQueue()
    # visited = []

    # start = (problem.getStartState(), [])
    # pq.push(start, heuristic(start, problem))


    # util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch