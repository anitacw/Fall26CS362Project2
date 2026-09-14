
import Graph, sld

### RomaniaState: represents the basic information needed to solve
### the Romania problem. You are welcome to extend or modify this as needed.

class RomaniaState:
    ### romania_graph and sld_matrix are class variables. They are shared across all instances.
    ### This is dangerous with mutable variables; we are using them read-only here.

    romania_graph = Graph.build_graph("romania.graph")
    sld_matrix = sld.build_sld_matrix()

    def __init__(self, loc=None, f_cost=0, g_cost=0, prev=None) :
        self.loc = loc
        self.f_cost = f_cost
        self.g_cost = g_cost
        self.prev = prev

    def __hash__(self):
        return self.__repr__().__hash__()

    def __eq__(self, other):
        return (self.loc == other.loc and
                self.f_cost == other.f_cost and
                self.g_cost == other.g_cost)

    def __lt__(self, other):
        return self.f_cost < other.f_cost

    def __gt__(self, other):
        return self.f_cost > other.f_cost

    def __le__(self, other):
        return self.f_cost <= other.f_cost

    def __ge__(self, other):
        return self.f_cost >= other.f_cost

    def __repr__(self):
        return f"{self.loc}, {self.f_cost}, {self.g_cost}"

    def successors(self) :
        slist = []
        for edge in RomaniaState.romania_graph.get_edges(self.loc) :
            slist.append(RomaniaState(edge[0],
                                      0,
                                      self.g_cost + edge[1],
                                      self))
        return slist