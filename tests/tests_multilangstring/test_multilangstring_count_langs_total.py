import pytest
from langstring import MultiLangString


@pytest.mark.parametrize(
    "mls_dict,expected_total",
    [
        ({"en": {"Hello", "Goodbye"}, "fr": {"Bonjour"}}, 2),  # Valid languages
        ({}, 0),  # Empty dictionary
        ({"en": set(), "fr": set()}, 2),  # Languages with no entries
        ({"рус": {"Привет"}, "ελλ": {"Γειά σου"}}, 2),  # Non-Latin alphabets
        ({"en": {"Hello"}, "en": {"Goodbye"}}, 1),  # Duplicate language codes, depending on implementation
        ({"emoji": {"😀", "😁"}, "special": {"!@#$%"}}, 2),  # Emojis and special characters as languages
        (
            {"  en  ": {" Hello "}, "fr": {" Bonjour "}},
            3,
        ),  # Treating "  en  " as a distinct language code due to spaces
        (["  en  ", "en"], 2),  # Differentiating based on spaces around language codes
        (["en", " en ", "  en"], 3),  # Treating each as unique due to spaces
        ({"  en  ": {"Hello"}, " en": {"Goodbye"}, "en ": {"Hi"}}, 3),  # Spaces in different positions
        ({"lower": {"case"}, "UPPER": {"CASE"}, "Mixed": {"Case"}}, 3),  # Case variations
        ({"": {"empty"}, " ": {"space"}, "  ": {"double space"}}, 3),  # Empty and space keys
        ({"👋": {"hello"}, "😊": {"happy"}}, 2),  # Emojis as language codes
        ({"num#1": {"first"}, "&*": {"special"}}, 2),  # Special characters as language codes
        ({"русский": {"Привет"}, "ελληνικά": {"Γειά σου"}}, 2),  # Cyrillic and Greek
        ({"long " * 10 + "lang": {"verbose"}, "short": {"concise"}}, 2),  # Long language name
    ],
)
def test_count_langs_total(mls_dict, expected_total):
    """
    Test the `count_langs_total` method for counting the total number of languages.

    :param mls_dict: Dictionary to initialize the MultiLangString instance with.
    :param expected_total: Expected total number of unique languages.
    """
    mls = MultiLangString(mls_dict)
    total_langs = mls.count_langs_total()
    assert total_langs == expected_total, f"Expected {expected_total} total languages, got {total_langs}"


# Assuming the setup for MultiLangString instances is done in each test or via a fixture
@pytest.mark.parametrize(
    "langs,expected_total",
    [
        ([], 0),  # No languages added
        (["en"], 1),  # Single language
        (["en", "fr", "es"], 3),  # Multiple unique languages
        (["en", "En", "eN"], 1),  # Duplicate languages
        (["en"] * 1000, 1),  # Stress test with duplicates
        (["en", "fr", "es", "de", "it", "ru"], 6),  # Multiple unique languages, broader set
    ],
)
def test_count_langs_total(langs, expected_total):
    """
    Test the `count_langs_total` method for various scenarios including no languages, unique languages, and duplicate languages.
    """
    mls = MultiLangString()
    assert mls.count_langs_total() == 0
    for lang in langs:
        mls.add_entry("test", lang)  # Assuming a method to add languages exists
    assert (
        mls.count_langs_total() == expected_total
    ), f"Expected total languages count of {expected_total}, got {mls.count_langs_total()}"
