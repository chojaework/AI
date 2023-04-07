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
        Returns the start CurrentItem for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, CurrentItem):
        """
          CurrentItem: Search CurrentItem

        Returns True if and only if the CurrentItem is a valid goal CurrentItem.
        """
        util.raiseNotDefined()

    def getSuccessors(self, CurrentItem):
        """
          CurrentItem: Search CurrentItem

        For a given CurrentItem, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the CurrentItem
        CurrentItem, 'action' is the action required to get there, and 'stepCost' is
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
    # dfs uses a stack to implement
    stk = util.Stack()
    # list used to check if the node has been visited
    visited = []
    StartState = problem.getStartState()
    # StartItem: [(5, 5), [Cumulated Path from StartState]]
    StartItem = [StartState, []]
    stk.push(StartItem)

    # repeat until stack is empty
    while stk.isEmpty != 1:
        CurrentItem = stk.pop()
        CurrentState = CurrentItem[0]
        CurrentPath = CurrentItem[1]

        if CurrentState in visited: continue
        visited.append(CurrentState)

        # GoalState found
        if problem.isGoalState(CurrentState):
            return CurrentPath
        
        # GoalState not found -> Push successors to the stack
        for succ in problem.getSuccessors(CurrentState):
            succState = succ[0]
            succPath = succ[1]
            stk.push([succState, CurrentPath + [succPath]])

    return None
    # util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    # bfs uses a stack to implement
    q = util.Queue()
    # list used to check if the node has been visited
    visited = []
    StartState = problem.getStartState()
    # StartItem: [(5, 5), [Cumulated Path from StartState]]
    StartItem = [StartState, []]
    q.push(StartItem)

    # repeat until queue is empty
    while q.isEmpty != 1:
        CurrentItem = q.pop()
        CurrentState = CurrentItem[0]
        CurrentPath = CurrentItem[1]

        if CurrentState in visited: continue
        visited.append(CurrentState)

        # GoalState found
        if problem.isGoalState(CurrentState):
            return CurrentPath
        
        # GoalState not found -> Push successors to the stack
        for succ in problem.getSuccessors(CurrentState):
            succState = succ[0]
            succPath = succ[1]
            q.push([succState, CurrentPath + [succPath]])
    # util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    # print(problem.getCostOfActions(['South', 'West']))
    pq = util.PriorityQueue() # [(priority, self.count, ((5,5), None, None)), ]
    visited = []
    StartState = problem.getStartState()
    StartItem = (StartState, []) 
    # [((5, 5), [Cumulated Path from StartState])]
    pq.push(StartItem, 0)
    # 0: Cost

    # repeat until priority queue is empty
    while pq.isEmpty != 1:
        CurrentItem = pq.pop()
        CurrentState =CurrentItem[0]
        CurrentPath = CurrentItem[1]

        if(CurrentState in visited): continue 
        visited.append(CurrentState)

        # GoalState found
        if problem.isGoalState(CurrentState):
            return CurrentPath
        
        # GoalState not found
        for succ in problem.getSuccessors(CurrentState):
            succState = succ[0]
            succPath = succ[1]
            succCost = succ[2]
            
            pq.update((succState, 
                       CurrentPath + [succPath]
                       ), 
                       problem.getCostOfActions(CurrentPath) + succCost)

    return None
    # util.raiseNotDefined()

def nullHeuristic(CurrentItem, problem=None):
    """
    A heuristic function estimates the cost from the CurrentItem CurrentItem to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    pq = util.PriorityQueue() # [(priority, self.count, ((5,5), None, None)), ]
    visited = []
    StartState = problem.getStartState()
    StartItem = (StartState, []) # [((5, 5), [])]
    pq.push(StartItem, heuristic(StartState, problem))
    
    # repeat until priority queue is empty
    while pq.isEmpty != 1:
        CurrentItem = pq.pop()
        CurrentState =CurrentItem[0]
        CurrentPath = CurrentItem[1]

        if(CurrentState in visited): continue
        visited.append(CurrentState)

        # GoalState found
        if problem.isGoalState(CurrentState):
            return CurrentPath
        
        # GoalState not found
        for succ in problem.getSuccessors(CurrentState):
            succState = succ[0]
            succPath = succ[1]
            succCost = succ[2]

            pq.update((succState, 
                       CurrentPath + [succPath]), 
                       problem.getCostOfActions(CurrentPath) + succCost + heuristic(succState, problem))

    return None
    # util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch