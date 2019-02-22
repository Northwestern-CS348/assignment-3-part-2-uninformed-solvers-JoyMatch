from solver import *
from queue import Queue

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        if self.currentState not in self.visited:
            self.visited[self.currentState]=True
            return self.currentState.state == self.victoryCondition

        if self.currentState.state == self.victoryCondition:
            self.visited[self.currentState]=True
            return True

        if not self.currentState.children:
            for move in self.gm.getMovables():
                self.gm.makeMove(move)
                childrenState = GameState(self.gm.getGameState(), self.currentState.depth+1, move)
                if childrenState not in self.visited:
                    childrenState.parent = self.currentState
                    self.currentState.children.append(childrenState)
                self.gm.reverseMove(move)

        if self.currentState.nextChildToVisit<len(self.currentState.children):
            nextState = self.currentState.children[self.currentState.nextChildToVisit]
            self.currentState.nextChildToVisit += 1
            self.gm.makeMove(nextState.requiredMovable)
            self.currentState = nextState
            return self.solveOneStep()
        else:
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = self.currentState.parent
            return self.solveOneStep()


class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
        self.queue = Queue()

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        if self.currentState.state == self.victoryCondition:
            self.visited[self.currentState]=True
            return True
        return self.BFS()


    def BFS(self):

        for move in self.gm.getMovables():
            self.gm.makeMove(move)
            childrenState = GameState(self.gm.getGameState(), self.currentState.depth+1, move)
            self.currentState.children.append(childrenState)
            if childrenState in self.visited:
                self.gm.reverseMove(move)
                continue
            childrenState.parent = self.currentState
            self.queue.put(childrenState)
            self.visited[childrenState] = True
            self.gm.reverseMove(move)

        backState = self.currentState
        while backState.requiredMovable is not None:
            move = backState.requiredMovable
            self.gm.reverseMove(move)
            backState = backState.parent

        if self.queue.empty():
            return True
        self.currentState = self.queue.get()

        stackMovable = []
        backState = self.currentState
        while backState.requiredMovable is not None:
            move = backState.requiredMovable
            stackMovable.append(move)
            backState = backState.parent

        while len(stackMovable) != 0:
            self.gm.makeMove(stackMovable.pop())

        return False