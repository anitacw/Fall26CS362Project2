class WordState:

    def __init__(self,word, f_cost, g_cost):
        self.word = word

    def __eq__(self,other):
        return self.word == other.word

    def __lt__(self,other):
        return self.f < other.f

    def __gt__(self,other):
        return self.f > other.f

    ## find all words that differ by one letter.
    def successors(self):
        pass

### h == # of letters different between word and goal_word.
def heuristic_fn(word, goal_word):
    pass