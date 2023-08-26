import cProfile
import pstats
import copy
from random import shuffle

from util import Node, QueueFrontier, print_tiles  # StackFrontier


def gen_board(rows, cols):
    # init board
    board_row = [*range(0, rows * cols)]
    shuffle(board_row)
    start_board = []
    for row in range(rows):
        start_board.append(board_row[row * cols:row * cols + cols])

    # easy 4x4
    # start_board[0][0:4] = [1, 2, 3, 7]
    # start_board[1][3] = 0

    # easy 2x3
    # start_board[0][0:3] = [1, 2, 5]
    # start_board[1][2] = 0

    return start_board


class Board:

    def __init__(self, start_board):
        self.start = Node(state=start_board, parent=None, action=None)
        self.size = (len(start_board), len(start_board[0]))
        self.total = self.size[0] * self.size[1]

        # Keep track of number of states explored
        self.num_explored = 0
        # Initialize an empty explored set
        self.explored = set()

        self.goal_1d = [*range(0, self.total)]

    def neighbors(self, node):
        empty_idx = node.state_1d.index(0)
        empty_row = empty_idx // self.size[1]
        empty_col = empty_idx % self.size[1]
        candidates = [
            ("up", (empty_row - 1, empty_col)),
            ("down", (empty_row + 1, empty_col)),
            ("left", (empty_row, empty_col - 1)),
            ("right", (empty_row, empty_col + 1))
        ]

        result = []
        for action, (r, c) in candidates:
            if 0 <= r < self.size[0] and 0 <= c < self.size[1]:
                new_state = copy.deepcopy(node.state)
                new_state[empty_row][empty_col] = node.state[r][c]
                new_state[r][c] = 0
                result.append((action, new_state))
        return result

    def solve(self):
        """Finds a solution to a 15 tiles board, if one exists."""

        # Initialize frontier to just the starting position
        frontier = QueueFrontier()
        frontier.add(self.start)

        # Keep looping until solution found
        while True:

            # If nothing left in frontier, then no path
            if frontier.empty():
                raise Exception("no solution")

            # Choose a node from the frontier
            node = frontier.remove()
            self.num_explored += 1
            if not self.num_explored % 1000:
                print(f"{self.num_explored} states explored, {len(frontier.frontier)} in frontier")

            # If node is the goal, then we have a solution
            if node.state_1d == self.goal_1d:
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return

            # Mark node as explored
            self.explored.add(node.state_str)

            # Add neighbors to frontier
            for action, state in self.neighbors(node):
                child = Node(state=state, parent=node, action=action)
                if not frontier.contains_state(state) and child.state_str not in self.explored:
                    frontier.add(child)

    def print_start(self):
        print_tiles(self.start.state)


def main():
    board = Board(gen_board(2, 4))
    print("Original board:")
    board.print_start()
    print("Solving...")
    board.solve()
    print("States Explored:", board.num_explored)
    print("Solution:")

    print(f"{len(board.solution[0])} steps.")
    idx = 1
    for action, step in zip(*board.solution):
        print(f"Step {idx} is {action}")
        print_tiles(step)
        idx += 1


if __name__ == "__main__":
    with cProfile.Profile() as profile:
        main()

    results = pstats.Stats(profile)
    results.sort_stats(pstats.SortKey.TIME)
    results.print_stats()
    # TODO code coverage, remove dead code
    # TODO run profiler, optimize timing
