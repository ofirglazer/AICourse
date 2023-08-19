"""
Tic Tac Toe Player
"""
import copy
# import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    Any return value is acceptable for terminal board.
    """
    count_x = count_o = 0
    for row in range(3):
        count_x += board[row].count('X')
        count_o += board[row].count('O')

    if count_x == 0 or count_x == count_o:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    Any return value is acceptable if a terminal board is provided as input.
    """
    actions_set = set()
    for row in range(3):
        for col in range(3):
            if board[row][col] == EMPTY:
                actions_set.add((row, col))

    return actions_set


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    If invalid move, raise Exception.
    Result is a deepcopy board
    """

    # check validity of move
    if board[action[0]][action[1]] != EMPTY:
        raise Exception("Invalid move - not empty")

    next_board = copy.deepcopy(board)
    next_board[action[0]][action[1]] = player(board)
    return next_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    Otherwise, return None.
    """

    for idx in range(3):
        # check rows
        if board[idx][0] == X and board[idx][1] == X and board[idx][2] == X:
            return X
        if board[idx][0] == O and board[idx][1] == O and board[idx][2] == O:
            return O

        # check columns
        if board[0][idx] == X and board[1][idx] == X and board[2][idx] == X:
            return X
        if board[0][idx] == O and board[1][idx] == O and board[2][idx] == O:
            return O

        # check diagonals
        if board[0][0] == X and board[1][1] == X and board[2][2] == X:
            return X
        if board[0][2] == X and board[1][1] == X and board[2][0] == X:
            return X
        if board[0][0] == O and board[1][1] == O and board[2][2] == O:
            return O
        if board[0][2] == O and board[1][1] == O and board[2][0] == O:
            return O

    # no winner
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    # if any player has won
    if winner(board) is not None:
        return True

    # if all squares are occupied
    count_xo = 0
    for row in range(3):
        count_xo += board[row].count('X')
        count_xo += board[row].count('O')
    if count_xo == 9:
        return True

    # otherwise, game in not ended
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    Assuming utility will only be called on a board if terminal(board) is True.
    """
    winner_player = winner(board)
    if winner_player == X:
        return 1
    if winner_player == O:
        return -1
    return 0


def minimax_eval(board):

    if terminal(board):
        return utility(board)


    if player(board) == X:
        # maximizing player
        v = -2
        for action in actions(board):
            v = max(v, minimax_eval(result(board, action)))
        return v
    else:
        # minimizing player
        v = 2
        for action in actions(board):
            v = min(v, minimax_eval(result(board, action)))
    return v


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    If the board is a terminal board, the minimax function should return None.

    Pseudocode:

    Given a state s
    The maximizing player picks action a in Actions(s) that produces the highest value of Min-Value(Result(s, a)).
    The minimizing player picks action a in Actions(s) that produces the lowest value of Max-Value(Result(s, a)).

    Function Max-Value(state)
    v = -∞
    if Terminal(state):
    return Utility(state)
    for action in Actions(state):
    v = Max(v, Min-Value(Result(state, action)))
    return v

    Function Min-Value(state):
    v = ∞
    if Terminal(state):
    return Utility(state)
    for action in Actions(state):
    v = Min(v, Max-Value(Result(state, action)))
    return v
    """

    if terminal(board):
        return None

    evaluated_actions = []
    for action in actions(board):
        evaluated_actions.append((action, minimax_eval(result(board, action))))
    if player(board) == X:
        return max(evaluated_actions, key=lambda item: item[1])[0]
    else:
        return min(evaluated_actions, key=lambda item: item[1])[0]
