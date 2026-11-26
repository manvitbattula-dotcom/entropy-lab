
import networkx as nx

from simulations.algorithms import compare_algorithms


# ==========================================
# CREATE SAMPLE ENVIRONMENT
# ==========================================

G = nx.Graph()

G.add_edges_from([
    ("A", "B"),
    ("A", "C"),
    ("B", "D"),
    ("B", "E"),
    ("C", "F"),
    ("C", "G"),
    ("D", "H"),
    ("E", "H"),
    ("F", "H"),
    ("G", "H")
])


# ==========================================
# RUN BOTH ALGORITHMS
# ==========================================

results = compare_algorithms(
    graph=G,
    start_node="A",
    steps=100,
    rho=0.75,
    eta=0.15,
    initial_temperature=1.0,
    seed=42
)


# ==========================================
# DISPLAY COMPARISON TABLE
# ==========================================

print("\n========== SRW vs EBW ==========\n")

srw = results["SRW"]["metrics"]
ebw = results["EBW"]["metrics"]

print(f"{'Metric':<30} {'SRW':>12} {'EBW':>12}")
print("-" * 56)

for metric in srw:

    print(
        f"{metric:<30}"
        f"{srw[metric]:>12}"
        f"{ebw[metric]:>12}"
    )


# ==========================================
# DISPLAY SAMPLE PATHS
# ==========================================

print("\n========== SAMPLE PATHS ==========")

print("\nSRW:")
print(results["SRW"]["path"][:15])

print("\nEBW:")
print(results["EBW"]["path"][:15])


# ==========================================
# DISPLAY ENTROPY
# ==========================================

print("\n========== ENTROPY COMPARISON ==========")

print("SRW entropy samples:")
print(results["SRW"]["entropy"][:10])

print("\nEBW entropy samples:")
print(results["EBW"]["entropy"][:10])


# ==========================================
# DISPLAY TEMPERATURE
# ==========================================

print("\n========== EBW TEMPERATURE ==========")

print("Temperature used:")
print(results["EBW"]["temperature"][:10])

print("\nTemperature for next decision:")
print(results["EBW"]["next_temperature"][:10])


# ==========================================
# VALIDATION CHECKS
# ==========================================

assert len(results["SRW"]["path"]) <= 101
assert len(results["EBW"]["path"]) <= 101

assert len(results["SRW"]["entropy"]) == len(results["SRW"]["path"]) - 1
assert len(results["EBW"]["entropy"]) == len(results["EBW"]["path"]) - 1

assert all(
    0 <= p <= 1
    for record in results["EBW"]["probabilities"]
    for p in record["probabilities"]
)

assert all(
    abs(sum(record["probabilities"]) - 1) < 1e-9
    for record in results["EBW"]["probabilities"]
)

print("\nAll validation checks passed!")
