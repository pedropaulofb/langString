import pytest
from langstring import MultiLangString


@pytest.mark.parametrize(
    "mls_setup, input_lang, expected_output",
    [
        ({"en": {"hello"}, "fr": {"bonjour"}}, "en", "en"),  # Standard case with common languages
        ({"en": {"hello"}, "fr": {"bonjour"}}, "EN", "en"),  # Test case insensitivity
        ({"en": {"hello"}, "fr": {"bonjour"}}, "eN", "en"),  # Test case insensitivity
        ({"de": {"hallo"}, "es": {"hola"}}, "de", "de"),  # Different language setup
        ({"de": {"hallo"}, "es": {"hola"}}, "ES", "es"),  # Case insensitivity with different setup
        ({"es": {"hola"}, "jp": {"こんにちは"}}, "es", "es"),  # Including a non-Latin alphabet language
        ({"es": {"hola"}, "jp": {"こんにちは"}}, "JP", "jp"),  # Non-Latin alphabet
        ({"en": {"hello"}, "fr": {"bonjour"}}, "es", None),  # Non-existent language
        ({"en": {"hello"}, "fr": {"bonjour"}}, "", None),  # Empty string as input
        ({"ru": {"привет"}}, "ru", "ru"),  # Cyrillic charset
        ({"gr": {"γειά σου"}}, "gr", "gr"),  # Greek charset
        ({"en": {"hello", " world "}, "fr": {"bonjour"}}, " world ", None),  # Input with spaces before and after
        (
            {"en": {"hello"}, "fr": {"bonjour", "😀"}},
            "😀",
            None,
        ),  # Emoji as input language (invalid case but to validate handling)
        ({"en": {"hello"}, "fr": {"bonjour"}}, "EN ", None),  # Space after uppercase language code
        ({"en": {"hello"}, "fr": {"bonjour"}}, " en", None),  # Space before lowercase language code
        ({"en": {"hello"}, "special": {"#@$%"}}, "special", "special"),  # Special characters as language code
    ],
)
def test_get_registered_lang(mls_setup: dict, input_lang: str, expected_output: str):
    """Test the _get_registered_lang method for various scenarios and mls instantiations.

    :param mls_setup: The setup dictionary for MultiLangString instantiation.
    :param input_lang: The input language code to be tested.
    :param expected_output: The expected output from the _get_registered_lang method.
    """
    mls = MultiLangString(mls_setup)
    result = mls._get_registered_lang(input_lang)
    assert (
        result == expected_output
    ), f"Given mls setup {mls_setup}, expected '{expected_output}' for input language '{input_lang}', but got '{result}'."


@pytest.mark.parametrize(
    "mls_setup, input_lang, expected_exception",
    [
        ({"en": {"hello"}, "fr": {"bonjour"}}, 123, TypeError),
        ({"en": {"hello"}, "fr": {"bonjour"}}, ["en"], TypeError),
        ({"en": {"hello"}, "fr": {"bonjour"}}, {"lang": "en"}, TypeError),
        ({"en": {"hello"}, "fr": {"bonjour"}}, None, TypeError),
    ],
)
def test_get_registered_lang_invalid_cases(mls_setup: dict, input_lang, expected_exception):
    """Test the _get_registered_lang method for handling invalid types and values.

    :param mls_setup: The setup dictionary for MultiLangString instantiation.
    :param input_lang: The input language code to be tested, especially for invalid types/values.
    :param expected_exception: The type of exception expected to be raised.
    """
    mls = MultiLangString(mls_setup)
    with pytest.raises(expected_exception):
        mls._get_registered_lang(input_lang)
