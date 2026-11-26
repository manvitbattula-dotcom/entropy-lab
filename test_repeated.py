
import networkx as nx

from simulations.algorithms import compare_repeated_experiments


# ==========================================
# CREATE A TEST GRAPH
# ==========================================

graph = nx.DiGraph()

graph.add_edges_from([
    ("Low", "Low"),
    ("Low", "Moderate"),
    ("Moderate", "Low"),
    ("Moderate", "Moderate"),
    ("Moderate", "High"),
    ("High", "Moderate"),
    ("High", "High"),
    ("High", "Very High"),
    ("Very High", "High"),
    ("Very High", "Very High")
])


# ==========================================
# RUN 100 REPEATED EXPERIMENTS
# ==========================================

results = compare_repeated_experiments(
    graph=graph,
    start_node="Low",
    steps=100,
    experiments=100,
    rho=0.75,
    eta=0.15,
    initial_temperature=1.0,
    base_seed=42
)


# ==========================================
# DISPLAY RESULTS
# ==========================================

print("\n========== REPEATED EXPERIMENT RESULTS ==========")

print("Total experiments:", results["Experiments"])

for algorithm in ["SRW", "EBW"]:

    print(f"\n========== {algorithm} AVERAGES ==========")

    for metric, values in results["Summary"][algorithm].items():

        print(f"\n{metric}")
        print("Mean:", values["Mean"])
        print("Standard Deviation:", values["Standard Deviation"])
        print("Minimum:", values["Minimum"])
        print("Maximum:", values["Maximum"])


# ==========================================
# VALIDATION
# ==========================================

assert results["Experiments"] == 100
assert len(results["Individual Results"]) == 100

for algorithm in ["SRW", "EBW"]:

    assert "Node Coverage (%)" in results["Summary"][algorithm]
    assert "Mean Transition Entropy" in results["Summary"][algorithm]
    assert "Execution Time (ms)" in results["Summary"][algorithm]

print("\nAll repeated experiment tests passed!")

