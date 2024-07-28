import pytest
from langstring import Controller
from langstring import Converter
from langstring import MultiLangString
from langstring import MultiLangStringFlag


def test_from_multilangstring_to_string_valid() -> None:
    """Test conversion of a valid MultiLangString object to a string.

    :raises AssertionError: If the conversion does not return the expected string value.
    """
    multilangstring = MultiLangString({"en": {"Hello"}, "es": {"Hola"}})
    result = Converter.from_multilangstring_to_string(multilangstring)
    expected = "{'Hello'}@en, {'Hola'}@es"
    assert result == expected, f"Expected '{expected}', got {result}"


def test_from_multilangstring_to_string_empty() -> None:
    """Test conversion of an empty MultiLangString object to a string.

    :raises AssertionError: If the conversion does not return an empty string.
    """
    multilangstring = MultiLangString()
    result = Converter.from_multilangstring_to_string(multilangstring)
    assert result == "{}", f"Expected '{{}}', got {result}"


def test_from_multilangstring_to_string_invalid_type() -> None:
    """Test conversion of an invalid type input.

    :raises TypeError: If the input is not of type MultiLangString.
    """
    with pytest.raises(
        TypeError, match="Invalid argument with value 'invalid'. Expected 'MultiLangString', but got 'str'."
    ):
        Converter.from_multilangstring_to_string("invalid")


def test_from_multilangstring_to_string_special_characters() -> None:
    """Test conversion of a MultiLangString object with special characters to a string.

    :raises AssertionError: If the conversion does not return the expected string value.
    """
    multilangstring = MultiLangString({"en": {"Hello😊"}, "el": {"Γειά σου Κόσμε"}, "ja": {"こんにちは世界"}})
    result = Converter.from_multilangstring_to_string(multilangstring)
    expected = "{'Γειά σου Κόσμε'}@el, {'Hello😊'}@en, {'こんにちは世界'}@ja"
    assert result == expected, f"Expected '{expected}', got {result}"


def test_from_multilangstring_to_string_edge_cases() -> None:
    """Test conversion of a MultiLangString object with edge cases to a string.

    :raises AssertionError: If the conversion does not return the expected string value.
    """
    multilangstring = MultiLangString({"": {""}, " ": {" "}, "en": {"Hello\nWorld"}})
    result = Converter.from_multilangstring_to_string(multilangstring)
    expected = "{''}@, {' '}@ , {'Hello\nWorld'}@en"
    assert result == expected, f"Expected '{expected}', got {result}"


def test_from_multilangstring_to_string_null_input() -> None:
    """Test conversion of null (None) input to a string.

    :raises TypeError: If the input is None.
    """
    with pytest.raises(
        TypeError, match="Invalid argument with value 'None'. Expected 'MultiLangString', but got 'NoneType'."
    ):
        Converter.from_multilangstring_to_string(None)


def test_from_multilangstring_to_string_unusual_but_valid_usage() -> None:
    """Test unusual but valid usage of MultiLangString object.

    :raises AssertionError: If the conversion does not return the expected string value.
    """
    multilangstring = MultiLangString({"en": {"Hello\nWorld"}, "es": {"\tHola"}})
    result = Converter.from_multilangstring_to_string(multilangstring)
    expected = "{'Hello\nWorld'}@en, {'\tHola'}@es"
    assert result == expected, f"Expected '{expected}', got {result}"


def test_from_multilangstring_to_string_with_flags_effect() -> None:
    """Test conversion with global flag affecting behavior.

    :raises AssertionError: If the conversion does not reflect the flag's effect.
    """
    multilangstring = MultiLangString({"en": {"Hello"}, "es": {"Hola"}})
    Controller.set_flag(MultiLangStringFlag.PRINT_WITH_QUOTES, False)
    Controller.set_flag(MultiLangStringFlag.PRINT_WITH_LANG, True)
    result = Converter.from_multilangstring_to_string(multilangstring)
    expected = "{Hello}@en, {Hola}@es"
    assert result == expected, f"Expected '{expected}', got {result}"
    Controller.reset_flag(MultiLangStringFlag.PRINT_WITH_QUOTES)
    Controller.reset_flag(MultiLangStringFlag.PRINT_WITH_LANG)


def test_from_multilangstring_to_string_operation_on_itself() -> None:
    """Test operation on itself (conversion of the result again).

    :raises AssertionError: If the conversion does not return the expected string value.
    """
    Controller.set_flag(MultiLangStringFlag.PRINT_WITH_QUOTES, False)
    multilangstring = MultiLangString({"en": {"Hello"}, "es": {"Hola"}})
    result = Converter.from_multilangstring_to_string(multilangstring)
    multilangstring2 = MultiLangString({"en": {result}, "es": {result}})
    result2 = Converter.from_multilangstring_to_string(multilangstring2)
    expected = "{{Hello}@en, {Hola}@es}@en, {{Hello}@en, {Hola}@es}@es"
    assert result2 == expected, f"Expected '{expected}', got {result2}"


