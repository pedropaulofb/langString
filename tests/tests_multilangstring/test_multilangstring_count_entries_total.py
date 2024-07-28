import pytest
from langstring import MultiLangString


@pytest.mark.parametrize(
    "mls_dict, expected_total",
    [
        ({"en": {"Hello", "Goodbye"}, "fr": {"Bonjour"}}, 3),  # Basic usage with different languages
        ({}, 0),  # Empty MultiLangString
        ({"en": set(), "fr": set()}, 0),  # Languages present but no entries
        ({"ru": {"Привет", "До свидания"}, "gr": {"Γειά σου"}}, 3),  # Non-Latin alphabets
        ({"emoji": {"😀", "😃"}, "special": {"@#&*"}}, 3),  # Emojis and special characters
        ({"space": {" leading", "trailing "}}, 2),  # Entries with leading and trailing spaces
        ({"mixedCase": {"Test1"}, "MIXEDCASE": {"Test2"}}, 2),  # Case sensitivity in language codes
        ({"en": {"Duplicate", "Duplicate"}}, 1),  # Duplicate entries in a single language
        (
            {"en": {"Hello", "Goodbye"}, "es": {"Hola", "Adiós"}, "fr": {"Bonjour", "Au revoir"}},
            6,
        ),  # Multiple languages
        ({"": {""}, "  ": {" "}}, 2),  # Languages and entries with whitespace
        ({"emoji": {"😊", "😂", "😭"}, "special": {"*&^%", "$#@!"}}, 5),  # Emojis and special characters
        ({"mixed": {"Hello", "Hola", "こんにちは"}}, 3),  # Mixed language entries
        ({"long_text": {"a" * 1000}}, 1),  # Very long single entry
        ({"dupes": {"same", "same"}}, 1),  # Duplicate entries
        ({"dupes": {"same"}, "dupes": {"same"}}, 1),  # Duplicate entries
        ({"dupes": {"same"}, "dupes": {"same"}, "nodupes": {"same"}}, 2),  # Duplicate entries
        ({"many_empty": set([""] * 100)}, 1),  # Many empty strings as entries
        (
            {"numerics": {"123", "456"}, "booleans": {"True", "False"}},
            4,
        ),  # Numeric strings and boolean strings as entries
        ({"long_lang": {"a" * 1000, "b" * 1000}}, 2),  # Languages with very long entries
        ({"repeated_words": {"hello", "hello", "HELLO"}}, 2),  # Case sensitivity and repetition in entries
        (
            {"multi_charsets": {"こんにちは", "안녕하세요"}},
            2,
        ),  # Entries in different character sets (Japanese and Korean)
        ({"invisibles": {"\t", "\n", "  "}}, 3),  # Entries with invisible characters: tab, newline, spaces
        (
            {"compound_entries": {"hello-world", "test_drive"}},
            2,
        ),  # Entries with compound words using special characters
        ({"mixed_emotions": {"😀😃", "😃😀"}}, 2),  # Different combinations of emojis as entries
    ],
)
def test_count_entries_total(mls_dict, expected_total):
    """
    Test the `count_entries_total` method for counting the total number of entries across all languages.

    :param mls_dict: Dictionary to initialize the MultiLangString instance with.
    :param expected_total: Expected total number of entries.
    """
    mls = MultiLangString(mls_dict)
    assert (
        mls.count_entries_total() == expected_total
    ), f"Expected {expected_total} total entries, got {mls.count_entries_total()}"
