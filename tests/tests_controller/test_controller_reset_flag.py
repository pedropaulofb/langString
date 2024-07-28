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


@pytest.mark.parametrize("flag", all_flags)
def test_reset_specific_flag(flag):
    """Test resetting a specific flag to its default value."""
    # Set the flag to a non-default state and then reset it
    non_default_state = not Controller._DEFAULT_FLAGS[flag]
    Controller.set_flag(flag, non_default_state)
    Controller.reset_flag(flag)
    assert Controller.get_flag(flag) == Controller._DEFAULT_FLAGS[flag], f"{flag} should be reset to its default state"


@pytest.mark.parametrize("invalid_flag", [0, "invalid_flag", None, 123.456])
def test_reset_flag_invalid_type(invalid_flag):
    """Test resetting a flag with an invalid type."""
    with pytest.raises(TypeError, match="Invalid flag."):
        Controller.reset_flag(invalid_flag)


@pytest.mark.parametrize("flag", all_flags)
def test_reset_flag_idempotence(flag):
    """Test the idempotence of resetting a flag."""
    Controller.reset_flag(flag)
    initial_state = Controller.get_flag(flag)
    Controller.reset_flag(flag)
    assert Controller.get_flag(flag) == initial_state, f"Resetting {flag} multiple times should not change its state"


def test_reset_flag_affects_only_specified_flag():
    """Test that resetting one flag does not affect the state of other flags."""
    # Set all flags to a non-default state
    for f in all_flags:
        Controller.set_flag(f, not Controller._DEFAULT_FLAGS[f])

    # Reset one flag
    test_flag = GlobalFlag.DEFINED_TEXT
    Controller.reset_flag(test_flag)

    # Check that only the reset flag and its equivalents are affected
    for f in all_flags:
        if f.name == test_flag.name:
            expected_state = Controller._DEFAULT_FLAGS[f]  # Reset to default
        else:
            expected_state = not Controller._DEFAULT_FLAGS[f]  # Remain unchanged
        assert Controller.get_flag(f) == expected_state, f"Flag {f} was incorrectly affected by resetting {test_flag}"


@pytest.mark.parametrize("flag", all_flags)
def test_reset_flag_already_in_default_state(flag):
    """Test resetting a flag that is already in its default state."""
    # Ensure the flag is in its default state
    Controller.reset_flag(flag)
    initial_state = Controller.get_flag(flag)
    # Reset again and check if the state remains unchanged
    Controller.reset_flag(flag)
    assert (
        Controller.get_flag(flag) == initial_state
    ), f"Resetting {flag} already in default state should not change its state"
