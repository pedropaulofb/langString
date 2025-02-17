import pytest
from langstring import MultiLangString
from tests.conftest import TYPEERROR_MSG_SINGULAR


@pytest.mark.parametrize(
    "lang, expected_key",
    [
        ("en", "en"),
        ("FR", "FR"),
        ("  es  ", "  es  "),
        ("DE-de", "DE-de"),
        ("\u03b5\u03bb", "\u03b5\u03bb"),  # Greek for 'el'
        ("🌐", "🌐"),
        ("@#$%", "@#$%"),
        ("    ", "    "),
        ("", ""),
        ("\t", "\t"),
        ("\tfr\t", "\tfr\t"),  # Tab characters around the language code
        (" en ", " en "),  # Spaces inside the language code
        ("рус", "рус"),  # Cyrillic characters
    ],
)
def test_add_empty_lang_adds_language_with_empty_set(lang: str, expected_key: str):
    """Test `add_empty_lang` adds the specified language with an empty set if it does not exist.

    :param lang: The language code to add.
    :param expected_key: The expected language code key in `mls_dict` after addition.
    """
    mls = MultiLangString()
    mls.add_empty_lang(lang)
    assert expected_key in mls.mls_dict, f"Language '{expected_key}' not added as expected."
    assert mls.mls_dict[expected_key] == set(), f"Language '{expected_key}' does not map to an empty set."


@pytest.mark.parametrize(
    "lang",
    [
        "en",
        "FR",
        "es",
    ],
)
def test_add_empty_lang_does_not_overwrite_existing_languages(lang: str):
    """Test `add_empty_lang` does not overwrite existing languages with content.

    :param lang: The language code to test.
    """
    initial_texts = {"Hello", "World"}
    mls = MultiLangString({lang: initial_texts})
    mls.add_empty_lang(lang)
    assert mls.mls_dict[lang] == initial_texts, f"Existing texts for language '{lang}' were unexpectedly modified."


@pytest.mark.parametrize(
    "lang, expected_exception",
    [
        (123, TypeError),
        (None, TypeError),
        ([], TypeError),
        (True, TypeError),
    ],
)
def test_add_empty_lang_with_invalid_language_type(lang, expected_exception):
    """Test `add_empty_lang` raises TypeError for invalid language types.

    :param lang: The invalid language code to add.
    :param expected_exception: The type of exception expected to be raised.
    :param match_message: A substring of the expected error message to match against the raised exception.
    """
    mls = MultiLangString()
    with pytest.raises(expected_exception, match=TYPEERROR_MSG_SINGULAR):
        mls.add_empty_lang(lang)


@pytest.mark.parametrize(
    "lang, expected_dict",
    [
        ("  en  ", {"  en  ": set()}),  # Preserving leading/trailing spaces as significant
        ("fr ", {"fr ": set()}),  # Trailing space considered part of the language code
        (" de", {" de": set()}),  # Leading space considered part of the language code
        ("🌐 ", {"🌐 ": set()}),  # Trailing space with an emoji as a language code
        ("en\t", {"en\t": set()}),  # Tab character at the end of the language code
        ("\ten", {"\ten": set()}),  # Tab character at the beginning of the language code
        ("✨Sparkle✨", {"✨Sparkle✨": set()}),  # Emoji in the language code
        ("çç", {"çç": set()}),  # Special character in the language code
    ],
)
def test_add_empty_lang_valid_whitespace_cases(lang: str, expected_dict: dict):
    """Test valid handling of language codes with leading/trailing spaces.

    :param lang: The language code to add, potentially with spaces.
    :param expected_dict: The expected state of mls_dict after adding the language.
    """
    mls = MultiLangString()
    mls.add_empty_lang(lang)
    assert mls.mls_dict == expected_dict, f"Expected mls_dict to match {expected_dict}, but got {mls.mls_dict}."


@pytest.mark.parametrize(
    "initial_langs, new_lang, expected_dict",
    [
        ({"en": {"Hello"}}, "fr", {"en": {"Hello"}, "fr": set()}),
        ({"en": {"Hello"}, "FR": {"Oui"}}, "fr", {"en": {"Hello"}, "FR": {"Oui"}}),
        ({"en": {"Hello"}, "fr": {"Oui"}}, "fr", {"en": {"Hello"}, "fr": {"Oui"}}),
        ({"en": {"Hello"}, "fr": {"Oui"}}, "FR", {"en": {"Hello"}, "fr": {"Oui"}}),
        ({"en": {"Hello"}, "FR": {"Oui"}}, "FR", {"en": {"Hello"}, "FR": {"Oui"}}),
        ({"fr": {"Bonjour"}, "es": {"Hola"}}, "de", {"fr": {"Bonjour"}, "es": {"Hola"}, "de": set()}),
        ({"ru": {"Привет"}}, "🌐", {"ru": {"Привет"}, "🌐": set()}),  # Including an emoji language code
    ],
)
def test_add_empty_lang_preserves_existing_languages(initial_langs: dict, new_lang: str, expected_dict: dict):
    """Test adding a new empty language does not affect pre-existing languages in the MultiLangString.

    :param initial_langs: Initial languages and their texts in the MultiLangString.
    :param new_lang: New language code to add as empty.
    :param expected_dict: Expected state of the internal dictionary after adding the new language.
    """
    mls = MultiLangString(initial_langs)
    mls.add_empty_lang(new_lang)
    assert mls.mls_dict == expected_dict, (
        "Adding a new empty language incorrectly modified pre-existing languages "
        "or failed to add the new language as expected."
    )


def test_pref_lang():
    mls = MultiLangString()
    initial_pref_lang = mls.pref_lang
    mls.add_empty_lang("en")
    assert initial_pref_lang == mls.pref_lang
