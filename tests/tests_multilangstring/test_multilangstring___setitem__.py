import pytest
from langstring import Controller
from langstring import MultiLangString
from langstring import MultiLangStringFlag
from tests.conftest import TYPEERROR_MSG_SINGULAR


# Test setting new language entries
@pytest.mark.parametrize(
    "lang, texts, expected",
    [
        ("en", {"Hello", "World"}, {"en": {"Hello", "World"}}),
        ("fr", {"Bonjour", "Monde"}, {"fr": {"Bonjour", "Monde"}}),
        ("Ελ", {"Γειά", "Κόσμος"}, {"Ελ": {"Γειά", "Κόσμος"}}),  # Greek characters
        ("Ру", {"Привет", "Мир"}, {"Ру": {"Привет", "Мир"}}),  # Cyrillic characters
        ("👋", {"😃", "🌍"}, {"👋": {"😃", "🌍"}}),  # Emojis
        ("en@", {"Hello&", "<World>"}, {"en@": {"Hello&", "<World>"}}),  # Special characters
        ("", set(), {"": set()}),  # Adding a new language with an empty set of texts
    ],
)
def test_setitem_new_language(lang: str, texts: set, expected: dict):
    """Test setting text entries for a new language updates the MultiLangString correctly.

    :param lang: Language code for the text entries.
    :param texts: A set of text entries to add.
    :param expected: Expected internal dictionary after the operation.
    """
    mls = MultiLangString()
    mls[lang] = texts
    assert mls.mls_dict == expected, f"Setting new language {lang} failed to update mls_dict as expected."


@pytest.mark.parametrize(
    "initial_dict, lang, new_texts, expected_dict",
    [
        ({"en": {"Hello"}}, "en", {"World"}, {"en": {"World"}}),
        ({"en": {"Hello"}}, "en-us", {"World"}, {"en": {"Hello"}, "en-us": {"World"}}),
        ({"fr": {"Bonjour"}}, "fr", {"Salut"}, {"fr": {"Salut"}}),
        ({"de": {"Guten Tag"}}, "de", {"Hallo"}, {"de": {"Hallo"}}),
        ({"es": {"Hola"}}, "es", {"Adiós"}, {"es": {"Adiós"}}),
        ({"pt": {"Olá"}}, "pt", {"Tchau"}, {"pt": {"Tchau"}}),
        ({"en": set()}, "en", {"Hello"}, {"en": {"Hello"}}),  # Test updating an empty set
        (
            {"en ": {"Hello"}},
            "en ",
            {"World", " Everyone"},
            {"en ": {"World", " Everyone"}},
        ),  # Space in language code
        ({"es": {"Hola"}}, "es", {"", "Adiós"}, {"es": {"", "Adiós"}}),  # Empty string as text
    ],
)
def test_setitem_update_existing_language(initial_dict, lang, new_texts, expected_dict):
    """Test updating an existing language with new texts correctly merges those texts.

    :param initial_dict: The initial state of the MultiLangString's internal dictionary.
    :param lang: The language code to update.
    :param new_texts: The new texts to add to the specified language.
    :param expected_dict: The expected state of the internal dictionary after the update.
    """
    mls = MultiLangString(initial_dict)
    mls[lang] = new_texts
    assert (
        mls.mls_dict == expected_dict
    ), f"Failed to update {lang} correctly. Expected {expected_dict}, got {mls.mls_dict}."


