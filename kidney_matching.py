
import random
import itertools
from ortools.sat.python import cp_model

## find cycles of length 2
def find_2_cycles(compat):
    cycles = []
    n = len(compat)
    for i, j in itertools.combinations(range(n), 2):
        if compat[i][j] and compat[j][i]:
            cycles.append((i, j))
    return cycles

## find cycles of length 3
def find_3_cycles(compat):
    cycles = []
    n = len(compat)
    for i, j, k in itertools.permutations(range(n), 3):
        if i < j and i < k:
            if compat[i][j] and compat[j][k] and compat[k][i]:
                cycles.append((i, j, k))
    return cycles

def solve_kidney_exchange(compat, weights=None):
    n = len(compat)
    all_cycles = find_2_cycles(compat) + find_3_cycles(compat)

    model = cp_model.CpModel()
    x = [model.NewBoolVar(f'cycle_{idx}') for idx in range(len(all_cycles))]

    # Each pair used in at most one selected cycle (disjointness)
    for i in range(n):
        involved = [x[idx] for idx, c in enumerate(all_cycles) if i in c]
        if involved:
            model.Add(sum(involved) <= 1)

    if weights is None:
        weights = [1] * len(all_cycles)
    model.Maximize(sum(len(c) * weights[idx] * x[idx]
                        for idx, c in enumerate(all_cycles)))

    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        selected = [all_cycles[idx] for idx in range(len(all_cycles))
                    if solver.Value(x[idx])]
        return selected, solver.ObjectiveValue()
    return None, None


#### Generates an adjacency matrix where an edge is true if i is compatible with j

def generate_pairs(n, compat_prob=0.15, seed=42):
    random.seed(seed)
    compat = [[False]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j and random.random() < compat_prob:
                compat[i][j] = True
    return compat


def generate_pairs_with_priority(n, compat_prob=0.15, sensitized_frac=0.2, seed=42):
    random.seed(seed)
    compat = [[False]*n for _ in range(n)]

    # Highly sensitized patients get a much lower compatibility probability
    sensitized = [random.random() < sensitized_frac for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if i != j:
                # compat[i][j]: donor i -> patient j
                prob = compat_prob * (0.2 if sensitized[j] else 1.0)
                compat[i][j] = random.random() < prob

    return compat, sensitized

def generate_match_quality(compat, seed=42):
    random.seed(seed)
    n = len(compat)
    quality = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if compat[i][j]:
                quality[i][j] = random.randint(1, 10)  # 10 = excellent match
    return quality


if __name__ == '__main__':
    compat = generate_pairs(15)
    print(compat)
    print(solve_kidney_exchange(compat))
