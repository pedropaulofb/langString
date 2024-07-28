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
def test_get_flag_valid(flag) -> None:
    """Test retrieving the state of a valid flag."""
    Controller.set_flag(flag, True)  # Set flag to True for testing
    assert Controller.get_flag(flag) is True, "Flag state should be retrievable"


@pytest.mark.parametrize("flag, expected_state", [(flag, False) for flag in all_flags])
def test_get_flag_default_states(flag, expected_state: bool) -> None:
    """Test retrieving the default state of each flag."""
    # Handle exceptions where the default state is not False
    if flag in [
        GlobalFlag.PRINT_WITH_LANG,
        GlobalFlag.PRINT_WITH_QUOTES,
        LangStringFlag.PRINT_WITH_QUOTES,
        LangStringFlag.PRINT_WITH_LANG,
        SetLangStringFlag.PRINT_WITH_QUOTES,
        SetLangStringFlag.PRINT_WITH_LANG,
        MultiLangStringFlag.PRINT_WITH_QUOTES,
        MultiLangStringFlag.PRINT_WITH_LANG,
    ]:
        expected_state = True
    assert Controller.get_flag(flag) == expected_state


@pytest.mark.parametrize("flag, state_to_set", [(flag, True) for flag in all_flags])
def test_get_flag_after_setting_state(flag, state_to_set: bool) -> None:
    """Test retrieving the state of a flag after setting it to a specific state."""
    Controller.set_flag(flag, state_to_set)
    assert Controller.get_flag(flag) == state_to_set, f"State of {flag.name} should be {state_to_set} after setting"


def test_get_flag_nonexistent() -> None:
    """Test retrieving the state of a nonexistent flag."""
    with pytest.raises(
        TypeError,
        match="Invalid flag type. Expected GlobalFlag, LangStringFlag, SetLangStringFlag, or MultiLangStringFlag",
    ):
        Controller.get_flag("NonexistentFlag")


@pytest.mark.parametrize("invalid_flag", [123, 4.5, None, [], {}])
def test_get_flag_invalid_type(invalid_flag) -> None:
    """Test retrieving the state of a flag with an invalid type."""
    with pytest.raises(
        TypeError,
        match="Invalid flag type. Expected GlobalFlag, LangStringFlag, SetLangStringFlag, or MultiLangStringFlag",
    ):
        Controller.get_flag(invalid_flag)


@pytest.mark.parametrize("flag, state_to_set", [(flag, False) for flag in all_flags])
def test_get_flag_after_setting_state_to_false(flag, state_to_set: bool) -> None:
    """
    Test retrieving the state of a flag after setting it to False.

    :param flag: The flag to be tested.
    :param state_to_set: The state to set the flag to (False in this case).
    :type flag: Union[GlobalFlag, LangStringFlag, SetLangStringFlag, MultiLangStringFlag]
    :type state_to_set: bool
    """
    Controller.set_flag(flag, state_to_set)
    assert Controller.get_flag(flag) == state_to_set, f"State of {flag.name} should be {state_to_set} after setting"


@pytest.mark.parametrize("flag, invalid_state", [(flag, "invalid") for flag in all_flags])
def test_get_flag_setting_invalid_state(flag, invalid_state: str) -> None:
    """
    Test setting a flag to an invalid state and retrieving it.

    :param flag: The flag to be tested.
    :param invalid_state: The invalid state to set the flag to.
    :type flag: Union[GlobalFlag, LangStringFlag, SetLangStringFlag, MultiLangStringFlag]
    :type invalid_state: str
    """
    with pytest.raises(
        TypeError,
        match="Invalid state received. State must be a boolean new_text.",
    ):
        Controller.set_flag(flag, invalid_state)


@pytest.mark.parametrize("flag", all_flags)
def test_get_flag_after_resetting(flag) -> None:
    """
    Test retrieving the state of a flag after resetting it.

    :param flag: The flag to be tested.
    :type flag: Union[GlobalFlag, LangStringFlag, SetLangStringFlag, MultiLangStringFlag]
    """
    Controller.set_flag(flag, True)
    Controller.set_flag(flag, False)
    assert Controller.get_flag(flag) is False, f"State of {flag.name} should be False after resetting"


@pytest.mark.parametrize("flag", all_flags)
def test_get_flag_under_high_load(flag) -> None:
    """
    Test retrieving the state of a flag under high load, by setting and getting it repeatedly.

    :param flag: The flag to be tested.
    :type flag: Union[GlobalFlag, LangStringFlag, SetLangStringFlag, MultiLangStringFlag]
    """
    for _ in range(1000):
        Controller.set_flag(flag, True)
        assert Controller.get_flag(flag) is True
        Controller.set_flag(flag, False)
        assert Controller.get_flag(flag) is False


def test_get_flag_with_high_volume_of_flags() -> None:
    """
    Test the performance of get_flag method under a high volume of flags.

    This test simulates a scenario where a large number of flags are set and then retrieved,
    testing the method's performance and stability under load.
    """
    for flag in all_flags[:1000]:  # Limiting to a subset of existing flags
        Controller.set_flag(flag, True)
        assert Controller.get_flag(flag) is True, f"Failed to retrieve state for {flag}"
        Controller.set_flag(flag, False)
        assert Controller.get_flag(flag) is False, f"Failed to retrieve state for {flag}"
