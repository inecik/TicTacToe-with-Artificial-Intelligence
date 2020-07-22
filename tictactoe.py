"""
Tic Tac Toe Player
"""

from copy import deepcopy
import math

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
    """
    return X if [j for i in board for j in i].count(EMPTY) % 2 == 1 else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    return {(i, j) for i in range(len(board)) for j in range(len(board)) if board[i][j] == EMPTY}


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    board_new = deepcopy(board)
    assert action in actions(board_new)
    board_new[action[0]][action[1]] = player(board_new)
    return board_new


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for row in board:
        if len(set(row)) == 1 and row[0]:
            return row[0]
    for col in map(list, zip(*board)):
        if len(set(col)) == 1 and col[0]:
            return col[0]
    if (len({board[0][0], board[1][1], board[2][2]}) == 1 or len({board[2][0], board[1][1], board[2][0]}) == 1) \
            and board[1][1]:
        return board[1][1]
    return None



def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return len(actions(board)) == 0 or winner(board) is not None


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    game_over = winner(board)
    if game_over == X:
        return 1
    elif game_over == O:
        return -1
    else:
        return 0


class MinimaxNode():
    def __init__(self):
        self.board = None
        self.player = None
        self.utility = None
        self.parent = None


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    utility_under_tree = []
    actions_under_tree = []
    whose_turn = player(board)
    possible_actions = actions(board)
    for action in possible_actions:
        board_new = result(board, action)
        if terminal(board_new):
            utility_under_tree.append(utility(board_new))
        else:
            # This is not alpha-beta prone.
            # It is implemented to make the code work faster.
            if whose_turn == X and 1 in utility_under_tree:
                break
            elif whose_turn == O and -1 in utility_under_tree:
                break
            utility_under_tree.append(minimax(board_new)[0])  # To give the value under the child branch
        actions_under_tree.append(action)
    if whose_turn == X:
        how_to_select = max(utility_under_tree)
    else:
        how_to_select = min(utility_under_tree)
    return how_to_select, actions_under_tree[utility_under_tree.index(how_to_select)]
