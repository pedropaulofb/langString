import pytest
from langstring import Controller
from langstring import GlobalFlag
from langstring import LangString
from langstring import LangStringFlag
from tests.conftest import TYPEERROR_MSG_SINGULAR


@pytest.mark.parametrize(
    "text, lang, expected_text, expected_lang",
    [
        ("Hello", "en", "Hello", "en"),
        ("こんにちは", "ja", "こんにちは", "ja"),
    ],
)
def test_langstring_init_valid_inputs(text, lang, expected_text, expected_lang):
    """Test the __init__ method with various valid inputs."""
    lang_string = LangString(text, lang)
    assert lang_string.text == expected_text, "LangString text does not match expected value"
    assert lang_string.lang == expected_lang, "LangString language tag does not match expected value"


@pytest.mark.parametrize(
    "text, lang, error",
    [
        (123, "en", TypeError),
        ("Hello", 123, TypeError),
    ],
)
def test_langstring_init_invalid_inputs(text, lang, error):
    """Test the __init__ method with invalid input types."""
    with pytest.raises(error, match=TYPEERROR_MSG_SINGULAR):
        LangString(text, lang)


@pytest.mark.parametrize(
    "text, lang, flag, match",
    [
        ("", "en", LangStringFlag.DEFINED_TEXT, "Expected non-empty 'str'"),
        ("Hello", "", LangStringFlag.DEFINED_LANG, "Expected non-empty 'str'"),
    ],
)
def test_langstring_init_with_control_flags(text, lang, flag, match):
    """Test the __init__ method with control flags enforcing constraints."""
    Controller.set_flag(flag, True)
    with pytest.raises(ValueError, match=match):
        LangString(text, lang)
    Controller.set_flag(flag, False)


def test_langstring_init_with_default_values():
    """Test the __init__ method with default values."""
    lang_string = LangString()
    assert lang_string.text == "", "Default text should be an empty string"
    assert lang_string.lang == "", "Default language tag should be an empty string"


@pytest.mark.parametrize(
    "text, lang, error",
    [
        ("Hello", None, None),  # This should not raise an error
        (None, "en", None),  # This should not raise a TypeError
        (None, None, None),  # This should not raise a TypeError
    ],
)
def test_langstring_init_with_none(text, lang, error):
    """Test initialization with None."""
    if error:
        with pytest.raises(error, match=TYPEERROR_MSG_SINGULAR):
            LangString(text, lang)
    else:
        LangString(text, lang)  # This should not raise an error


@pytest.mark.parametrize(
    "text, lang, error",
    [
        ([], "en", TypeError),
        ("Hello", (), TypeError),
    ],
)
def test_langstring_init_with_list_or_tuple(text, lang, error):
    """Test initialization with list or tuple."""
    with pytest.raises(error, match=TYPEERROR_MSG_SINGULAR):
        LangString(text, lang)


@pytest.mark.parametrize(
    "text, lang, expected_text, expected_lang",
    [
        ("  Hello  ", "  en  ", "Hello", "en"),
    ],
)
def test_langstring_init_with_strip_flags(text, lang, expected_text, expected_lang):
    """Test the init method with STRIP_TEXT and STRIP_LANG flags enabled."""
    Controller.set_flag(LangStringFlag.STRIP_TEXT, True)
    Controller.set_flag(LangStringFlag.STRIP_LANG, True)
    lang_string = LangString(text, lang)
    assert lang_string.text == expected_text, "LangString text should be stripped"
    assert lang_string.lang == expected_lang, "LangString language should be stripped"


@pytest.mark.parametrize(
    "lang, expected_lang",
    [
        ("EN", "en"),
        ("Fr", "fr"),
    ],
)
def test_langstring_init_with_lowercase_lang_flag(lang, expected_lang):
    """Test the init method with LOWERCASE_LANG flag enabled."""
    Controller.set_flag(LangStringFlag.LOWERCASE_LANG, True)
    lang_string = LangString("text", lang)
    assert lang_string.lang == expected_lang, "LangString language should be lowercase"


