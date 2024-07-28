from typing import Optional

import pytest
from langstring import Converter


@pytest.mark.parametrize(
    "input_string, method, lang, separator, expected_text, expected_lang",
    [
        # Existing cases
        ("Hello, World!", "manual", "en", "@", "Hello, World!", "en"),
        ("Bonjour le monde!", "manual", "fr", "@", "Bonjour le monde!", "fr"),
        ("Hello@World", "parse", None, "@", "Hello", "World"),
        ("Bonjour le monde@fr", "parse", None, "@", "Bonjour le monde", "fr"),
        ("", "manual", "en", "@", "", "en"),
        ("", "parse", None, "@", "", ""),
        ("NoSeparatorHere", "parse", None, "@", "NoSeparatorHere", ""),
        ("@", "parse", None, "@", "", ""),
        ("@lang", "parse", None, "@", "", "lang"),
        ("text@", "parse", None, "@", "text", ""),
        ("text@lang@extra", "parse", None, "@", "text@lang", "extra"),
        # New cases to add
        ("MixedCASEtext", "manual", "en", "@", "MixedCASEtext", "en"),  # Mixed case
        (" mixed spaces ", "manual", "en", "@", " mixed spaces ", "en"),  # Spaces around
        ("text_with_underscores", "manual", "en", "@", "text_with_underscores", "en"),  # Underscores
        ("special-characters!$&", "manual", "en", "@", "special-characters!$&", "en"),  # Special characters
        ("multi lingual 你好 мир", "manual", "en", "@", "multi lingual 你好 мир", "en"),  # Multi-lingual
        ("emoji 😊 text", "manual", "en", "@", "emoji 😊 text", "en"),  # Emojis
        ("   leading and trailing spaces   ", "manual", "en", "@", "   leading and trailing spaces   ", "en"),
        # Leading and trailing spaces
        ("Hello@World", "parse", None, "#", "Hello@World", ""),  # Separator not in string
        ("Separator test", "parse", None, " ", "Separator", "test"),  # Space separator
    ],
)
def test_from_string_to_langstring(
    input_string: str, method: str, lang: Optional[str], separator: str, expected_text: str, expected_lang: str
):
    """Test the from_string_to_langstring method with various inputs.

    :param input_string: The text to be converted.
    :param method: The method to use for conversion ('manual' or 'parse').
    :param lang: The language code (used only with 'manual' method).
    :param separator: The separator used to split the text and language (used only with 'parse' method).
    :param expected_text: The expected text in the LangString.
    :param expected_lang: The expected language code in the LangString.
    :return: None
    """
    result = Converter.from_string_to_langstring(method, input_string, lang, separator)
    assert result.text == expected_text, f"Expected text '{expected_text}', but got '{result.text}'"
    assert result.lang == expected_lang, f"Expected language '{expected_lang}', but got '{result.lang}'"


@pytest.mark.parametrize(
    "input_string, method, lang, separator, expected_exception, match",
    [
        # Existing cases
        (
            "Hello, World!",
            "unknown_method",
            None,
            "@",
            ValueError,
            "Unknown method: unknown_method. Valid methods are 'manual' and 'parse'.",
        ),
        (123, "manual", None, "@", TypeError, "Invalid argument with value '123'. Expected 'str', but got 'int'."),
        (
            "Hello, World!",
            123,
            None,
            "@",
            TypeError,
            "Invalid argument with value '123'. Expected 'str', but got 'int'.",
        ),
        (
            "Hello, World!",
            "manual",
            123,
            "@",
            TypeError,
            "Invalid argument with value '123'. Expected 'str', but got 'int'.",
        ),
        (
            "Hello, World!",
            "parse",
            None,
            123,
            TypeError,
            "Invalid argument with value '123'. Expected 'str', but got 'int'.",
        ),
        (
            "Hello, World!",
            "manual",
            None,
            123,
            TypeError,
            "Invalid argument with value '123'. Expected 'str', but got 'int'.",
        ),
        # New cases to add
        (
            "Hello, World!",
            "manual",
            "en",
            123,
            TypeError,
            "Invalid argument with value '123'. Expected 'str', but got 'int'.",
        ),
        ("", "", None, "", ValueError, "Unknown method: . Valid methods are 'manual' and 'parse'."),
    ],
)
def test_from_string_to_langstring_exceptions(input_string, method, lang, separator, expected_exception, match):
    """Test the from_string_to_langstring method for expected exceptions.

    :param input_string: The text to be converted.
    :param method: The method to use for conversion ('manual' or 'parse').
    :param lang: The language code (used only with 'manual' method).
    :param separator: The separator used to split the text and language (used only with 'parse' method).
    :param expected_exception: The expected exception to be raised.
    :param match: The expected exception message.
    :raises expected_exception: If the input types or method are incorrect.
    :return: None
    """
    with pytest.raises(expected_exception, match=match):
        Converter.from_string_to_langstring(method, input_string, lang, separator)
