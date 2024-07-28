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


def test_get_flags() -> None:
    """Test retrieving the states of all flags."""
    expected_flags = Controller._DEFAULT_FLAGS  # Use the actual default flags
    assert Controller.get_flags() == expected_flags, "All flags should be retrieved correctly"


@pytest.mark.parametrize("flag", all_flags)
def test_get_flags_after_modification(flag) -> None:
    """
    Test retrieving the states of all flags after modifying a single flag.
    """
    # Set a single flag to True and check its state
    Controller.set_flag(flag, True)
    flags = Controller.get_flags()
    assert flags[flag] is True, f"Flag {flag.name} should be True after modification"


def test_get_flags_after_reset() -> None:
    """
    Test retrieving the states of all flags after resetting them to their default values.
    """
    for flag in all_flags:
        Controller.set_flag(flag, True)
    Controller.reset_flags()
    expected_flags = Controller._DEFAULT_FLAGS  # Assuming _DEFAULT_FLAGS is the correct default state
    assert Controller.get_flags() == expected_flags, "Flags should return to default states after reset"


@pytest.mark.parametrize("flag, state", [(flag, True) for flag in all_flags])
def test_get_flags_individual_modifications(flag, state: bool) -> None:
    Controller.set_flag(flag, state)
    flags = Controller.get_flags()
    assert flags[flag] is state, f"State of {flag.name} should be {state} after modification"


def test_get_flags_immutable_return() -> None:
    """
    Test that the dictionary returned by get_flags is a copy and does not modify the original flags.
    """
    original_flags = Controller.get_flags()
    modified_flags = Controller.get_flags()
    modified_flags[next(iter(all_flags))] = not original_flags[next(iter(all_flags))]
    assert (
        Controller.get_flags() == original_flags
    ), "Modifying the returned dictionary should not affect original flags"


def test_get_flags_consistency() -> None:
    """
    Test that multiple calls to get_flags return consistent results.
    """
    flags_first_call = Controller.get_flags()
    flags_second_call = Controller.get_flags()
    assert flags_first_call == flags_second_call, "Multiple calls to get_flags should return consistent results"


def test_get_flags_complete_mapping() -> None:
    """
    Test that get_flags returns a dictionary with all known flags and boolean values.
    """
    flags = Controller.get_flags()
    for flag in all_flags:
        assert flag in flags, f"Flag {flag.name} should be present in the returned dictionary"
        assert isinstance(flags[flag], bool), f"The value for flag {flag.name} should be a boolean"


def test_get_flags_no_direct_reference() -> None:
    """
    Test that the dictionary returned by get_flags is not a direct reference to the internal flag storage.
    """
    flags_before_modification = Controller.get_flags()
    flags_after_modification = Controller.get_flags()
    flags_after_modification[next(iter(all_flags))] = not flags_before_modification[next(iter(all_flags))]
    assert (
        Controller.get_flags() == flags_before_modification
    ), "Modifying the returned dictionary should not affect the internal flag storage"
