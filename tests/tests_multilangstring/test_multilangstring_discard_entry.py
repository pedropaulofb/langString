import pytest
from langstring import Controller
from langstring import MultiLangString
from langstring import MultiLangStringFlag
from tests.conftest import TYPEERROR_MSG_SINGULAR


@pytest.fixture
def setup_mls():
    mls = MultiLangString()
    mls.add_entry("Hello", "en")
    mls.add_entry("World", "en")
    mls.add_entry("Bonjour", "fr")
    return mls


@pytest.mark.parametrize(
    "text, lang, expected_result",
    [
        ("Hello", "en", {"en": {"World"}, "fr": {"Bonjour"}}),
        ("World", "en", {"en": {"Hello"}, "fr": {"Bonjour"}}),
        ("Bonjour", "fr", {"en": {"Hello", "World"}, "fr": set()}),
        ("G'day", "en-AU", {"en": {"Hello", "World"}, "fr": {"Bonjour"}}),  # Discard from 'en-AU'
        ("你好", "zh-CN", {"en": {"Hello", "World"}, "fr": {"Bonjour"}}),  # Discard from 'zh-CN'
        ("Hello 😊", "en", {"en": {"Hello", "World"}, "fr": {"Bonjour"}}),  # Discard with emoji in 'en'
    ],
)
def test_discard_existing_entry(setup_mls, text, lang, expected_result):
    setup_mls.discard_entry(text, lang)
    assert setup_mls.mls_dict == expected_result, "Failed to remove existing entry"
    setup_mls.discard_entry(text, lang)
    assert setup_mls.mls_dict == expected_result, "Failed discard idempotency test"


def test_discard_non_existing_entry(setup_mls):
    setup_mls.discard_entry("Hola", "es")  # Non-existing entry and language
    # Assuming initial state from setup_mls fixture
    expected_result = {"en": {"Hello", "World"}, "fr": {"Bonjour"}}
    assert setup_mls.mls_dict == expected_result


def test_clean_empty_language_set(setup_mls):
    setup_mls.discard_entry("Bonjour", "fr", True)  # Removing last entry in 'fr'
    expected_result = {"en": {"Hello", "World"}}  # 'fr' should be removed
    assert setup_mls.mls_dict == expected_result


@pytest.mark.parametrize(
    "text, lang",
    [
        (123, "en"),  # Invalid text type
        ("Hello", 123),  # Invalid lang type
        (None, "en"),  # Invalid text type: None
        ("Hello", None),  # Invalid lang type: None
    ],
)
def test_discard_entry_invalid_type(setup_mls, text, lang):
    with pytest.raises(TypeError):
        setup_mls.discard_entry(text, lang)


@pytest.mark.parametrize(
    "text, lang, flag, expected_dict_before, expected_dict_after",
    [
        (
            "World",
            "EN",
            MultiLangStringFlag.LOWERCASE_LANG,
            {"en": {"Hello", "World"}, "fr": {"Bonjour"}},
            {"en": {"Hello"}, "fr": {"Bonjour"}},
        ),
        (
            "World",
            "eN",
            MultiLangStringFlag.LOWERCASE_LANG,
            {"en": {"Hello", "World"}, "fr": {"Bonjour"}},
            {"en": {"Hello"}, "fr": {"Bonjour"}},
        ),
        (
            "  Hello  ",
            "en",
            MultiLangStringFlag.STRIP_TEXT,
            {"en": {"Hello", "World"}, "fr": {"Bonjour"}},
            {"en": {"World"}, "fr": {"Bonjour"}},
        ),  # STRIP_TEXT effect
    ],
)
def test_discard_with_lowercase_lang_flag_effect(
    setup_mls, text, lang, flag, expected_dict_before, expected_dict_after
):
    Controller.set_flag(flag, True)
    assert setup_mls.mls_dict == expected_dict_before  # Ensure initial state is as expected
    setup_mls.discard_entry(text.strip(), lang)
    assert setup_mls.mls_dict == expected_dict_after


# Additional test for discarding empty string as text
@pytest.mark.parametrize(
    "lang, expected_dict",
    [
        ("en", {"en": {"World", "Hello"}, "fr": {"Bonjour"}}),
    ],
)
def test_discard_empty_string(setup_mls, lang, expected_dict):
    setup_mls.discard_entry("", lang)
    assert setup_mls.mls_dict == expected_dict, "Discarding empty string failed."


# Test for discarding with a very long string
def test_discard_very_long_string(setup_mls):
    long_text = "a" * 10000
    setup_mls.add_entry(long_text, "en")  # Adding before discarding
    setup_mls.discard_entry(long_text, "en")
    assert long_text not in setup_mls.mls_dict.get("en", {}), "Failed to discard very long string."


