class Node:
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action
        self.state_to_str()  # string used to store in set
        self.state_to_1d()  # 1d used to index and compare

    def state_to_str(self):
        self.state_str = ','.join(str(num) for num in self.state)

    def state_to_1d(self):
        size = (len(self.state), len(self.state[0]))
        total = size[0] * size[1]
        self.state_1d = []
        for idx in range(total):
            self.state_1d.append(self.state[idx // size[1]][idx % size[1]])


def print_tiles(state):
    print()
    for row in range(len(state)):
        for col in range(len(state[0])):
            print("%2d" % state[row][col], end=" ")
        print()
    print()


class StackFrontier:
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node


class QueueFrontier(StackFrontier):

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node
