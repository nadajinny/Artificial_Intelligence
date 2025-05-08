# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.

import random

from search import SearchProblem


class EightPuzzleState:
    """
    This class defines the mechanics of the puzzle itself.
    The task of recasting this puzzle as a search problem is left to the EightPuzzleSearchProblem class.
    """

    def __init__(self, numbers):
        """
          Constructs a new eight puzzle from an ordering of numbers.

        numbers: a list of integers from 0 to 8 representing an
          instance of the eight puzzle.  0 represents the blanㅎk
          space.  Thus, the list

            [1, 0, 2, 3, 4, 5, 6, 7, 8]

          represents the eight puzzle:
            -------------
            | 1 |   | 2 |
            -------------
            | 3 | 4 | 5 |
            -------------
            | 6 | 7 | 8 |
            ------------

        The configuration of the puzzle is stored in a 2-dimensional
        list (a list of lists) 'cells'.
        """
        self.cells = []
        numbers = numbers[:]  # Make a copy so as not to cause side-effects.
        numbers.reverse()
        for row in range(3):
            self.cells.append([])
            for col in range(3):
                self.cells[row].append(numbers.pop())
                if self.cells[row][col] == 0:
                    self.blankLocation = row, col

    def isGoal(self):
        """
          Checks to see if the puzzle is in its goal state.

            -------------
            | 1 | 2 | 3 |
            -------------
            | 4 | 5 | 6 |
            -------------
            | 7 | 8 | 0 |
            -------------

        >>> EightPuzzleState([1, 2, 3, 4, 5, 6, 7, 8, 0]).isGoal()
        True

        >>> EightPuzzleState([1, 0, 2, 3, 4, 5, 6, 7, 8]).isGoal()
        False
        """
        current = 1
        for row in range(3):
            for col in range(3):
                if current % 9 != self.cells[row][col]:
                    return False
                current += 1
        return True

    def legalMoves(self):
        """
          Returns a list of legal moves from the current state.

        Moves consist of moving the blank space up, down, left or right.
        These are encoded as 'up', 'down', 'left' and 'right' respectively.

        >>> EightPuzzleState([1, 2, 3, 4, 5, 6, 7, 8, 0]).legalMoves()
        ['up', 'left']
        """
        moves = []
        row, col = self.blankLocation
        if row != 0:
            moves.append('up')
        if row != 2:
            moves.append('down')
        if col != 0:
            moves.append('left')
        if col != 2:
            moves.append('right')
        return moves

    def result(self, move):
        """
        Returns a new eightPuzzle with the current state and blankLocation
        updated based on the provided move.

        The move should be a string drawn from a list returned by legalMoves.
        Illegal moves will raise an exception, which may be an array bounds
        exception.

        NOTE: This function *does not* change the current object.
        Instead, it returns a new object.
        """
        row, col = self.blankLocation
        if move == 'up':
            newrow = row - 1
            newcol = col
        elif move == 'down':
            newrow = row + 1
            newcol = col
        elif move == 'left':
            newrow = row
            newcol = col - 1
        elif move == 'right':
            newrow = row
            newcol = col + 1
        else:
            raise Exception("Illegal Move")

        # Create a copy of the current eightPuzzle
        newPuzzle = EightPuzzleState([0, 0, 0, 0, 0, 0, 0, 0, 0])
        newPuzzle.cells = [values[:] for values in self.cells]

        # And update it to reflect the move
        newPuzzle.cells[row][col] = self.cells[newrow][newcol]
        newPuzzle.cells[newrow][newcol] = self.cells[row][col]
        newPuzzle.blankLocation = newrow, newcol

        return newPuzzle

    # Utilities for comparison and display
    def __eq__(self, other):
        """
            Overloads '==' such that two eightPuzzles with the same configuration
          are equal.

          >>> EightPuzzleState([0, 1, 2, 3, 4, 5, 6, 7, 8]) == \
              EightPuzzleState([1, 0, 2, 3, 4, 5, 6, 7, 8]).result('left')
          True
        """
        for row in range(3):
            if self.cells[row] != other.cells[row]:
                return False
        return True

    def __hash__(self):
        return hash(str(self.cells))

    def __str__(self):
        lines = []
        horizontal_line = ('-' * 13)
        lines.append(horizontal_line)
        for row in self.cells:
            rowLine = '|'
            for col in row:
                if col == 0:
                    col = ' '
                rowLine = rowLine + ' ' + col.__str__() + ' |'
            lines.append(rowLine)
            lines.append(horizontal_line)
        return '\n'.join(lines)


class EightPuzzleSearchProblem(SearchProblem):
    """
      Implementation of a SearchProblem for the EightPuzzle domain
      Each state is represented by an instance of an eightPuzzle.
    """

    def __init__(self, puzzle):
        self.puzzle = puzzle

    def getStartState(self):
        return self.puzzle

    def isGoalState(self, state):
        return state.isGoal()

    def getSuccessors(self, state):
        """
          Returns list of (successor, action, stepCost) pairs where
          each succesor is either left, right, up, or down
          from the original state and the cost is 1.0 for each
        """
        succ = []
        for a in state.legalMoves():
            succ.append((state.result(a), a, 1))
        return succ

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves
        """
        return len(actions)


def createRandomEightPuzzle(moves=100):
    """
      moves: number of random moves to apply

      Creates a random eight puzzle by applying a series of 'moves' random moves to a solved puzzle.
    """
    puzzle = EightPuzzleState([1, 2, 3, 4, 5, 6, 7, 8, 0])
    for _ in range(moves):
        # Execute a random legal move
        puzzle = puzzle.result(random.sample(puzzle.legalMoves(), 1)[0])
    return puzzle
