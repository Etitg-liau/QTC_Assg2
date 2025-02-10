import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from qiskit_aer import Aer
from qiskit import QuantumCircuit
from qiskit_algorithms import QAOA
from qiskit_optimization.applications import Maxcut
from qiskit_optimization import QuadraticProgram
from qiskit.visualization import plot_histogram
from qiskit import transpile, assemble
from qiskit.primitives import Estimator

# Step 1: Create a graph with 3 botnet nodes and 10 surrounding blue nodes
n_botnet_nodes = 3
n_blue_nodes = 15
total_nodes = n_botnet_nodes + n_blue_nodes

# Create a complete graph where each node is connected to every other node
G = nx.complete_graph(total_nodes)

# Mark the botnet nodes in red (center nodes)
botnet_nodes = list(range(n_botnet_nodes))  # Botnet nodes are the first 3 nodes
color_map = ['lightcoral' if node in botnet_nodes else 'lightsteelblue' for node in G.nodes]

# Visualize the graph
pos = nx.spring_layout(G, seed=42)  # Use a spring layout for better spacing
plt.figure(figsize=(8, 6))
nx.draw(G, pos, node_color=color_map, with_labels=True, node_size=700, font_size=15, font_weight='bold')
plt.title(f"Botnet Network Diagram\n3 Botnet Nodes in Red, 10 Blue Nodes Surrounding Them")
plt.show()

# Step 2: Set up the QAOA for MaxCut
# We will use QAOA to solve the MaxCut problem, which is useful in separating botnet nodes.

# Convert the graph into a MaxCut Quadratic Program
maxcut = Maxcut(G)
qp = maxcut.to_quadratic_program()

# Define the QAOA algorithm
qaoa = QAOA(optimizer='COBYLA', reps=3)

# Set up the Estimator
backend = Aer.get_backend('statevector_simulator')
estimator = Estimator(backend=backend)

# Solve the problem using QAOA
qaoa_result = qaoa.compute_minimum_eigenvalue(qp)

# Extract the result (solution to the MaxCut)
solution = qaoa_result.eigenstate
print(f"QAOA Result: {solution}")

# Step 3: Simulate Quantum Walks
# Use a quantum walk on the graph to simulate the botnet's spread.
def quantum_walk(graph, steps=5):
    n = len(graph.nodes)
    # Create a simple quantum walk circuit
    qc = QuantumCircuit(n)
    qc.h(range(n))  # Apply Hadamard to all qubits (superposition)
    
    # Apply the quantum walk (e.g., a simple walk based on the adjacency matrix)
    for step in range(steps):
        for u, v in graph.edges():
            qc.cx(u, v)  # Use CNOT gates to simulate the walk
    
    # Measure the result
    qc.measure_all()
    return qc

# Run a quantum walk simulation on the graph
walk_circuit = quantum_walk(G)

# Transpile and assemble the circuit for the simulator
compiled_circuit = transpile(walk_circuit, backend)
qobj = assemble(compiled_circuit)

# Run the simulation and get the results
result = Aer.get_backend('qasm_simulator').run(qobj).result()

# Plot the histogram of the quantum walk result
counts = result.get_counts()
plot_histogram(counts)
plt.title("Quantum Walk Histogram")
plt.show()