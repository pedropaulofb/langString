import pytest
from langstring import LangString
from langstring import MultiLangString
from langstring import SetLangString


@pytest.mark.parametrize(
    "text, lang, clean_empty, expected_error",
    [
        (("test1", "en", False, None)),
        (("test1", "EN", False, None)),
        (("test1", " en", False, ValueError)),
        (("test1 ", "en", False, ValueError)),
        (("test1", "en ", False, ValueError)),
        (("nonexistent", "en", False, ValueError)),
        (("nonexistent", "EN", False, ValueError)),
        (("test2", "fr", True, None)),
        (("test3", "de", False, ValueError)),
        (" ", "en", False, ValueError),  # Test with space as text
        ("", "en", False, ValueError),  # Test with empty string as text
        ("Γειά", "gr", False, ValueError),  # Test with Greek characters
        ("Привет", "ru", False, ValueError),  # Test with Cyrillic characters
        ("👋", "emoji", False, ValueError),  # Test with emoji as text
        ("test1 ", "en", False, ValueError),  # Test with trailing space in text
        (" te st2", "fr", False, ValueError),  # Test with spaces inside text
        ("TEST1", "EN", False, ValueError),  # Test with uppercase
    ],
)
def test_remove_entry(text: str, lang: str, clean_empty: bool, expected_error):
    """Test the removal of entries from a MultiLangString instance.

    :param text: The text to be removed.
    :param lang: The language of the text to be removed.
    :param clean_empty: Whether to remove the language key if its set becomes empty after removal.
    :param expected_error: The expected error if the operation is supposed to fail.
    """
    mls = MultiLangString({"en": {"test1", "test2"}, "fr": {"test2"}})
    if expected_error:
        with pytest.raises(expected_error, match=f".*{text}@{lang}.*"):
            mls.remove((text, lang), clean_empty)
    else:
        mls.remove((text, lang), clean_empty)
        assert text not in mls.mls_dict.get(lang, set()), f"Text '{text}' should have been removed from '{lang}'."


def test_remove_nonexistent_entry_raises_value_error():
    """Test that removing a nonexistent entry raises a ValueError."""
    mls = MultiLangString({"en": {"hello"}})
    with pytest.raises(ValueError, match=".*not found in the MultiLangString."):
        mls.remove(("nonexistent", "en"), clean_empty=False)


@pytest.mark.parametrize(
    "text, lang, expected_contents",
    [
        ("hello", "en", {"world"}),
        ("world", "en", {"hello"}),
        ("salut", "fr", set()),
    ],
)
def test_remove_langstring_object(text: str, lang: str, expected_contents: set):
    """Test removing a LangString object from the MultiLangString with various cases.

    :param text: The text to be removed.
    :param lang: The language of the text to be removed.
    :param expected_contents: Expected contents of the MultiLangString after removal.
    """
    ls = LangString(text, lang)
    mls = MultiLangString({"en": {"hello", "world"}, "fr": {"salut"}})
    mls.remove(ls)
    assert mls.mls_dict.get(lang, set()) == expected_contents, f"After removing {text}, contents mismatch."


@pytest.mark.parametrize(
    "texts, lang, expected_contents, mls_setup, clean_empty",
    [
        ({"hello", "world"}, "en", set(), {"en": {"hello", "world"}, "fr": {"salut"}}, False),
        ({"salut"}, "fr", set(), {"en": {"hello", "world"}, "fr": {"salut"}}, False),
        ({"hello"}, "en", {"world"}, {"en": {"hello", "world"}}, False),
        ({"bye"}, "en", {"hello", "world"}, {"en": {"hello", "world", "bye"}}, False),
        ({"bonjour"}, "fr", set(), {"fr": {"bonjour"}}, True),
        ({"こんにちは"}, "jp", set(), {"jp": {"こんにちは"}}, False),
        ({"👋", "world"}, "en", {"hello"}, {"en": {"hello", "world", "👋"}}, False),
        ({"", " "}, "en", {"hello", "world"}, {"en": {"hello", "world", "", " "}}, False),
        ({"HELLO"}, "en", {"hello", "world"}, {"en": {"hello", "world", "HELLO"}}, False),
        # Removing entries across multiple languages is not a valid case as SetLangString is language-specific.
    ],
)
def test_remove_setlangstring_object(texts: set, lang: str, expected_contents: set, mls_setup: dict, clean_empty: bool):
    """Test removing a SetLangString object from the MultiLangString with various cases.

    :param texts: The set of texts to be removed.
    :param lang: The language of the texts to be removed.
    :param expected_contents: Expected contents of the MultiLangString after removal.
    :param mls_setup: The initial setup of the MultiLangString.
    :param clean_empty: Whether to clean up the language entry if it becomes empty after removal.
    """
    sls = SetLangString(texts, lang)
    mls = MultiLangString(mls_setup)
    mls.remove(sls, clean_empty=clean_empty)
    assert (
        mls.mls_dict.get(lang, set()) == expected_contents
    ), f"After removing {texts} with clean_empty={clean_empty}, contents mismatch."


