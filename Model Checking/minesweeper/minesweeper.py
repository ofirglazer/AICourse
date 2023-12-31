# import itertools
import random


class Minesweeper:
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):
        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence:
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count
        self.mines = set()
        self.safes = set()

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        return self.mines

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        return self.safes

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1
            if self.count == 0:
                for safe_cell in self.cells.copy():
                    self.mark_safe(safe_cell)
        self.mines.add(cell)

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            if self.count == len(self.cells):
                for mine_cell in self.cells.copy():
                    self.mark_mine(mine_cell)
        self.safes.add(cell)


class MinesweeperAI:
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """

        # add move as made and safe
        self.moves_made.add(cell)
        self.mark_safe(cell)

        '''
        To add a cell to new sentence based on returned count, check if:
            cell is around last move but inside board, not identical to the last move
            if cell already marked as safe, exclude it
            if cell already marked as mine, exclude it and reduce count
            if the list of new cells is not empty:
                if returned count is 0, mark cells as safes, not a new sentence
                if returned count == number of cells, mark cells as mines, not a new sentence
                else add new sentence to knowledge
        '''
        allowed_row = range(0, self.height)
        allowed_col = range(0, self.width)
        new_cell_list = set()
        # going over cells around last move
        for row in range(cell[0] - 1, cell[0] + 2):
            for col in range(cell[1] - 1, cell[1] + 2):
                # cell is in board, != last move
                if (row in allowed_row and col in allowed_col and
                        not ((row, col) == cell)):
                    # not already marked as safe
                    if (row, col) not in self.safes:
                        # if already marked as mine, reduce count
                        if (row, col) in self.mines:
                            count -= 1
                        else:
                            new_cell_list.add((row, col))

        # if the list of new cells is not empty
        if len(new_cell_list):
            # if returned count is 0, mark cells as safe
            if count == 0:
                for cell in new_cell_list:
                    self.mark_safe(cell)
            # if returned count == number of cells, mark cells as mines
            elif len(new_cell_list) == count:
                for cell in new_cell_list:
                    self.mark_mine(cell)
            # 0 < count < number of cells, add sentence
            else:
                self.knowledge.append(Sentence(new_cell_list, count))

        # after processing the new input, update sentences with known mines and safes
        for sentence in self.knowledge:
            for mine in self.mines:
                sentence.mark_mine(mine)
            for safe in self.safes:
                sentence.mark_safe(safe)
        for sentence in self.knowledge:
            self.mines.update(sentence.known_mines())
            self.safes.update(sentence.known_safes())

        '''
        Too add inferred sentences based on knowledge:
        find: a subset of b, a != b, a not empty
        generate new sentence: b-a
        if b-a count is 0, update safes, not a new sentence
        if b-a count == b-a, update mines, not a new sentence
        if b-a already exists, skip new sentence        
        '''
        for sentence_a in self.knowledge.copy():
            for sentence_b in self.knowledge.copy():
                if (len(sentence_a.cells) > 0 and sentence_a.cells < sentence_b.cells):
                    # a is subset of b, a != b, a not empty
                    # print(f"reached subset of {sentence_a} in {sentence_b}")
                    new_count = sentence_b.count - sentence_a.count
                    new_cells = sentence_b.cells - sentence_a.cells
                    new_sentence = Sentence(new_cells, new_count)

                    if new_count == 0:
                        # found new safes
                        for safe_cell in new_cells:
                            self.mark_safe(safe_cell)
                    elif new_count == len(new_cells):
                        # found new mines
                        for mine_cell in new_cells:
                            self.mark_mine(mine_cell)
                    elif new_sentence not in self.knowledge:
                        # found NEW sentence
                        self.knowledge.append(new_sentence)
                        # print(f"Sentence A: {sentence_a}")
                        # print(f"Sentence B: {sentence_b}")
                        # print(f"subsetting, total {len(self.knowledge)} sentences")

        # print("\nAfter adding knowledge")
        # print(f"Mines: {self.mines}")
        # print(f"Unused safes: {self.safes - self.moves_made}")
        # for sentence in self.knowledge:
        #     print(sentence)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # print(f"Mines: {self.mines}")
        # print(f"Unused safes: {self.safes - self.moves_made}")
        for safe in self.safes:
            if safe not in self.moves_made:
                # print(f"Next safe move: {safe}\n")
                return safe
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # if found all mines and covered all other cells
        if len(self.moves_made) + len(self.mines) == self.height * self.width:
            return None
        count = 0
        while count < 20:  # TODO implement using a set of all cells
            row = random.randrange(self.height)
            col = random.randrange(self.width)
            if ((row, col) not in self.moves_made and
                    (row, col) not in self.mines):
                return (row, col)
            count += 1
