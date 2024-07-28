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


@pytest.mark.parametrize("flag, expected_state", [(flag, False) for flag in all_flags])
def test_default_flag_state(flag, expected_state: bool):
    # Handle exceptions where the default state is not False
    if flag in [
        GlobalFlag.PRINT_WITH_QUOTES,
        GlobalFlag.PRINT_WITH_LANG,
        LangStringFlag.PRINT_WITH_QUOTES,
        LangStringFlag.PRINT_WITH_LANG,
        SetLangStringFlag.PRINT_WITH_QUOTES,
        SetLangStringFlag.PRINT_WITH_LANG,
        MultiLangStringFlag.PRINT_WITH_QUOTES,
        MultiLangStringFlag.PRINT_WITH_LANG,
    ]:
        expected_state = True
    assert Controller.get_flag(flag) == expected_state


def test_instantiation_of_langstringcontrol():
    with pytest.raises(TypeError, match="Controller class cannot be instantiated."):
        Controller()


@pytest.mark.parametrize("initial_state, new_state", [(False, True), (True, False)])
def test_flag_state_persistence(initial_state: bool, new_state: bool):
    for flag in all_flags:
        Controller.set_flag(flag, initial_state)
        assert Controller.get_flag(flag) == initial_state, f"Error for {flag} with initial state."
        Controller.set_flag(flag, new_state)
        assert Controller.get_flag(flag) == new_state, f"Error for {flag} with new state."


def test_multiple_flag_modifications_integrity():
    for flag in all_flags:
        Controller.set_flag(flag, True)
    for flag in all_flags:
        assert Controller.get_flag(flag), f"{flag.name} flag should be True"
    Controller.reset_flags()


def test_flag_state_consistency_across_methods():
    for flag in all_flags:
        Controller.set_flag(flag, True)
    all_flags_state = Controller.get_flags()
    for flag in all_flags:
        assert (
            Controller.get_flag(flag) == all_flags_state[flag]
        ), f"Flag state for {flag.name} should be consistent across get_flag and get_flags methods"
    Controller.reset_flags()


def test_get_flag_equals_get_flags():
    all_flags_dict = Controller.get_flags()
    for flag in all_flags:
        assert Controller.get_flag(flag) == all_flags_dict[flag], "get_flag should match get_flags for each flag"


def test_reset_flag_global_equals_reset_flags():
    # Set all flags to a non-default state
    for flag in all_flags:
        Controller.set_flag(flag, not Controller._DEFAULT_FLAGS[flag])

    # Reset GlobalFlag
    for global_flag in list(GlobalFlag.__members__.values()):
        Controller.reset_flag(global_flag)

    Controller.print_flags()

    # Get the state after resetting GlobalFlag
    state_after_reset_global = Controller.get_flags()

    # Set all flags to a non-default state
    for flag in all_flags:
        Controller.set_flag(flag, not Controller._DEFAULT_FLAGS[flag])

    # Reset all flags
    Controller.reset_flags()

    Controller.print_flags()

    # Get the state after resetting all flags
    state_after_reset_all = Controller.get_flags()

    # Check if the states match for resetting GlobalFlag and resetting all flags
    assert (
        state_after_reset_global == state_after_reset_all
    ), "reset_flag(GlobalFlag) should match the state after reset_flags()"


def test_reset_flags_to_default_after_modification():
    # Modify flags
    for flag in all_flags:
        Controller.set_flag(flag, not Controller._DEFAULT_FLAGS[flag])
    # Reset flags
    Controller.reset_flags()
    # Verify flags are reset to default
    for flag in all_flags:
        assert Controller.get_flag(flag) == Controller._DEFAULT_FLAGS[flag], f"{flag} should be reset to default"


def test_partial_reset_consistency():
    # Set all flags to a non-default state
    for flag in all_flags:
        Controller.set_flag(flag, not Controller._DEFAULT_FLAGS[flag])
    # Reset only LangStringFlag type flags
    Controller.reset_flags(LangStringFlag)
    # Check if other flag types remain unchanged
    for flag in all_flags:
        if isinstance(flag, LangStringFlag):
            expected_state = Controller._DEFAULT_FLAGS[flag]
        else:
            expected_state = not Controller._DEFAULT_FLAGS[flag]
        assert Controller.get_flag(flag) == expected_state, f"Flag {flag} state inconsistency after partial reset"


def test_flag_state_after_sequential_resets():
    # Set all flags to a non-default state
    for flag in all_flags:
        Controller.set_flag(flag, not Controller._DEFAULT_FLAGS[flag])
    # Sequentially reset different flag types
    Controller.reset_flags(GlobalFlag)
    Controller.reset_flags(LangStringFlag)
    # Verify flags are reset to default
    for flag in all_flags:
        assert (
            Controller.get_flag(flag) == Controller._DEFAULT_FLAGS[flag]
        ), f"{flag} should be reset to default after sequential resets"
