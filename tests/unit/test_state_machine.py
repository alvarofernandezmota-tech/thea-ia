import pytest
from theaia.core.state_machine import StateMachineFactory

def test_fsm_initial_state():
    """
    Verifica que la máquina de estados arranca en el estado 'IDLE'.
    """
    fsm = StateMachineFactory().create()
    assert fsm.state == "IDLE"
