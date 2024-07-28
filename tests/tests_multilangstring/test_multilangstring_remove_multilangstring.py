from copy import deepcopy

import pytest
from langstring import MultiLangString


@pytest.fixture
def multilangstring_sample():
    """Fixture to create a sample MultiLangString instance for testing with more diverse cases."""
    return MultiLangString(
        mls_dict={
            "en": {"Hello World", "Good morning"},
            "fr": {"Bonjour le monde", "Bon matin"},
            "es": {"Hola Mundo", "Buenos días"},
            "emoji": {"👋", "🌍"},
            "ru": {"Привет мир"},
            "gr": {"Γειά σου Κόσμε"},
        }
    )


@pytest.mark.parametrize(
    "removable_dict, clean_empty",
    [
        ({"fr": {"Bonjour le monde", "Bon matin"}}, True),  # Full overlap
        ({"FR": {"Bonjour le monde", "Bon matin"}}, True),  # Case-insensitive removal.
        ({"en": {"Good morning"}, "es": {"Buenos días"}}, True),  # Multiple language removal.
        ({"emoji": {"👋", "🌍"}}, True),  # Removal using emojis as language codes.
        ({"ru": {"Привет мир"}, "gr": {"Γειά σου Κόσμε"}}, True),  # Removal with Cyrillic and Greek characters.
    ],
)
def test_remove_multilangstring_valid_cases(multilangstring_sample, removable_dict, clean_empty):
    """Test valid removal cases for a MultiLangString with varying degrees of overlap.

    :param multilangstring_sample: A MultiLangString instance for testing.
    :param removable_dict: The dictionary to construct a removable MultiLangString from.
    :param clean_empty: Whether to clean empty entries after removal.
    """
    removable_mls = MultiLangString(mls_dict=removable_dict)
    multilangstring_sample.remove_multilangstring(removable_mls, clean_empty=clean_empty)
    assert not multilangstring_sample.contains_multilangstring(removable_mls), f"Failed to remove."


@pytest.mark.parametrize(
    "removable_dict, clean_empty",
    [
        ({"en": {"Hello World"}, "de": {"Guten Tag"}}, False),  # Partial overlap
        ({"it": {"Buongiorno", "Buona sera"}}, False),  # No overlap
        ({" ": {"Some text"}}, False),  # Language code with a space.
        ({"123": {"Numbers as language code"}}, False),  # Numeric language code.
        ({"*special*": {"Special chars in language code"}}, False),  # Special characters in language code.
        ({"nonexistent": {"This does not exist"}}, False),  # Nonexistent language and text.
        ({"en": {"Nonexistent text"}}, False),  # Valid language but nonexistent text.
        ({"   ": {"Leading and trailing spaces"}}, False),  # Language code with leading and trailing spaces.
        ({"ru": {" "}}, False),  # Cyrillic with a space as a value, expecting failure if not matching exactly.
        ({"emojiLang": {"🙂"}}, False),  # Using emoji in the text value for removal.
    ],
)
def test_remove_multilangstring_invalid_cases(multilangstring_sample, removable_dict, clean_empty):
    """Test invalid removal cases for a MultiLangString with no or partial overlap.

    :param multilangstring_sample: A MultiLangString instance for testing.
    :param removable_dict: The dictionary to construct a removable MultiLangString from.
    :param clean_empty: Whether to clean empty entries after removal, irrelevant here but kept for consistency.
    """
    removable_mls = MultiLangString(mls_dict=removable_dict)
    with pytest.raises(ValueError, match="Entry .+ not found in the MultiLangString"):
        multilangstring_sample.remove_multilangstring(removable_mls, clean_empty=clean_empty)


@pytest.mark.parametrize(
    "removable_dict, clean_empty, expected_error",
    [
        (None, False, TypeError),  # Removing None
        ("invalid_type", False, TypeError),  # Invalid type for removable_dict
        ([], False, TypeError),  # Invalid type (list)
        (set(), False, TypeError),  # Invalid type (set)
    ],
)
def test_remove_multilangstring_invalid_type_cases(multilangstring_sample, removable_dict, clean_empty, expected_error):
    """Test removal with invalid types for the removable dictionary.

    :param multilangstring_sample: A MultiLangString instance for testing.
    :param removable_dict: An invalid removable dictionary.
    :param clean_empty: Whether to clean empty entries after removal.
    :param expected_error: The expected error type.
    """
    with pytest.raises(expected_error):
        multilangstring_sample.remove_multilangstring(removable_dict, clean_empty=clean_empty)


def test_remove_multilangstring_operation_on_itself(multilangstring_sample):
    """Test removing a MultiLangString instance from itself.

    :param multilangstring_sample: A MultiLangString instance for testing.
    """
    with pytest.raises(RuntimeError, match="Set changed size during iteration"):
        multilangstring_sample.remove_multilangstring(multilangstring_sample, clean_empty=True)


@pytest.mark.parametrize(
    "removable_dict, expected_result",
    [
        ({"en": {""}}, ValueError),  # Empty string as a value
        ({"": {"some value"}}, ValueError),  # Empty string as a language code
    ],
)
def test_remove_multilangstring_edge_cases(multilangstring_sample, removable_dict, expected_result):
    """Test handling of edge cases in removal.

    :param multilangstring_sample: A MultiLangString instance for testing.
    :param removable_dict: The dictionary representing edge cases for removal.
    :param expected_result: The expected result or error.
    """
    removable_mls = MultiLangString(mls_dict=removable_dict)
    with pytest.raises(expected_result):
        multilangstring_sample.remove_multilangstring(removable_mls, clean_empty=True)


def test_remove_empty(multilangstring_sample):
    mls = deepcopy(multilangstring_sample)
    removable_mls = MultiLangString(mls_dict={})
    mls.remove_multilangstring(removable_mls)
    assert mls == multilangstring_sample