@pytest.mark.parametrize(
    "lang, error, match",
    [
        ("invalid-lang-code", ValueError, "Expected valid language code"),
    ],
)
def test_langstring_init_with_valid_lang_flag(lang, error, match):
    """Test the init method with VALID_LANG flag enabled."""
    Controller.set_flag(LangStringFlag.VALID_LANG, True)
    with pytest.raises(error, match=match):
        LangString("text", lang)


@pytest.mark.parametrize(
    "text, lang, error, match",
    [
        ("", "en", ValueError, "Expected non-empty 'str'"),
        ("Hello", "", ValueError, "Expected non-empty 'str'"),
    ],
)
def test_langstring_init_with_global_defined_flags(text, lang, error, match):
    """Test the init method with Global DEFINED_TEXT and DEFINED_LANG flags enabled."""
    Controller.set_flag(GlobalFlag.DEFINED_TEXT, True)
    Controller.set_flag(GlobalFlag.DEFINED_LANG, True)
    with pytest.raises(error, match=match):
        LangString(text, lang)


@pytest.mark.parametrize(
    "text, lang, expected_text, expected_lang",
    [
        ("  Hello  ", "EN  ", "Hello", "en"),
    ],
)
def test_langstring_init_with_combined_flags(text, lang, expected_text, expected_lang):
    """Test the __init__ method with a combination of STRIP_TEXT, STRIP_LANG, and LOWERCASE_LANG flags."""
    Controller.reset_flags()
    Controller.set_flag(LangStringFlag.STRIP_TEXT, True)
    Controller.set_flag(LangStringFlag.STRIP_LANG, True)
    Controller.set_flag(LangStringFlag.LOWERCASE_LANG, True)

    lang_string = LangString(text, lang)
    assert lang_string.text == expected_text, "LangString text should be stripped and unchanged"
    assert lang_string.lang == expected_lang, "LangString language should be stripped and lowercase"


@pytest.mark.parametrize(
    "text, lang",
    [
        ("", ""),  # Empty strings
        (" " * 1000, "en"),  # Very long string
        ("Hello\nWorld", "en"),  # Newline characters
        ("Hello\tWorld", "en"),  # Tab characters
        ("👋🌍", "en"),  # Unicode characters
    ],
)
def test_langstring_init_edge_cases(text, lang):
    """Test the __init__ method with various edge cases."""
    Controller.reset_flags()
    lang_string = LangString(text, lang)
    assert lang_string.text == text, "LangString text should match input text"
    assert lang_string.lang == lang, "LangString language should match input language"


def test_langstring_init_resetting_flags():
    """Test the __init__ method behavior after resetting flags."""
    Controller.set_flag(LangStringFlag.STRIP_TEXT, True)
    Controller.set_flag(LangStringFlag.LOWERCASE_LANG, True)
    Controller.reset_flags()

    text, lang = "  Hello  ", "EN  "
    lang_string = LangString(text, lang)
    assert lang_string.text == text, "LangString text should be unchanged after resetting flags"
    assert lang_string.lang == lang, "LangString language should be unchanged after resetting flags"


@pytest.mark.parametrize(
    "text, lang",
    [
        ("123", "num"),  # Numeric strings
        ("true", "bool"),  # Boolean-like strings
        ("", "empty"),  # Empty text with valid lang
        ("Hello", ""),  # Valid text with empty lang
    ],
)
def test_langstring_init_unusual_valid_inputs(text, lang):
    """Test the __init__ method with unusual but valid inputs."""
    lang_string = LangString(text, lang)
    assert lang_string.text == text, "LangString text should match input text"
    assert lang_string.lang == lang, "LangString language should match input language"


@pytest.mark.parametrize(
    "text, lang",
    [
        ("Hello", "fr-CA"),  # Locale-specific language code
        ("Hola", "es-419"),  # Latin American Spanish
        ("Hello", "i-klingon"),  # Non-standard language code
    ],
)
def test_langstring_init_with_varied_language_codes(text, lang):
    """Test the __init__ method with a variety of language codes."""
    lang_string = LangString(text, lang)
    assert lang_string.lang == lang, "LangString language should match input language"


