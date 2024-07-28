import pytest
from langstring import Controller
from langstring import MultiLangString
from langstring import MultiLangStringFlag
from tests.conftest import TYPEERROR_MSG_SINGULAR


@pytest.mark.parametrize(
    "text, pref_lang, expected",
    [
        ("Hello", "en", True),  # Text present in preferred language
        ("Hello", "es", False),  # Text present in preferred language
        ("Hello", "En", True),  # Text present in preferred language
        ("Hello", "eS", False),  # Text present in preferred language
        ("Bonjour", "fr", False),  # Text not present in preferred language
        (
            "Hola",
            "es",
            True,
        ),  # Text present in non-preferred but available language, expected False since it's not the preferred language
        ("Hello", "de", False),  # Preferred language not available
        ("", "en", False),  # Empty text
    ],
)
def test_contains_text_in_pref_lang_valid_input(text: str, pref_lang: str, expected: bool):
    """
    Test if specific text exists in the preferred language.

    :param text: The text to search for.
    :param pref_lang: The preferred language set for the MultiLangString instance.
    :param expected: Expected result (True if text is found in preferred language, False otherwise).
    """
    mls = MultiLangString(mls_dict={"en": {"Hello"}, "es": {"Hola"}}, pref_lang=pref_lang)
    assert (
        mls.contains_text_in_pref_lang(text) == expected
    ), f"Expected {expected} for '{text}' in preferred language '{pref_lang}'"


@pytest.mark.parametrize(
    "text",
    [
        123,  # Invalid type: Integer
        None,  # Invalid type: None
        [],  # Invalid type: List
        {},  # Invalid type: Dictionary
    ],
)
def test_contains_text_in_pref_lang_invalid_input_type(text):
    """
    Test `contains_text_in_pref_lang` with invalid input types for text.

    :param text: Invalid text input to test.
    :raises TypeError: Expected when input type is not a string.
    """
    mls = MultiLangString()
    with pytest.raises(TypeError, match=TYPEERROR_MSG_SINGULAR):
        mls.contains_text_in_pref_lang(text)


# Test for flags' effect on contains_text_in_pref_lang
@pytest.mark.parametrize(
    "flag, text, pref_lang, setup_dict, expected",
    [
        (
            MultiLangStringFlag.STRIP_TEXT,
            "hello",
            "en",
            {"en": {"  hello  "}},
            True,
        ),
    ],
)
def test_contains_text_in_pref_lang_with_flags(flag, text, pref_lang, setup_dict, expected):
    """
    Test the effect of MultiLangString flags on `contains_text_in_pref_lang` method.

    :param flag: Flag to activate for the test.
    :param text: Text to search within the preferred language.
    :param pref_lang: Preferred language to search the text in.
    :param setup_dict: Dictionary to initialize the MultiLangString with.
    :param expected: Expected outcome of the search.
    """
    Controller.set_flag(flag, True)
    mls = MultiLangString(mls_dict=setup_dict, pref_lang=pref_lang)
    assert mls.contains_text_in_pref_lang(text) == expected, f"Flag '{flag}' affected search unexpectedly."


# Test for unusual but valid usage
@pytest.mark.parametrize(
    "text, pref_lang, setup_dict, expected",
    [
        ("こんにちは", "jp", {"jp": {"こんにちは"}, "en": {"Hello"}}, True),  # Non-Latin script
        ("👋", "emojis", {"emojis": {"👋"}, "en": {"Hello"}}, True),  # Emoji as valid text
    ],
)
def test_contains_text_in_pref_lang_unusual_usage(text, pref_lang, setup_dict, expected):
    """
    Test `contains_text_in_pref_lang` with unusual but valid inputs.

    :param text: Unusual text to search for.
    :param pref_lang: Preferred language set for the test.
    :param setup_dict: MultiLangString initialization dictionary.
    :param expected: Expected result of the method call.
    """
    mls = MultiLangString(mls_dict=setup_dict, pref_lang=pref_lang)
    assert (
        mls.contains_text_in_pref_lang(text) == expected
    ), f"Unusual but valid text '{text}' in language '{pref_lang}' was not handled as expected."
