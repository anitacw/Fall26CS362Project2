import heapq


import RomaniaState
import RomaniaState as rs


def a_star(startState, goal_test, heuristic_fn, use_closed_list=True) :
    search_queue = []
    closed_list = {}

    heapq.heappush(search_queue, startState)
    if use_closed_list :
        closed_list[startState] = True
    while len(search_queue) > 0 :
        next_state = heapq.heappop(search_queue)
        if goal_test(next_state):
            print("Goal found")
            print(next_state)
            ptr = next_state.prev
            while ptr is not None :
                ptr = ptr.prev
                print(ptr)
            return next_state
        else :
            successor_list = next_state.successors()
            if use_closed_list :
                successor_list = [item for item in successor_list
                                    if item not in closed_list]
                for s in successor_list :
                    closed_list[s] = True
                    s.f_cost = s.g_cost + heuristic_fn(s)
                    heapq.heappush(search_queue,s)

def hfn(state) :
    return state.sld_matrix[state.loc]["Bucharest"]

def bucharest_test(state) :
    return state.loc == "Bucharest"

if __name__ == "__main__" :
    a = RomaniaState.RomaniaState("Arad")
    res = a_star(a, bucharest_test, hfn)