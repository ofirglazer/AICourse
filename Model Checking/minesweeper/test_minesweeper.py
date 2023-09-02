from unittest import TestCase
from minesweeper import Sentence, MinesweeperAI, Minesweeper


class Test(TestCase):
    """def test_minesweeper(self):
        # ms = Minesweeper()
        # ms.print()
        self.skipTest('no test relevant')"""

    def test_sentence(self):
        s1 = Sentence({(0, 0), (1, 0)}, 1)
        s2 = Sentence({(0, 0), (1, 0)}, 1)
        s3 = Sentence({(0, 0), (1, 0)}, 2)
        s4 = Sentence({(0, 1), (1, 0)}, 2)
        self.assertTrue(s1 == s2, "Sentence equal")
        self.assertFalse(s1 == s3, "Sentence not equal - count")
        self.assertFalse(s1 == s4, "Sentence not equal - cells")
        self.assertEqual(str(s4), "{(0, 1), (1, 0)} = 2", "str(Sentence)")

        s4.mark_mine((0, 1))
        s4a = Sentence({(1, 0)}, 1)
        self.assertEqual(s4, s4a, "after marking a mine")
        s4.mark_mine((1, 0))
        s4a = Sentence({}, 0)
        self.assertEqual(s4, s4a, "after marking a mine")
        self.assertEqual({(0, 1), (1, 0)}, s4.known_mines(), "known mines added")

        s2 = Sentence({(0, 0), (1, 0), (1, 1)}, 1)
        s2.mark_safe((0, 1))  # marking safe out of the set - should change nothing
        s2a = Sentence({(0, 0), (1, 0), (1, 1)}, 1)
        self.assertEqual(s2, s2a, "after marking safe - not belong to sentence")
        s2.mark_safe((1, 0))
        s2a = Sentence({(0, 0), (1, 1)}, 1)
        self.assertEqual(s2, s2a, "after marking safe")
        self.assertEqual({(0, 1), (1, 0)}, s2.known_safes(), "known safes added")

        s5 = Sentence({(0, 1), (1, 0), (1, 1), (0, 0)}, 2)
        s5.mark_safe((0, 0))
        s5.mark_safe((1, 1))
        self.assertEqual({(0, 1), (1, 0)}, s5.known_mines(), "mines known when adding safes")

        s6 = Sentence({(0, 1), (1, 0), (1, 1), (0, 0)}, 1)
        s6.mark_mine((0, 0))
        self.assertEqual({(0, 1), (1, 0), (1, 1)}, s6.known_safes(), "safes known when adding mines")

    '''def test_minesweeper_ai(self):
        HEIGHT = 8
        WIDTH = 8
        MINES = 8
        ai = MinesweeperAI(height=HEIGHT, width=WIDTH)

        ai.add_knowledge((0, 0), 1)
        self.assertEqual({(0, 0)}, ai.safes, "safes known after move")
        ai.add_knowledge((0, 2), 0)
        self.assertEqual({(1, 0)}, ai.mines, "mines known after move")
        safe_set = {(0, 0), (0, 1), (0, 2), (0, 3), (1, 1), (1, 2), (1, 3)}
        self.assertEqual(safe_set, ai.safes, "safes known after move")
        safe_move = ai.make_safe_move()
        self.assertTrue(safe_move in safe_set)'''

    def test_minesweeper_ai_script(self):
        HEIGHT = 4
        WIDTH = 4
        MINES = 4
        revealed = set()
        flags = set()
        lost = False
        game = Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
        ai = MinesweeperAI(height=HEIGHT, width=WIDTH)
        game.print()

        while not lost:
            move = ai.make_safe_move()
            if move is None:
                move = ai.make_random_move()
                if move is None:
                    pass
                else:
                    print("No known safe moves, AI making random move.")
            else:
                print("AI making safe move.")

            if move:
                print(f"move is {move}")
                if game.is_mine(move):
                    lost = True
                    print("Lost")
                else:
                    nearby = game.nearby_mines(move)
                    revealed.add(move)
                    ai.add_knowledge(move, nearby)
