# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()
        # print("legalMoves: ", legalMoves)
        # legalMoves:  ['West', 'Stop', 'East', 'North', 'South']

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        # print("currentGameState: \n", currentGameState)
            # %%%%%%%%%%%%%%%%%%%%%%%%%
            # %                       %
            # %     .>          G     %
            # %                       %
            # %                       %
            # %                       %
            # %                       %
            # %                      o%
            # %%%%%%%%%%%%%%%%%%%%%%%%%
            # score: 
        successorGameState = currentGameState.generatePacmanSuccessor(action) #Game State
        # print("successorGameState: \n", successorGameState)
            # %%%%%%%%%%%%%%%%%%%%%%%%%
            # %                       %
            # %     .           G     %
            # %      ^                %
            # %                       %
            # %                       %
            # %                       %
            # %                      o%
            # %%%%%%%%%%%%%%%%%%%%%%%%%
            # score: 
        newPos = successorGameState.getPacmanPosition() #Pacman Position
        #print("newPos: \n", newPos)
        # newPos: 
        # (7, 5)
        newFood = successorGameState.getFood() #Food Position
        # print("newFood: \n", newFood)
        # FFFFFFFFFFFFFFFFFFFFFFFFF
        # FFFFFFFFFFFFFFFFFFFFFFFFF
        # FFFFFFTFFFFFFFFFFFFFFFFFF
        # FFFFFFFFFFFFFFFFFFFFFFFFF
        # FFFFFFFFFFFFFFFFFFFFFFFFF
        # FFFFFFFFFFFFFFFFFFFFFFFFF
        # FFFFFFFFFFFFFFFFFFFFFFFFF
        # FFFFFFFFFFFFFFFFFFFFFFFFF
        # FFFFFFFFFFFFFFFFFFFFFFFFF
        # food = T, no food = F
        # print("newFood.asList(): ",newFood.asList())
        # newFood.asList():  [(6, 6), (15, 3), (15, 5), (16, 3), (17, 3), (17, 4), (18, 4), (19, 4)]

        newGhostStates = successorGameState.getGhostStates() #Ghost State
        # newGhostStates object has a function such as getPosition, getDirection
        # print("newGhostStates: \n", newGhostStates)
        # newGhostStates: 
        # [<game.AgentState object at 0x10860fc40>]
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates] #
        # print("newScaredTimes: \n", newScaredTimes)
        
        "*** YOUR CODE HERE ***"
        # distance from pacman to ghost
        if successorGameState.isWin(): # if there exists winning in next state
            return float("inf")
        
        # Ghost
        ClosestActiveGhost_Dist = float("inf")
        for ghost in newGhostStates:
            if ghost.scaredTimer == 0: # if ghost is not in scared state
                ClosestActiveGhost_Dist = min(ClosestActiveGhost_Dist, manhattanDistance(newPos, ghost.getPosition()))
            if ClosestActiveGhost_Dist < 2: # if pacman and ghost is too close
                return float("-inf")
        GhostScore = ClosestActiveGhost_Dist

        # Food
        ClosestFood_Dist = float("inf")
        
        for food in newFood.asList():
            ClosestFood_Dist = min(ClosestFood_Dist, manhattanDistance(newPos, food))
        NumFood = successorGameState.getNumFood() # number of food left
        FoodScore = - ClosestFood_Dist - 45 * NumFood

        # BonusScore
        BonusScore = 0
        if ClosestActiveGhost_Dist < 2: # if Pacman is close to Active Ghost
            BonusScore = -40/ClosestActiveGhost_Dist
        if ClosestFood_Dist < 2: # if Food is close to Pacman
            BonusScore += 30
        if action == "Stop": # if Pacman doesn't do an action
            BonusScore -= 10

        # The Safer, the higher score
        # Smaller, Better For Pacman => evalFunc -
        # ClosestFood_Dist

        # Larger, Better For Pacman => evalFunc +
        # ClosestGhost_Dist

        Score = BonusScore + FoodScore + GhostScore
        return Score

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(AgentIndex):
        Returns a list of legal actions for an agent
        AgentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(AgentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        # def value(state):
        def value(gameState, CurrentDepth, AgentIndex):
            # if the state is a terminal state: return the state's utility
            if gameState.isWin() or gameState.isLose() or CurrentDepth == self.depth:
                return self.evaluationFunction(gameState)
            # if the next agent is MAX: return max-value(state)
            if AgentIndex == 0:
                return max_value(gameState, CurrentDepth)
            # if the next agent is MIN: return min-value(state)
            else:
                return min_value(gameState, CurrentDepth, AgentIndex)
            
        # def max-value(state):
        def max_value(gameState, CurrentDepth):
            # initialize v = -infinite
            v = float("-inf")
            LegalActions = gameState.getLegalActions(0)
            # for each successor of state:
            for action in LegalActions:
                SuccessorState = gameState.generateSuccessor(0, action)
                 # v = max(v, value(successor))
                v = max(v, value(SuccessorState, CurrentDepth, 1))
            # return v
            return v

        # def min-value(state)
        def min_value(gameState, CurrentDepth, AgentIndex):
            # initialize v = +inf
            v = float("+inf")
            # for each successor of state:
            LegalActions = gameState.getLegalActions(AgentIndex)
            for action in LegalActions:
                SuccessorState = gameState.generateSuccessor(AgentIndex, action)
                if AgentIndex == gameState.getNumAgents() - 1: # if last ghost agent
                    # v = min(v, value(successor))
                    v = min(v, value(SuccessorState, CurrentDepth + 1, 0))
                else:
                    v = min(v, value(SuccessorState, CurrentDepth, AgentIndex + 1))
            # return v
            return v
        
        MaxValue = float("-inf")
        BestAction = Directions.STOP # initialize BestAction as STOP
        LegalActions = gameState.getLegalActions(0) # available actions from root state
        for action in LegalActions:
            # available successorstates from available actions
            SuccessorState = gameState.generateSuccessor(0, action)
            # starting point: depth = 0
            TempValue = value(SuccessorState, 0, 1)
            # find MaxValue and BestAction
            if MaxValue < TempValue:
                MaxValue = TempValue
                BestAction = action

        return BestAction
        # util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        # def value(state):
        def value(gameState, CurrentDepth, AgentIndex, a, b):
            # if the state is a terminal state: return the state's utility
            if gameState.isWin() or gameState.isLose() or CurrentDepth == self.depth:
                return self.evaluationFunction(gameState)
            # if the next agent is MAX: return max-value(state)
            if AgentIndex == 0:
                return max_value(gameState, CurrentDepth, a, b)
            # if the next agent is MIN: return min-value(state)
            else:
                return min_value(gameState, CurrentDepth, AgentIndex, a, b)
        
        # def max-value(state):
        def max_value(gameState, CurrentDepth, a, b):
            # initialize v = -infinite
            v = float("-inf")
            LegalActions = gameState.getLegalActions(0)
            # for each successor of state:
            for action in LegalActions:
                SuccessorState = gameState.generateSuccessor(0, action)
                # v = max(v, value(successor))
                v = max(v, value(SuccessorState, CurrentDepth, 1, a, b))
                # if v > b return v
                if v > b:
                    return v
                # a = max(a, v)
                a = max(a, v)
            # return v
            return v

        # def min-value(state)
        def min_value(gameState, CurrentDepth, AgentIndex, a, b):
            # initialize v = +inf
            v = float("+inf")
            # for each successor of state:
            LegalActions = gameState.getLegalActions(AgentIndex)
            for action in LegalActions:
                SuccessorState = gameState.generateSuccessor(AgentIndex, action)
                if AgentIndex == gameState.getNumAgents() - 1: # if last ghost agent
                    # v = min(v, value(successor))
                    v = min(v, value(SuccessorState, CurrentDepth + 1, 0, a, b))
                else:
                    v = min(v, value(SuccessorState, CurrentDepth, AgentIndex + 1, a, b))
                # if v < a return v
                if v < a:
                    return v
                # b = min(b, v)
                b = min(b, v)
            # return v
            return v

        MaxValue = float("-inf")
        a = float("-inf")
        b = float("+inf")
        BestAction = Directions.STOP # initialize BestAction as STOP
        LegalActions = gameState.getLegalActions(0) # available actions from root state
        for action in LegalActions:
            # available successorstates from available actions
            SuccessorState = gameState.generateSuccessor(0, action) 
            # starting point: depth = 0
            TempValue = value(SuccessorState, 0, 1, a, b)
            # find MaxValue and BestAction
            if MaxValue < TempValue:
                MaxValue = TempValue
                BestAction = action
            if MaxValue > b:
                return BestAction
            a = max(a, MaxValue)

        return BestAction
        # util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
