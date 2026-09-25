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
            # Print total distance
            print(f"\nTotal distance: {next_state.g_cost}")
            
            # Reconstruct full path from start to goal using .prev
            path = []
            curr = next_state
            while curr is not None:
                path.append(curr.loc)
                curr = curr.prev
            path.reverse()  # Flip list so it reads start -> goal
            
            # Print each city step in forward order
            for city in path:
                print(city)
                
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

    # Print notice if priority queue empties without reaching goal
    print("\nNo path found.")
    return None

def hfn(state) :
    # Reads state.goal dynamically and catches invalid city lookups safely
    try:
        return state.sld_matrix[state.loc][state.goal]
    except KeyError:
        return float('inf')

def bucharest_test(state) :
    # Checks against state.goal dynamically
    return state.loc == state.goal

if __name__ == "__main__" :
    # Prompt user for dynamic start and goal cities (title-cased)
    start_city = input("Enter start city: ").strip().title()
    goal_city = input("Enter goal city: ").strip().title()

    # Create starting state with goal and execute search
    start_state = RomaniaState.RomaniaState(start_city, goal=goal_city)
    start_state.f_cost = hfn(start_state)
    
    if start_state.f_cost == float('inf'):
        print("Error: Invalid city entered.")
    else:
        a_star(start_state, bucharest_test, hfn)