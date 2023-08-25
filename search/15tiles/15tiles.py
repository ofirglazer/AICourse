# import sys
import copy
from random import shuffle

from util import Node, StackFrontier, QueueFrontier


class Board():

    def __init__(self):

        # init board
        board_row = [*range(0, 16)]
        # shuffle(board_row)
        start_board = []
        for row in range(4):
            start_board.append(board_row[row * 4:row * 4 + 4])
        # start_board[0][0] = 14
        # start_board[3][2:4] = [0, 15]
        start_board[0][0:4] = [1, 2, 3, 7]
        start_board[1][3] = 0
        self.start = Node(state=start_board, parent=None, action=None)

        self.goal_1d = [*range(0, 16)]


    def neighbors(self, node):
        empty_idx = node.state_1d.index(0)
        empty_row = empty_idx // 4
        empty_col = empty_idx % 4
        candidates = [
            ("up", (empty_row - 1, empty_col)),
            ("down", (empty_row + 1, empty_col)),
            ("left", (empty_row, empty_col - 1)),
            ("right", (empty_row, empty_col + 1))
        ]

        result = []
        for action, (r, c) in candidates:
            if 0 <= r < 4 and 0 <= c < 4:
                new_state = copy.deepcopy(node.state)
                new_state[empty_row][empty_col] = node.state[r][c]
                new_state[r][c] = 0
                result.append((action, new_state))
        return result


    def solve(self):
        """Finds a solution to a 15 tiles board, if one exists."""

        # Keep track of number of states explored
        self.num_explored = 0

        # Initialize frontier to just the starting position
        frontier = QueueFrontier()
        frontier.add(self.start)

        # Initialize an empty explored set
        self.explored = set()

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
        self.start.print()


    def output_image(self, filename, show_solution=True, show_explored=False):
        from PIL import Image, ImageDraw
        cell_size = 50
        cell_border = 2

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.width * cell_size, self.height * cell_size),
            "black"
        )
        draw = ImageDraw.Draw(img)

        solution = self.solution[1] if self.solution is not None else None
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):

                # Walls
                if col:
                    fill = (40, 40, 40)

                # Start
                elif (i, j) == self.start:
                    fill = (255, 0, 0)

                # Goal
                elif (i, j) == self.goal:
                    fill = (0, 171, 28)

                # Solution
                elif solution is not None and show_solution and (i, j) in solution:
                    fill = (220, 235, 113)

                # Explored
                elif solution is not None and show_explored and (i, j) in self.explored:
                    fill = (212, 97, 85)

                # Empty cell
                else:
                    fill = (237, 240, 252)

                # Draw cell
                draw.rectangle(
                    ([(j * cell_size + cell_border, i * cell_size + cell_border),
                      ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)]),
                    fill=fill
                )

        img.save(filename)


def main():
    board = Board()
    print("Original board:")
    board.print_start()
    print("Solving...")
    board.solve()
    print("States Explored:", board.num_explored)
    print("Solution:")

    print(f"{len(board.solution[0])} steps:")
    idx = 1
    for action, step in zip(*board.solution):
        print(f"Step {idx}: {action}")
        for row in range(4):
            for col in range(4):
                print("%2d" % step[row][col], end=" ")
            print()
        print()
        idx += 1

def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """

    # Initialize frontier to just the starting position
    start = Node(state=source, parent=None, action=None)
    frontier = QueueFrontier()
    frontier.add(start)

    # Initialize an empty explored set
    explored = set()

    # Keep looping until solution found
    while True:
        # If nothing left in frontier, then no path
        if frontier.empty():
            return None
        else:

            # Choose a node from the frontier
            node = frontier.remove()

            # If node is the goal, then we have a solution
            if node.state == target:
                links = []
                while node.parent is not None:
                    links.append((node.action, node.state))
                    node = node.parent
                links.reverse()
                return links

            # Mark node as explored
            explored.add(node.state)

            # Add neighbors to frontier
            neighbors = neighbors_for_person(node.state)
            for neighbor in neighbors:
                if not frontier.contains_state(neighbor[1]) and neighbor[1] not in explored:
                    child = Node(state=neighbor[1], parent=node, action=neighbor[0])
                    frontier.add(child)



def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
