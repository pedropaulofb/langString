import re
from collections import Counter
from typing import List
from typing import Optional

import pytest
from langstring import Converter
from langstring import MultiLangString


@pytest.mark.parametrize(
    "method, strings, lang, separator, expected_texts, expected_langs",
    [
        # Manual method cases
        ("manual", ["Hello", "World"], "en", "@", ["Hello", "World"], ["en", "en"]),
        ("manual", ["Bonjour", "le", "monde"], "fr", "@", ["Bonjour", "le", "monde"], ["fr", "fr", "fr"]),
        ("manual", ["Hola", "Mundo"], "", "@", ["Hola", "Mundo"], ["", ""]),
        ("manual", [], "en", "@", [], []),  # Empty list
        ("manual", [""], "en", "@", [""], ["en"]),  # Empty string in list
        ("manual", ["Only one string"], "en", "@", ["Only one string"], ["en"]),  # Single string
        # Parse method cases
        ("parse", ["Hello@en", "World@en"], None, "@", ["Hello", "World"], ["en", "en"]),
        ("parse", ["Bonjour@fr", "le@fr", "monde@fr"], None, "@", ["Bonjour", "le", "monde"], ["fr", "fr", "fr"]),
        ("parse", ["Hola@es", "Mundo@es"], None, "@", ["Hola", "Mundo"], ["es", "es"]),
        ("parse", ["NoSeparatorHere"], None, "@", ["NoSeparatorHere"], [""]),
        ("parse", ["Special!@Chars"], None, "@", ["Special!"], ["Chars"]),
        ("parse", ["With space @ separator"], None, "@", ["With space "], [" separator"]),
        # Edge cases with different charsets and special characters
        ("manual", ["こんにちは", "世界"], "jp", "@", ["こんにちは", "世界"], ["jp", "jp"]),  # Japanese
        ("manual", ["Привет", "мир"], "ru", "@", ["Привет", "мир"], ["ru", "ru"]),  # Russian
        ("manual", ["Γειά", "σου", "κόσμε"], "el", "@", ["Γειά", "σου", "κόσμε"], ["el", "el", "el"]),  # Greek
        ("manual", ["😊", "🌍"], "", "@", ["😊", "🌍"], ["", ""]),  # Emojis
        ("manual", ["Special", "#&*Characters"], "", "@", ["Special", "#&*Characters"], ["", ""]),  # Special characters
        # Additional
        # Default values
        ("manual", ["Default", "Test"], "en", "@", ["Default", "Test"], ["en", "en"]),
        ("manual", ["EmptyLang"], "", "@", ["EmptyLang"], [""]),
        ("parse", ["Default@Test"], None, "@", ["Default"], ["Test"]),
        # Null values
        ("manual", ["NullLang"], None, "@", ["NullLang"], [""]),
        ("parse", ["Null@Lang"], None, "@", ["Null"], ["Lang"]),
        # Flags' effects (assuming flags are part of MultiLangString's behavior)
        ("manual", ["Flagged", "Text"], "flagged_lang", "@", ["Flagged", "Text"], ["flagged_lang", "flagged_lang"]),
        # Unusual but valid usage
        ("manual", ["Valid", "Unusual", "Usage"], "un", "@", ["Valid", "Unusual", "Usage"], ["un", "un", "un"]),
        # Operation on itself
        ("manual", ["Self", "Operation"], "self", "@", ["Self", "Operation"], ["self", "self"]),
    ],
)
def test_from_strings_to_multilangstring(
    method: str,
    strings: List[str],
    lang: Optional[str],
    separator: str,
    expected_texts: List[str],
    expected_langs: List[str],
) -> None:
    """Test the from_strings_to_multilangstring method with various inputs.

    :param method: Method to use for conversion ("manual" or "parse").
    :param strings: List of strings to be converted.
    :param lang: Language code for the "manual" method.
    :param separator: Separator for the "parse" method.
    :param expected_texts: The expected texts in the MultiLangString.
    :param expected_langs: The expected languages in the MultiLangString.
    :return: None
    """
    result = Converter.from_strings_to_multilangstring(method, strings, lang, separator)
    assert isinstance(result, MultiLangString), "Expected result to be an instance of MultiLangString"

    # Gather actual texts and languages from the result's mls_dict
    actual_texts = []
    actual_langs = []

    for lang_key, texts in result.mls_dict.items():
        for text in texts:
            actual_texts.append(text)
            actual_langs.append(lang_key)

    assert Counter(actual_texts) == Counter(expected_texts), f"Expected texts {expected_texts}, but got {actual_texts}"
    assert Counter(actual_langs) == Counter(
        expected_langs
    ), f"Expected languages {expected_langs}, but got {actual_langs}"


