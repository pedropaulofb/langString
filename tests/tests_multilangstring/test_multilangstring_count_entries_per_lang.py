import pytest
from langstring import MultiLangString


def test_count_entries_per_lang_empty():
    """Test that count_entries_per_lang returns an empty dictionary when there are no entries."""
    mls = MultiLangString()
    assert mls.count_entries_per_lang() == {}, "Expected an empty dictionary for an empty MultiLangString"


import pytest
from langstring import MultiLangString


@pytest.mark.parametrize(
    "texts, expected_counts",
    [
        ({"en": {"Hello", "World"}, "es": {"Hola", "Mundo"}, "fr": {"Bonjour"}}, {"en": 2, "es": 2, "fr": 1}),
        (
            {"en": {"One", "Two", "Three"}, "de": {"Eins", "Zwei", "Drei"}, "it": {"Uno", "Due", "Tre"}},
            {"en": 3, "de": 3, "it": 3},
        ),
        # Testing with empty sets for each language
        ({"en": set(), "es": set(), "fr": set()}, {"en": 0, "es": 0, "fr": 0}),
        # Testing with mixed case, special characters, and spaces
        (
            {
                "en": {"Hello", "world!", " Good morning "},
                "de": {"Guten Tag", "Welt"},
                "fr": {"Bonjour", "le monde", " "},
            },
            {"en": 3, "de": 2, "fr": 3},
        ),
        # Testing with non-ASCII characters and emojis
        (
            {"ru": {"Привет", "Мир"}, "jp": {"こんにちは", "世界"}, "emoji": {"😊", "🌍"}},
            {"ru": 2, "jp": 2, "emoji": 2},
        ),
        # Testing with a large dataset for scalability
        ({"en": {str(i) for i in range(500)}, "es": {str(i) for i in range(250)}}, {"en": 500, "es": 250}),
        # Testing with languages having only one entry to verify minimal cases
        ({"en": {"Hello"}, "es": {"Hola"}, "fr": {"Bonjour"}}, {"en": 1, "es": 1, "fr": 1}),
    ],
)
def test_count_entries_per_lang_multiple_languages_parametrized(texts, expected_counts):
    """Test that count_entries_per_lang correctly counts entries across multiple languages using parametrization."""
    mls = MultiLangString(texts)
    assert (
        mls.count_entries_per_lang() == expected_counts
    ), f"Expected {expected_counts}, got {mls.count_entries_per_lang()}"


@pytest.mark.parametrize(
    "lang, texts, expected_count",
    [
        ("en", set(), 0),
        ("", {""}, 1),
        ("en", {"Hello", "World", "Python"}, 3),
        ("de", {"Hallo", "Welt"}, 2),
        ("fr", {"Bonjour", "Monde", "Python", "AI"}, 4),
        ("en", {"   "}, 1),  # Spaces only
        ("en", {"Hello", "HELLO", "hello"}, 3),  # Case sensitivity
        ("ru", {"Привет", "Мир"}, 2),  # Cyrillic characters
        ("gr", {"Γειά", "Κόσμος"}, 2),  # Greek characters
        ("en", {"😊", "🚀", "🌟"}, 3),  # Emojis
        ("en", {"Hello-world", "Hello@world", "Hello#world"}, 3),  # Special characters
        ("en", {" Hello ", "World "}, 2),  # Leading and trailing spaces
        ("jp", {"こんにちは", "世界"}, 2),  # Japanese characters
    ],
)
def test_count_entries_per_lang_parametrized(lang, texts, expected_count):
    """Parametrized test to verify correct counts for various languages and number of texts."""
    mls = MultiLangString({lang: texts})
    result = mls.count_entries_per_lang()
    assert (
        result.get(lang, 0) == expected_count
    ), f"Expected {expected_count} entries for '{lang}', got {result.get(lang, 0)}"


def test_count_entries_per_lang_incorrect_lang_code():
    """Test that count_entries_per_lang functions correctly even with incorrect language codes."""
    mls = MultiLangString({"en": {"Hello", "World"}, "xx": {"Foo"}})
    result = mls.count_entries_per_lang()
    assert result == {"en": 2, "xx": 1}, "Expected correct handling of incorrect language codes"


@pytest.mark.parametrize(
    "lang, expected_result",
    [
        ("", {"": 0}),  # Testing with an empty language code and no entries
        ("en", {"en": 0}),  # Testing with a valid language code but no entries
    ],
)
def test_count_entries_per_lang_with_no_texts(lang, expected_result):
    """Test count_entries_per_lang with languages defined but no texts."""
    mls = MultiLangString({lang: set()})
    result = mls.count_entries_per_lang()
    assert result == expected_result, f"Expected {expected_result}, got {result} for language '{lang}' with no texts"


def test_count_entries_per_lang_with_large_dataset():
    """Test count_entries_per_lang with a large number of entries to ensure scalability."""
    mls = MultiLangString({"en": {str(i) for i in range(1000)}})
    expected = {"en": 1000}
    result = mls.count_entries_per_lang()
    assert result == expected, "Expected correct count for a large dataset"
