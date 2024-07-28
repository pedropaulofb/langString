import pytest
from langstring import MultiLangString
from tests.conftest import TYPEERROR_MSG_SINGULAR


# TypeError test for remove_entry
@pytest.mark.parametrize(
    "text, lang",
    [
        (123, "en"),  # text is not a string
        ("hello", 123),  # lang is not a string
    ],
)
def test_remove_entry_type_error(text, lang):
    """
    Test remove_entry method raises TypeError for invalid input types.

    :param text: Text of the entry to be removed.
    :param lang: Language of the entry to be removed.
    """
    mls = MultiLangString({"en": {"hello", "world"}})
    with pytest.raises(TypeError, match=TYPEERROR_MSG_SINGULAR):
        mls.remove_entry(text, lang)


# ValueError test for remove_entry
@pytest.mark.parametrize(
    "text, lang",
    [
        ("123", "en"),  # Assuming this value combination is invalid for the operation
        (" hello", "en"),  # Leading space in text might be considered invalid
        ("Hello", "en"),  # Case sensitivity issue, assuming 'Hello' is not present
        ("hello", " en"),  # Leading space in lang might be considered invalid
        ("hello", ""),  # Empty lang string is invalid
    ],
)
def test_remove_entry_value_error(text, lang):
    """
    Test remove_entry method raises ValueError for invalid input values.

    :param text: Text of the entry to be removed.
    :param lang: Language of the entry to be removed.
    """
    mls = MultiLangString({"en": {"hello", "world"}})
    with pytest.raises(ValueError, match="Entry .+ not found in the MultiLangString."):
        mls.remove_entry(text, lang)


@pytest.mark.parametrize(
    "initial_contents, text_to_remove, lang_to_remove, expected_contents",
    [
        ({"en": {"hello", "world"}, "fr": {"bonjour"}}, "hello", "en", {"en": {"world"}, "fr": {"bonjour"}}),
        ({"en": {"hello", "world"}, "fr": {"bonjour"}}, "hello", "En", {"en": {"world"}, "fr": {"bonjour"}}),
        ({"en": {"hello", "world"}, "fr": {"bonjour"}}, "hello", "EN", {"en": {"world"}, "fr": {"bonjour"}}),
        ({"en": {"hello"}, "fr": {"bonjour"}}, "hello", "en", {"en": set(), "fr": {"bonjour"}}),
        (
            {"en": {"   hello   ", "world"}, "fr": {"bonjour"}},
            "   hello   ",
            "en",
            {"en": {"world"}, "fr": {"bonjour"}},
        ),
        ({"en": {"HELLO", "world"}, "fr": {"bonjour"}}, "HELLO", "en", {"en": {"world"}, "fr": {"bonjour"}}),
        ({"gr": {"Γειά"}, "ru": {"привет"}}, "Γειά", "gr", {"gr": set(), "ru": {"привет"}}),
        ({"emoji": {"👋"}}, "👋", "emoji", {"emoji": set()}),
        ({"en-special": {"hello-world"}}, "hello-world", "en-special", {"en-special": set()}),
        (
            {"ru": {"Привет", "Мир"}, "gr": {"Γεια", "Κόσμος"}},
            "Привет",
            "ru",
            {"ru": {"Мир"}, "gr": {"Γεια", "Κόσμος"}},
        ),
        ({"mixed": {"hello", "HELLO"}}, "hello", "mixed", {"mixed": {"HELLO"}}),  # Case sensitivity
        ({"spaces": {" hello ", "world"}}, " hello ", "spaces", {"spaces": {"world"}}),  # Leading/trailing spaces
        (
            {"special-chars": {"hello-world!", "hello"}},
            "hello-world!",
            "special-chars",
            {"special-chars": {"hello"}},
        ),  # Special characters
    ],
)
def test_remove_entry_content(initial_contents, text_to_remove, lang_to_remove, expected_contents):
    """
    Test remove_entry method correctly modifies the content of the MultiLangString instance.

    :param initial_contents: Initial contents of the MultiLangString.
    :param text_to_remove: Text of the entry to be removed.
    :param lang_to_remove: Language of the entry to be removed.
    :param expected_contents: Expected contents of the MultiLangString after removal.
    """
    mls = MultiLangString(initial_contents)
    mls.remove_entry(text_to_remove, lang_to_remove)
    assert (
        mls.mls_dict == expected_contents
    ), f"Expected contents after removal: {expected_contents}, got: {mls.mls_dict}"


import pytest


@pytest.mark.parametrize(
    "text, lang",
    [
        (123, "en"),  # text is not a string
        ("hello", 123),  # lang is not a string
    ],
)
def test_remove_entry_type_error(text, lang):
    """
    Test remove_entry method raises TypeError for invalid input types.

    :param text: Text of the entry to be removed.
    :param lang: Language of the entry to be removed.
    """
    mls = MultiLangString({"en": {"hello", "world"}})
    with pytest.raises(TypeError, match=TYPEERROR_MSG_SINGULAR):
        mls.remove_entry(text, lang)


# ValueError test for remove_entry
@pytest.mark.parametrize(
    "text, lang",
    [
        ("123", "en"),  # Assuming this value combination is invalid for the operation
        (" hello", "en"),  # Leading space in text might be considered invalid
        ("Hello", "en"),  # Case sensitivity issue, assuming 'Hello' is not present
        ("hello", " en"),  # Leading space in lang might be considered invalid
        ("hello", ""),  # Empty lang string is invalid
    ],
)
def test_remove_entry_value_error(text, lang):
    """
    Test remove_entry method raises ValueError for invalid input values.

    :param text: Text of the entry to be removed.
    :param lang: Language of the entry to be removed.
    """
    mls = MultiLangString({"en": {"hello", "world"}})
    with pytest.raises(ValueError, match="Entry .+ not found in the MultiLangString."):
        mls.remove_entry(text, lang)