@pytest.mark.parametrize(
    "lang, texts, expected_exception, match_message",
    [
        (123, {"Hello"}, TypeError, "Invalid argument with value '.+'. Expected 'str', but got 'int'."),
        ("en", None, TypeError, "Invalid argument with value 'None'. Expected 'set', but got 'NoneType'."),
        ("en", {None}, TypeError, "Invalid argument with value 'None'. Expected 'str', but got 'NoneType'."),
        (None, {"Hello"}, TypeError, "Invalid argument with value '.+'. Expected 'str', but got 'NoneType'."),
        ("en", ["Hello"], TypeError, r"Invalid argument with value '\['Hello'\]'. Expected 'set', but got 'list'."),
        ("en", {"Hello", 123}, TypeError, "Invalid argument with value '123'. Expected 'str', but got 'int'."),
        ("en", {"Hello", None}, TypeError, "Invalid argument with value 'None'. Expected 'str', but got 'NoneType'."),
        (True, {"World"}, TypeError, "Invalid argument with value '.+'. Expected 'str', but got 'bool'."),
        ("fr", "Bonjour", TypeError, "Invalid argument with value 'Bonjour'. Expected 'set', but got 'str'."),
        ([], {"Hello"}, TypeError, "Invalid argument with value '.+'. Expected 'str', but got 'list'."),
        ("de", 123, TypeError, "Invalid argument with value '123'. Expected 'set', but got 'int'."),
        ("en", {}, TypeError, "Invalid argument with value '{}'. Expected 'set', but got 'dict'."),  # Empty set
    ],
)
def test_setitem_invalid_inputs(lang, texts, expected_exception, match_message):
    """Test input validation for `__setitem__` rejects non-string languages and non-set texts.

    :param lang: The language code to test, which might be of an invalid type.
    :param texts: The texts to test, which might be of an invalid type or structure.
    :param expected_exception: The type of exception expected to be raised.
    :param match_message: A substring of the expected error message to match against the raised exception message.
    """
    mls = MultiLangString()
    with pytest.raises(expected_exception, match=match_message):
        mls[lang] = texts


@pytest.mark.parametrize(
    "first_lang, first_texts, second_lang, second_texts, expected_dict",
    [
        ("EN", {"Hello"}, "en", {"World"}, {"EN": {"World"}}),
        ("FR", {"Bonjour"}, "fr", {"Monde"}, {"FR": {"Monde"}}),
        ("de", {"Guten Tag"}, "DE", {"Hallo"}, {"de": {"Hallo"}}),
        ("ES", {"Hola"}, "es", {"Adiós"}, {"ES": {"Adiós"}}),
        ("pt", {"Olá"}, "PT", {"Tchau"}, {"pt": {"Tchau"}}),
        ("CASE", {"Test"}, "case", {"Another Test"}, {"CASE": {"Another Test"}}),  # Upper vs lower case
        ("Case", {"Mix"}, "cAsE", {"Mixed"}, {"Case": {"Mixed"}}),  # Mixed case variations
        ("Case", {"Mix"}, "cAsE", {"123", "Mixed"}, {"Case": {"123", "Mixed"}}),  # Mixed case variations
    ],
)
def test_setitem_language_case_insensitivity(first_lang, first_texts, second_lang, second_texts, expected_dict):
    """Verify language codes are treated case-insensitively when setting items.

    :param first_lang: First language code to add to the MultiLangString.
    :param first_texts: Set of texts associated with the first language code.
    :param second_lang: Second language code, differing only by case, to add to the MultiLangString.
    :param second_texts: Set of texts associated with the second language code.
    :param expected_dict: Expected internal dictionary after adding both sets of texts.
    """
    mls = MultiLangString()
    mls[first_lang] = first_texts
    mls[second_lang] = second_texts
    assert (
        mls.mls_dict == expected_dict
    ), f"Failed for {first_lang} and {second_lang}: Expected {expected_dict}, got {mls.mls_dict}"


@pytest.mark.parametrize(
    "lang, texts, expected_dict",
    [
        ("", {"Empty"}, {"": {"Empty"}}),  # Empty string as a language code
        ("  ", {"Whitespace"}, {"  ": {"Whitespace"}}),  # Whitespace as a language code
        ("en" * 100, {"LongLangCode"}, {"en" * 100: {"LongLangCode"}}),  # Unusually long language code
        ("  en", {"Leading space"}, {"  en": {"Leading space"}}),  # Leading space in language code
        ("en  ", {"Trailing space"}, {"en  ": {"Trailing space"}}),  # Trailing space in language code
        (" en ", {"Surrounding spaces"}, {" en ": {"Surrounding spaces"}}),  # Surrounding spaces in language code
        ("EN-en", {"Hyphen"}, {"EN-en": {"Hyphen"}}),  # Hyphen in language code
    ],
)
def test_setitem_unusual_valid_usage(lang, texts, expected_dict):
    """Test unusual but valid language codes and text entries."""
    mls = MultiLangString()
    mls[lang] = texts
    assert mls.mls_dict == expected_dict, "Failed to handle unusual, but valid scenarios."


