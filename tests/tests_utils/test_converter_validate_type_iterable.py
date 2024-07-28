import re
from typing import Any
from typing import Optional

import pytest
from langstring.utils.validators import TypeValidator


@pytest.mark.parametrize(
    "arg, arg_exp_type, arg_content_exp_type, optional",
    [
        ([], list, int, False),  # Empty list
        ([1, 2, 3], list, int, False),  # List with integers
        ([1.0, 2.0], list, float, False),  # List with floats
        (["a", "b", "c"], list, str, False),  # List with strings
        (set(), set, int, False),  # Empty set
        ({1, 2, 3}, set, int, False),  # Set with integers
        ({1.0, 2.0}, set, float, False),  # Set with floats
        (("a", "b"), tuple, str, False),  # Tuple with strings
        (None, list, int, True),  # None value when optional
        ([None], list, Optional[int], False),  # List with None value and Optional[int]
        ([], list, str, False),  # Empty list with string type check
        ([[]], list, list, False),  # Empty nested list
        ([{}, {}], list, dict, False),  # List of empty dicts
        ([{1: "a"}, {2: "b"}], list, dict, False),  # List of dicts
        (["", "test"], list, str, False),  # List with empty string and valid string
        (["    ", "\n"], list, str, False),  # List with whitespace strings
        (["😀", "😂"], list, str, False),  # List with emojis
        (["тест", "δοκιμή"], list, str, False),  # List with Cyrillic and Greek strings
        (["", " ", "   "], list, str, False),  # List with empty strings and spaces
        (["a", "A", "aA", "Aa"], list, str, False),  # List with mixed case strings
        (["a test", "test a"], list, str, False),  # List with strings containing spaces
        (["тест", "δοκιμή", "テスト"], list, str, False),  # List with Cyrillic, Greek, and Japanese strings
        (["😀", "😂", "👍"], list, str, False),  # List with multiple emojis
        (["test!", "test?", "test#"], list, str, False),  # List with strings containing special characters
        ([{"a", "b"}, {"c", "d"}, set()], list, set, False),
    ],
)
def test_validate_type_iterable_valid_cases(
    arg: Any, arg_exp_type: type, arg_content_exp_type: type, optional: bool
) -> None:
    """Test TypeValidator.validate_type_iterable with valid cases.

    :param arg: The iterable argument to check.
    :param arg_exp_type: The expected type of the iterable argument.
    :param arg_content_exp_type: The expected type of the elements within the iterable argument.
    :param optional: Whether the argument is optional.
    :return: None
    :raises: None
    """
    try:
        TypeValidator.validate_type_iterable(arg, arg_exp_type, arg_content_exp_type, optional)
    except TypeError:
        pytest.fail(
            f"validate_type_iterable raised TypeError unexpectedly for arg: {arg}, type: {arg_exp_type}, content type: {arg_content_exp_type}"
        )


@pytest.mark.parametrize(
    "arg, arg_exp_type, arg_content_exp_type, optional, error_message",
    [
        (1, list, int, False, re.escape("Invalid argument with value '1'. Expected 'list', but got 'int'.")),
        ("test", list, int, False, re.escape("Invalid argument with value 'test'. Expected 'list', but got 'str'.")),
        ([1, "2"], list, int, False, re.escape("Invalid argument with value '2'. Expected 'int', but got 'str'.")),
        (
            {"a": 1},
            list,
            int,
            False,
            re.escape("Invalid argument with value '{'a': 1}'. Expected 'list', but got 'dict'."),
        ),
        (None, list, int, False, re.escape("Invalid argument with value 'None'. Expected 'list', but got 'NoneType'.")),
        (
            [1, 2, 3],
            set,
            int,
            False,
            re.escape("Invalid argument with value '[1, 2, 3]'. Expected 'set', but got 'list'."),
        ),
        (
            [1.0, "2.0"],
            list,
            float,
            False,
            re.escape("Invalid argument with value '2.0'. Expected 'float', but got 'str'."),
        ),
        (["a", 1], list, str, False, re.escape("Invalid argument with value '1'. Expected 'str', but got 'int'.")),
        (set(), list, int, False, re.escape("Invalid argument with value 'set()'. Expected 'list', but got 'set'.")),
        ({1, 2, "3"}, set, int, False, re.escape("Invalid argument with value '3'. Expected 'int', but got 'str'.")),
        ((1, "b"), tuple, int, False, re.escape("Invalid argument with value 'b'. Expected 'int', but got 'str'.")),
        ([1, 2, 3], list, str, False, re.escape("Invalid argument with value '1'. Expected 'str', but got 'int'.")),
        ([1, "2", 3], list, int, False, re.escape("Invalid argument with value '2'. Expected 'int', but got 'str'.")),
        (["", 1], list, str, False, re.escape("Invalid argument with value '1'. Expected 'str', but got 'int'.")),
        (
            ["    ", 3.14],
            list,
            str,
            False,
            re.escape("Invalid argument with value '3.14'. Expected 'str', but got 'float'."),
        ),
        (["😀", 123], list, str, False, re.escape("Invalid argument with value '123'. Expected 'str', but got 'int'.")),
        (
            ["тест", 3.14],
            list,
            str,
            False,
            re.escape("Invalid argument with value '3.14'. Expected 'str', but got 'float'."),
        ),
        (None, list, int, False, re.escape("Invalid argument with value 'None'. Expected 'list', but got 'NoneType'.")),
        (
            [1, 2, None],
            list,
            int,
            False,
            re.escape("Invalid argument with value 'None'. Expected 'int', but got 'NoneType'."),
        ),
        (
            ["a", None, "c"],
            list,
            str,
            False,
            re.escape("Invalid argument with value 'None'. Expected 'str', but got 'NoneType'."),
        ),
        (["a", 1, "c"], list, str, False, re.escape("Invalid argument with value '1'. Expected 'str', but got 'int'.")),
        (
            ["a", "b", 3.14],
            list,
            str,
            False,
            re.escape("Invalid argument with value '3.14'. Expected 'str', but got 'float'."),
        ),
        (
            [{1: "a"}, {2: "b"}, []],
            list,
            dict,
            False,
            re.escape("Invalid argument with value '[]'. Expected 'dict', but got 'list'."),
        ),
    ],
)
def test_validate_type_iterable_invalid_cases(
    arg: Any, arg_exp_type: type, arg_content_exp_type: type, optional: bool, error_message: str
) -> None:
    """Test TypeValidator.validate_type_iterable with invalid cases.

    :param arg: The iterable argument to check.
    :param arg_exp_type: The expected type of the iterable argument.
    :param arg_content_exp_type: The expected type of the elements within the iterable argument.
    :param optional: Whether the argument is optional.
    :param error_message: The expected error message.
    :return: None
    :raises TypeError: If the argument does not match the expected type or if its contents do not match the expected type.
    """
    with pytest.raises(TypeError, match=error_message):
        TypeValidator.validate_type_iterable(arg, arg_exp_type, arg_content_exp_type, optional)