@pytest.mark.parametrize(
    "initial_contents, lang_to_remove",
    [
        ({"en": {"hello", "world"}}, None),  # lang_to_remove is None
    ],
)
def test_remove_entry_edge_cases_lang_type_error(initial_contents, lang_to_remove):
    """
    Test remove_entry method with edge cases for 'lang' parameter, such as null value.

    :param initial_contents: Initial contents of the MultiLangString.
    :param lang_to_remove: Language code to remove entry from, testing null value.
    """
    mls = MultiLangString(initial_contents)
    with pytest.raises(TypeError, match=TYPEERROR_MSG_SINGULAR):
        mls.remove_entry("hello", lang_to_remove)


# ValueError test for remove_entry with edge cases for 'lang' parameter
@pytest.mark.parametrize(
    "initial_contents, lang_to_remove",
    [
        ({"en": {"hello", "world"}}, ""),  # lang_to_remove is an empty string
    ],
)
def test_remove_entry_edge_cases_lang_value_error(initial_contents, lang_to_remove):
    """
    Test remove_entry method with edge cases for 'lang' parameter, such as empty string value.

    :param initial_contents: Initial contents of the MultiLangString.
    :param lang_to_remove: Language code to remove entry from, testing empty string value.
    """
    mls = MultiLangString(initial_contents)
    with pytest.raises(ValueError, match="Entry .+ not found in the MultiLangString."):
        mls.remove_entry("hello", lang_to_remove)


# TypeError test for remove_entry with invalid text type
@pytest.mark.parametrize(
    "text, lang",
    [
        (None, "en"),  # text is None
    ],
)
def test_remove_entry_invalid_types_type_error(text, lang):
    """
    Test remove_entry method handles null type parameters correctly.

    :param text: Text of the entry to be removed, testing null value.
    :param lang: Language of the entry to be removed.
    """
    mls = MultiLangString({"en": {"hello", "world"}})
    with pytest.raises(TypeError, match=TYPEERROR_MSG_SINGULAR):
        mls.remove_entry(text, lang)


# ValueError test for remove_entry with empty text value
@pytest.mark.parametrize(
    "text, lang",
    [
        ("", "en"),  # text is an empty string
    ],
)
def test_remove_entry_invalid_values_value_error(text, lang):
    """
    Test remove_entry method handles empty value parameters correctly.

    :param text: Text of the entry to be removed, testing empty value.
    :param lang: Language of the entry to be removed.
    """
    mls = MultiLangString({"en": {"hello", "world"}})
    with pytest.raises(ValueError, match="Entry .+ not found in the MultiLangString."):
        mls.remove_entry(text, lang)


@pytest.mark.parametrize(
    "initial_contents, text_to_remove, lang_to_remove, expected_contents",
    [
        # Correct expectations to match the class's behavior
        (
            {"gr": {"Γειά"}, "ru": {"привет"}},
            "Γειά",
            "gr",
            {"gr": set(), "ru": {"привет"}},
        ),  # gr remains with an empty set
        ({"emoji": {"👋"}}, "👋", "emoji", {"emoji": set()}),  # emoji remains with an empty set
        (
            {"en-special": {"hello-world"}},
            "hello-world",
            "en-special",
            {"en-special": set()},
        ),  # en-special remains with an empty set
    ],
)
def test_remove_entry_various_inputs(initial_contents, text_to_remove, lang_to_remove, expected_contents):
    mls = MultiLangString(initial_contents)
    mls.remove_entry(text_to_remove, lang_to_remove)
    assert (
        mls.mls_dict == expected_contents
    ), f"Expected contents after removal: {expected_contents}, got: {mls.mls_dict}"


@pytest.mark.parametrize(
    "initial_contents, text, lang, clean_empty, expected_contents",
    [
        ({"en": {"hello", "world"}, "fr": {"bonjour"}}, "world", "en", True, {"en": {"hello"}, "fr": {"bonjour"}}),
        (
            {"en": {"world"}, "fr": {"bonjour"}},
            "world",
            "en",
            True,
            {"fr": {"bonjour"}},
        ),  # en becomes empty and should be removed
        (
            {"en": {"world"}, "fr": {"bonjour"}},
            "world",
            "en",
            False,
            {"en": set(), "fr": {"bonjour"}},
        ),  # en remains but is empty
        (
            {"en": {"hello"}, "fr": {"bonjour", "salut"}},
            "bonjour",
            "fr",
            True,
            {"en": {"hello"}, "fr": {"salut"}},
        ),  # fr remains
    ],
)
def test_remove_entry_with_clean_empty(initial_contents, text, lang, clean_empty, expected_contents):
    """
    Test the `remove_entry` method with the `clean_empty` parameter affecting the final state of `mls_dict`.

    :param initial_contents: Initial contents of the MultiLangString.
    :param text: The text of the entry to be removed.
    :param lang: The language of the entry to be removed.
    :param clean_empty: Whether to remove empty language sets after removal.
    :param expected_contents: Expected state of `mls_dict` after the operation.
    """
    mls = MultiLangString(initial_contents)
    mls.remove_entry(text, lang, clean_empty=clean_empty)
    assert mls.mls_dict == expected_contents, "The `mls_dict` did not match expected contents after the operation."
