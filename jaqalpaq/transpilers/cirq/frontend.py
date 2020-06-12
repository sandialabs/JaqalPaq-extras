from jaqalpaq.core.circuit import ScheduledCircuit
from jaqalpaq.core.gatedef import NATIVE_GATES
from jaqalpaq import JaqalError
from cirq import (
    XXPowGate,
    XPowGate,
    YPowGate,
    ZPowGate,
    PhasedXPowGate,
    MeasurementGate,
)
import numpy as np

CIRQ_NAMES = {
    XXPowGate: (lambda g, q1, q2: ("MS", q1, q2, 0, g.exponent * np.pi)),
    XPowGate: (lambda g, q: ("R", q, 0, g.exponent * np.pi)),
    YPowGate: (lambda g, q: ("R", q, 90.0, g.exponent * np.pi)),
    ZPowGate: (lambda g, q: ("Rz", q, g.exponent * np.pi)),
    PhasedXPowGate: (
        lambda g, q: ("R", q, g.phase_exponent * np.pi, g.exponent * np.pi)
    ),
}


def qscout_circuit_from_cirq_circuit(ccirc, names=None, native_gates=None):
    """Converts a Cirq Circuit object to a :class:`qscout.core.ScheduledCircuit`.
    The circuit will be structured as a sequence of parallel blocks, one for each Cirq
    Moment in the input.

    Measurement are supported, but only if applied to every qubit in the circuit in the
    same moment. If so, they will be mapped to a measure_all gate. If the measure_all gate
    is not the last gate in the circuit, a prepare_all gate will be inserted after it.
    Additionally, a prepare_all gate will be inserted before the first moment. If the
    circuit does not end with a measurement, then a measure_all gate will be appended.

    Circuits built on a line register will map each qubit to the qubit of the same index
    on the hardware. This may leave some qubits unused. Otherwise, the qubits will be
    mapped onto the hardware in the order given by ccirc.all_qubits().

    :param cirq.Circuit ccirc: The Circuit to convert.
    :param names: A mapping from Cirq gate classes to the corresponding native Jaqal gate
    	names. If omitted, maps ``cirq.XXPowGate``, ``cirq.XPowGate``, ``cirq.YPowGate``,
        ``cirq.ZPowGate``, and ``cirq.PhasedXPowGate`` to their QSCOUT counterparts. The
        ``cirq.ConvertToIonGates`` function will transpile a circuit into this basis.
    :type names: dict or None
    :param native_gates: The native gate set to target. If None, target the QSCOUT native gates.
    :type native_gates: dict or None
    :returns: The same quantum circuit, converted to JaqalPaq.
    :rtype: ScheduledCircuit
    :raises JaqalError: If the circuit includes a gate not included in `names`.
    """  # TODO: Document this better.
    qcirc = ScheduledCircuit(native_gates=native_gates)
    if names is None:
        names = CIRQ_NAMES
    try:
        n = 1 + max([qb.x for qb in ccirc.all_qubits()])
        line = True
    except:
        cqubits = ccirc.all_qubits()
        n = len(cqubits)
        qubitmap = {cqubits[i]: i for i in range(n)}
        line = False
    allqubits = qcirc.reg("allqubits", n)
    need_prep = True
    for moment in ccirc:
        if len(moment) == 0:
            continue
        if need_prep:
            qcirc.gate("prepare_all")
            need_prep = False
        if (
            len(moment) == n
            and all([op.gate for op in moment])
            and all([isinstance(op.gate, MeasurementGate) for op in moment])
        ):
            qcirc.gate("measure_all")
            need_prep = True
            continue
        if len(moment) > 1:
            block = qcirc.block(
                parallel=True
            )  # Note: If you tell Cirq you want MS gates in parallel, we'll generate a Jaqal file with exactly that, never mind that QSCOUT can't execute it.
        else:
            block = qcirc.body
        for op in moment:
            if op.gate:
                if type(op.gate) in names:
                    if line:
                        block.append(
                            qcirc.build_gate(
                                *names[type(op.gate)](
                                    op.gate, *[allqubits[qb.x] for qb in op.qubits]
                                )
                            )
                        )
                    else:
                        block.append(
                            qcirc.build_gate(
                                *names[type(op.gate)](
                                    op.gate,
                                    *[allqubits[qubitmap[qb]] for qb in op.qubits]
                                )
                            )
                        )
                else:
                    raise JaqalError("Convert circuit to ion gates before compiling.")
            else:
                raise JaqalError("Cannot compile operation %s." % op)
    if (
        not need_prep
    ):  # If we just measured, or the circuit is empty, don't add a final measurement.
        qcirc.gate("measure_all")
    return qcirc
