import pytest
from langstring import MultiLangString
from tests.conftest import TYPEERROR_MSG_SINGULAR


@pytest.mark.parametrize(
    "lang,expected_count",
    [
        ("en", 2),  # Assuming two entries exist for 'en'
        ("En", 2),  # Assuming two entries exist for 'en'
        ("fr", 1),  # Assuming one entry exists for 'fr'
        ("FR", 1),  # Assuming one entry exists for 'fr'
        (" fr", 0),  # Assuming one entry exists for 'fr'
        ("es", 0),  # Assuming no entries exist for 'es'
        ("", 0),  # Assuming no entries exist for 'es'
        ("en ", 0),  # Space after
        (" EN", 0),  # Space before, uppercase
        ("рус", 0),  # Cyrillic characters, no entries
        (":)", 0),  # Emoji as language code, assuming no entries
        ("en😀", 0),  # Valid language code followed by emoji, assuming no entries
        ("fr-fr", 0),  # Locale format, assuming no entries
        ("\tfr", 0),  # Tab before language code, assuming no entries
        ("fr\n", 0),  # Newline after language code, assuming no entries
        ("--fr--", 0),  # Special characters around language code, assuming no entries
    ],
)
def test_count_entries_by_lang(lang: str, expected_count: int):
    """
    Test the `count_entries_by_lang` method for a given language code.

    :param lang: The language code to count entries for.
    :param expected_count: The expected number of entries for the given language.
    """
    mls = MultiLangString({"en": {"Hello", "Goodbye"}, "fr": {"Bonjour"}})
    count = mls.count_entries_of_lang(lang)
    assert count == expected_count, f"Expected {expected_count} entries for lang '{lang}', got {count}"


@pytest.mark.parametrize("invalid_lang", [123, None, 3.14, [], {}])
def test_count_entries_by_lang_invalid_lang_type(invalid_lang):
    """
    Test the `count_entries_by_lang` method with various invalid language types to ensure type validation.
    """
    mls = MultiLangString()
    with pytest.raises(TypeError, match=TYPEERROR_MSG_SINGULAR):
        mls.count_entries_of_lang(invalid_lang)
