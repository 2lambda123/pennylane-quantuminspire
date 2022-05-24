import numpy as np
import pytest

import pennylane as qml
import qiskit.providers.aer.noise as noise


class TestProbabilities:
    """Tests for the probability function"""

    def test_probability_no_results(self, hardware_backend):
        """
        Test that the probabilities function returns None if no job has yet been run.
        """
        dev = qml.device("quantuminspire.qi", backend=hardware_backend, wires=1, shots=None)
        assert dev.analytic_probability(wires=1) is None


class TestQuantumInspireBackendOptions:
    """Test the backend options of QuantumInspire backends."""

    def test_backend_options_cleaned(self):
        """Test that the backend memory options is reset upon new qxsim device
        initialization."""
        dev = qml.device("quantuminspire.qxsim", wires=2, memory=False)
        assert dev.backend.options.get("memory") == True

        dev2 = qml.device("quantuminspire.qxsim", wires=2)
        assert dev2.backend.options.get("memory") == True

    def test_backend_unsupported_options(self):
        """Test that an unsupported backend options triggers an Exception."""
        noise_model = noise.NoiseModel()
        bit_flip = noise.pauli_error([("X", 1), ("I", 0)])

        # Create a noise model where the RX operation always flips the bit
        noise_model.add_all_qubit_quantum_error(bit_flip, ["rx"])

        with pytest.raises(AttributeError) as exc_info:
            dev = qml.device("quantuminspire.qxsim", wires=2, noise_model=noise_model)

        assert str(exc_info.value) == 'Options field noise_model is not valid for this backend'


class TestAnalyticWarningHWSimulator:
    """Tests the warnings for when the analytic attribute of a device is set to true"""

    def test_warning_raised_for_hardware_backend_analytic_expval(self, hardware_backend, recorder):
        """Tests that a warning is raised if the analytic attribute is true on
        hardware simulators when calculating the expectation"""

        with pytest.warns(UserWarning) as record:
            dev = qml.device("quantuminspire.qi", backend=hardware_backend, wires=2, shots=None)

        # check that only one warning was raised
        assert len(record) == 1
        # check that the message matches
        assert (
            record[0].message.args[0] == "The analytic calculation of "
                                         "expectations, variances and probabilities is only supported on "
                                         "statevector backends, not on the {}. Such statistics obtained from this "
                                         "device are estimates based on samples.".format(dev.backend)
        )
