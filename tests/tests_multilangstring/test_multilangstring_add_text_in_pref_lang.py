import pytest
from langstring import MultiLangString
from tests.conftest import TYPEERROR_MSG_SINGULAR


@pytest.mark.parametrize(
    "initial_dict, pref_lang, text_to_add, expected_dict",
    [
        ({}, "en", "Hello", {"en": {"Hello"}}),  # Basic addition
        ({"en": {"Hello"}}, "en", "World", {"en": {"Hello", "World"}}),  # Adding another text
        ({"fr": {"Bonjour"}}, "fr", "Salut", {"fr": {"Bonjour", "Salut"}}),
        ({"en": set(), "fr": {"Bonjour"}}, "en", "Greetings", {"en": {"Greetings"}, "fr": {"Bonjour"}}),
        ({"fr": {"Bonjour"}}, "fr", "Salut", {"fr": {"Bonjour", "Salut"}}),  # In another language
        (
            {"en": {"Hello"}, "fr": {"Bonjour"}},
            "en",
            "Greetings",
            {"en": {"Hello", "Greetings"}, "fr": {"Bonjour"}},
        ),  # Multiple languages
        # Dynamic pref_lang change
        (
            {"en": {"Hello"}},
            "fr",
            "Bonjour",
            {"en": {"Hello"}, "fr": {"Bonjour"}},
        ),  # Changing pref_lang then adding text
        # Special characters and emojis
        ({"en": {"Hello"}}, "en", "Café", {"en": {"Hello", "Café"}}),  # Special characters
        ({"en": {"Hello"}}, "en", "😀", {"en": {"Hello", "😀"}}),  # Emojis
        # Duplicate text
        ({"en": {"Hello"}}, "en", "Hello", {"en": {"Hello"}}),  # Adding duplicate text
    ],
)
def test_add_text_in_pref_lang(initial_dict: dict, pref_lang: str, text_to_add: str, expected_dict: dict):
    """Tests adding text to the preferred language in MultiLangString.

    :param initial_dict: Initial dictionary setup for mls_dict.
    :param pref_lang: Preferred language to add text to.
    :param text_to_add: Text to be added to the preferred language set.
    :param expected_dict: Expected mls_dict after adding the text.
    """
    mls = MultiLangString(mls_dict=initial_dict, pref_lang=pref_lang)
    mls.add_text_in_pref_lang(text_to_add)
    assert (
        mls.mls_dict == expected_dict
    ), f"Text '{text_to_add}' was not correctly added to the '{pref_lang}' language set."


@pytest.mark.parametrize(
    "text_to_add, expected_error",
    [
        (123, TypeError),
        ([], TypeError),
    ],
)
def test_add_text_in_pref_lang_invalid_type(text_to_add, expected_error):
    """Tests adding invalid types as text to the preferred language, expecting TypeError.

    :param text_to_add: Text to be added, with invalid type.
    :param expected_error: Expected error type.
    """
    mls = MultiLangString(pref_lang="en")
    with pytest.raises(expected_error, match=TYPEERROR_MSG_SINGULAR):
        mls.add_text_in_pref_lang(text_to_add)


# Test for adding text with null value
@pytest.mark.parametrize(
    "text_to_add, expected_error",
    [
        (None, TypeError),
    ],
)
def test_add_text_in_pref_lang_with_null(text_to_add, expected_error):
    """Tests adding a None value as text, expecting TypeError."""
    mls = MultiLangString(pref_lang="en")
    with pytest.raises(expected_error, match=TYPEERROR_MSG_SINGULAR):
        mls.add_text_in_pref_lang(text_to_add)


# Test for edge case: adding extremely long string
def test_add_text_in_pref_lang_long_string():
    """Tests adding an extremely long string to the preferred language."""
    long_text = "a" * 10000  # Very long string
    mls = MultiLangString(pref_lang="en")
    mls.add_text_in_pref_lang(long_text)
    assert long_text in mls.mls_dict["en"], "Long text was not correctly added."


def test_add_text_in_pref_lang_empty_string():
    """Tests adding an empty string to the preferred language."""
    mls = MultiLangString(pref_lang="en")
    mls.add_text_in_pref_lang("")
    assert "" in mls.mls_dict["en"], "Empty text was not correctly added."


@pytest.mark.parametrize(
    "initial_dict, initial_pref_lang, text_to_add, expected_dict_after_addition",
    [
        # Case when pref_lang is not initially set in mls_dict
        ({}, None, "New Text", {"en": {"New Text"}}),
        # Adding text to a new pref_lang not initially present in mls_dict
        ({"en": {"Hello"}}, "fr", "Bonjour", {"en": {"Hello"}, "fr": {"Bonjour"}}),
    ],
)
def test_add_text_in_new_pref_lang(initial_dict, initial_pref_lang, text_to_add, expected_dict_after_addition):
    """Tests adding text to a preferred language that is not initially set in mls_dict."""
    if initial_pref_lang is None:
        mls = MultiLangString(mls_dict=initial_dict)
    else:
        mls = MultiLangString(mls_dict=initial_dict, pref_lang=initial_pref_lang)
    mls.add_text_in_pref_lang(text_to_add)
    assert mls.mls_dict == expected_dict_after_addition, "Text not correctly added to new pref_lang."


def test_change_pref_lang_then_add_text():
    """Tests changing pref_lang after adding texts and then adding more texts."""
    mls = MultiLangString(pref_lang="en")
    mls.add_text_in_pref_lang("Hello")
    mls.pref_lang = "fr"
    mls.add_text_in_pref_lang("Bonjour")
    assert mls.mls_dict == {
        "en": {"Hello"},
        "fr": {"Bonjour"},
    }, "mls_dict not correctly updated after pref_lang change."


@pytest.mark.parametrize(
    "text_to_add",
    [
        (" "),
        ("\t"),
        ("\n"),
    ],
)
def test_add_unusual_valid_text(text_to_add):
    """Tests adding strings that are valid but unusual, such as whitespace characters."""
    mls = MultiLangString(pref_lang="en")
    mls.add_text_in_pref_lang(text_to_add)
    assert text_to_add in mls.mls_dict["en"], f"Unusual text '{text_to_add}' not correctly added."


import pytest
from langstring import MultiLangString, Controller, MultiLangStringFlag


@pytest.mark.parametrize(
    "flag, flag_value, text, expected_result",
    [
        (
            MultiLangStringFlag.LOWERCASE_LANG,
            True,
            "Hello",
            {"en": {"Hello"}},
        ),  # Assuming pref_lang is 'EN' but should be treated as 'en'
        (MultiLangStringFlag.STRIP_TEXT, True, "  World  ", {"en": {"World"}}),  # Assuming pref_lang is 'en'
    ],
)
def test_add_text_in_pref_lang_with_flags(flag, flag_value, text, expected_result):
    """Tests the effect of flags on adding text in the preferred language."""
    Controller.set_flag(flag, flag_value)
    mls = MultiLangString(pref_lang="EN" if flag == MultiLangStringFlag.LOWERCASE_LANG else "en")
    mls.add_text_in_pref_lang(text)
    assert mls.mls_dict == expected_result, "The text was not added correctly considering the flag effects."
