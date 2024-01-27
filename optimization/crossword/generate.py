import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }
        self.counter = 0

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for var in self.domains:
            words_to_enforce = []
            for word in self.domains[var]:
                if not len(word) == var.length:
                    words_to_enforce.append(word)
            for word in words_to_enforce:
                self.domains[var].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        conflict = self.crossword.overlaps[x, y]
        revised = False
        words_not_AC = []

        if conflict:
            for word_x in self.domains[x]:

                is_y_possible = False
                for word_y in self.domains[y]:
                    if word_x[conflict[0]] == word_y[conflict[1]]:
                        is_y_possible = True
                        break
                if not is_y_possible:
                    words_not_AC.append(word_x)

            for word in words_not_AC:
                self.domains[x].remove(word)
                revised = True

        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs is None:
            arcs = list(self.crossword.overlaps)

        while arcs:
            arc = arcs.pop()
            revised = self.revise(arc[0], arc[1])
            if revised:
                if not self.domains[arc[0]]:
                    return False
                for neighbour in self.crossword.neighbors(arc[0]):
                    if not (neighbour, arc[0]) in arcs:
                        arcs.append((neighbour, arc[0]))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        if len(assignment) == len(self.crossword.variables):
            return True
        return False

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # all values are distinct
        for var1 in assignment:
            # all values are correct length
            if not len(assignment[var1]) == var1.length:
                return False
            # all values are distinct
            for var2 in assignment:
                if not var1 == var2:
                    # different variables, same word
                    if assignment[var1] == assignment[var2]:
                        return False
                    # no conflicts between neighboring variables
                    if (var1, var2) in self.crossword.overlaps:
                        conflict = self.crossword.overlaps[(var1, var2)]
                        if conflict is not None:
                            if not assignment[var1][conflict[0]] == assignment[var2][conflict[1]]:
                                return False
        return True



    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        rule_out = dict()
        candidates = list(self.crossword.neighbors(var))
        for word in list(self.domains[var]):
            same_word = 0
            for neighbor in candidates:
                if word in self.domains[neighbor]:
                    same_word += 1
            rule_out[word] = same_word

        domain_sorted = sorted(self.domains[var], key= lambda ruled: rule_out[ruled])
        return domain_sorted

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        unassigned_vars = []
        for var in self.crossword.variables:
            if var not in assignment:
                unassigned_vars.append(var)
        # first: secondary sort
        unassigned_vars.sort(key=lambda degree: len(self.crossword.neighbors(degree)))
        # second: primary sort
        unassigned_vars.sort(key= lambda domain: len(self.domains[domain]))
        return unassigned_vars[0]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        self.counter += 1
        if self.assignment_complete(assignment):
            print(f"number of tries is {self.counter}")
            return assignment

        var = self.select_unassigned_variable(assignment)
        for word in self.order_domain_values(var, assignment):
            new_assignment = assignment.copy()
            new_assignment[var] = word
            if self.consistent(new_assignment):
                result = self.backtrack(new_assignment)
                if result is not None:
                    return result
            # recheck_arcs = []
            # for neighbor in self.crossword.neighbors(var):
            #     recheck_arcs.append((neighbor, var))
            # new_var_ok = self.ac3(recheck_arcs)
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
