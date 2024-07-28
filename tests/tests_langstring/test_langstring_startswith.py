import pytest
from langstring import LangString


@pytest.mark.parametrize(
    "invalid_prefix",
    [
        123,  # Integer
        True,  # Boolean
        123.45,  # Float (Real number)
        ["list"],  # List
        {"set"},  # Set
        {"key": "value"},  # Dictionary
    ],
)
def test_startswith_invalid_type(invalid_prefix) -> None:
    """
    Test the `startswith` method with various invalid types for the prefix.

    :param invalid_prefix: An invalid prefix of various types.
    :return: None
    """
    lang_string = LangString("Hello, World!", "en")
    with pytest.raises(TypeError, match="startswith first arg must be str or a tuple of str"):
        lang_string.startswith(invalid_prefix)


@pytest.mark.parametrize(
    "text, prefix, start, end, expected",
    [
        ("Hello, World!", "Hello", None, None, True),
        ("Hello, World!", "World", None, None, False),
        ("Hello, World!", ("Hello", "World"), None, None, True),
        ("Hello, World!", "lo, W", 3, 8, True),
        ("Hello, World!", "Hello", 0, 5, True),
        ("", "World", None, None, False),
        ("Hello, World!", "", 10, 20, True),
        ("", "", None, None, True),  # Testing empty string with empty prefix
        ("Hello, World!", "Hello, World!", None, None, True),  # Prefix is the entire string
        ("Hello", "Hello, World!", None, None, False),  # Longer prefix than string
        ("Hello, World!", "World", None, None, False),  # Prefix at the end
        (" Hello, World!", " ", None, None, True),  # Prefix with whitespace
        ("@#$Special", "@#$", None, None, True),  # Prefix with special characters
    ],
)
def test_startswith_variations(text: str, prefix, start, end, expected: bool) -> None:
    """
    Test the `startswith` method with various combinations of prefixes and string ranges.

    :param text: The text of the LangString.
    :param prefix: The prefix to check.
    :param start: The starting index.
    :param end: The ending index.
    :param expected: The expected result.
    :return: None
    """
    lang_string = LangString(text, "en")
    if start is None and end is None:
        assert lang_string.startswith(prefix) == expected
    else:
        assert lang_string.startswith(prefix, start, end) == expected


@pytest.mark.parametrize(
    "invalid_prefix_tuple",
    [
        ("valid", 123),  # Tuple with a string and an integer
        ("valid", True),  # Tuple with a string and a boolean
        ("valid", 123.45),  # Tuple with a string and a float
        ("valid", ["list"]),  # Tuple with a string and a list
        ("valid", {"set"}),  # Tuple with a string and a set
        ("valid", {"key": "value"}),  # Tuple with a string and a dictionary
        (123, "valid"),  # Tuple with an integer and a string
        (True, "valid"),  # Tuple with a boolean and a string
        (123.45, "valid"),  # Tuple with a float and a string
        (["list"], "valid"),  # Tuple with a list and a string
        ({"set"}, "valid"),  # Tuple with a set and a string
        ({"key": "value"}, "valid"),  # Tuple with a dictionary and a string
        (123, 456),  # Tuple with two integers
        (True, False),  # Tuple with two booleans
        ([], {}),  # Tuple with a list and a dictionary
    ],
)
def test_startswith_invalid_tuple_elements(invalid_prefix_tuple) -> None:
    """
    Test the `startswith` method with tuples containing invalid values.

    :param invalid_prefix_tuple: A tuple containing invalid prefix elements.
    :return: None
    """
    lang_string = LangString("Hello, World!", "en")
    with pytest.raises(TypeError, match="tuple for startswith must only contain str, not"):
        lang_string.startswith(invalid_prefix_tuple)