@pytest.mark.parametrize(
    "method, strings, lang, separator, expected_exception, match",
    [
        # Invalid method type
        (
            123,
            ["Hello", "World"],
            "en",
            "@",
            TypeError,
            "Invalid argument with value '123'. Expected 'str', but got 'int'.",
        ),
        # Invalid strings type
        ("manual", 123, "en", "@", TypeError, "Invalid argument with value '123'. Expected 'list', but got 'int'."),
        # Invalid lang type
        (
            "manual",
            ["Hello", "World"],
            123,
            "@",
            TypeError,
            "Invalid argument with value '123'. Expected 'str', but got 'int'.",
        ),
        (
            "manual",
            ["Hello", "World"],
            [],
            "@",
            TypeError,
            re.escape("Invalid argument with value '[]'. Expected 'str', but got 'list'."),
        ),
        (
            "manual",
            ["Hello", "World"],
            set(),
            "@",
            TypeError,
            re.escape("Invalid argument with value 'set()'. Expected 'str', but got 'set'."),
        ),
        # Invalid separator type
        (
            "parse",
            ["Hello@World"],
            None,
            123,
            TypeError,
            "Invalid argument with value '123'. Expected 'str', but got 'int'.",
        ),
        # Invalid string elements
        (
            "manual",
            [123, "World"],
            "en",
            "@",
            TypeError,
            "Invalid argument with value '123'. Expected 'str', but got 'int'.",
        ),
        (
            "manual",
            ["Hello", None],
            "en",
            "@",
            TypeError,
            "Invalid argument with value 'None'. Expected 'str', but got 'NoneType'.",
        ),
        (
            "manual",
            ["Hello", {}],
            "en",
            "@",
            TypeError,
            re.escape("Invalid argument with value '{}'. Expected 'str', but got 'dict'."),
        ),
        (
            "manual",
            ["Hello", ["Nested"]],
            "en",
            "@",
            TypeError,
            re.escape("Invalid argument with value '['Nested']'. Expected 'str', but got 'list'."),
        ),
        (
            "manual",
            ["Hello", set()],
            "en",
            "@",
            TypeError,
            re.escape("Invalid argument with value 'set()'. Expected 'str', but got 'set'."),
        ),
        # Additional invalid cases
        (
            "manual",
            None,
            "en",
            "@",
            TypeError,
            "Invalid argument with value 'None'. Expected 'list', but got 'NoneType'.",
        ),
        # Additional
        # Default values
        (
            "manual",
            ["Default"],
            None,
            None,
            TypeError,
            "Invalid argument with value 'None'. Expected 'str', but got 'NoneType'.",
        ),
        # Null values
        (
            "parse",
            ["Null@Lang"],
            None,
            None,
            TypeError,
            "Invalid argument with value 'None'. Expected 'str', but got 'NoneType'.",
        ),
        # Operation on itself with invalid values
        (
            "manual",
            [None],
            "self",
            "@",
            TypeError,
            "Invalid argument with value 'None'. Expected 'str', but got 'NoneType'.",
        ),
    ],
)
def test_from_strings_to_multilangstring_exceptions(
    method: str,
    strings: list[str],
    lang: Optional[str],
    separator: str,
    expected_exception: type[Exception],
    match: str,
) -> None:
    """Test the from_strings_to_multilangstring method for expected exceptions.

    :param method: Method to use for conversion ("manual" or "parse").
    :param strings: List of strings to be converted.
    :param lang: Language code for the "manual" method.
    :param separator: Separator for the "parse" method.
    :param expected_exception: The expected exception to be raised.
    :param match: The expected exception message.
    :raises expected_exception: If the input types are incorrect.
    :return: None
    """
    with pytest.raises(expected_exception, match=match):
        Converter.from_strings_to_multilangstring(method, strings, lang, separator)