@pytest.mark.parametrize(
    "mls_dict, expected",
    [
        ({"en": {"Hello"}, "es": {"Hola"}}, "{'Hello'}@en, {'Hola'}@es"),
        (
            {"en": {"Hello😊"}, "el": {"Γειά σου Κόσμε"}, "ja": {"こんにちは世界"}},
            "{'Γειά σου Κόσμε'}@el, {'Hello😊'}@en, {'こんにちは世界'}@ja",
        ),
        ({"": {""}, " ": {" "}, "en": {"Hello\nWorld"}}, "{''}@, {' '}@ , {'Hello\nWorld'}@en"),
        ({"en": {"Hello\nWorld"}, "es": {"\tHola"}}, "{'Hello\nWorld'}@en, {'\tHola'}@es"),
        # New cases
        ({"en": {""}, "es": {""}}, "{''}@en, {''}@es"),
        ({"en": {"hello", "HELLO", "Hello"}}, "{'HELLO', 'Hello', 'hello'}@en"),
        ({"en": {"hello world", " hello world "}}, "{' hello world ', 'hello world'}@en"),
        ({"en": {"你好"}, "zh": {"世界"}}, "{'你好'}@en, {'世界'}@zh"),
        ({"en": {"Hello 🌍"}}, "{'Hello 🌍'}@en"),
        ({"en": {"Hello!", "@Hello", "#Hello"}}, "{'#Hello', '@Hello', 'Hello!'}@en"),
    ],
)
def test_from_multilangstring_to_string_various_cases(mls_dict, expected) -> None:
    """Test conversion of various MultiLangString objects to a string.

    :param mls_dict: The dictionary representing the MultiLangString object.
    :param expected: The expected string representation.
    :raises AssertionError: If the conversion does not return the expected string value.
    """
    Controller.reset_flags()
    multilangstring = MultiLangString(mls_dict)
    result = Converter.from_multilangstring_to_string(multilangstring)
    assert result == expected, f"Expected '{expected}', got {result}"


@pytest.mark.parametrize(
    "mls_dict, flags, expected",
    [
        (
            {"en": {"Hello"}, "es": {"Hola"}},
            {MultiLangStringFlag.PRINT_WITH_QUOTES: False, MultiLangStringFlag.PRINT_WITH_LANG: True},
            "{Hello}@en, {Hola}@es",
        ),
        # New cases
        (
            {"en": {"hello"}, "es": {"hola"}},
            {MultiLangStringFlag.PRINT_WITH_QUOTES: False, MultiLangStringFlag.PRINT_WITH_LANG: False},
            "{hello}, {hola}",
        ),
        (
            {"en": {"HELLO"}, "es": {"HOLA"}},
            {MultiLangStringFlag.PRINT_WITH_QUOTES: True, MultiLangStringFlag.PRINT_WITH_LANG: True},
            "{'HELLO'}@en, {'HOLA'}@es",
        ),
        (
            {"en": {"Hello 😊"}, "fr": {"Bonjour"}},
            {MultiLangStringFlag.PRINT_WITH_QUOTES: False, MultiLangStringFlag.PRINT_WITH_LANG: True},
            "{Hello 😊}@en, {Bonjour}@fr",
        ),
        (
            {"en": {"Hello"}, "es": {"Hola"}},
            {MultiLangStringFlag.PRINT_WITH_QUOTES: True, MultiLangStringFlag.PRINT_WITH_LANG: False},
            "{'Hello'}, {'Hola'}",
        ),
    ],
)
def test_from_multilangstring_to_string_with_flags_effect_various_cases(mls_dict, flags, expected) -> None:
    """Test conversion with global flag affecting behavior.

    :param mls_dict: The dictionary representing the MultiLangString object.
    :param flags: A dictionary of flags to set and their values.
    :param expected: The expected string representation.
    :raises AssertionError: If the conversion does not reflect the flag's effect.
    """
    multilangstring = MultiLangString(mls_dict)
    for flag, value in flags.items():
        Controller.set_flag(flag, value)
    result = str(multilangstring)
    assert result == expected, f"Expected '{expected}', got {result}"


@pytest.mark.parametrize(
    "mls_dict, expected",
    [
        ({"en": {"Hello"}, "es": {"Hola"}}, "{Hello}@en, {Hola}@es@en, {{Hello}@en, {Hola}@es}@en@es"),
        # New cases
        ({"en": {"你好"}, "zh": {"世界"}}, "{你好}@en, {世界}@zh@en, {{你好}@en, {世界}@zh}@en@es"),
        ({"en": {"Hello😊"}}, "{Hello😊}@en@en, {{Hello😊}@en}@en@es"),
        ({"en": {"HELLO"}, "es": {"HOLA"}}, "{HELLO}@en, {HOLA}@es@en, {{HELLO}@en, {HOLA}@es}@en@es"),
    ],
)
def test_from_multilangstring_to_string_operation_on_itself_various_cases(mls_dict, expected) -> None:
    """Test operation on itself (conversion of the result again).

    :param mls_dict: The dictionary representing the initial MultiLangString object.
    :param expected: The expected string representation after two conversions.
    :raises AssertionError: If the conversion does not return the expected string value.
    """
    Controller.set_flag(MultiLangStringFlag.PRINT_WITH_QUOTES, False)
    Controller.set_flag(MultiLangStringFlag.PRINT_WITH_LANG, True)
    multilangstring = MultiLangString(mls_dict)

    # First conversion
    first_result = Converter.from_multilangstring_to_string(multilangstring)

    # Second conversion
    second_multilangstring = MultiLangString({"en": {first_result}})
    second_result = Converter.from_multilangstring_to_string(second_multilangstring)

    result = f"{first_result}@en, {second_result}@es"

    assert result == expected, f"Expected '{expected}', got {result}'"
