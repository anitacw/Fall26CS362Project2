import matplotlib.pyplot as plt
import numpy as np
from kidney_matching import (
    generate_pairs,
    generate_blood_type_pairs,
    generate_pairs_with_priority,
    generate_match_quality,
    solve_kidney_exchange
)

print("Starting experiments...")

# Part 1: Grid Experiment (Patient Count vs Probability)
print("Running Part 1...")
probs = [0.1, 0.3, 0.5, 0.7, 0.9]
plt.figure(figsize=(7, 4))
for n in [15, 20, 25, 30]:
    pcts = [np.mean([(solve_kidney_exchange(generate_pairs(n, p, s))[2] / n) * 100 for s in range(5)]) for p in probs]
    plt.plot(probs, pcts, marker="o", label=f"{n} Patients")
plt.title("Part 1: Matched % vs Compatibility Probability")
plt.xlabel("Probability")
plt.ylabel("Matched (%)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("part1_basic_grid.png")
plt.close()

# Part 2: US Blood Type Distribution
print("Running Part 2...")
patients = list(range(15, 31))
pcts = [np.mean([(solve_kidney_exchange(generate_blood_type_pairs(n, s)[0])[2] / n) * 100 for s in range(5)]) for n in patients]
plt.figure(figsize=(7, 4))
plt.plot(patients, pcts, marker="s", color="darkred")
plt.title("Part 2: Matched % with US Blood Type Frequencies")
plt.xlabel("Patients")
plt.ylabel("Matched (%)")
plt.grid(True)
plt.tight_layout()
plt.savefig("part2_blood_types.png")
plt.close()

# Part 3: Sensitized Bonus Sensitivity Curve
print("Running Part 3...")
bonuses = [0, 1, 2, 5, 10, 20]
totals, sens = [], []
for b in bonuses:
    t_acc, s_acc = [], []
    for s in range(10):
        c, sz = generate_pairs_with_priority(30, 0.15, 0.3, seed=s)
        q = generate_match_quality(c, seed=s)
        _, _, tm, sm = solve_kidney_exchange(c, q, sz, sensitized_bonus=b)
        t_acc.append(tm)
        s_acc.append(sm)
    totals.append(np.mean(t_acc))
    sens.append(np.mean(s_acc))

plt.figure(figsize=(7, 4))
plt.plot(bonuses, totals, marker="o", label="Total Matches", color="blue")
plt.plot(bonuses, sens, marker="^", label="Sensitized Matches", color="green")
plt.title("Part 3: Impact of Sensitized Priority Bonus")
plt.xlabel("Sensitized Bonus")
plt.ylabel("Number of Matches")
plt.xticks(bonuses)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("part3_sensitized_curve.png")
plt.close()

print("Done! Check your folder for part1_basic_grid.png, part2_blood_types.png, and part3_sensitized_curve.png.")