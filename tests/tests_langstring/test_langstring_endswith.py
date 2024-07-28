import pytest
from langstring import LangString


@pytest.mark.parametrize(
    "invalid_suffix",
    [
        123,  # Integer
        True,  # Boolean
        123.45,  # Float (Real number)
        ["list"],  # List
        {"set"},  # Set
        {"key": "value"},  # Dictionary
    ],
)
def test_endswith_invalid_type(invalid_suffix) -> None:
    """
    Test the `endswith` method with various invalid types for the suffix.

    :param invalid_suffix: An invalid suffix of various types.
    :return: None
    """
    lang_string = LangString("Hello, World!", "en")
    with pytest.raises(TypeError, match="endswith first arg must be str or a tuple of str"):
        lang_string.endswith(invalid_suffix)


@pytest.mark.parametrize(
    "text, suffix, start, end, expected",
    [
        ("Hello, World!", "World!", None, None, True),
        ("Hello, World!", "Hello", None, None, False),
        ("Hello, World!", ("World!", "Hello"), None, None, True),
        ("Hello, World!", "lo, W", 3, 8, True),
        ("Hello, World!", "World", 0, 5, False),
        ("", "World", None, None, False),
        ("Hello, World!", "", 10, 20, True),
        ("", "", None, None, True),  # Testing empty string with empty suffix
        ("Hello, World!", "Hello, World!", None, None, True),  # Suffix is the entire string
        ("Hello", "Hello, World!", None, None, False),  # Longer suffix than string
        ("Hello, World!", "Hello", None, None, False),  # Suffix at the start
        ("Hello, World! ", " ", None, None, True),  # Suffix with whitespace
        ("Special@#$", "@#$", None, None, True),  # Suffix with special characters
    ],
)
def test_endswith_variations(text: str, suffix, start, end, expected: bool) -> None:
    """
    Test the `endswith` method with various combinations of suffixes and string ranges.

    :param text: The text of the LangString.
    :param suffix: The suffix to check.
    :param start: The starting index.
    :param end: The ending index.
    :param expected: The expected result.
    :return: None
    """
    lang_string = LangString(text, "en")
    if start is None and end is None:
        assert lang_string.endswith(suffix) == expected
    else:
        assert lang_string.endswith(suffix, start, end) == expected


@pytest.mark.parametrize(
    "invalid_suffix_tuple",
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
def test_endswith_invalid_tuple_elements(invalid_suffix_tuple) -> None:
    """
    Test the `endswith` method with tuples containing invalid values.

    :param invalid_suffix_tuple: A tuple containing invalid suffix elements.
    :return: None
    """
    lang_string = LangString("Hello, World!", "en")
    with pytest.raises(TypeError, match="tuple for endswith must only contain str, not"):
        lang_string.endswith(invalid_suffix_tuple)
