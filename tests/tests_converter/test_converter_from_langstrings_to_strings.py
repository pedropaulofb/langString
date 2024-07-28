import pytest
from langstring import Controller
from langstring import Converter
from langstring import GlobalFlag
from langstring import LangString


def test_from_langstrings_to_strings_valid_list() -> None:
    """Test conversion of a list of valid LangString objects to a list of strings.

    :raises AssertionError: If the conversion does not return the expected list of strings.
    """
    langstrings = [LangString("Hello", "en"), LangString("World", "es")]
    result = Converter.from_langstrings_to_strings(langstrings)
    expected = ['"Hello"@en', '"World"@es']
    assert result == expected, f"Expected {expected}, got {result}"


def test_from_langstrings_to_strings_empty_list() -> None:
    """Test conversion of an empty list of LangString objects to an empty list of strings.

    :raises AssertionError: If the conversion does not return an empty list.
    """
    langstrings = []
    result = Converter.from_langstrings_to_strings(langstrings)
    assert result == [], f"Expected [], got {result}"


def test_from_langstrings_to_strings_none_input() -> None:
    """Test conversion of None input to a list of strings.

    :raises TypeError: If the input is None.
    """
    with pytest.raises(TypeError, match="Invalid argument with value 'None'. Expected 'list', but got 'NoneType'."):
        Converter.from_langstrings_to_strings(None)


def test_from_langstrings_to_strings_invalid_type() -> None:
    """Test conversion of an invalid type input to a list of strings.

    :raises TypeError: If the input is not of type list.
    """
    with pytest.raises(TypeError, match="Invalid argument with value 'invalid'. Expected 'list', but got 'str'."):
        Converter.from_langstrings_to_strings("invalid")


def test_from_langstrings_to_strings_mixed_valid_invalid() -> None:
    """Test conversion of a list with mixed valid and invalid LangString objects to a list of strings.

    :raises TypeError: If any element in the list is not of type LangString.
    """
    langstrings = [LangString("Hello", "en"), "invalid"]
    with pytest.raises(TypeError, match="Invalid argument with value 'invalid'. Expected 'LangString', but got 'str'."):
        Converter.from_langstrings_to_strings(langstrings)


def test_from_langstrings_to_strings_edge_cases() -> None:
    """Test conversion of a list of LangString objects with edge cases to a list of strings.

    :raises AssertionError: If the conversion does not return the expected list of strings.
    """
    langstrings = [LangString("", ""), LangString(" ", " "), LangString("Hello\nWorld", "en")]
    result = Converter.from_langstrings_to_strings(langstrings)
    expected = ['""@', '" "@ ', '"Hello\nWorld"@en']
    assert result == expected, f"Expected {expected}, got {result}"


def test_from_langstrings_to_strings_special_characters() -> None:
    """Test conversion of a list of LangString objects with special characters to a list of strings.

    :raises AssertionError: If the conversion does not return the expected list of strings.
    """
    langstrings = [LangString("Hello😊", "en"), LangString("Γειά σου Κόσμε", "el"), LangString("こんにちは世界", "ja")]
    result = Converter.from_langstrings_to_strings(langstrings)
    expected = ['"Hello😊"@en', '"Γειά σου Κόσμε"@el', '"こんにちは世界"@ja']
    assert result == expected, f"Expected {expected}, got {result}"


@pytest.mark.parametrize(
    "langstrings, expected",
    [
        ([LangString("Hello", "en"), LangString("World", "es")], ['"Hello"@en', '"World"@es']),
        ([], []),
        (
            [LangString("", ""), LangString(" ", " "), LangString("Hello\nWorld", "en")],
            ['""@', '" "@ ', '"Hello\nWorld"@en'],
        ),
        (
            [LangString("Hello😊", "en"), LangString("Γειά σου Κόσμε", "el"), LangString("こんにちは世界", "ja")],
            ['"Hello😊"@en', '"Γειά σου Κόσμε"@el', '"こんにちは世界"@ja'],
        ),
        ([LangString("HELLO", "EN"), LangString("world", "ES")], ['"HELLO"@EN', '"world"@ES']),
        ([LangString("   ", " "), LangString("\nNew\nLine\n", "en")], ['"   "@ ', '"\nNew\nLine\n"@en']),
        ([LangString("Special@#$%^&*()Chars", "en")], ['"Special@#$%^&*()Chars"@en']),
        ([LangString("Hello", ""), LangString("", "en")], ['"Hello"@', '""@en']),
        (
            [LangString("Привет", "ru"), LangString("안녕하세요", "ko"), LangString("مرحبا", "ar")],
            ['"Привет"@ru', '"안녕하세요"@ko', '"مرحبا"@ar'],
        ),
    ],
)
def test_from_langstrings_to_strings_various_cases(langstrings: list[LangString], expected: list[str]) -> None:
    """Test conversion of various lists of LangString objects to lists of strings.

    :param langstrings: The list of LangString objects to convert.
    :param expected: The expected result of the conversion.
    :raises AssertionError: If the conversion does not return the expected list of strings.
    """
    result = Converter.from_langstrings_to_strings(langstrings)
    assert result == expected, f"Expected {expected}, got {result}"


def test_from_langstrings_to_strings_with_global_flag() -> None:
    """Test conversion with global flag affecting behavior.

    :raises AssertionError: If the conversion does not reflect the flag's effect.
    """
    langstrings = [LangString("Hello", "en"), LangString("World", "es")]
    Controller.set_flag(GlobalFlag.PRINT_WITH_QUOTES, False)
    result = Converter.from_langstrings_to_strings(langstrings)
    expected = ["Hello@en", "World@es"]
    assert result == expected, f"Expected {expected}, got {result}"
    Controller.set_flag(GlobalFlag.PRINT_WITH_QUOTES, True)


def test_from_langstrings_to_strings_unusual_valid_usage() -> None:
    """Test unusual but valid usage of LangString objects in a list.

    :raises AssertionError: If the conversion does not return the expected list of strings.
    """
    langstrings = [LangString("Hello\nWorld", "en"), LangString("\tTabbed", "en"), LangString("Mixed CASE", "en")]
    result = Converter.from_langstrings_to_strings(langstrings)
    expected = ['"Hello\nWorld"@en', '"\tTabbed"@en', '"Mixed CASE"@en']
    assert result == expected, f"Expected {expected}, got {result}"


def test_from_langstrings_to_strings_self_conversion() -> None:
    """Test operation on itself (conversion of the result again).

    :raises AssertionError: If the conversion does not return the expected list of strings.
    """
    langstrings = [LangString("Hello", "en"), LangString("World", "es")]
    result = Converter.from_langstrings_to_strings(langstrings)
    langstrings2 = [LangString(text, "en") for text in result]
    result2 = Converter.from_langstrings_to_strings(langstrings2)
    expected = ['""Hello"@en"@en', '""World"@es"@en']
    assert result2 == expected, f"Expected {expected}, got {result2}"
