import pytest
from langstring import MultiLangString


@pytest.mark.parametrize(
    "mls_dict, expected_length",
    [
        ({"en": {"Hello World"}}, 1),  # Single language
        ({"en": {"Hello World"}, "es": {"Hola Mundo"}}, 2),  # Multiple languages
        ({}, 0),  # No languages
        ({"EN": {"Hello", "World"}, "en-GB": {"Hello, mate"}}, 2),  # Case variations
        ({" fr ": {"Bonjour"}, "es ": {"Hola"}}, 2),  # Spaces in language codes
        ({"ελ": {"Γειά"}, "рус": {"Привет"}, "👋": {"Hello", "World!"}}, 3),  # Greek, Cyrillic, emoji keys
    ],
)
def test_multilangstring_len(mls_dict, expected_length):
    """
    Test the __len__ method for accurately counting the number of languages in a MultiLangString instance.

    :param mls_dict: Dictionary to initialize the MultiLangString instance with.
    :param expected_length: Expected number of languages (length) in the instance.
    """
    mls = MultiLangString(mls_dict=mls_dict)
    assert len(mls) == expected_length, f"Expected length {expected_length}, but got {len(mls)}"
