import re
from functools import wraps
from typing import Any
from typing import Callable
from typing import Optional
from typing import Union

import pytest
from langstring.utils.validators import TypeValidator


@pytest.mark.parametrize(
    "arg, hint, expected",
    [
        (1, int, True),
        ("test", str, True),
        (3.14, float, True),
        (True, bool, True),
        (None, Optional[int], True),
        (None, int, False),
        # Additional cases
        ("", str, True),  # Empty string
        ("   ", str, True),  # String with spaces
        ("Test", str, True),  # Capitalized string
        ("TEST", str, True),  # Uppercase string
        ("TeSt", str, True),  # Mixed case string
        ("тест", str, True),  # Cyrillic string
        ("δοκιμή", str, True),  # Greek string
        ("😀", str, True),  # Emoji
        ("test!", str, True),  # String with special character
        ([], list, True),  # Empty list
        ([""], list, True),  # List with empty string
        (["test"], list, True),  # List with one string
        (["test", ""], list, True),  # List with string and empty string
        ("test\ttest", str, True),  # String with tab character
        ("test\ntest", str, True),  # String with newline character
    ],
)
def test_check_arg_valid_cases(arg: Any, hint: type, expected: bool) -> None:
    """Test TypeValidator._check_arg with valid cases.

    :param arg: The argument to check.
    :param hint: The type hint to check against.
    :param expected: The expected result.
    :return: None
    :raises: None
    """
    try:
        result = TypeValidator._check_arg(arg, hint)
        assert result == expected, f"Expected {expected} but got {result} for arg: {arg} and hint: {hint}"
    except TypeError:
        assert not expected, f"Expected {expected} but got a TypeError for arg: {arg} and hint: {hint}"


def test_validate_type_decorator_with_valid_types() -> None:
    """Test Validator.validate_type_decorator with valid argument types.

    :return: None
    :raises: None
    """

    @TypeValidator.validate_type_decorator
    def func(a: int, _: str) -> None:
        pass

    try:
        func(1, "test")
    except TypeError:
        pytest.fail("validate_type_decorator raised TypeError unexpectedly!")


@pytest.mark.parametrize(
    "args, kwargs, match",
    [
        ((1,), {"b": "test"}, None),
        ((1,), {"b": 2}, "Expected 'str', but got 'int'"),
        ((1.0,), {"b": "test"}, "Expected 'int', but got 'float'"),
        # Additional cases
        ((1,), {"b": ""}, None),  # Empty string
        ((1,), {"b": "   "}, None),  # String with spaces
        ((1,), {"b": "Test"}, None),  # Capitalized string
        ((1,), {"b": "TEST"}, None),  # Uppercase string
        ((1,), {"b": "TeSt"}, None),  # Mixed case string
        ((1,), {"b": "тест"}, None),  # Cyrillic string
        ((1,), {"b": "δοκιμή"}, None),  # Greek string
        ((1,), {"b": "😀"}, None),  # Emoji
        ((1,), {"b": "test!"}, None),  # String with special character
        ((1,), {"b": ["test", 1]}, "Expected 'str', but got 'list'"),  # List with mixed types
        ((1,), {"b": "test\ttest"}, None),  # String with tab character
        ((1,), {"b": "test\ntest"}, None),  # String with newline character
        ((1,), {"b": {"key": "value"}}, "Expected 'str', but got 'dict'"),  # Invalid type with dictionary
        ((1,), {"b": "test"}, None),
        ((1,), {"b": 2}, "Expected 'str', but got 'int'"),
        ((1.0,), {"b": "test"}, "Expected 'int', but got 'float'"),
        # Additional cases
        ((1,), {"b": ""}, None),  # Empty string
        ((1,), {"b": "   "}, None),  # String with spaces
        ((1,), {"b": "Test"}, None),  # Capitalized string
        ((1,), {"b": "TEST"}, None),  # Uppercase string
        ((1,), {"b": "TeSt"}, None),  # Mixed case string
        ((1,), {"b": "тест"}, None),  # Cyrillic string
        ((1,), {"b": "δοκιμή"}, None),  # Greek string
        ((1,), {"b": "😀"}, None),  # Emoji
        ((1,), {"b": "test!"}, None),  # String with special character
        ((1,), {"b": ["test", 1]}, "Expected 'str', but got 'list'"),  # List with mixed types
        ((1,), {"b": "test\ttest"}, None),  # String with tab character
        ((1,), {"b": "test\ntest"}, None),  # String with newline character
        ((1,), {"b": {"key": "value"}}, "Expected 'str', but got 'dict'"),  # Invalid type with dictionary
    ],
)
def test_validate_type_decorator_with_invalid_types(args: tuple, kwargs: dict, match: Optional[str]) -> None:
    """Test Validator.validate_type_decorator with invalid argument types.

    :param args: The positional arguments to pass to the function.
    :param kwargs: The keyword arguments to pass to the function.
    :param match: The expected error message.
    :return: None
    :raises: TypeError: If the argument types do not match the type hints.
    """

    @TypeValidator.validate_type_decorator
    def func(a: int, b: str) -> None:  # noqa: Vulture
        pass

    if match:
        with pytest.raises(TypeError, match=match):
            func(*args, **kwargs)
    else:
        try:
            func(*args, **kwargs)
        except TypeError:
            pytest.fail("validate_type_decorator raised TypeError unexpectedly!")


