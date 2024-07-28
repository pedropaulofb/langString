import pytest
from langstring import Controller
from langstring import GlobalFlag
from langstring import LangStringFlag
from langstring import MultiLangStringFlag
from langstring import SetLangStringFlag


# Combine all flag types into a single list for parametrization
all_flags = (
    list(LangStringFlag.__members__.values())
    + list(SetLangStringFlag.__members__.values())
    + list(MultiLangStringFlag.__members__.values())
    + list(GlobalFlag.__members__.values())
)


@pytest.mark.parametrize("flag, state", [(flag, True) for flag in all_flags])
def test_set_flag_valid(flag, state) -> None:
    """Test setting a flag with valid values."""
    Controller.set_flag(flag, state)
    assert Controller.get_flag(flag) == state, "Flag state should be updated correctly"


@pytest.mark.parametrize("flag, state", [("InvalidFlag", True), (123, False)])
def test_set_flag_invalid(flag, state) -> None:
    """Test setting a flag with invalid flag values."""
    with pytest.raises(
        TypeError,
        match="Invalid flag type. Expected GlobalFlag, LangStringFlag, SetLangStringFlag, or MultiLangStringFlag",
    ):
        Controller.set_flag(flag, state)


@pytest.mark.parametrize("flag, state", [(flag, None) for flag in all_flags] + [(flag, 1) for flag in all_flags])
def test_set_flag_invalid_state_type(flag, state) -> None:
    """Test setting a flag with invalid state types."""
    with pytest.raises(TypeError, match="State must be a boolean"):
        Controller.set_flag(flag, state)


@pytest.mark.parametrize("flag, initial_state, new_state", [(flag, False, True) for flag in all_flags])
def test_toggle_flag_state(flag, initial_state: bool, new_state: bool) -> None:
    Controller.set_flag(flag, initial_state)
    assert Controller.get_flag(flag) == initial_state
    Controller.set_flag(flag, new_state)
    assert Controller.get_flag(flag) == new_state


@pytest.mark.parametrize("flag_sequence, state_sequence", [([flag for flag in all_flags], [True for _ in all_flags])])
def test_set_multiple_flags_sequentially(flag_sequence, state_sequence):
    for flag, state in zip(flag_sequence, state_sequence):
        Controller.set_flag(flag, state)
    for flag, state in zip(flag_sequence, state_sequence):
        assert Controller.get_flag(flag) == state


@pytest.mark.parametrize("flag, state", [(flag, True) for flag in all_flags])
def test_set_flag_same_value_multiple_times(flag, state: bool):
    for _ in range(3):
        Controller.set_flag(flag, state)
    assert Controller.get_flag(flag) == state


@pytest.mark.parametrize("flag", all_flags)
def test_set_flag_toggle_back_and_forth(flag):
    """Test toggling a flag's state back and forth."""
    initial_state = Controller.get_flag(flag)
    Controller.set_flag(flag, not initial_state)
    assert Controller.get_flag(flag) != initial_state, "Flag state should toggle to the opposite"
    Controller.set_flag(flag, initial_state)
    assert Controller.get_flag(flag) == initial_state, "Flag state should toggle back to the original"


@pytest.mark.parametrize("global_flag", list(GlobalFlag.__members__.values()))
def test_set_global_flag_affects_all(global_flag):
    """Test setting a GlobalFlag affects corresponding flags in other flag types."""
    initial_states = {flag: Controller.get_flag(flag) for flag in all_flags}
    new_state = not Controller.get_flag(global_flag)
    Controller.set_flag(global_flag, new_state)
    for flag in all_flags:
        if flag.name == global_flag.name:
            assert Controller.get_flag(flag) == new_state, f"GlobalFlag change should affect {flag}"
        else:
            assert Controller.get_flag(flag) == initial_states[flag], f"GlobalFlag change should not affect {flag}"


@pytest.mark.parametrize("flag", all_flags)
def test_set_flag_with_same_value(flag):
    """Test setting a flag with its current value."""
    current_state = Controller.get_flag(flag)
    Controller.set_flag(flag, current_state)
    assert Controller.get_flag(flag) == current_state, "Setting a flag with its current value should not change it"


@pytest.mark.parametrize("flag", all_flags)
def test_set_flag_with_different_enum_instance(flag):
    """Test setting a flag with a different enum instance but the same value."""
    # Create a new instance of the same flag
    new_flag_instance = type(flag)(flag.value)
    initial_state = Controller.get_flag(flag)
    Controller.set_flag(new_flag_instance, not initial_state)
    assert Controller.get_flag(flag) != initial_state, "Flag state should change with a different enum instance"


@pytest.mark.parametrize("flag", all_flags)
def test_set_flag_reset_and_check_default(flag):
    """Test setting a flag, resetting it, and checking if it returns to default."""
    default_state = Controller._DEFAULT_FLAGS[flag]
    Controller.set_flag(flag, not default_state)
    Controller.reset_flag(flag)
    assert Controller.get_flag(flag) == default_state, "Flag should return to default state after reset"


@pytest.mark.parametrize("global_flag, state", [(GlobalFlag.DEFINED_TEXT, True), (GlobalFlag.VALID_LANG, False)])
def test_set_global_flag_affects_others(global_flag, state):
    """Test setting a GlobalFlag affects corresponding flags in other flag types."""
    Controller.set_flag(global_flag, state)
    for flag in all_flags:
        if flag.name == global_flag.name:
            assert Controller.get_flag(flag) == state, f"Setting {global_flag} should affect {flag}"
