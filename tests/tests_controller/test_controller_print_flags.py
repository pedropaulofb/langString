import pytest
from langstring import Controller
from langstring import GlobalFlag
from langstring import LangStringFlag
from langstring import MultiLangStringFlag
from langstring import SetLangStringFlag

all_flags = (
    list(LangStringFlag.__members__.values())
    + list(SetLangStringFlag.__members__.values())
    + list(MultiLangStringFlag.__members__.values())
    + list(GlobalFlag.__members__.values())
)


def construct_expected_output():
    output = ""
    sorted_flags = sorted(Controller.flags.items(), key=lambda item: item[0].__class__.__name__ + "." + item[0].name)
    for flag, state in sorted_flags:
        flag_class_name = flag.__class__.__name__
        default_state = "True" if state else "False"
        output += f"{flag_class_name}.{flag.name} = {default_state}\n"
    return output


def construct_expected_output_for_type(flag_type=None):
    output = ""
    for flag, state in sorted(
        Controller.flags.items(), key=lambda item: item[0].__class__.__name__ + "." + item[0].name
    ):
        if flag_type is None or isinstance(flag, flag_type):
            flag_class_name = flag.__class__.__name__
            output += f"{flag_class_name}.{flag.name} = {state}\n"
    return output


def test_print_flags_default(capfd):
    Controller.print_flags()
    out, _ = capfd.readouterr()
    expected_output = construct_expected_output()
    assert out == expected_output, "Default flag settings should be printed correctly"


@pytest.mark.parametrize("flag", all_flags)
def test_print_flags_after_modification(capfd, flag):
    Controller.set_flag(flag, False)
    Controller.print_flags()
    out, _ = capfd.readouterr()

    # Construct the expected output for the modified flag
    expected_output = construct_expected_output()
    expected_line = f"{flag.__class__.__name__}.{flag.name} = False"
    assert expected_line in expected_output, "Modified flag settings should be printed correctly"


def test_print_flags_after_reset(capfd):
    Controller.set_flag(LangStringFlag.DEFINED_TEXT, False)
    Controller.reset_flags()
    Controller.print_flags()
    out, _ = capfd.readouterr()
    expected_output = construct_expected_output()
    assert out == expected_output, "Flag settings should be reset and printed correctly"


def test_print_flags_consistent_order(capfd):
    """
    Test that the output order of flags is consistent across multiple calls.
    """
    Controller.print_flags()
    out1, _ = capfd.readouterr()
    Controller.print_flags()
    out2, _ = capfd.readouterr()
    assert out1 == out2, "The output order of flags should be consistent across calls"


def test_print_flags_all_modified(capfd):
    """
    Test the output format when all flags are modified to a non-default state.
    """
    # Set all flags to a specific state (True or False)
    set_state = True  # You can choose True or False here
    for flag in all_flags:
        Controller.set_flag(flag, set_state)

    Controller.print_flags()
    out, _ = capfd.readouterr()

    # Construct the expected output based on the current state of flags
    expected_output = ""
    sorted_flags = sorted(Controller.flags.items(), key=lambda item: item[0].__class__.__name__ + "." + item[0].name)
    for flag, state in sorted_flags:
        flag_class_name = flag.__class__.__name__
        expected_output += f"{flag_class_name}.{flag.name} = {state}\n"

    assert out == expected_output, "All flags should be printed with their current states"


@pytest.mark.parametrize("flag_type", [None, GlobalFlag, LangStringFlag, SetLangStringFlag, MultiLangStringFlag])
def test_print_flags_valid_type(capfd, flag_type):
    Controller.print_flags(flag_type)
    out, _ = capfd.readouterr()
    expected_output = construct_expected_output_for_type(flag_type)
    assert out == expected_output, f"Should print flags correctly for type {flag_type}"


@pytest.mark.parametrize("invalid_type", [0, "invalid", float, list])
def test_print_flags_invalid_type(capfd, invalid_type):
    with pytest.raises(TypeError):
        Controller.print_flags(invalid_type)


def test_print_flags_all_same_state(capfd):
    """
    Test the output format when all flags are set to the same state.
    """
    # Set all flags to the same state (True or False)
    set_state = True  # or False
    for flag in all_flags:
        Controller.set_flag(flag, set_state)

    Controller.print_flags()
    out, _ = capfd.readouterr()

    # Construct the expected output based on the current state of flags
    expected_output = ""
    sorted_flags = sorted(Controller.flags.items(), key=lambda item: item[0].__class__.__name__ + "." + item[0].name)
    for flag, state in sorted_flags:
        flag_class_name = flag.__class__.__name__
        expected_output += f"{flag_class_name}.{flag.name} = {set_state}\n"

    assert out == expected_output, "All flags should be printed with the same state"
