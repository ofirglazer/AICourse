import tictactoe as ttt

# test implementation of ttt: player, actions, result, winner, terminal, utility, minimax


def test_player():
    # empty
    board = ttt.initial_state()
    print(f"Empty board, should be X: {ttt.player(board)}")

    # one X
    board[0][0] = ttt.X
    print(f"1 X, should be O: {ttt.player(board)}")

    # one X and one O
    board[1][2] = ttt.O
    print(f"1 X and 1 O, should be X: {ttt.player(board)}")


def test_winner_utility():
    board = ttt.initial_state()
    board[0][0] = board[0][1] = ttt.X
    board[1][0] = board[1][1] = ttt.O
    print(f"No winner: {ttt.winner(board)}")
    board[0][2] = ttt.X
    print(f"X wins: {ttt.winner(board)}")
    print(f"Utility for X win: {ttt.utility(board)}")
    board[0][2] = ttt.EMPTY
    board[1][2] = ttt.O
    print(f"O wins: {ttt.winner(board)}")
    print(f"Utility for O win: {ttt.utility(board)}")
    board[2][0] = board[1][2] = board[2][2] = ttt.X
    board[2][1] = board[0][2] = ttt.O
    print(f"Utility for tie: {ttt.utility(board)}")


def test_actions():
    # empty
    board = ttt.initial_state()
    print(f"Empty board, should all 9 moves: {ttt.actions(board)}")

    # after 5 moves
    board[1][2] = board[2][1] = board[0][0] = ttt.X
    board[0][1] = board[0][2] = ttt.O
    print(f"After 5 moves, should be (1,0),(1,1),(2,0),(2,2): {ttt.actions(board)}")


def test_result():
    board = ttt.initial_state()
    board = ttt.result(board, (0, 0))
    print(f"1st X in (0,0):")
    print(*board, sep="\n")

    board = ttt.result(board, (1, 1))
    print(f"2nd O in (1,1):")
    print(*board, sep="\n")

    print(f"Invalid (1,1):")
    board = ttt.result(board, (1, 1))


def test_terminal():
    board = ttt.initial_state()
    board[0][0] = board[0][1] = ttt.X
    board[1][0] = board[1][1] = ttt.O
    print(f"Not terminal: {ttt.terminal(board)}")

    board[0][2] = ttt.X
    print(f"Terminal due to win X: {ttt.terminal(board)}")

    board[2][1] = board[0][2] = board[0][2] = ttt.O
    board[2][0] = board[2][2] = board[1][2] = ttt.X
    print(f"Terminal due to tie: {ttt.terminal(board)}")


def test_minimax():
    board = ttt.initial_state()
    # board[0][0] = board[0][1] = board[1][2] = ttt.X
    # board[2][1] = board[0][2] = board[2][2] = ttt.O
    action = ttt.minimax(board)
    print(action)


def main():
    # test_player()
    # test_actions()
    # test_result()
    # test_winner_utility()
    # test_terminal()
    test_minimax()


if __name__ == "__main__":
    main()