@pytest.mark.parametrize(
    "remove_contents, expected_results, mls_setup, clean_empty",
    [
        (
            {"en": {"hello"}, "fr": {"salut"}},
            {"en": {"world"}, "fr": set()},
            {"en": {"hello", "world"}, "fr": {"salut"}},
            False,
        ),
        ({"en": {"world"}}, {"en": {"hello"}, "fr": {"salut"}}, {"en": {"hello", "world"}, "fr": {"salut"}}, True),
        (
            {"en": {" "}, "fr": {"salut"}},
            {"en": {"hello", "world"}, "fr": set()},
            {"en": {"hello", "world", " "}, "fr": {"salut"}},
            False,
        ),
        (
            {"en": {" "}, "fr": {"salut"}},
            {"en": {"hello", "world"}},
            {"en": {"hello", "world", " "}, "fr": {"salut"}},
            True,
        ),
        (
            {"en": {"👋"}, "emoji": {"👍"}},
            {"en": {"hello", "world"}},
            {"en": {"hello", "world", "👋"}, "emoji": {"👍"}},
            True,
        ),
        (
            {"ru": {"Привет"}},
            {"ru": set(), "en": {"hello", "world"}, "fr": {"salut"}},
            {"ru": {"Привет"}, "en": {"hello", "world"}, "fr": {"salut"}},
            False,
        ),
        (
            {"gr": {"Γειά"}},
            {"gr": set(), "en": {"hello", "world"}, "fr": {"salut"}},
            {"gr": {"Γειά"}, "en": {"hello", "world"}, "fr": {"salut"}},
            False,
        ),
        (
            {"gr": {"Γειά"}},
            {"en": {"hello", "world"}, "fr": {"salut"}},
            {"gr": {"Γειά"}, "en": {"hello", "world"}, "fr": {"salut"}},
            True,
        ),
    ],
)
def test_remove_multilangstring_object(
    remove_contents: dict, expected_results: dict, mls_setup: dict, clean_empty: bool
):
    mls_to_remove = MultiLangString(remove_contents)
    mls = MultiLangString(mls_setup)
    mls.remove(mls_to_remove, clean_empty=clean_empty)
    for lang, texts in expected_results.items():
        assert (
            mls.mls_dict.get(lang, set()) == texts
        ), f"After removing contents with clean_empty={clean_empty}, mismatch in {lang}."
    # New assertion to check for the presence or absence of languages, ensuring clean_empty logic is correctly applied.
    for lang in mls_setup.keys():
        assert (lang in mls.mls_dict) == (
            expected_results.get(lang, None) is not None
        ), f"Language {lang} presence/absence mismatch with clean_empty={clean_empty}."


def test_remove_clean_empty_removes_lang():
    """Test if 'clean_empty=True' removes the language key after entry removal."""
    mls = MultiLangString({"en": {"single_entry"}})
    mls.remove(("single_entry", "en"), clean_empty=True)
    assert "en" not in mls.mls_dict, "'en' should have been removed after last entry was removed."


@pytest.mark.parametrize(
    "text, lang, expected_exception, expected_message",
    [
        (123, "en", TypeError, "Argument .+ must be of type"),
        ("hello", 123, TypeError, "Argument .+ must be of type"),
        ("", "", ValueError, "Entry '@' not found in the MultiLangString."),
    ],
)
def test_remove_with_invalid_types_and_values(text, lang, expected_exception, expected_message):
    """Test the removal of entries with invalid types and empty values.

    :param text: The text to be removed, testing for invalid types.
    :param lang: The language code, testing for invalid types.
    :param expected_exception: The expected exception type.
    :param expected_message: The expected error message part.
    """
    mls = MultiLangString({"en": {"hello"}})
    with pytest.raises(expected_exception, match=expected_message):
        mls.remove((text, lang), clean_empty=False)


@pytest.mark.parametrize(
    "text, lang, clean_empty",
    [
        ("single_entry", "en", True),
    ],
)
def test_remove_entry_leading_to_empty_language(text, lang, clean_empty):
    """Test removal of the only entry in a language, checking clean_empty behavior.

    :param text: The text to be removed.
    :param lang: The language of the text.
    :param clean_empty: Specifies if the language should be removed if it becomes empty.
    """
    mls = MultiLangString({lang: {text}})
    mls.remove((text, lang), clean_empty)
    assert lang not in mls.mls_dict, f"Language '{lang}' should have been removed as it's empty."


@pytest.mark.parametrize(
    "self_content, expected_result",
    [
        ({"en": {"hello"}}, {"en": set()}),
    ],
)
def test_remove_operation_on_itself(self_content, expected_result):
    """Test the remove operation with the MultiLangString object removing entries from itself.

    :param self_content: The initial content of the MultiLangString object.
    :param expected_result: The expected content of the MultiLangString object after removal.
    """
    mls = MultiLangString(self_content)
    with pytest.raises(RuntimeError, match="Set changed size during iteration"):
        mls.remove(mls)