@pytest.mark.parametrize(
    "flag, lang, text, expected",
    [
        (True, " en", {"Hello", "World"}, "en"),
        (False, " en", {"Hello", "World"}, " en"),
        (True, "en ", {" Hello", "World "}, "en"),  # Trailing spaces in text
        (False, " en", {" Hello ", " World "}, " en"),  # Spaces inside and around texts
    ],
)
def test_setitem_text_validation(flag: bool, lang: str, text: set, expected: str):
    """Check if texts are validated correctly based on current flags.

    :param flag: Flag state to test text stripping functionality.
    :param text: Input texts.
    """
    Controller.set_flag(MultiLangStringFlag.STRIP_LANG, flag)
    mls = MultiLangString()
    mls[lang] = text
    assert expected in mls, "Text validation failed to process as expected."


def test_pref_lang_unchanged_after_setitem():
    """Test that the pref_lang attribute remains unchanged after using the __setitem__ method."""
    initial_pref_lang = "en"
    mls = MultiLangString(pref_lang=initial_pref_lang)
    mls["fr"] = {"Bonjour", "Monde"}  # Modify the instance by adding French entries
    mls["es"] = {"Hola", "Mundo"}  # Add another language for good measure

    # Check that pref_lang is still what it was initially set to, indicating it hasn't been changed by __setitem__
    assert (
        mls.pref_lang == initial_pref_lang
    ), f"Expected pref_lang to remain '{initial_pref_lang}', but it was modified to '{mls.pref_lang}'."


@pytest.mark.parametrize(
    "initial_contents, key_to_set, value_to_set, expected_contents",
    [
        # Setting an entry with the empty string as key on an empty MultiLangString.
        ({}, "", {"An entry without language"}, {"": {"An entry without language"}}),
        # Updating an existing entry where the key is an empty string.
        (
            {"": {"Old entry without language"}},
            "",
            {"Updated entry without language"},
            {"": {"Updated entry without language"}},
        ),
        # Adding a new entry with the empty string as key alongside existing specified languages.
        ({"en": {"Hello"}}, "", {"No language entry"}, {"": {"No language entry"}, "en": {"Hello"}}),
        # Updating an existing entry with the empty string as key alongside other languages.
        (
            {"": {"Old no language entry"}, "fr": {"Bonjour"}},
            "",
            {"New no language entry"},
            {"": {"New no language entry"}, "fr": {"Bonjour"}},
        ),
        # Introducing the empty string entry in a MultiLangString containing multiple languages.
        (
            {"en": {"Hello"}, "fr": {"Bonjour"}},
            "",
            {"No language entry"},
            {"": {"No language entry"}, "en": {"Hello"}, "fr": {"Bonjour"}},
        ),
        # Replacing an existing empty string entry with a new set of texts.
        ({"": {"Some old text"}, "es": {"Hola"}}, "", {"Some new text"}, {"": {"Some new text"}, "es": {"Hola"}}),
    ],
)
def test_multilangstring_setitem_with_empty_string(initial_contents, key_to_set, value_to_set, expected_contents):
    """
    Test the `__setitem__` method of the MultiLangString class for handling the empty string as a key across various scenarios.

    :param initial_contents: The initial contents to populate the MultiLangString instance.
    :param key_to_set: The key (language code) where the value is to be set, focusing on the empty string.
    :param value_to_set: The value (set of texts) to set for the given key.
    :param expected_contents: The expected contents of the MultiLangString after setting the item.
    """
    mls = MultiLangString(initial_contents)
    mls[key_to_set] = value_to_set
    assert mls.mls_dict == expected_contents, "MultiLangString contents after setting item did not match expected."


@pytest.mark.parametrize(
    "invalid_value",
    [
        "Not a set",  # String instead of a set
        ["Not", "a", "set"],  # List instead of a set
        None,  # None value
        123,  # Integer instead of a set
        {},  # Empty dictionary instead of a set
    ],
)
def test_multilangstring_setitem_with_invalid_values(invalid_value):
    """
    Test the `__setitem__` method of the MultiLangString class with invalid value types for the empty string key.

    :param invalid_value: An invalid value to attempt setting for a given language code.
    """
    mls = MultiLangString()
    with pytest.raises(TypeError, match=TYPEERROR_MSG_SINGULAR):
        mls[""] = invalid_value
