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


##linkhayeestefadeshode:
#https://github.com/lightninglu10/pacman-minimax/blob/master/multiAgents.py
#https://github.com/opalkale/pacman-multiagent/blob/master/multiAgents.py
import imp
from util import manhattanDistance
from game import Directions
import random
import util

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

        # Choose one of the best actions
        scores = [self.evaluationFunction(
            gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(
            len(scores)) if scores[index] == bestScore]
        # Pick randomly among the best
        chosenIndex = random.choice(bestIndices)

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
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        res = 0
        states=[]
        countoffood = currentGameState.getNumFood()
        if countoffood > successorGameState.getNumFood():
            states.append(1000) 
        if countoffood == 0:
            return float("inf")
        
        for ghost in newGhostStates:
            if manhattanDistance(newPos, ghost.getPosition()) < 2:
                if ghost.scaredTimer > 0:
                        states.append(300)
                else:
                    return float("-inf")
            
            else:
                states.append(-90*manhattanDistance(ghost.getPosition() , newPos))
        if len(newFood.asList()) > 0:
            for food in newFood.asList():
                states.append(100-manhattanDistance(food,newPos))
        nextcapsules = successorGameState.getCapsules()
        if len(nextcapsules) > 0:
            for capsule in successorGameState.getCapsules():
                states.append(manhattanDistance(capsule,newPos))
        capsule = currentGameState.getCapsules()
        if len(capsule) > 0:
            if capsule[0] == newPos:
                states.append(400) 
            else:
                states.append( 140- manhattanDistance(capsule[0], newPos))
        if action == 'Stop':
            return -9000
        return max(states)

        
        


        

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

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)
        self.nodesCount = 0


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """
    def MaxValue(self, gameState, depth):
        b1=gameState.isWin()
        b2=gameState.isLose()
        
        if  b1 or b2 or depth == 0:
            evalution=self.evaluationFunction(gameState)
            return evalution
        
        actions=gameState.getLegalActions(0)#get all legal actions for pacman ->5 number states
        infiniti = -9999999
        for action in actions:
            infiniti = max(infiniti, self.MinValue(gameState.generateSuccessor(0, action), depth, 1))
        return infiniti
    
    def MinValue(self, gameState, depth, numberofagent):
        b1=gameState.isWin()
        b2=gameState.isLose()
        if  b1 or b2 or depth == 0:
            evalution=self.evaluationFunction(gameState)
            return evalution
        actions=gameState.getLegalActions(numberofagent)
        infiniti = 99999999
        for action in actions:
            #generate successor: ba on actrion ke jahat ro mige state badi ro tolid mikone
            lastghost=gameState.getNumAgents() - 1
            if numberofagent == lastghost:
                infiniti = min(infiniti, self.MaxValue(gameState.generateSuccessor(numberofagent, action), depth - 1))
            if numberofagent < lastghost:
                infiniti = min(infiniti, self.MinValue(gameState.generateSuccessor(numberofagent, action), depth, numberofagent + 1))
        return infiniti
    
    def minimax(self, gameState):
        b1=gameState.isWin()
        b2=gameState.isLose()
        if  b1 or b2:
            evalution=self.evaluationFunction(gameState)
            return evalution
        min = -999999
        action = None
        nextactions=gameState.getLegalActions(0)
        for nextaction in nextactions:#max min haro migire va barmigardone bara pacman ke bazi azash shoro mishe yani dar roote
            successor = gameState.generateSuccessor(0, nextaction)
            next = self.MinValue(successor, self.depth, 1)#
            if next > min:
                min = next
                action = nextaction
        return action
    
    def getAction(self, gameState):
        
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        with open('MinimaxAgent.txt', 'a') as f:
            f.write(f"\n {self.nodesCount}")
        "*** YOUR CODE HERE ***"
        for i in range(self.depth):
            self.nodesCount += 1
            # chosen_action = self.minimax(gameState, self.depth)[1]
        # return chosen_action
        return self.minimax(gameState)
        
   

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        with open('AlphaBetaAgent.txt', 'a') as f:
            f.write(f"\n {self.nodesCount}")
        "*** YOUR CODE HERE ***"
        for i in range(self.depth):
            self.nodesCount += 1
        return self.minimax(gameState,  -999999, 999999,self.depth, 0)[1]
    def minimax(self, gameState,  alpha, beta,depth, numberofagent):
        if depth == 0 or gameState.isWin() or gameState.isLose():
            
            return self.evaluationFunction(gameState), None
        if numberofagent == 0:
            return self.Alphamaxvalue(gameState,  alpha, beta,depth, numberofagent)
        if numberofagent!=0:
            return self.betaminvalue(gameState,  alpha, beta,depth, numberofagent)
    def Alphamaxvalue(self, gameState,  alpha, beta,depth, numberofagent):
        mymax = -9999999
        bestact = None
        for action in gameState.getLegalActions(numberofagent):
            successor = gameState.generateSuccessor(numberofagent, action)
            next = self.minimax(successor, alpha, beta,depth, 1)[0]
            if (next > mymax):
                mymax = next
                bestact = action
            if mymax > beta:
                # agar in action ke ma dar hal max geraftan az anim as beta ke max marhale ghabl tar ast bozorg tar bashad niyaz be check kardan baghiye maghadir an action ha nist chon dar marhale bad ke minimum giri ast hargez entekhab nemishavand
                return mymax, bestact
            alpha = max(alpha, mymax)
            result=(mymax, bestact)
        return result
    def betaminvalue(self, gameState,  alpha, beta,depth, numberofagent):
        mymin = 99999
        bestact = None
        for action in gameState.getLegalActions(numberofagent):
            successor = gameState.generateSuccessor(numberofagent, action)
            lastghost=gameState.getNumAgents() - 1
            if numberofagent == lastghost:
                next = self.minimax(successor,  alpha, beta,depth - 1, 0)[0]
            else:
                next = self.minimax(successor,  alpha, beta,depth, numberofagent + 1)[0]
            if next < mymin:
                mymin = next
                bestact = action
            if mymin < alpha:
                return mymin, bestact
            beta = min(beta, mymin)
        result=(mymin, bestact)
        return result
    
    

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