@pytest.mark.parametrize(
    "text, lang, setup_texts, expected_result",
    [
        # Discarding entries with unusual but valid language codes
        ("Hello", "xx-lol", {"xx-lol": {"Hello"}}, {"xx-lol": set()}),
        # Discarding very long strings
        ("a" * 10000, "en", {"en": {"a" * 10000}}, {"en": set()}),
        # Discarding strings composed entirely of whitespace characters
        ("   ", "en", {"en": {"   "}}, {"en": set()}),
        ("G'day", "en-AU", {"en-AU": {"G'day"}}, {"en-AU": set()}),
        ("Hello", "en_us", {"en_us": {"Hello"}}, {"en_us": set()}),
        ("你好", "zh-CN", {"zh-CN": {"你好"}}, {"zh-CN": set()}),  # Non-Latin characters
    ],
)
def test_discard_special_cases_off(text, lang, setup_texts, expected_result):
    mls = MultiLangString(mls_dict=setup_texts)
    mls.discard_entry(text, lang)
    assert mls.mls_dict == expected_result, "Special case discarding failed."


@pytest.mark.parametrize(
    "text, lang, setup_texts, expected_result",
    [
        # Discarding entries with unusual but valid language codes
        ("Hello", "xx-lol", {"xx-lol": {"Hello"}}, {}),
        # Discarding very long strings
        ("a" * 10000, "en", {"en": {"a" * 10000}}, {}),
        # Discarding strings composed entirely of whitespace characters
        ("   ", "en", {"en": {"   "}}, {}),
        ("G'day", "en-AU", {"en-AU": {"G'day"}}, {}),
        ("Hello", "en_us", {"en_us": {"Hello"}}, {}),
        ("你好", "zh-CN", {"zh-CN": {"你好"}}, {}),  # Non-Latin characters
    ],
)
def test_discard_special_cases_on(text, lang, setup_texts, expected_result):
    mls = MultiLangString(mls_dict=setup_texts)
    mls.discard_entry(text, lang, True)
    assert mls.mls_dict == expected_result, "Special case discarding failed."


@pytest.mark.parametrize(
    "initial_dict, text, lang, expected_dict",
    [
        # Test clearing empty language set after discarding with clean_empty arg
        ({"en": {"Hello"}, "fr": set()}, "Hello", "en", {"fr": set()}),
    ],
)
def test_discard_with_clean_empty_effect(initial_dict, text, lang, expected_dict):
    mls = MultiLangString(mls_dict=initial_dict)
    mls.discard_entry(text, lang, True)
    assert mls.mls_dict == expected_dict, f"Discard with clean_empty effect failed."


@pytest.mark.parametrize(
    "setup_texts, lang_to_discard, expected_result",
    [
        ({"en": set(), "fr": set(), "es": {"Hola"}}, "fr", {"en": set(), "fr": set(), "es": {"Hola"}}),
    ],
)
def test_clear_multiple_empty_language_sets(setup_mls, setup_texts, lang_to_discard, expected_result):
    mls = MultiLangString(mls_dict=setup_texts)
    mls.discard_entry("", lang_to_discard)  # Discarding empty string trying to trigger language set clearance
    assert mls.mls_dict == expected_result, "No language should be cleared, as the entry is not removing anything."


# Test for attempting to discard an entry from a language that exists but the entry does not
@pytest.mark.parametrize(
    "text, lang, expected_result",
    [
        ("NonExistent", "en", {"en": {"Hello", "World"}, "fr": {"Bonjour"}}),
    ],
)
def test_discard_nonexistent_entry_existing_lang(setup_mls, text, lang, expected_result):
    setup_mls.discard_entry(text, lang)
    assert (
        setup_mls.mls_dict == expected_result
    ), "Incorrect behavior when discarding non-existing entry in existing language."


# Test for attempting to discard an entry that neither exists in the specified language nor the language exists
@pytest.mark.parametrize(
    "text, lang, expected_result",
    [
        ("NonExistent", "de", {"en": {"Hello", "World"}, "fr": {"Bonjour"}}),
    ],
)
def test_discard_nonexistent_entry_nonexistent_lang(setup_mls, text, lang, expected_result):
    setup_mls.discard_entry(text, lang)
    assert setup_mls.mls_dict == expected_result, "Incorrect behavior when discarding entry in non-existing language."


@pytest.mark.parametrize(
    "text, lang, flag, expected_dict_before, expected_dict_after",
    [
        (
            "Hello",
            "EN",
            MultiLangStringFlag.LOWERCASE_LANG,
            {"en": {"Hello", "World"}, "fr": {"Bonjour"}},
            {"en": {"World"}, "fr": {"Bonjour"}},
        ),
    ],
)
def test_discard_case_insensitive_lang(setup_mls, text, lang, flag, expected_dict_before, expected_dict_after):
    Controller.set_flag(flag, True)
    setup_mls.discard_entry(text, lang)
    assert setup_mls.mls_dict == expected_dict_after, "Case-insensitive language code discard failed."


