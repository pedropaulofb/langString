import pytest
from langstring import Controller
from langstring import GlobalFlag
from langstring import LangStringFlag
from langstring import MultiLangStringFlag
from langstring import SetLangStringFlag

# Combine all flag types into a single list for parametrization
all_flag_types = [GlobalFlag, LangStringFlag, SetLangStringFlag, MultiLangStringFlag]

all_flags = (
    list(LangStringFlag.__members__.values())
    + list(SetLangStringFlag.__members__.values())
    + list(MultiLangStringFlag.__members__.values())
    + list(GlobalFlag.__members__.values())
)


@pytest.mark.parametrize("flag_type", all_flag_types)
def test_reset_flags_valid_type(flag_type):
    """Test resetting flags of a valid type."""
    # Modify some flags before resetting
    for flag in flag_type:
        Controller.set_flag(flag, not Controller._DEFAULT_FLAGS[flag])
    # Reset flags of the specified type
    Controller.reset_flags(flag_type)
    # Check if all flags are reset to their default values
    for flag in flag_type:
        assert Controller.get_flag(flag) == Controller._DEFAULT_FLAGS[flag], f"Flag {flag} should be reset to default"


def test_reset_flags_all_types():
    """Test resetting all flags when no type is specified."""
    # Modify some flags before resetting
    for flag_type in all_flag_types:
        for flag in flag_type:
            Controller.set_flag(flag, not Controller._DEFAULT_FLAGS[flag])
    # Reset all flags
    Controller.reset_flags()
    # Check if all flags are reset to their default values
    for flag_type in all_flag_types:
        for flag in flag_type:
            assert (
                Controller.get_flag(flag) == Controller._DEFAULT_FLAGS[flag]
            ), f"Flag {flag} should be reset to default"


@pytest.mark.parametrize("invalid_type", [0, "invalid", float, list])
def test_reset_flags_invalid_type(invalid_type):
    """Test resetting flags with an invalid type."""
    with pytest.raises(TypeError, match="Invalid flag type."):
        Controller.reset_flags(invalid_type)


def test_reset_global_flag_resets_all_types():
    """Test that resetting GlobalFlag also resets flags of LangStringFlag, MultiLangStringFlag, and SetLangStringFlag."""
    # Modify some flags before resetting
    for flag in all_flags:
        new_state = not Controller._DEFAULT_FLAGS[flag]
        Controller.set_flag(flag, new_state)
        assert Controller.get_flag(flag) == new_state, f"Failed to set {flag} to {new_state}"

    # Reset only GlobalFlag type flags
    Controller.reset_flags(GlobalFlag)

    # Check if all flags are reset to their default values
    for flag in all_flags:
        assert Controller.get_flag(flag) == Controller._DEFAULT_FLAGS[flag], f"Flag {flag} should be reset to default"