@pytest.mark.parametrize(
    "arg, arg_exp_type, arg_content_exp_type, optional",
    [
        ([[]], list, list, False),  # List with an empty list
        ([set()], list, set, False),  # List with an empty set
        ([{}], list, dict, False),  # List with an empty dict
        ([()], list, tuple, False),  # List with an empty tuple
        ([["a", "b"]], list, list, False),  # List with a list of strings
        ([{1, 2}], list, set, False),  # List with a set of integers
        ([{"key": "value"}], list, dict, False),  # List with a dict
        ([["a", 1]], list, list, False),
        ([["a", " ", "   "]], list, list, False),  # Nested list with strings containing spaces
        ([["тест", "δοκιμή", "テスト"]], list, list, False),  # Nested list with Cyrillic, Greek, and Japanese strings
        ([["😀", "😂", "👍"]], list, list, False),  # Nested list with emojis
        ([["test!", "test?", "test#"]], list, list, False),  # Nested list with strings containing special characters
    ],
)
def test_validate_type_iterable_nested_valid_cases(
    arg: Any, arg_exp_type: type, arg_content_exp_type: type, optional: bool
) -> None:
    """Test TypeValidator.validate_type_iterable with nested valid cases.

    :param arg: The iterable argument to check.
    :param arg_exp_type: The expected type of the iterable argument.
    :param arg_content_exp_type: The expected type of the elements within the iterable argument.
    :param optional: Whether the argument is optional.
    :return: None
    :raises: None
    """
    try:
        TypeValidator.validate_type_iterable(arg, arg_exp_type, arg_content_exp_type, optional)
    except TypeError:
        pytest.fail(
            f"validate_type_iterable raised TypeError unexpectedly for arg: {arg}, type: {arg_exp_type}, content type: {arg_content_exp_type}"
        )


@pytest.mark.parametrize(
    "arg, arg_exp_type, arg_content_exp_type, optional, error_message",
    [
        (
            [{1: "a"}],
            list,
            set,
            False,
            re.escape("Invalid argument with value '{1: 'a'}'. Expected 'set', but got 'dict'."),
        ),
        (
            [{"key": "value"}],
            list,
            list,
            False,
            re.escape("Invalid argument with value '{'key': 'value'}'. Expected 'list', but got 'dict'."),
        ),
        (
            [{1, 2}],
            list,
            dict,
            False,
            re.escape("Invalid argument with value '{1, 2}'. Expected 'dict', but got 'set'."),
        ),
        (
            [["a", 1]],
            list,
            str,
            False,
            re.escape("Invalid argument with value '['a', 1]'. Expected 'str', but got 'list'."),
        ),
        (
            [{"a": 1}, {2: "b"}],
            list,
            list,
            False,
            re.escape("Invalid argument with value '{'a': 1}'. Expected 'list', but got 'dict'."),
        ),
    ],
)
def test_validate_type_iterable_nested_invalid_cases(
    arg: Any, arg_exp_type: type, arg_content_exp_type: type, optional: bool, error_message: str
) -> None:
    """Test TypeValidator.validate_type_iterable with nested invalid cases.

    :param arg: The iterable argument to check.
    :param arg_exp_type: The expected type of the iterable argument.
    :param arg_content_exp_type: The expected type of the elements within the iterable argument.
    :param optional: Whether the argument is optional.
    :param error_message: The expected error message.
    :return: None
    :raises TypeError: If the argument does not match the expected type or if its contents do not match the expected type.
    """
    with pytest.raises(TypeError, match=error_message):
        TypeValidator.validate_type_iterable(arg, arg_exp_type, arg_content_exp_type, optional)
