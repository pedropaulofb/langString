import re

import pytest
from langstring import Converter


@pytest.mark.parametrize(
    "string, separator, expected_text, expected_lang",
    [
        ("Hello@World", "@", "Hello", "World"),
        ("Bonjour le monde@fr", "@", "Bonjour le monde", "fr"),
        ("Hola Mundo@es", "@", "Hola Mundo", "es"),
        ("No separator here", "@", "No separator here", ""),
        ("Multiple@@separators@here@en", "@", "Multiple@@separators@here", "en"),
        ("No separator", "-", "No separator", ""),
        ("Separator at end@", "@", "Separator at end", ""),
        ("@Separator at start", "@", "", "Separator at start"),
        ("Special!@Chars", "@", "Special!", "Chars"),
        ("With space @ separator", "@", "With space ", " separator"),
        ("Multiple @ separators @ here", "@", "Multiple @ separators ", " here"),
        ("Japanese@こんにちは", "@", "Japanese", "こんにちは"),
        ("Russian@Привет", "@", "Russian", "Привет"),
        ("Greek@Γειά", "@", "Greek", "Γειά"),
        ("Emoji@😊", "@", "Emoji", "😊"),
        ("Empty@", "@", "Empty", ""),
        ("@Empty", "@", "", "Empty"),
        ("@@", "@", "@", ""),
        ("Hello World", " ", "Hello", "World"),  # Single space separator
        ("longstringwithnoseparator", "@", "longstringwithnoseparator", ""),  # Long string with no separators
        ("", "@", "", ""),  # Empty string
        ("@", "@", "", ""),  # Only separator
        ("@@@", "@", "@@", ""),  # Multiple separators only
        ("Hello@@@", "@", "Hello@@", ""),  # Multiple separators at end
        ("@@@Hello", "@", "@@", "Hello"),  # Multiple separators at start
        ("Hello@World@", "@", "Hello@World", ""),  # Separator at end
        ("@Hello@World", "@", "@Hello", "World"),  # Separator at start
        ("@Hello@World@", "@", "@Hello@World", ""),  # Separator at start and end
        ("Mixed separators @ and @@ here", "@", "Mixed separators @ and @", " here"),  # Mixed separators
        ("  @space at start", "@", "  ", "space at start"),  # Spaces at start
        ("space at end@  ", "@", "space at end", "  "),  # Spaces at end
        ("space @ in@side", "@", "space @ in", "side"),  # Spaces inside
        ("special chars!@#$%^&*()_", "@", "special chars!", "#$%^&*()_"),  # Special characters
        ("MixedCharset@Κόσμε", "@", "MixedCharset", "Κόσμε"),  # Mixed charset
        ("Hello World!@en-US", "@", "Hello World!", "en-US"),  # Language with region code
        # New test cases for additional coverage
        ("Mixed CASE@text", "@", "Mixed CASE", "text"),  # Mixed case
        ("Special@#&*Characters", "@", "Special", "#&*Characters"),  # Special characters in separator
        ("Emoji@😊😊😊", "@", "Emoji", "😊😊😊"),  # Multiple emojis
        # Explicitly testing empty separator
        ("Hello World", "", "Hello World", ""),  # Empty separator case
    ],
)
def test_from_string_to_langstring_parse(string: str, separator: str, expected_text: str, expected_lang: str):
    """Test the from_string_to_langstring_parse method with various inputs.

    :param string: The input text to be converted.
    :param separator: The separator used to split the text and language.
    :param expected_text: The expected text in the LangString.
    :param expected_lang: The expected language code in the LangString.
    :return: None
    """
    result = Converter.from_string_to_langstring_parse(string, separator)
    assert result.text == expected_text, f"Expected text '{expected_text}', but got '{result.text}'"
    assert result.lang == expected_lang, f"Expected language '{expected_lang}', but got '{result.lang}'"


@pytest.mark.parametrize(
    "string, separator, expected_exception, match",
    [
        (
            123,
            "@",
            TypeError,
            "Invalid argument with value '123'. Expected 'str', but got 'int'.",
        ),  # Invalid string type
        (
            "Hello@World",
            123,
            TypeError,
            "Invalid argument with value '123'. Expected 'str', but got 'int'.",
        ),  # Invalid separator type
        (
            "Hello@World",
            None,
            TypeError,
            "Invalid argument with value 'None'. Expected 'str', but got 'NoneType'.",
        ),  # None separator
        (
            None,
            "@",
            TypeError,
            "Invalid argument with value 'None'. Expected 'str', but got 'NoneType'.",
        ),  # None string
        (
            [],
            "@",
            TypeError,
            re.escape("Invalid argument with value '[]'. Expected 'str', but got 'list'."),
        ),  # List as string
        (
            set(),
            "@",
            TypeError,
            re.escape("Invalid argument with value 'set()'. Expected 'str', but got 'set'."),
        ),  # Set as string
        (
            "Hello@World",
            [],
            TypeError,
            re.escape("Invalid argument with value '[]'. Expected 'str', but got 'list'."),
        ),  # List as separator
        (
            "Hello@World",
            set(),
            TypeError,
            re.escape("Invalid argument with value 'set()'. Expected 'str', but got 'set'."),
        ),  # Set as separator
        (
            "",
            123,
            TypeError,
            "Invalid argument with value '123'. Expected 'str', but got 'int'.",
        ),  # Empty string with invalid separator type
    ],
)
def test_from_string_to_langstring_parse_invalid_inputs(string, separator, expected_exception, match):
    """Test the from_string_to_langstring_parse method with invalid inputs.

    :param string: The input text to be converted.
    :param separator: The separator used to split the text and language.
    :param expected_exception: The expected exception to be raised.
    :param match: The expected exception message.
    :raises expected_exception: If the input types are incorrect.
    :return: None
    """
    with pytest.raises(expected_exception, match=match):
        Converter.from_string_to_langstring_parse(string, separator)
