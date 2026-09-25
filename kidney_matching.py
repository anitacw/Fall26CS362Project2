import random
import itertools
import unittest
from ortools.sat.python import cp_model


# Cycle detection functions
def find_2_cycles(compat):
    n = len(compat)
    return [(i, j) for i, j in itertools.combinations(range(n), 2) if compat[i][j] and compat[j][i]]


def find_3_cycles(compat):
    n = len(compat)
    return [
        (i, j, k)
        for i, j, k in itertools.permutations(range(n), 3)
        if i < j and i < k and compat[i][j] and compat[j][k] and compat[k][i]
    ]


# Data generators
def generate_pairs(n, compat_prob=0.15, seed=42):
    random.seed(seed)
    return [[i != j and random.random() < compat_prob for j in range(n)] for i in range(n)]


def generate_blood_type_pairs(n, seed=42):
    random.seed(seed)
    blood_types = ['O', 'A', 'B', 'AB']
    blood_probs = [0.45, 0.40, 0.11, 0.04]
    
    can_give_to = {'O': {'O', 'A', 'B', 'AB'}, 'A': {'A', 'AB'}, 'B': {'B', 'AB'}, 'AB': {'AB'}}

    patients = random.choices(blood_types, weights=blood_probs, k=n)
    donors = random.choices(blood_types, weights=blood_probs, k=n)

    compat = [[i != j and patients[j] in can_give_to[donors[i]] for j in range(n)] for i in range(n)]
    return compat, patients, donors


def generate_pairs_with_priority(n, compat_prob=0.15, sensitized_frac=0.2, seed=42):
    random.seed(seed)
    sensitized = [random.random() < sensitized_frac for _ in range(n)]
    
    compat = [
        [i != j and random.random() < compat_prob * (0.2 if sensitized[j] else 1.0) for j in range(n)]
        for i in range(n)
    ]
    return compat, sensitized


def generate_match_quality(compat, seed=42):
    random.seed(seed)
    n = len(compat)
    return [[random.randint(1, 10) if compat[i][j] else 0 for j in range(n)] for i in range(n)]


# CP solver for kidney exchange optimization
def solve_kidney_exchange(
    compat, quality=None, sensitized=None, sensitized_bonus=0, base_weight=100
):
    n = len(compat)
    all_cycles = find_2_cycles(compat) + find_3_cycles(compat)

    if not all_cycles:
        return [], 0, 0, 0

    model = cp_model.CpModel()
    x = [model.NewBoolVar(f"cycle_{idx}") for idx in range(len(all_cycles))]

    # Ensure each patient/donor pair is in at most one chosen cycle
    for i in range(n):
        involved = [x[idx] for idx, c in enumerate(all_cycles) if i in c]
        if involved:
            model.Add(sum(involved) <= 1)

    # Calculate objective cycle weights
    cycle_weights = []
    for idx, c in enumerate(all_cycles):
        weight = 0
        for pos in range(len(c)):
            donor_i = c[pos]
            patient_j = c[(pos + 1) % len(c)]

            w_step = base_weight
            if quality:
                w_step += quality[donor_i][patient_j]
            if sensitized and sensitized[patient_j]:
                w_step += sensitized_bonus

            weight += w_step
        cycle_weights.append(weight)

    model.Maximize(sum(cycle_weights[idx] * x[idx] for idx in range(len(all_cycles))))

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        selected = [all_cycles[idx] for idx in range(len(all_cycles)) if solver.Value(x[idx])]

        matched_nodes = set()
        for c in selected:
            matched_nodes.update(c)

        total_matched = len(matched_nodes)
        sensitized_matched = sum(1 for i in matched_nodes if sensitized and sensitized[i])

        return selected, solver.ObjectiveValue(), total_matched, sensitized_matched

    return [], 0, 0, 0


# Unit tests
class TestKidneyMatching(unittest.TestCase):

    def test_2_cycle_detection(self):
        compat = [[False, True], [True, False]]
        cycles = find_2_cycles(compat)
        self.assertIn((0, 1), cycles)

    def test_3_cycle_detection(self):
        compat = [
            [False, True, False],
            [False, False, True],
            [True, False, False]
        ]
        cycles = find_3_cycles(compat)
        self.assertIn((0, 1, 2), cycles)

    def test_solver_disjointness(self):
        compat = [
            [False, True, True],
            [True, False, False],
            [True, False, False]
        ]
        selected, _, total_m, _ = solve_kidney_exchange(compat)
        self.assertEqual(len(selected), 1)
        self.assertEqual(total_m, 2)


# Interactive runner
if __name__ == "__main__":
    print("Running Unit Tests")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestKidneyMatching)
    runner = unittest.TextTestRunner(verbosity=1)
    test_result = runner.run(suite)

    if test_result.wasSuccessful():
        print("\nInteractive Kidney Exchange Test")
        try:
            num_pairs = int(input("Enter number of pairs (default 15): ").strip() or "15")
        except ValueError:
            num_pairs = 15

        compat, sensitized = generate_pairs_with_priority(num_pairs, compat_prob=0.2, seed=42)
        quality = generate_match_quality(compat, seed=42)

        cycles, obj, total_m, sens_m = solve_kidney_exchange(
            compat, quality, sensitized, sensitized_bonus=10
        )

        print("\nMatch Results")
        print(f"Total Matches: {total_m} / {num_pairs}")
        print(f"Sensitized Patients Matched: {sens_m} / {sum(sensitized)}")
        print("Selected Cycles:")
        for c in cycles:
            print(f"  Cycle {len(c)}: {c}")