# Discarding entries after changing the preferred language
@pytest.mark.parametrize(
    "initial_pref_lang, new_pref_lang, text_to_discard, lang, expected_dict",
    [
        ("en", "fr", "Hello", "en", {"en": {"World"}, "fr": {"Bonjour"}}),
    ],
)
def test_discard_after_changing_pref_lang(
    setup_mls, initial_pref_lang, new_pref_lang, text_to_discard, lang, expected_dict
):
    setup_mls.pref_lang = new_pref_lang
    setup_mls.discard_entry(text_to_discard, lang)
    assert setup_mls.mls_dict == expected_dict, "Discarding entry after changing preferred language failed."


# Discarding entries with special characters or emojis
@pytest.mark.parametrize(
    "text, lang, expected_result",
    [
        ("Hello 😊", "en", {"en": {"Hello", "World"}, "fr": {"Bonjour"}}),
        ("Special&Char*", "en", {"en": {"Hello", "World"}, "fr": {"Bonjour"}}),
    ],
)
def test_discard_special_characters_emojis(setup_mls, text, lang, expected_result):
    setup_mls.discard_entry(text, lang)
    assert setup_mls.mls_dict == expected_result, "Failed to discard entries with special characters or emojis."


# Effect of STRIP_TEXT flag on discarding entries
@pytest.mark.parametrize(
    "text, lang, flag, setup_texts, expected_result",
    [
        (
            "  Hello  ",
            "en",
            MultiLangStringFlag.STRIP_TEXT,
            {"en": {"  Hello  "}, "fr": {"Bonjour"}},
            {"en": {"Hello"}, "fr": {"Bonjour"}},
        ),
    ],
)
def test_discard_with_strip_text_flag_effect(setup_mls, text, lang, flag, setup_texts, expected_result):
    Controller.set_flag(flag, True)
    mls = MultiLangString(mls_dict=setup_texts)
    mls.discard_entry(text, lang)
    assert mls.mls_dict == expected_result, "Discard with STRIP_TEXT flag effect failed."
    Controller.reset_flag(flag)


@pytest.mark.parametrize(
    "setup_texts, expected_dict",
    [
        ({}, {}),  # Initial state with all languages empty
    ],
)
def test_discard_from_all_empty_languages(setup_mls, setup_texts, expected_dict):
    mls = MultiLangString(mls_dict=setup_texts)
    mls.discard_entry("Hello", "en")
    assert mls.mls_dict == expected_dict


@pytest.mark.parametrize("clean_empty", [True, False])
def test_discard_last_entry_with_clean_empty_option(setup_mls, clean_empty):
    """Test discarding the last entry in a language with clean_empty option.

    :param setup_mls: Fixture for setting up a MultiLangString instance.
    :param clean_empty: Boolean flag to test both behaviors of clean_empty.
    """
    setup_mls.discard_entry("Bonjour", "fr", clean_empty=clean_empty)
    expected = {"en": {"Hello", "World"}} if clean_empty else {"en": {"Hello", "World"}, "fr": set()}
    assert setup_mls.mls_dict == expected, "Discard last entry with clean_empty={} did not behave as expected.".format(
        clean_empty
    )


@pytest.mark.parametrize("text,lang,clean_empty", [("NonExistent", "en", True), ("Hello", "nonexistent", True)])
def test_discard_nonexistent_with_clean_empty(setup_mls, text, lang, clean_empty):
    """Test discarding a non-existent entry or language with clean_empty=True does not alter the dictionary.

    :param setup_mls: Fixture for setting up a MultiLangString instance.
    :param text: Text to discard.
    :param lang: Language code of the text to discard.
    :param clean_empty: Boolean flag indicating whether to clean empty languages.
    """
    initial_dict = setup_mls.mls_dict.copy()
    setup_mls.discard_entry(text, lang, clean_empty=clean_empty)
    assert (
        setup_mls.mls_dict == initial_dict
    ), "Discarding non-existent entry or language with clean_empty=True should not alter the mls_dict."


@pytest.mark.parametrize("text,lang", [(123, "en"), ("Hello", 123)])
def test_discard_invalid_types_with_clean_empty(setup_mls, text, lang):
    """Test discarding entry with invalid types for text and lang parameters, ensuring TypeError is raised.

    :param setup_mls: Fixture for setting up a MultiLangString instance.
    :param text: Text to discard, intentionally of incorrect type.
    :param lang: Language code of the text, intentionally of incorrect type.
    """
    with pytest.raises(TypeError, match=TYPEERROR_MSG_SINGULAR):
        setup_mls.discard_entry(text, lang, clean_empty=True)