@pytest.mark.parametrize(
    "text, lang",
    [
        ("Hello, 世界", "en"),  # Mixed English and Chinese characters
        ("🌍🌎🌏", "emoji"),  # Emoji characters
    ],
)
def test_langstring_init_with_special_characters(text, lang):
    """Test the __init__ method with special character strings."""
    lang_string = LangString(text, lang)
    assert lang_string.text == text, "LangString text should match input text"


@pytest.mark.parametrize(
    "text, lang",
    [
        ("a" * 10000, "en"),  # Very long string
        ("", "en"),  # Empty string
    ],
)
def test_langstring_init_with_boundary_values(text, lang):
    """Test the __init__ method with boundary value strings."""
    lang_string = LangString(text, lang)
    assert lang_string.text == text, "LangString text should match input text"


@pytest.mark.parametrize(
    "text, lang, expected_text, match",
    [
        ("  Hello  ", "invalid-lang-code  ", "Hello", "Expected valid language code"),
    ],
)
def test_langstring_init_with_combined_unusual_flags(text, lang, expected_text, match):
    """Test the __init__ method with a combination of unusual flags."""
    Controller.set_flag(LangStringFlag.STRIP_TEXT, True)
    Controller.set_flag(LangStringFlag.VALID_LANG, True)

    with pytest.raises(ValueError, match=match):
        LangString(text, lang)


@pytest.mark.parametrize(
    "text, lang, expected_text, expected_lang",
    [
        ("שלום", "he", "שלום", "he"),  # Hebrew
        ("नमस्ते", "hi", "नमस्ते", "hi"),  # Hindi
        ("مرحبا", "ar", "مرحبا", "ar"),  # Arabic
        ("Привет", "ru", "Привет", "ru"),  # Russian
        ("안녕하세요", "ko", "안녕하세요", "ko"),  # Korean
    ],
)
def test_langstring_init_valid_inputs_extended(text, lang, expected_text, expected_lang):
    lang_string = LangString(text, lang)
    assert lang_string.text == expected_text
    assert lang_string.lang == expected_lang


@pytest.mark.parametrize(
    "text, lang, error",
    [
        (3.14, "en", TypeError),
        (True, "en", TypeError),
        ({"greeting": "hello"}, "en", TypeError),
    ],
)
def test_langstring_init_with_various_types(text, lang, error):
    with pytest.raises(error, match=TYPEERROR_MSG_SINGULAR):
        LangString(text, lang)


@pytest.mark.parametrize(
    "text, lang",
    [
        ("Hello", "zh-Hant"),  # Traditional Chinese
        ("Bonjour", "fr-CA"),  # Canadian French
        ("Saluton", "eo"),  # Esperanto
        ("Sawubona", "zu"),  # Zulu
    ],
)
def test_langstring_init_with_more_varied_language_codes(text, lang):
    lang_string = LangString(text, lang)
    assert lang_string.lang == lang


@pytest.mark.parametrize(
    "text, lang",
    [
        ("Hello-こんにちは", "en-ja"),  # English and Japanese
        ("123-abc-👍", "en"),  # Numbers, English letters, and emoji
        ("Hello-Привет", "en-ru"),  # Combining English and Russian
        ("123-bonjour-@", "fr"),  # Combining numbers, French, and symbols
    ],
)
def test_langstring_init_with_mixed_characters(text, lang):
    Controller.reset_flags()
    lang_string = LangString(text, lang)
    assert lang_string.text == text


@pytest.mark.parametrize(
    "text, lang",
    [
        (" " * 1000, "en"),  # Long string of spaces
        ("a" * 1, "en"),  # Single character
        ("x" * 10000, "en"),  # Very long string
    ],
)
def test_langstring_init_with_additional_boundary_values(text, lang):
    Controller.reset_flags()
    lang_string = LangString(text, lang)
    assert lang_string.text == text


@pytest.mark.parametrize(
    "text, lang",
    [
        ("    ", "en"),  # String with only spaces
        ("\u200b\u200c\u200d", "en"),  # Zero-width characters
        ("Hello\nWorld", "en"),  # String with newline characters
        ("\t \n \r", "en"),  # String with various whitespace characters
    ],
)
def test_langstring_init_with_more_edge_cases(text, lang):
    lang_string = LangString(text, lang)
    assert lang_string.text == text
