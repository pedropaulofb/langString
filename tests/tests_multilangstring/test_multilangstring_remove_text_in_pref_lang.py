import pytest
from langstring import MultiLangString


@pytest.mark.parametrize(
    "initial_contents, pref_lang, text_to_remove, clean_empty, expected_contents",
    [
        # Default case with existing text in preferred language
        ({"en": {"hello", "world"}}, "en", "hello", False, {"en": {"world"}}),
        # Empty set, clean_empty True
        ({"en": {"hello"}}, "en", "hello", True, {}),
        # Empty set, clean_empty False
        ({"en": {"hello"}}, "en", "hello", False, {"en": set()}),
        # Text with leading and trailing spaces
        ({"en": {"  hello  ", "world"}}, "en", "  hello  ", False, {"en": {"world"}}),
        # Text in uppercase
        ({"en": {"HELLO", "world"}}, "en", "HELLO", False, {"en": {"world"}}),
        # Text in mixed case
        ({"en": {"HeLLo", "world"}}, "en", "HeLLo", False, {"en": {"world"}}),
        # Text with special characters
        ({"en": {"hello!", "world"}}, "en", "hello!", False, {"en": {"world"}}),
        # Text with emojis
        ({"en": {"hello 😊", "world"}}, "en", "hello 😊", False, {"en": {"world"}}),
        # Non-ASCII characters (Cyrillic)
        ({"ru": {"привет", "мир"}}, "ru", "привет", False, {"ru": {"мир"}}),
        # Non-ASCII characters (Greek)
        ({"el": {"γειά", "σου"}}, "el", "γειά", False, {"el": {"σου"}}),
        # Text with spaces only
        ({"en": {" ", "world"}}, "en", " ", False, {"en": {"world"}}),
    ],
)
def test_remove_text_in_pref_lang_valid_cases(
    initial_contents, pref_lang, text_to_remove, clean_empty, expected_contents
):
    """Test removing a text in the preferred language from MultiLangString under various valid conditions.

    :param initial_contents: Initial contents of the MultiLangString instance.
    :param pref_lang: The preferred language for this test instance.
    :param text_to_remove: The text to be removed from the preferred language.
    :param clean_empty: Whether to clean up the language entry if it becomes empty after removal.
    :param expected_contents: Expected contents of the MultiLangString after the removal operation.
    """
    mls = MultiLangString(initial_contents, pref_lang=pref_lang)
    mls.remove_text_in_pref_lang(text_to_remove, clean_empty=clean_empty)
    assert (
        mls.mls_dict == expected_contents
    ), "The MultiLangString contents after removal did not match the expected result."


@pytest.mark.parametrize(
    "initial_contents, pref_lang, text_to_remove, clean_empty, expected_exception, expected_message",
    [
        # Removing text not in preferred language
        (
            {"en": {"world"}, "fr": {"bonjour"}},
            "en",
            "bonjour",
            False,
            ValueError,
            "Entry 'bonjour@en' not found in the MultiLangString.",
        ),
        # Invalid type for text_to_remove
        (
            {"en": {"hello"}},
            "en",
            123,
            False,
            TypeError,
            r"Invalid argument with value '.+?'. Expected '.+?', but got '.+?'\.",
        ),
        # Removing text from a non-existent language
        ({"en": {"hello"}}, "fr", "bonjour", False, ValueError, "Entry 'bonjour@fr' not found in the MultiLangString."),
        # Text to remove is empty string
        ({"en": {"hello", "world"}}, "en", "", False, ValueError, "Entry '@en' not found in the MultiLangString."),
        # Text with emojis that does not exist
        (
            {"en": {"hello", "world"}},
            "en",
            "goodbye 😊",
            False,
            ValueError,
            "Entry 'goodbye 😊@en' not found in the MultiLangString.",
        ),
        # Non-ASCII text not found
        (
            {"ru": {"привет", "мир"}},
            "ru",
            "до свидания",
            False,
            ValueError,
            "Entry 'до свидания@ru' not found in the MultiLangString.",
        ),
    ],
)
def test_remove_text_in_pref_lang_invalid_cases(
    initial_contents, pref_lang, text_to_remove, clean_empty, expected_exception, expected_message
):
    """Test removing a text in the preferred language from MultiLangString under various invalid conditions.

    :param initial_contents: Initial contents of the MultiLangString instance.
    :param pref_lang: The preferred language for this test instance.
    :param text_to_remove: The text to be removed from the preferred language.
    :param clean_empty: Whether to clean up the language entry if it becomes empty after removal.
    :param expected_exception: Expected exception type if an error is expected.
    :param expected_message: Expected message in the exception if an error is expected.
    """
    mls = MultiLangString(initial_contents, pref_lang=pref_lang)
    with pytest.raises(expected_exception, match=expected_message):
        mls.remove_text_in_pref_lang(text_to_remove, clean_empty=clean_empty)
