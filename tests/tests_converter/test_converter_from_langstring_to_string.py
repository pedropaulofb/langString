import pytest
from langstring import Controller
from langstring import Converter
from langstring import GlobalFlag
from langstring import LangString


def test_from_langstring_to_string_valid_langstring() -> None:
    """Test conversion of a valid LangString object to a string.

    :raises AssertionError: If the conversion does not return the expected string value.
    """
    langstring = LangString("Hello", "en")
    result = Converter.from_langstring_to_string(langstring)
    assert result == '"Hello"@en', f"Expected '\"Hello\"@en', got {result}"


def test_from_langstring_to_string_none_input() -> None:
    """Test conversion of None input to a string.

    :raises TypeError: If the input is None.
    """
    with pytest.raises(
        TypeError, match="Invalid argument with value 'None'. Expected 'LangString', but got 'NoneType'."
    ):
        Converter.from_langstring_to_string(None)


def test_from_langstring_to_string_invalid_type() -> None:
    """Test conversion of an invalid type input.

    :raises TypeError: If the input is not of type LangString or None.
    """
    with pytest.raises(TypeError, match="Invalid argument with value 'invalid'. Expected 'LangString', but got 'str'."):
        Converter.from_langstring_to_string("invalid")


def test_from_langstring_to_string_empty_langstring() -> None:
    """Test conversion of an empty LangString object to a string.

    :raises AssertionError: If the conversion does not return an empty string.
    """
    langstring = LangString("", "")
    result = Converter.from_langstring_to_string(langstring)
    assert result == '""@', f"Expected '\"\"@', got {result}"


def test_from_langstring_to_string_strip_whitespace() -> None:
    """Test conversion of a LangString object with leading and trailing whitespace to a string.

    :raises AssertionError: If the conversion does not return a stripped string.
    """
    langstring = LangString("  Hello  ", "en")
    result = Converter.from_langstring_to_string(langstring)
    assert result == '"  Hello  "@en', f"Expected '\"  Hello  \"@en', got {result}"


def test_from_langstring_to_string_non_str_value() -> None:
    """Test conversion of a LangString object with a non-string value.

    :raises TypeError: If the value of LangString is not a string.
    """
    with pytest.raises(TypeError, match="Invalid argument with value '123'. Expected 'str', but got 'int'."):
        LangString(123, "en")


def test_from_langstring_to_string_non_str_lang() -> None:
    """Test conversion of a LangString object with a non-string language code.

    :raises TypeError: If the language code of LangString is not a string.
    """
    with pytest.raises(TypeError, match="Invalid argument with value '123'. Expected 'str', but got 'int'."):
        LangString("Hello", 123)


def test_from_langstring_to_string_with_global_flag() -> None:
    """Test conversion with global flag affecting behavior.

    :raises AssertionError: If the conversion does not reflect the flag's effect.
    """
    langstring = LangString("Hello", "en")
    Controller.set_flag(GlobalFlag.PRINT_WITH_QUOTES, False)
    result = Converter.from_langstring_to_string(langstring)
    assert result == "Hello@en", f"Expected 'Hello@en', got {result}"
    Controller.set_flag(GlobalFlag.PRINT_WITH_QUOTES, True)


def test_from_langstring_to_string_with_empty_lang_code() -> None:
    """Test conversion of a LangString object with an empty language code.

    :raises AssertionError: If the conversion does not return the expected string.
    """
    langstring = LangString("Hello", "")
    result = Converter.from_langstring_to_string(langstring)
    assert result == '"Hello"@', f"Expected '\"Hello\"@', got {result}"


def test_from_langstring_to_string_edge_case_empty_text() -> None:
    """Test conversion of a LangString object with empty text.

    :raises AssertionError: If the conversion does not return the expected string.
    """
    langstring = LangString("", "en")
    result = Converter.from_langstring_to_string(langstring)
    assert result == '""@en', f"Expected '\"\"@en', got {result}"


def test_from_langstring_to_string_unusual_valid_usage() -> None:
    """Test unusual but valid usage of LangString.

    :raises AssertionError: If the conversion does not return the expected string.
    """
    langstring = LangString("Hello\nWorld", "en")
    result = Converter.from_langstring_to_string(langstring)
    assert result == '"Hello\nWorld"@en', f"Expected '\"Hello\nWorld\"@en', got {result}"


def test_from_langstring_to_string_self_conversion() -> None:
    """Test operation on itself (conversion of the result again).

    :raises AssertionError: If the conversion does not return the expected string.
    """
    langstring = LangString("Hello", "en")
    result = Converter.from_langstring_to_string(langstring)
    langstring2 = LangString(result, "en")
    result2 = Converter.from_langstring_to_string(langstring2)
    assert result2 == '""Hello"@en"@en', f'Expected \'""Hello"@en"@en\', got {result2}'


@pytest.mark.parametrize(
    "langstring, expected",
    [
        (LangString("Hello", "en"), '"Hello"@en'),
        (LangString(None, "en"), '""@en'),
        (LangString("Hello", None), '"Hello"@'),
        (LangString(None, None), '""@'),
        (LangString("", ""), '""@'),
        (LangString("  Hello  ", "en"), '"  Hello  "@en'),
        (LangString("HELLO", "en"), '"HELLO"@en'),
        (LangString("hello", "en"), '"hello"@en'),
        (LangString("Hello World", "en"), '"Hello World"@en'),
        (LangString(" Hello ", "en"), '" Hello "@en'),
        (LangString("Γειά σου Κόσμε", "el"), '"Γειά σου Κόσμε"@el'),
        (LangString("Привет мир", "ru"), '"Привет мир"@ru'),
        (LangString("こんにちは世界", "ja"), '"こんにちは世界"@ja'),
        (LangString("مرحبا بالعالم", "ar"), '"مرحبا بالعالم"@ar'),
        (LangString("Hello😊", "en"), '"Hello😊"@en'),
        (LangString("Hello@World!", "en"), '"Hello@World!"@en'),
    ],
)
def test_from_langstring_to_string_various_cases(langstring: LangString, expected: str) -> None:
    """Test conversion of various LangString objects to strings.

    :param langstring: The LangString object to convert.
    :param expected: The expected result of the conversion.
    :raises AssertionError: If the conversion does not return the expected string value.
    """
    result = Converter.from_langstring_to_string(langstring)
    assert result == expected, f"Expected '{expected}', got {result}"


@pytest.mark.parametrize(
    "value, lang, error_message",
    [
        (123, "en", "Invalid argument with value '123'. Expected 'str', but got 'int'."),
        ("Hello", 123, "Invalid argument with value '123'. Expected 'str', but got 'int'."),
        ([], "en", r"Invalid argument with value '\[\]'. Expected 'str', but got 'list'."),
        ("Hello", [], r"Invalid argument with value '\[\]'. Expected 'str', but got 'list'."),
        ({}, "en", r"Invalid argument with value '\{\}'. Expected 'str', but got 'dict'."),
        ("Hello", {}, r"Invalid argument with value '\{\}'. Expected 'str', but got 'dict'."),
    ],
)
def test_from_langstring_to_string_non_str_values(value: str, lang: str, error_message: str) -> None:
    """Test conversion of a LangString object with non-string values.

    :param value: The value of the LangString.
    :param lang: The language code of the LangString.
    :param error_message: The expected error message.
    :raises TypeError: If the value or language code of LangString is not a string.
    """
    with pytest.raises(TypeError, match=error_message):
        LangString(value, lang)
