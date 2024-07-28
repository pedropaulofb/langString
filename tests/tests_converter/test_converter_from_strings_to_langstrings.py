from typing import Optional

import pytest
from langstring import Converter


@pytest.mark.parametrize(
    "strings, method, lang, separator, expected_texts, expected_langs",
    [
        # Existing cases
        (["Hello, World!"], "manual", "en", "@", ["Hello, World!"], ["en"]),
        (["Bonjour le monde!"], "manual", "fr", "@", ["Bonjour le monde!"], ["fr"]),
        (
            ["Hello, World!", "Bonjour le monde!"],
            "manual",
            "en",
            "@",
            ["Hello, World!", "Bonjour le monde!"],
            ["en", "en"],
        ),
        (["Hello@World"], "parse", None, "@", ["Hello"], ["World"]),
        (["Bonjour le monde@fr"], "parse", None, "@", ["Bonjour le monde"], ["fr"]),
        (["Hello@World", "Bonjour le monde@fr"], "parse", None, "@", ["Hello", "Bonjour le monde"], ["World", "fr"]),
        ([], "manual", "en", "@", [], []),  # Empty list
        (["", "NoSeparatorHere", "@"], "parse", None, "@", ["", "NoSeparatorHere", ""], ["", "", ""]),
        (["text@lang@extra"], "parse", None, "@", ["text@lang"], ["extra"]),
        (["Hello, World!"], "parse", None, "", ["Hello, World!"], [""]),
        # New cases for additional coverage
        (
            [" Mixed CASE text ", " 123@abc "],
            "parse",
            None,
            "@",
            [" Mixed CASE text ", " 123"],
            ["", "abc "],
        ),  # Mixed case and whitespace
        (["1234@@", "@@@@"], "parse", None, "@", ["1234@", "@@@"], ["", ""]),  # Multiple @ signs
        (
            ["multi lingual 你好@世界", "пример@тест"],
            "parse",
            None,
            "@",
            ["multi lingual 你好", "пример"],
            ["世界", "тест"],
        ),  # Multi-lingual
        (
            ["Special!@#&*Characters", "Emoji@😊"],
            "parse",
            None,
            "@",
            ["Special!", "Emoji"],
            ["#&*Characters", "😊"],
        ),  # Special characters and emoji
        ([""], "manual", "en", "@", [""], ["en"]),  # Empty string with 'manual'
    ],
)
def test_from_strings_to_langstrings(
    strings: list[str],
    method: str,
    lang: Optional[str],
    separator: str,
    expected_texts: list[str],
    expected_langs: list[str],
) -> None:
    """Test the from_strings_to_langstrings method with various inputs.

    :param strings: List of strings to be converted.
    :param method: The method to use for conversion ('manual' or 'parse').
    :param lang: The language code for 'manual' method.
    :param separator: The separator used in 'parse' method.
    :param expected_texts: The expected texts in the list of LangString objects.
    :param expected_langs: The expected language codes in the list of LangString objects.
    :return: None
    """
    results = Converter.from_strings_to_langstrings(method, strings, lang, separator)
    for result, expected_text, expected_lang in zip(results, expected_texts, expected_langs):
        assert result.text == expected_text, f"Expected text '{expected_text}', but got '{result.text}'"
        assert result.lang == expected_lang, f"Expected language '{expected_lang}', but got '{result.lang}'"


@pytest.mark.parametrize(
    "strings, method, lang, separator, expected_exception, match",
    [
        # Existing cases
        (
            ["Hello, World!"],
            "unknown_method",
            None,
            "@",
            ValueError,
            "Unknown method: unknown_method. Valid methods are 'manual' and 'parse'.",
        ),
        (123, "manual", None, "@", TypeError, "Invalid argument with value '123'. Expected 'list', but got 'int'."),
        (
            ["Hello, World!"],
            123,
            None,
            "@",
            TypeError,
            "Invalid argument with value '123'. Expected 'str', but got 'int'.",
        ),
        (
            ["Hello, World!"],
            "manual",
            123,
            "@",
            TypeError,
            "Invalid argument with value '123'. Expected 'str', but got 'int'.",
        ),
        (
            ["Hello, World!"],
            "parse",
            None,
            123,
            TypeError,
            "Invalid argument with value '123'. Expected 'str', but got 'int'.",
        ),
        (
            ["Hello, World!"],
            "manual",
            None,
            123,
            TypeError,
            "Invalid argument with value '123'. Expected 'str', but got 'int'.",
        ),
        (
            ["Hello, World!", 123],
            "manual",
            "en",
            "@",
            TypeError,
            "Invalid argument with value '123'. Expected 'str', but got 'int'.",
        ),
        ([""], "", None, "", ValueError, "Unknown method: . Valid methods are 'manual' and 'parse'."),
    ],
)
def test_from_strings_to_langstrings_exceptions(strings, method, lang, separator, expected_exception, match) -> None:
    """Test the from_strings_to_langstrings method for expected exceptions.

    :param strings: List of strings to be converted.
    :param method: The method to use for conversion ('manual' or 'parse').
    :param lang: The language code for 'manual' method.
    :param separator: The separator used in 'parse' method.
    :param expected_exception: The expected exception to be raised.
    :param match: The expected exception message.
    :raises expected_exception: If the input types or method are incorrect.
    :return: None
    """
    with pytest.raises(expected_exception, match=match):
        Converter.from_strings_to_langstrings(method, strings, lang, separator)
