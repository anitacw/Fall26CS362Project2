import heapq
import unittest

# Load word set once
with open("four_letter_words", "r") as f:
    ALL_WORDS = set(word.strip().lower() for word in f.readlines())


class WordState:

    def __init__(self, word, goal_word="", g_cost=0, f_cost=0, prev=None):
        self.word = word.lower()
        self.loc = self.word  # Map loc directly so a_star.py can read it
        self.goal_word = goal_word.lower()
        self.g_cost = g_cost
        self.f_cost = f_cost
        self.f = f_cost
        self.prev = prev

    def __eq__(self, other):
        return self.word == other.word if isinstance(other, WordState) else False

    def __lt__(self, other):
        return self.f < other.f

    def __gt__(self, other):
        return self.f > other.f

    def __hash__(self):
        return hash(self.word)

    ## find all words that differ by one letter.
    def successors(self):
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        successor_list = []
        word_chars = list(self.word)

        for i in range(len(word_chars)):
            original_char = word_chars[i]
            for c in alphabet:
                if c != original_char:
                    word_chars[i] = c
                    new_word = "".join(word_chars)
                    if new_word in ALL_WORDS:
                        new_g = self.g_cost + 1
                        new_f = new_g + heuristic_fn(new_word, self.goal_word)
                        successor_list.append(
                            WordState(
                                word=new_word,
                                goal_word=self.goal_word,
                                g_cost=new_g,
                                f_cost=new_f,
                                prev=self
                            )
                        )
            word_chars[i] = original_char

        return successor_list


### h == # of letters different between word and goal_word.
def heuristic_fn(state, goal_word=None):
    word = state.word if isinstance(state, WordState) else state
    target = state.goal_word if isinstance(state, WordState) else goal_word
    return sum(1 for a, b in zip(word, target) if a != b)


# Unit Tests
class TestWordState(unittest.TestCase):

    def test_heuristic_fn(self):
        # 0 differences
        s1 = WordState("cold", "cold")
        self.assertEqual(heuristic_fn(s1), 0)

        # 4 differences (c!=w, o!=a, l!=r, d!=m)
        s2 = WordState("cold", "warm")
        self.assertEqual(heuristic_fn(s2), 4)

        # 3 differences (l!=g, e!=o, a!=l)
        s3 = WordState("lead", "gold")
        self.assertEqual(heuristic_fn(s3), 3)

    def test_successors(self):
        s = WordState("cold", "warm")
        succs = s.successors()
        succ_words = [item.word for item in succs]

        self.assertIn("cord", succ_words)
        self.assertNotIn("cold", succ_words)  # Should not contain itself
        for w in succ_words:
            self.assertIn(w, ALL_WORDS)


# Main
if __name__ == "__main__":
    import sys
    from a_star import a_star

    # Run Unit Tests First
    print("Running Unit Test")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestWordState)
    runner = unittest.TextTestRunner(verbosity=1)
    test_result = runner.run(suite)

    # If tests pass, launch interactive runner
    if test_result.wasSuccessful():
        print("\nInteractive Word Ladder Test")
        start_word = input("Enter start word: ").strip().lower()
        goal_word = input("Enter goal word: ").strip().lower()

        if start_word in ALL_WORDS and goal_word in ALL_WORDS:
            start_state = WordState(start_word, goal_word)
            start_state.f_cost = start_state.f = heuristic_fn(start_state)
            a_star(start_state, lambda s: s.word == s.goal_word, heuristic_fn)
        else:
            print("Error: Invalid word entered.")