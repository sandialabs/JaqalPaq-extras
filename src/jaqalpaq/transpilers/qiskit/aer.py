from qiskit.result.result import Result
from qiskit.providers.basejob import BaseJob
from qiskit.providers.basebackend import BaseBackend
from qiskit.providers.jobstatus import JobStatus
from qiskit import Aer
from qiskit.aqua import QuantumInstance
from .unroller import IonUnroller
from .frontend import jaqal_circuit_from_qiskit_circuit
from qiskit.transpiler import PassManager
from jaqalpaq.emulator import run_jaqal_circuit
import numpy as np
from collections import Counter


class IonResult:
    def __init__(self, counts):
        self.counts = counts

    def get_counts(self, name=None):
        if len(self.counts) == 1:
            return next(iter(self.counts.values()))
        if isinstance(name, int):
            name = list(self.counts.keys())[name]
        return self.counts[name]

    def data(self, idx):
        return {}


class IonInstance(QuantumInstance):
    def transpile(self, circuits):
        if isinstance(circuits, list):
            return [
                PassManager([IonUnroller()]).run(circuit.decompose())
                for circuit in circuits
            ]
        else:
            return [PassManager([IonUnroller()]).run(circuits.decompose())]

    def execute(self, circuits, had_transpiled=False):
        if not had_transpiled:
            circuits = self.transpile(circuits)
        counts = {}
        for circuit in circuits:
            jcircuit = jaqal_circuit_from_qiskit_circuit(circuit)
            results = run_jaqal_circuit(jcircuit)
            probs = np.array(results.subcircuits[0].probability_by_int)
            qubits = len(circuit.qubits)
            shots = [
                f"{np.random.choice(2 ** qubits, p=probs):b}".zfill(qubits)
                for shot in range(self._run_config.shots)
            ]
            counts[circuit.name] = dict(Counter(shots))
        # job = IonJob(self.backend, "")
        # job._result = IonResult(statevectors)
        return IonResult(counts)


def get_ion_instance():
    return IonInstance(Aer.get_backend("qasm_simulator"))
