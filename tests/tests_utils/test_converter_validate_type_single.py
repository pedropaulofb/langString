import re
from typing import Any
from typing import Optional

import pytest
from langstring.utils.validators import TypeValidator


@pytest.mark.parametrize(
    "arg, arg_exp_type, optional",
    [
        (1, int, False),
        ("test", str, False),
        (3.14, float, False),
        (True, bool, False),
        (None, Optional[int], True),
        ([], list, False),
        ({}, dict, False),
        (set(), set, False),
        ((1, 2), tuple, False),
        ("", str, False),  # Empty string
        ("   ", str, False),  # String with spaces
        ("Test", str, False),  # Capitalized string
        ("TEST", str, False),  # Uppercase string
        ("TeSt", str, False),  # Mixed case string
        ("тест", str, False),  # Cyrillic string
        ("δοκιμή", str, False),  # Greek string
        ("😀", str, False),  # Emoji
        ("test!", str, False),  # String with special character
        ("test\ttest", str, False),  # String with tab character
        ("test\ntest", str, False),  # String with newline character
        ([""], list, False),  # List with empty string
        (["test"], list, False),  # List with one string
        (["test", ""], list, False),  # List with string and empty string
        ([], list, True),  # Empty list when optional is True
        (set(), set, True),  # Empty set when optional is True
        ({}, dict, True),  # Empty dict when optional is True
        ("", str, False),  # Empty string
        ("   ", str, False),  # String with spaces
        ("Test", str, False),  # Capitalized string
        ("TEST", str, False),  # Uppercase string
        ("TeSt", str, False),  # Mixed case string
        ("тест", str, False),  # Cyrillic string
        ("δοκιμή", str, False),  # Greek string
        ("😀", str, False),  # Emoji
        ("test!", str, False),  # String with special character
        ("test\ttest", str, False),  # String with tab character
        ("test\ntest", str, False),  # String with newline character
        ([""], list, False),  # List with empty string
        (["test"], list, False),  # List with one string
        (["test", ""], list, False),  # List with string and empty string
    ],
)
def test_validate_type_single_valid_cases(arg: Any, arg_exp_type: type, optional: bool) -> None:
    """Test TypeValidator.validate_type_single with valid cases.

    :param arg: The argument to check.
    :param arg_exp_type: The expected type of the argument.
    :param optional: Whether the argument is optional.
    :return: None
    :raises: None
    """
    try:
        TypeValidator.validate_type_single(arg, arg_exp_type, optional)
    except TypeError:
        pytest.fail(f"validate_type_single raised TypeError unexpectedly for arg: {arg} and type: {arg_exp_type}")


@pytest.mark.parametrize(
    "arg, arg_exp_type, optional, error_message",
    [
        (1, str, False, re.escape("Invalid argument with value '1'. Expected 'str', but got 'int'.")),
        ("test", int, False, re.escape("Invalid argument with value 'test'. Expected 'int', but got 'str'.")),
        (3.14, int, False, re.escape("Invalid argument with value '3.14'. Expected 'int', but got 'float'.")),
        (None, int, False, re.escape("Invalid argument with value 'None'. Expected 'int', but got 'NoneType'.")),
        ([], dict, False, re.escape("Invalid argument with value '[]'. Expected 'dict', but got 'list'.")),
        ({}, list, False, re.escape("Invalid argument with value '{}'. Expected 'list', but got 'dict'.")),
        (set(), list, False, re.escape("Invalid argument with value 'set()'. Expected 'list', but got 'set'.")),
        ((1, 2), list, False, re.escape("Invalid argument with value '(1, 2)'. Expected 'list', but got 'tuple'.")),
        ("", int, False, re.escape("Invalid argument with value ''. Expected 'int', but got 'str'.")),  # Empty string
        ([], int, False, re.escape("Invalid argument with value '[]'. Expected 'int', but got 'list'.")),  # Empty list
        ({}, int, False, re.escape("Invalid argument with value '{}'. Expected 'int', but got 'dict'.")),  # Empty dict
        (
            set(),
            int,
            False,
            re.escape("Invalid argument with value 'set()'. Expected 'int', but got 'set'."),
        ),  # Empty set
        (
            (),
            int,
            False,
            re.escape("Invalid argument with value '()'. Expected 'int', but got 'tuple'."),
        ),  # Empty tuple
        (b"bytes", str, False, re.escape("Invalid argument with value 'b'bytes''. Expected 'str', but got 'bytes'.")),
        # Bytes
        ("123", int, False, re.escape("Invalid argument with value '123'. Expected 'int', but got 'str'.")),
        # Numeric string
        ("1.23", float, False, re.escape("Invalid argument with value '1.23'. Expected 'float', but got 'str'.")),
        # String with space
        ("тест", int, False, re.escape("Invalid argument with value 'тест'. Expected 'int', but got 'str'.")),
        # Cyrillic string as int
        (
            "😀",
            int,
            False,
            re.escape("Invalid argument with value '😀'. Expected 'int', but got 'str'."),
        ),  # Emoji as int
    ],
)
def test_validate_type_single_invalid_cases(arg: Any, arg_exp_type: type, optional: bool, error_message: str) -> None:
    """Test TypeValidator.validate_type_single with invalid cases.

    :param arg: The argument to check.
    :param arg_exp_type: The expected type of the argument.
    :param optional: Whether the argument is optional.
    :param error_message: The expected error message.
    :return: None
    :raises TypeError: If the argument does not match the expected type.
    """
    with pytest.raises(TypeError, match=error_message):
        TypeValidator.validate_type_single(arg, arg_exp_type, optional)


