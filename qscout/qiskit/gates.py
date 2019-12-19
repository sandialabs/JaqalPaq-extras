# The below classes are a derivative work of Qiskit's Gate class. They have been altered from the original.

# This code is part of Qiskit.
#
# (C) Copyright IBM 2017, 2018.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

from qiskit.circuit import Gate, QuantumCircuit, QuantumRegister
from qiskit.extensions.standard.u3 import U3Gate
from qiskit.extensions.standard.cx import CnotGate
from qiskit.extensions.standard.rx import RXGate
from qiskit.extensions.standard.ry import RYGate
from qiskit.extensions.standard.rz import RZGate
from qiskit.qasm import pi

class MSGate(Gate):
	"""two-parameter Mølmer-Sørensen gate"""
	def __init__(self, theta, phi, label=None):
		super().__init__("ms", 2, [theta, phi], label=label)
	
	def _define(self):
		"""
		gate ms(theta, phi) a,b
		{
		rz(phi) a;
		rz(phi+pi/2) b;
		CX b,a;
		rz(-pi/2) a;
		ry(theta+pi/2) b;
		CX a,b;
		ry(-pi/2) b;
		CX b,a;
		rz(-phi-pi/2) a;
		rz(-phi) b;
		}
		"""
		definition = []
		q = QuantumRegister(2, "q")
		theta, phi = tuple(self.params)
		rule = [
			(U3Gate(0, 0, phi), [q[0]], []),
			(U3Gate(0, 0, phi+pi/2), [q[1]], []),
			(CnotGate(), [q[1], q[0]], []),
			(U3Gate(0, 0, -pi/2), [q[0]], []),
			(U3Gate(theta+pi/2,0,0), [q[0]], []),
			(CnotGate(), [q[0], q[1]], []),
			(U3Gate(-pi/2,0,0), [q[0]], []),
			(CnotGate(), [q[1], q[0]], []),
			(U3Gate(0, 0, -phi-pi/2), [q[0]], []),
			(U3Gate(0, 0, -phi), [q[0]], []),
		]
		for inst in rule:
			definition.append(inst)
		self.definition = definition

def ms(self, theta, phi, a, b):
	return self.append(MSGate(theta, phi), [a, b], [])
QuantumCircuit.ms = ms

class SXGate(Gate):
	"""sqrt(X) gate"""
	def __init__(self, label=None):
		super().__init__("sx", 1, [], label=label)
	
	def _define(self):
		"""
		gate sx() a
		{
		rx(pi/2) a;
		}
		"""
		definition = []
		q = QuantumRegister(2, "q")
		rule = [
			(RXGate(pi/2), [q[0]], []),
		]
		for inst in rule:
			definition.append(inst)
		self.definition = definition

def sx(self, q):
	return self.append(SXGate(), [q], [])
QuantumCircuit.sx = sx

class SYGate(Gate):
	"""sqrt(Y) gate"""
	def __init__(self, label=None):
		super().__init__("sy", 1, [], label=label)
	
	def _define(self):
		"""
		gate sy() a
		{
		ry(pi/2) a;
		}
		"""
		definition = []
		q = QuantumRegister(2, "q")
		rule = [
			(RYGate(pi/2), [q[0]], []),
		]
		for inst in rule:
			definition.append(inst)
		self.definition = definition

def sy(self, q):
	return self.append(SYGate(), [q], [])
QuantumCircuit.sy = sy

class RGate(Gate):
	"""arbitrary rotation around an axis in the X-Y plane"""
	def __init__(self, axis_angle, rotation_angle, label=None):
		super().__init__("r", 1, [axis_angle, rotation_angle], label=label)
	
	def _define(self):
		"""
		gate r(theta, phi) a
		{
		rz(-theta) a;
		rx(phi) a;
		rz(theta) a;
		}
		"""
		definition = []
		q = QuantumRegister(2, "q")
		theta, phi = tuple(self.params)
		rule = [
			(RZGate(-theta), [q[0]], []),
			(RXGate(phi), [q[0]], []),
			(RZGate(theta), [q[0]], []),
		]
		for inst in rule:
			definition.append(inst)
		self.definition = definition

def r(self, theta, phi, q):
	return self.append(RGate(theta, phi), [q], [])
QuantumCircuit.r = r