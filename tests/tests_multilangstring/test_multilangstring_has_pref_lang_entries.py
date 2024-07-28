import pytest
from langstring import MultiLangString


@pytest.mark.parametrize(
    "mls_data, pref_lang, expected_result",
    [
        ({"en": {"Hello", "World"}}, "en", True),  # Entries present in the preferred language
        ({"en": set()}, "en", False),  # No entries in the preferred language
        ({"en": {"Hello"}, "es": {"Hola", "Mundo"}}, "es", True),  # Entries present in a non-English preferred language
        ({"fr": set(), "de": set()}, "fr", False),  # Preferred language empty, others also empty
        ({"fr": {"Bonjour"}, "de": {"Guten Tag"}}, "it", False),  # Preferred language not present
        ({"en": {" "}}, "en", True),  # Spaces only in English entries
        ({"EN": {" "}}, "en", True),  # Case insensivity in mls_dict
        ({"en": {" "}}, "EN", True),  # Case insensivity in pref_lang
        ({" en": {" "}}, "en", False),
        ({"ru": {"Привет", "Мир"}}, "ru", True),  # Cyrillic characters in Russian entries
        ({"gr": {"Γειά σου", "Κόσμος"}}, "gr", True),  # Greek characters in Greek entries
        ({"emoji": {"😊", "🌍"}}, "emoji", True),  # Emojis as entries
        ({"mixed": {"Hello", "世界", "123"}}, "mixed", True),  # Mixed charset and numbers
        ({"special": {"@Hello#", "$World&"}}, "special", True),  # Special characters in entries
        ({"spaces": {" Hello", "World "}}, "spaces", True),  # Leading and trailing spaces in entries
        ({"empty_strings": {""}}, "empty_strings", True),  # Empty string as an entry
        ({"multiple_spaces": {"   "}}, "multiple_spaces", True),  # Multiple spaces as an entry
        ({"upper_case": {"HELLO", "WORLD"}}, "en", False),  # Upper case preferred language code with no match
    ],
)
def test_has_pref_lang_entries_parametrized(mls_data, pref_lang, expected_result):
    """Test has_pref_lang_entries with various configurations to ensure it correctly identifies presence or absence of preferred language entries."""
    mls = MultiLangString(mls_data, pref_lang=pref_lang)
    assert (
        mls.has_pref_lang_entries() == expected_result
    ), f"Expected {expected_result} for preferred language '{pref_lang}' with data {mls_data}"


@pytest.mark.parametrize(
    "initial_contents, pref_lang, expected_result",
    [
        # Case 1: Preferred language is empty string, and entries exist for it.
        ({"": {"An entry without language"}}, "", True),
        # Case 2: Entries for both specified languages and empty string exist, preferred language is empty string.
        ({"": {"An entry without language"}, "en": {"Hello"}, "fr": {"Bonjour"}}, "", True),
        # Case 3: No entries for the empty string, but other languages exist; preferred language is empty string.
        ({"en": {"Hello"}, "fr": {"Bonjour"}}, "", False),
        # Case 4: MultiLangString is entirely empty, preferred language is empty string.
        ({}, "", False),
        # Case 5: Only specified languages exist in MultiLangString, no empty string entries; preferred language is empty string.
        ({"en": {"Hello"}, "fr": {"Bonjour"}, "es": {"Hola"}}, "", False),
    ],
)
def test_has_pref_lang_entries_with_empty_string(initial_contents, pref_lang, expected_result):
    """
    Test the `has_pref_lang_entries` method for handling the empty string as a preferred language across various scenarios.

    :param initial_contents: Initial contents of the MultiLangString instance.
    :param pref_lang: The preferred language set for the test, specifically focusing on the empty string.
    :param expected_result: The expected boolean result indicating whether entries for the preferred language exist.
    """
    mls = MultiLangString(initial_contents)
    mls.pref_lang = pref_lang  # Setting the preferred language to the test case's preference
    result = mls.has_pref_lang_entries()
    assert (
        result is expected_result
    ), f"Expected {expected_result} for preferred language '{pref_lang}', but got {result}."
