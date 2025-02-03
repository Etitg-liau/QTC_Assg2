#Goal: To Understand How Quantum Walks work

from qiskit import QuantumCircuit, transpile, assemble
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

def create_quantum_walk_circuit(num_qubits):
    qc = QuantumCircuit(num_qubits)
    
    # Apply Hadamard gates to create superposition
    for qubit in range(num_qubits):
        qc.h(qubit)
    
    # Apply controlled-phase gates for interference (simulating adjacency matrix)
    for i in range(num_qubits - 1):
        qc.cz(i, i + 1)
    
    # Apply Hadamard again to mix states
    for qubit in range(num_qubits):
        qc.h(qubit)
    
    qc.measure_all()
    return qc

def simulate_quantum_walk(qc):
    simulator = Aer.get_backend('aer_simulator')
    transpiled_qc = transpile(qc, simulator)
    qobj = assemble(transpiled_qc)
    result = simulator.run(qobj).result()
    counts = result.get_counts()
    return counts

def create_network_graph():
    G = nx.Graph()
    G.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 4), (1, 3), (0, 4)])  # Example network structure
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2000)
    plt.title("Network Graph Representing Connections")
    plt.show()

def main():
    num_qubits = 10
    create_network_graph()
    
    qc = create_quantum_walk_circuit(num_qubits)
    counts = simulate_quantum_walk(qc)
    
    print("Quantum Walk Measurement Results:")
    print(counts)
    plot_histogram(counts)
    plt.show()

main()