def test_validate_type_single_none_optional() -> None:
    """Test TypeValidator.validate_type_single with None value when optional.

    :return: None
    :raises: None
    """
    try:
        TypeValidator.validate_type_single(None, int, True)
    except TypeError:
        pytest.fail(
            "validate_type_single raised TypeError unexpectedly for arg: None and type: int when optional is True"
        )


@pytest.mark.parametrize(
    "arg, arg_exp_type, optional",
    [
        (None, int, True),  # None value when optional is True
        (None, str, True),  # None value with a different type when optional is True
        ([], list, True),  # Empty list when optional is True
        (set(), set, True),  # Empty set when optional is True
        ({}, dict, True),  # Empty dict when optional is True
    ],
)
def test_validate_type_single_optional_cases(arg: Any, arg_exp_type: type, optional: bool) -> None:
    """Test TypeValidator.validate_type_single with optional cases.

    :param arg: The argument to check.
    :param arg_exp_type: The expected type of the argument.
    :param optional: Whether the argument is optional.
    :return: None
    :raises: None
    """
    try:
        TypeValidator.validate_type_single(arg, arg_exp_type, optional)
    except TypeError:
        pytest.fail(f"validate_type_single raised TypeError unexpectedly for arg: {arg} and type: {arg_exp_type}")


@pytest.mark.parametrize(
    "arg, arg_exp_type, optional, error_message",
    [
        ("", int, False, re.escape("Invalid argument with value ''. Expected 'int', but got 'str'.")),  # Empty string
        ([], int, False, re.escape("Invalid argument with value '[]'. Expected 'int', but got 'list'.")),  # Empty list
        ({}, int, False, re.escape("Invalid argument with value '{}'. Expected 'int', but got 'dict'.")),  # Empty dict
        (
            set(),
            int,
            False,
            re.escape("Invalid argument with value 'set()'. Expected 'int', but got 'set'."),
        ),  # Empty set
        (
            (),
            int,
            False,
            re.escape("Invalid argument with value '()'. Expected 'int', but got 'tuple'."),
        ),  # Empty tuple
        (
            b"bytes",
            str,
            False,
            re.escape("Invalid argument with value 'b'bytes''. Expected 'str', but got 'bytes'."),
        ),  # Bytes
    ],
)
def test_validate_type_single_additional_invalid_cases(
    arg: Any, arg_exp_type: type, optional: bool, error_message: str
) -> None:
    """Test TypeValidator.validate_type_single with additional invalid cases.

    :param arg: The argument to check.
    :param arg_exp_type: The expected type of the argument.
    :param optional: Whether the argument is optional.
    :param error_message: The expected error message.
    :return: None
    :raises TypeError: If the argument does not match the expected type.
    """
    with pytest.raises(TypeError, match=error_message):
        TypeValidator.validate_type_single(arg, arg_exp_type, optional)
