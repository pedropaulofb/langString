import pytest
from langstring import MultiLangString
from langstring import SetLangString
from tests.conftest import TYPEERROR_MSG_SINGULAR


@pytest.mark.parametrize(
    "lang, expected_texts, expected_lang",
    [
        # Existing valid input cases with adjustments for clarity and comprehensiveness
        ("en", {"Hello"}, "en"),  # Language exists with one entry
        ("fr", {"Bonjour", "Salut"}, "fr"),  # Language exists with multiple entries
        ("de", set(), "de"),  # Language does not exist, should return empty SetLangString
        (
            " ",
            set(),
            " ",
        ),  # Test with space as lang, should return empty SetLangString considering spaces are unusual but valid
        ("", set(), ""),  # Test with empty string as lang, emphasizing handling of entries without specified language
        ("Ελ", set(), "Ελ"),  # Test with Greek characters, non-existent language
        ("Ру", {"Привет"}, "Ру"),  # Test with Cyrillic characters, valid language with one entry
        ("en😀", set(), "en😀"),  # Test with emojis in the language code, non-existent language
    ],
)
def test_get_setlangstring_valid_inputs(lang: str, expected_texts: set, expected_lang: str):
    """
    Test `get_setlangstring` with valid language inputs, including edge cases and non-existent languages.
    """
    mls = MultiLangString({"en": {"Hello"}, "fr": {"Bonjour", "Salut"}, "Ру": {"Привет"}})
    result = mls.get_setlangstring(lang)
    assert isinstance(result, SetLangString), "Expected result to be a SetLangString instance."
    assert result.texts == expected_texts, f"Expected texts for language '{lang}' did not match."
    assert result.lang == expected_lang, f"Expected language '{expected_lang}' did not match."


@pytest.mark.parametrize(
    "lang",
    [
        # Extended invalid input cases to cover a wider range of invalid types
        123,  # Integer input
        [],  # List input
        None,  # None input
        {},  # Dictionary input
        True,  # Boolean input
    ],
)
def test_get_setlangstring_invalid_inputs(lang):
    """
    Test `get_setlangstring` with invalid language inputs to ensure type validation.
    """
    mls = MultiLangString({"en": {"Hello"}})
    with pytest.raises(TypeError, match=TYPEERROR_MSG_SINGULAR):
        mls.get_setlangstring(lang)


def test_get_setlangstring_unusual_but_valid_usage():
    """
    Test `get_setlangstring` with unusual but valid inputs, including case sensitivity and regional language codes.
    """
    mls = MultiLangString({"EN-us": {"Hello, American!"}, "EN-gb": {"Hello, British!"}})
    result_us = mls.get_setlangstring("EN-us")
    assert result_us.lang == "EN-us" and result_us.texts == {
        "Hello, American!"
    }, "Failed to handle case-sensitive and region-specific language code 'EN-us'."
    result_gb = mls.get_setlangstring("EN-gb")
    assert result_gb.lang == "EN-gb" and result_gb.texts == {
        "Hello, British!"
    }, "Failed to handle case-sensitive and region-specific language code 'EN-gb'."


@pytest.mark.parametrize(
    "initial_contents, expected_texts",
    [
        # Case 1: The empty string is used, and there are texts associated with it.
        ({"": {"Text without language"}}, {"Text without language"}),
        # Case 2: The empty string and other languages exist, testing retrieval for the empty string.
        ({"": {"Text without language"}, "en": {"Hello"}, "fr": {"Bonjour"}}, {"Text without language"}),
        # Case 3: The MultiLangString contains no entry for the empty string, but has other languages.
        ({"en": {"Hello"}, "fr": {"Bonjour"}}, set()),
        # Case 4: The MultiLangString contains multiple entries for the empty string.
        (
            {"": {"Text1 without language", "Text2 without language"}},
            {"Text1 without language", "Text2 without language"},
        ),
        # Case 5: An empty MultiLangString is used, ensuring the method handles this gracefully.
        ({}, set()),
        # Case 6: The MultiLangString contains only an empty string entry with multiple texts.
        ({"": {"Only text1", "Only text2"}}, {"Only text1", "Only text2"}),
    ],
)
def test_get_setlangstring_empty_string_scenarios(initial_contents, expected_texts):
    """
    Test the `get_setlangstring` method for handling the empty string as a language code across various scenarios.

    :param initial_contents: Initial contents of the MultiLangString instance.
    :param expected_texts: The expected set of texts associated with the empty string language code.
    """
    mls = MultiLangString(initial_contents)
    result = mls.get_setlangstring("")
    assert isinstance(
        result, SetLangString
    ), "Expected result to be a SetLangString instance for empty string language code."
    assert result.texts == expected_texts, "Expected texts did not match for empty string language code."
    assert result.lang == "", "Expected language code to be an empty string."
