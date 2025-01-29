import time
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library.standard_gates import XGate
import matplotlib.pyplot as plt
from qiskit_aer import AerSimulator
from qiskit import transpile
from qiskit.visualization import plot_histogram
BASIS_GATES = ["u", "cx"]
OPT_LEVEL = 3
SIZE = 6
# mcx from control on X
def mcx_gate(num_ctrl_qubits):
   my_mcx_gate = XGate().control(num_ctrl_qubits)
   return my_mcx_gate
# get increment circuit as an MCX cascade
def get_increment_circuit(num_qubits):
   increment_circuit= QuantumCircuit(num_qubits)
   for j in range(num_qubits - 1):
       increment_circuit.append(mcx_gate(num_qubits-1-j),[k for k in range(num_qubits-j)])
   increment_circuit.x(0)
   return increment_circuit
# run an example
start_time = time.time()
q_walk_step = QuantumCircuit(SIZE+1)
q_walk_step.h(0)
q_walk_step.append(get_increment_circuit(SIZE).control(1, ctrl_state=1),
                       [k for k in range(SIZE+1)])
q_walk_step.append(get_increment_circuit(SIZE).inverse().control(1, ctrl_state=0),
                       [k for k in range(SIZE+1)])
transpiled_cir = transpile(
           q_walk_step,
           basis_gates=BASIS_GATES,
           optimization_level=OPT_LEVEL,
   )
q_walk_step.draw('mpl')
plt.show()
transpilation_time = time.time()-start_time
depth = transpiled_cir.depth()
cx_counts = transpiled_cir.count_ops()["cx"]
width = transpiled_cir.width()
print(f"==== qiskit for {SIZE}==== time: {transpilation_time}")
q_walk_step.measure_all()
simulatorUsed = AerSimulator()
transpiled_circuit = transpile(q_walk_step, simulatorUsed)
result = simulatorUsed.run(transpiled_circuit).result()
counts = result.get_counts(transpiled_circuit)
plot_histogram(counts)
plt.show()

# 