def test_validate_type_decorator_instance_method() -> None:
    """Test Validator.validate_type_decorator on an instance method.

    :return: None
    :raises: None
    """

    class TestClass:
        @TypeValidator.validate_type_decorator
        def instance_method(self, a: int, _: str) -> None:
            pass

    instance = TestClass()
    try:
        instance.instance_method(1, "test")
    except TypeError:
        pytest.fail("validate_type_decorator raised TypeError unexpectedly on instance method!")


def test_validate_type_decorator_with_default_values() -> None:
    """Test Validator.validate_type_decorator with default argument values.

    :return: None
    :raises: None
    """

    @TypeValidator.validate_type_decorator
    def func(a: int = 1, _: str = "default") -> None:
        pass

    try:
        func()
        func(2)
        func(3, "test")
    except TypeError:
        pytest.fail("validate_type_decorator raised TypeError unexpectedly with default values!")


def test_validate_type_decorator_with_empty_values() -> None:
    """Test Validator.validate_type_decorator with empty values.

    :return: None
    :raises: None
    """

    @TypeValidator.validate_type_decorator
    def func(a: list[int]) -> None:
        pass

    try:
        func([])
    except TypeError:
        pytest.fail("validate_type_decorator raised TypeError unexpectedly with empty values!")


def test_validate_type_decorator_with_null_values() -> None:
    """Test Validator.validate_type_decorator with null values.

    :return: None
    :raises: None
    """

    @TypeValidator.validate_type_decorator
    def func(a: Optional[int]) -> None:
        pass

    try:
        func(None)
    except TypeError:
        pytest.fail("validate_type_decorator raised TypeError unexpectedly with null values!")


def test_validate_type_decorator_with_optional_arguments() -> None:
    """Test Validator.validate_type_decorator with optional arguments.

    :return: None
    :raises: None
    """

    @TypeValidator.validate_type_decorator
    def func(a: int, _: Optional[str] = None) -> None:
        pass

    try:
        func(1)
        func(1, "test")
        func(1, None)
    except TypeError:
        pytest.fail("validate_type_decorator raised TypeError unexpectedly with optional arguments!")


def test_validate_type_decorator_with_keyword_arguments() -> None:
    """Test Validator.validate_type_decorator with keyword arguments.

    :return: None
    :raises: None
    """

    @TypeValidator.validate_type_decorator
    def func(a: int, b: str) -> None:  # noqa: Vulture
        pass

    try:
        func(a=1, b="test")
    except TypeError:
        pytest.fail("validate_type_decorator raised TypeError unexpectedly with keyword arguments!")


def test_validate_type_decorator_with_unusual_but_valid_usage() -> None:
    """Test Validator.validate_type_decorator with unusual but valid usage.

    :return: None
    :raises: None
    """

    @TypeValidator.validate_type_decorator
    def func(a: int, _: str = "test") -> None:
        pass

    try:
        func(1)
        func(1, "example")
    except TypeError:
        pytest.fail("validate_type_decorator raised TypeError unexpectedly with unusual but valid usage!")


def test_validate_type_decorator_with_nested_decorators() -> None:
    """Test Validator.validate_type_decorator with nested decorators.

    :return: None
    :raises: None
    """

    def example_decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return func(*args, **kwargs)

        return wrapper

    @example_decorator
    @TypeValidator.validate_type_decorator
    def func(a: int, _: str) -> None:
        pass

    try:
        func(1, "test")
    except TypeError:
        pytest.fail("validate_type_decorator raised TypeError unexpectedly with nested decorators!")


@pytest.mark.parametrize(
    "arg, hint, expected, error_message",
    [
        (
            [1, "test"],
            list[int],
            False,
            re.escape("Invalid item with value 'test' in 'list'. Expected one of 'int', but got 'str'."),
        ),
        (
            [{"key": "value"}, 1],
            list[dict],
            False,
            re.escape("Invalid item with value '1' in 'list'. Expected one of 'dict', but got 'int'."),
        ),
    ],
)
def test_check_arg_with_parametrized_generics(
    arg: Any, hint: type, expected: bool, error_message: Optional[str]
) -> None:
    """Test TypeValidator._check_arg with parameterized generics and invalid items.

    :param arg: The argument to check.
    :param hint: The type hint to check against.
    :param expected: The expected result.
    :param error_message: The expected error message if a TypeError is raised.
    :return: None
    :raises: None
    """
    if expected:
        try:
            result = TypeValidator._check_arg(arg, hint)
            assert result == expected, f"Expected {expected} but got {result} for arg: {arg} and hint: {hint}"
        except TypeError:
            assert not expected, f"Expected {expected} but got a TypeError for arg: {arg} and hint: {hint}"
    else:
        with pytest.raises(TypeError, match=error_message):
            TypeValidator._check_arg(arg, hint)


