import sys
from io import StringIO

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
def test_print_flag_valid(flag):
    """
    Test printing a valid flag.
    """
    # Capture the output of the print_flag method
    captured_output = StringIO()
    sys.stdout = captured_output

    # Set the flag to a known state and print it
    Controller.set_flag(flag, True)
    Controller.print_flag(flag)

    # Restore stdout
    sys.stdout = sys.__stdout__

    # Check if the output is as expected
    expected_output = f"{flag.__class__.__name__}.{flag.name} = True\n"
    assert captured_output.getvalue() == expected_output


@pytest.mark.parametrize("invalid_flag", [123, "InvalidFlag", 4.5, None, []])
def test_print_flag_invalid_type(invalid_flag):
    """
    Test printing a flag with an invalid type.
    """
    with pytest.raises(
        TypeError,
        match="Invalid flag type. Expected GlobalFlag, LangStringFlag, SetLangStringFlag, or MultiLangStringFlag",
    ):
        Controller.print_flag(invalid_flag)


@pytest.mark.parametrize("flag", all_flags)
def test_print_flag_default_state(flag):
    """
    Test printing a flag in its default state.
    """
    # Capture the output of the print_flag method
    captured_output = StringIO()
    sys.stdout = captured_output

    # Reset the flag to its default state and print it
    Controller.reset_flags()
    Controller.print_flag(flag)

    # Restore stdout
    sys.stdout = sys.__stdout__

    # Check if the output is as expected
    default_state = (
        "True"
        if flag
        in [
            GlobalFlag.PRINT_WITH_LANG,
            GlobalFlag.PRINT_WITH_QUOTES,
            LangStringFlag.PRINT_WITH_QUOTES,
            LangStringFlag.PRINT_WITH_LANG,
            SetLangStringFlag.PRINT_WITH_QUOTES,
            SetLangStringFlag.PRINT_WITH_LANG,
            MultiLangStringFlag.PRINT_WITH_QUOTES,
            MultiLangStringFlag.PRINT_WITH_LANG,
        ]
        else "False"
    )
    expected_output = f"{flag.__class__.__name__}.{flag.name} = {default_state}\n"
    assert captured_output.getvalue() == expected_output


@pytest.mark.parametrize("flag", all_flags)
def test_print_flag_nonexistent(flag):
    """
    Test printing a flag that exists in the enum but is not set in the Controller.flags dictionary.
    """
    # Capture the output of the print_flag method
    captured_output = StringIO()
    sys.stdout = captured_output

    # Remove the flag from the Controller.flags dictionary if it exists
    Controller.flags.pop(flag, None)
    Controller.print_flag(flag)

    # Restore stdout
    sys.stdout = sys.__stdout__

    # Check if the output indicates the flag is False (default for non-existent flags)
    expected_output = f"{flag.__class__.__name__}.{flag.name} = False\n"
    assert captured_output.getvalue() == expected_output, "Non-existent flags should print as False"


@pytest.mark.parametrize("flag, state", [(flag, state) for flag in all_flags for state in [True, False]])
def test_print_flag_output_format(flag, state: bool):
    """
    Test the output format of the print_flag method for different flag states.
    """
    # Capture the output of the print_flag method
    captured_output = StringIO()
    sys.stdout = captured_output

    # Set the flag to the specified state and print it
    Controller.set_flag(flag, state)
    Controller.print_flag(flag)

    # Restore stdout
    sys.stdout = sys.__stdout__

    # Check if the output format is as expected
    expected_output = f"{flag.__class__.__name__}.{flag.name} = {state}\n"
    assert (
        captured_output.getvalue() == expected_output
    ), f"Output format for {flag.name} should be '{expected_output.strip()}'"
