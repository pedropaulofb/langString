import re
from typing import Optional

import pytest
from langstring import Converter
from langstring import SetLangString


@pytest.mark.parametrize(
    "strings, lang, expected_texts, expected_lang",
    [
        # Existing cases
        (["Hello", "World"], "en", {"Hello", "World"}, "en"),
        (["Bonjour", "le", "monde"], "fr", {"Bonjour", "le", "monde"}, "fr"),
        (["Hola", "Mundo"], "", {"Hola", "Mundo"}, ""),  # Use empty string instead of None
        ([], "en", set(), "en"),  # Empty list
        ([""], "en", {""}, "en"),  # Empty string in list
        (["Only one string"], "en", {"Only one string"}, "en"),  # Single string
        # Edge cases with different charsets and special characters
        (["こんにちは", "世界"], "jp", {"こんにちは", "世界"}, "jp"),  # Japanese
        (["Привет", "мир"], "ru", {"Привет", "мир"}, "ru"),  # Russian
        (["Γειά", "σου", "κόσμε"], "el", {"Γειά", "σου", "κόσμε"}, "el"),  # Greek
        (["😊", "🌍"], "", {"😊", "🌍"}, ""),  # Emojis, use empty string instead of None
        (
            ["Special", "#&*Characters"],
            "",
            {"Special", "#&*Characters"},
            "",
        ),  # Special characters, use empty string instead of None
        # Additional edge cases
        (["MixedCharset", "Κόσμε"], "en", {"MixedCharset", "Κόσμε"}, "en"),  # Mixed charset
        (["With space", "separator"], "en", {"With space", "separator"}, "en"),  # Space in strings
        (["Multiple\nlines"], "en", {"Multiple\nlines"}, "en"),  # Newline in string
        (["Tab\tseparated"], "en", {"Tab\tseparated"}, "en"),  # Tab in string
        (["    Leading", "Trailing    "], "en", {"    Leading", "Trailing    "}, "en"),  # Leading and trailing spaces
        (["UpperCASE", "lowercase", "MiXeD"], "en", {"UpperCASE", "lowercase", "MiXeD"}, "en"),  # Case variations
        # New cases to cover more scenarios
        (["Hello", "WORLD"], "en", {"Hello", "WORLD"}, "en"),  # Mixed case within strings
        (["With,comma", "and.period."], "en", {"With,comma", "and.period."}, "en"),  # Strings with punctuation
        (["\n", "\t", " "], "en", {"\n", "\t", " "}, "en"),  # Strings with only whitespace characters
        (["null", "NULL"], "en", {"null", "NULL"}, "en"),  # Strings that could be mistaken for null values
        (["😊😊", "🌍🌍"], "en", {"😊😊", "🌍🌍"}, "en"),  # Repeated emojis
    ],
)
def test_from_strings_to_setlangstring(
    strings: list[str], lang: Optional[str], expected_texts: set[str], expected_lang: Optional[str]
) -> None:
    """Test the from_strings_to_setlangstring method with various inputs.

    :param strings: List of strings to be converted.
    :param lang: Language code for the 'manual' method.
    :param expected_texts: The expected texts in the SetLangString.
    :param expected_lang: The expected language code in the SetLangString.
    :return: None
    """
    result = Converter.from_strings_to_setlangstring(strings, lang)
    assert isinstance(result, SetLangString), "Expected result to be an instance of SetLangString"
    assert result.texts == expected_texts, f"Expected texts {expected_texts}, but got {result.texts}"
    assert result.lang == expected_lang, f"Expected language '{expected_lang}', but got '{result.lang}'"


@pytest.mark.parametrize(
    "strings, lang, expected_exception, match",
    [
        # Existing invalid cases
        (123, "en", TypeError, "Invalid argument with value '123'. Expected 'list', but got 'int'."),
        (["Hello", "World"], 123, TypeError, "Invalid argument with value '123'. Expected 'str', but got 'int'."),
        (
            ["Hello", "World"],
            [],
            TypeError,
            re.escape("Invalid argument with value '[]'. Expected 'str', but got 'list'."),
        ),
        (
            ["Hello", "World"],
            set(),
            TypeError,
            re.escape("Invalid argument with value 'set()'. Expected 'str', but got 'set'."),
        ),
        ([123, "World"], "en", TypeError, "Invalid argument with value '123'. Expected 'str', but got 'int'."),
        (["Hello", None], "en", TypeError, "Invalid argument with value 'None'. Expected 'str', but got 'NoneType'."),
        # Additional invalid cases
        (
            ["Hello", {}],
            "en",
            TypeError,
            re.escape("Invalid argument with value '{}'. Expected 'str', but got 'dict'."),
        ),
        (
            ["Hello", ["Nested"]],
            "en",
            TypeError,
            re.escape("Invalid argument with value '['Nested']'. Expected 'str', but got 'list'."),
        ),
        (
            ["Hello", set()],
            "en",
            TypeError,
            re.escape("Invalid argument with value 'set()'. Expected 'str', but got 'set'."),
        ),
        ([None], "en", TypeError, "Invalid argument with value 'None'. Expected 'str', but got 'NoneType'."),
    ],
)
def test_from_strings_to_setlangstring_exceptions(strings, lang, expected_exception, match) -> None:
    """Test the from_strings_to_setlangstring method for expected exceptions.

    :param strings: List of strings to be converted.
    :param lang: Language code for the 'manual' method.
    :param expected_exception: The expected exception to be raised.
    :param match: The expected exception message.
    :raises expected_exception: If the input types are incorrect.
    :return: None
    """
    with pytest.raises(expected_exception, match=match):
        Converter.from_strings_to_setlangstring(strings, lang)