def test_validate_type_decorator_invalid_positional_arg() -> None:
    """Test Validator.validate_type_decorator with invalid positional argument types.

    :return: None
    :raises: None
    """

    @TypeValidator.validate_type_decorator
    def func(a: int, _: str) -> None:
        pass

    with pytest.raises(TypeError, match="Invalid argument with value 'test'. Expected 'int', but got 'str'."):
        func("test", "valid")


def test_validate_type_decorator_invalid_keyword_arg() -> None:
    """Test Validator.validate_type_decorator with invalid keyword argument types.

    :return: None
    :raises: None
    """

    @TypeValidator.validate_type_decorator
    def func(a: int, b: str) -> None:  # noqa: Vulture
        pass

    with pytest.raises(TypeError, match="Invalid argument with value '2'. Expected 'str', but got 'int'."):
        func(1, b=2)


def test_validate_type_decorator_invalid_positional_and_keyword_arg() -> None:
    """Test Validator.validate_type_decorator with both invalid positional and keyword argument types.

    :return: None
    :raises: None
    """

    @TypeValidator.validate_type_decorator
    def func(a: int, _: str) -> None:
        pass

    with pytest.raises(TypeError, match="Invalid argument with value 'test'. Expected 'int', but got 'str'."):
        func("test", b=2)


def test_validate_type_decorator_invalid_default_arg() -> None:
    """Test Validator.validate_type_decorator with invalid default argument types.

    :return: None
    :raises: None
    """

    @TypeValidator.validate_type_decorator
    def func(a: int = 1, _: str = "default") -> None:
        pass

    with pytest.raises(TypeError, match="Invalid argument with value '2'. Expected 'str', but got 'int'."):
        func(1, 2)


def test_validate_type_decorator_invalid_list_arg() -> None:
    """Test Validator.validate_type_decorator with invalid list argument types.

    :return: None
    :raises: None
    """

    @TypeValidator.validate_type_decorator
    def func(a: list[int]) -> None:
        pass

    with pytest.raises(
        TypeError, match="Invalid item with value 'test' in 'list'. Expected one of 'int', but got 'str'."
    ):
        func([1, 2, "test"])


def test_validate_type_decorator_invalid_dict_arg() -> None:
    """Test Validator.validate_type_decorator with invalid dictionary argument types.

    :return: None
    :raises: None
    """

    @TypeValidator.validate_type_decorator
    def func(a: dict[str, int]) -> None:
        pass

    with pytest.raises(TypeError, match="Invalid argument with value '1'. Expected 'str', but got 'int'."):
        func({1: 1})


def test_validate_type_decorator_invalid_optional_arg() -> None:
    """Test Validator.validate_type_decorator with invalid optional argument types.

    :return: None
    :raises: None
    """

    @TypeValidator.validate_type_decorator
    def func(a: Optional[int] = None) -> None:
        pass

    with pytest.raises(
        TypeError, match="Invalid argument with value 'test'. Expected one of 'int' or 'NoneType', but got 'str'."
    ):
        func("test")


def test_validate_type_decorator_invalid_dict_value_arg() -> None:
    """Test Validator.validate_type_decorator with invalid dictionary value types.

    :return: None
    :raises: None
    """

    @TypeValidator.validate_type_decorator
    def func(a: dict[str, int]) -> None:
        pass

    with pytest.raises(TypeError, match="Invalid argument with value 'test'. Expected 'int', but got 'str'."):
        func({"key": "test"})


def test_validate_type_decorator_invalid_mixed_list_arg() -> None:
    """Test Validator.validate_type_decorator with a list containing mixed invalid argument types.

    :return: None
    :raises: None
    """

    @TypeValidator.validate_type_decorator
    def func(a: list[int]) -> None:
        pass

    with pytest.raises(
        TypeError, match="Invalid item with value 'test' in 'list'. Expected one of 'int', but got 'str'."
    ):
        func([1, 2, "test"])


def test_validate_type_decorator_invalid_union_arg() -> None:
    """Test Validator.validate_type_decorator with invalid Union type argument.

    :return: None
    :raises: None
    """

    @TypeValidator.validate_type_decorator
    def func(a: Union[int, str]) -> None:
        pass

    with pytest.raises(
        TypeError, match="Invalid argument with value '\[1, 2, 3\]'. Expected one of 'int' or 'str', but got 'list'."
    ):
        func([1, 2, 3])


def test_validate_type_decorator_invalid_set_arg() -> None:
    """Test Validator.validate_type_decorator with invalid set argument types.

    :return: None
    :raises: None
    """

    @TypeValidator.validate_type_decorator
    def func(a: set[int]) -> None:
        pass

    with pytest.raises(
        TypeError, match="Invalid item with value 'test' in 'set'. Expected one of 'int', but got 'str'."
    ):
        func({1, 2, "test"})


def test_check_arg_invalid_origin_type() -> None:
    """Test TypeValidator._check_arg with an invalid origin type.

    This test ensures that a TypeError is raised when the argument type does not match the expected origin type.
    """
    with pytest.raises(
        TypeError, match="Invalid argument with value '\\[1, 2, 3\\]'. Expected 'dict', but got 'list'."
    ):
        TypeValidator._check_arg([1, 2, 3], dict[str, int])
