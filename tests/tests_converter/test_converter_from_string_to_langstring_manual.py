from typing import Optional

import pytest
from langstring import Converter
from langstring import LangString


@pytest.mark.parametrize(
    "string, lang, expected_text, expected_lang",
    [
        (None, "en", "", "en"),
        ("text", None, "text", ""),
        (None, None, "", ""),
        ("Hello, World!", "en", "Hello, World!", "en"),
        ("Bonjour le monde!", "fr", "Bonjour le monde!", "fr"),
        ("", "en", "", "en"),  # Empty string
        ("Empty string", "", "Empty string", ""),  # Empty language
        (" ", "en", " ", "en"),  # String with a space
        ("Hello", "en", "Hello", "en"),  # String without special characters
        ("hello", "en", "hello", "en"),  # Lowercase string
        ("HELLO", "en", "HELLO", "en"),  # Uppercase string
        ("Hello", "EN", "Hello", "EN"),  # Uppercase language code
        ("Hello, World! ", "en", "Hello, World! ", "en"),  # Space at the end
        (" Hello, World!", "en", " Hello, World!", "en"),  # Space at the beginning
        ("Hello,  World!", "en", "Hello,  World!", "en"),  # Multiple spaces inside
        ("こんにちは世界", "ja", "こんにちは世界", "ja"),  # Japanese characters
        ("Привет, мир!", "ru", "Привет, мир!", "ru"),  # Russian characters
        ("Γειά σου Κόσμε!", "el", "Γειά σου Κόσμε!", "el"),  # Greek characters
        ("¡Hola, Mundo!", "es", "¡Hola, Mundo!", "es"),  # Spanish with special character
        ("Olá, Mundo!", "pt", "Olá, Mundo!", "pt"),  # Portuguese with special character
        ("Hello 😊", "en", "Hello 😊", "en"),  # String with emoji
        ("Hello, World! 😀👍", "en", "Hello, World! 😀👍", "en"),  # String with multiple emojis
        ("Hello, World!", "en-GB", "Hello, World!", "en-GB"),  # Language with region code
        ("Special chars !@#$%^&*()_+", "en", "Special chars !@#$%^&*()_+", "en"),  # String with special characters
    ],
)
def test_from_string_to_langstring_manual(
    string: str, lang: Optional[str], expected_text: str, expected_lang: Optional[str]
):
    """Test the from_string_to_langstring_manual method with various inputs.

    :param string: The input text to be converted.
    :param lang: The language code.
    :param expected_text: The expected text in the LangString.
    :param expected_lang: The expected language code in the LangString.
    """
    result = Converter.from_string_to_langstring_manual(string, lang)
    assert result.text == expected_text, f"Expected text '{expected_text}', but got '{result.text}'"
    assert result.lang == expected_lang, f"Expected language '{expected_lang}', but got '{result.lang}'"


def test_from_string_to_langstring_manual_invalid_lang():
    """Test the from_string_to_langstring_manual method with invalid language type.

    :raises TypeError: If the language type is incorrect.
    """
    with pytest.raises(TypeError, match="Invalid argument with value '123'. Expected .+ but got 'int'."):
        Converter.from_string_to_langstring_manual("Hello, World!", 123)


def test_from_string_to_langstring_manual_invalid_string():
    """Test the from_string_to_langstring_manual method with invalid string type.

    :raises TypeError: If the string type is incorrect.
    """
    with pytest.raises(
        TypeError, match="Invalid argument with value '123'. Expected one of 'str' or 'NoneType', but got 'int'."
    ):
        Converter.from_string_to_langstring_manual(123, "en")


# Append this to your current test set


@pytest.mark.parametrize(
    "string, lang, expected_text, expected_lang",
    [
        ("", "en", "", "en"),
        ("Empty string", "", "Empty string", ""),
        (" ", "en", " ", "en"),  # String with a space
        ("hello", "en", "hello", "en"),  # Lowercase string
        ("HELLO", "en", "HELLO", "en"),  # Uppercase string
        ("Hello", "EN", "Hello", "EN"),  # Uppercase language code
        ("Hello, World! ", "en", "Hello, World! ", "en"),  # Space at the end
        (" Hello, World!", "en", " Hello, World!", "en"),  # Space at the beginning
        ("Hello,  World!", "en", "Hello,  World!", "en"),  # Multiple spaces inside
        ("こんにちは世界", "ja", "こんにちは世界", "ja"),  # Japanese characters
        ("Привет, мир!", "ru", "Привет, мир!", "ru"),  # Russian characters
        ("Γειά σου Κόσμε!", "el", "Γειά σου Κόσμε!", "el"),  # Greek characters
        ("¡Hola, Mundo!", "es", "¡Hola, Mundo!", "es"),  # Spanish with special character
        ("Olá, Mundo!", "pt", "Olá, Mundo!", "pt"),  # Portuguese with special character
        ("Hello 😊", "en", "Hello 😊", "en"),  # String with emoji
        ("Hello, World! 😀👍", "en", "Hello, World! 😀👍", "en"),  # String with multiple emojis
        ("Hello, World!", "en-GB", "Hello, World!", "en-GB"),  # Language with region code
        ("Special chars !@#$%^&*()_+", "en", "Special chars !@#$%^&*()_+", "en"),  # String with special characters
    ],
)
def test_from_string_to_langstring_manual_edge_cases(
    string: str, lang: Optional[str], expected_text: str, expected_lang: Optional[str]
):
    """Test the from_string_to_langstring_manual method with edge cases.

    :param string: The input text to be converted.
    :param lang: The language code.
    :param expected_text: The expected text in the LangString.
    :param expected_lang: The expected language code in the LangString.
    """
    result = Converter.from_string_to_langstring_manual(string, lang)
    assert result.text == expected_text, f"Expected text '{expected_text}', but got '{result.text}'"
    assert result.lang == expected_lang, f"Expected language '{expected_lang}', but got '{result.lang}'"


def test_from_string_to_langstring_manual_empty_string():
    """Test the from_string_to_langstring_manual method with an empty string."""
    string = ""
    lang = "en"
    result = Converter.from_string_to_langstring_manual(string, lang)
    assert result.text == string, f"Expected text '{string}', but got '{result.text}'"
    assert result.lang == lang, f"Expected language '{lang}', but got '{result.lang}'"


def test_from_string_to_langstring_manual_self_operation():
    """Test the from_string_to_langstring_manual method with the same object.

    This is not directly applicable as it doesn't return the same object type.
    """
    string = "Hello, World!"
    lang = "en"
    result = Converter.from_string_to_langstring_manual(string, lang)
    assert isinstance(result, LangString), "Expected result to be an instance of LangString"
    assert result.text == string, f"Expected text '{string}', but got '{result.text}'"
    assert result.lang == lang, f"Expected language '{lang}', but got '{result.lang}'"
