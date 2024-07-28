from typing import Any

import pytest
from langstring import MultiLangString
from tests.conftest import TYPEERROR_MSG_SINGULAR


@pytest.mark.parametrize(
    "input_mls_dict,expected",
    [
        ({"en": {"Hello"}, "fr": {"Bonjour"}}, {"en": {"Hello"}, "fr": {"Bonjour"}}),
        ({"es": {"Hola"}, "de": {"Hallo"}}, {"es": {"Hola"}, "de": {"Hallo"}}),
        ({"EN": {"HELLO"}, "en": {"Hello"}}, {"en": {"HELLO", "Hello"}}),
        ({"en": {"Hello, world!"}, "fr": {"Bonjour, monde!"}}, {"en": {"Hello, world!"}, "fr": {"Bonjour, monde!"}}),
        ({"en": {" Hello "}, "fr": {" Bonjour "}}, {"en": {" Hello "}, "fr": {" Bonjour "}}),
        ({"en": {"Hello", "Hi"}, "EN": {"Greetings"}}, {"en": {"Hello", "Hi", "Greetings"}}),
        ({}, {}),
        ({"en": set(), "fr": set()}, {"en": set(), "fr": set()}),
        ({"en": {"Hello"}, "en": {"Hello"}}, {"en": {"Hello"}}),
        # Multiple casing
        (
            {"En": {"Hello"}, "FR": {"Bonjour"}, "en": {"hello"}, "fr": {"bonjour"}},
            {"en": {"Hello", "hello"}, "fr": {"Bonjour", "bonjour"}},
        ),
        # Different char sets (Cyrillic, Greek, Chinese)
        ({"ru": {"Привет"}, "el": {"Γειά"}, "zh": {"你好"}}, {"ru": {"Привет"}, "el": {"Γειά"}, "zh": {"你好"}}),
        # Different spacing
        ({"en": {"  Hello  "}, "fr": {"  Bonjour  "}}, {"en": {"  Hello  "}, "fr": {"  Bonjour  "}}),
        # Special chars
        (
            {"en": {"Hello!"}, "fr": {"Bonjour?"}, "es": {"¡Hola!"}, "de": {"Guten Tag."}},
            {"en": {"Hello!"}, "fr": {"Bonjour?"}, "es": {"¡Hola!"}, "de": {"Guten Tag."}},
        ),
        # Mixed casing, char sets, spacing, and special chars
        (
            {
                "EN": {"HELLO", "HELLO!"},
                "en": {"hello", "hello?"},
                "fr": {"  Bonjour  ", "Bonjour?"},
                "zh": {"  你好  ", "你好!"},
            },
            {
                "en": {"HELLO", "HELLO!", "hello", "hello?"},
                "fr": {"  Bonjour  ", "Bonjour?"},
                "zh": {"  你好  ", "你好!"},
            },
        ),
    ],
)
def test_merge_with_non_overlapping_keys(input_mls_dict: dict[str, Any], expected: dict[str, Any]) -> None:
    """
    Test _merge_language_entries with dictionaries having non-overlapping keys.

    :param input_mls_dict: First input dictionary to merge.
    :param dict_b: Second input dictionary to merge, with no overlapping keys with input_mls_dict.
    :param expected: The expected result of merging input_mls_dict and dict_b.
    :return: None
    :raises: AssertionError if the merged result does not correctly include all entries from both dictionaries.
    """
    mls = MultiLangString()
    result = mls._merge_language_entries(input_mls_dict)
    assert result == expected, f"Merging {input_mls_dict} failed to produce {expected}."


@pytest.mark.parametrize(
    "input_mls_dict",
    [
        (["en"]),
        ("not a dict"),
        (12345),
        (None),
        ({"str"}),
    ],
)
def test_merge_with_invalid_input_types(input_mls_dict: Any) -> None:
    """
    Test _merge_language_entries with invalid input types to ensure it raises TypeError.

    :param input_mls_dict: First input to the merge function, potentially invalid type.
    :return: None
    :raises: TypeError if input types are not dictionaries.
    """
    mls = MultiLangString()
    with pytest.raises(TypeError, match=TYPEERROR_MSG_SINGULAR):
        mls._merge_language_entries(input_mls_dict)


@pytest.mark.parametrize(
    "input_mls_dict,expected",
    [
        # Case Insensitivity with Non-Latin Scripts
        ({"ru": {"Привет"}, "RU": {"Добрый день"}}, {"ru": {"Привет", "Добрый день"}}),
        # Empty Strings in Sets
        ({"en": {"Hello", ""}, "EN": {""}}, {"en": {"Hello", ""}}),
        # Languages with Hyphens and Underlines
        ({"en-US": {"Hello"}, "en-us": {"Howdy"}}, {"en-us": {"Hello", "Howdy"}}),
        # Languages with Hyphens and Underlines - Python restriction
        ({"en-US": {"Hello"}, "en-US": {"Howdy"}}, {"en-US": {"Howdy"}}),
        # Languages with Hyphens and Underlines - Should not merge, as is different
        ({"en-US": {"Hello"}, "en_US": {"Howdy"}}, {"en-US": {"Hello"}, "en_US": {"Howdy"}}),
        # Keys with Leading and Trailing Spaces
        ({" en ": {"Hello"}, "en": {"Hi"}}, {" en ": {"Hello"}, "en": {"Hi"}}),
        # Very Similar but Distinct Languages
        ({"en": {"Hello"}, "eng": {"Hello again"}}, {"en": {"Hello"}, "eng": {"Hello again"}}),
    ],
)
def test_merge_language_entries_special_cases(input_mls_dict: dict[str, Any], expected: dict[str, Any]) -> None:
    """
    Test _merge_language_entries with dictionaries that have special cases,
    including non-Latin scripts, empty strings, hyphens, underscores, and similar language codes.

    :param input_mls_dict: Input dictionary to merge.
    :param expected: The expected result of merging.
    """
    mls = MultiLangString()
    result = mls._merge_language_entries(input_mls_dict)
    assert result == expected, f"Merging {input_mls_dict} failed to produce {expected}."
