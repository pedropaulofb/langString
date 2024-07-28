import pytest
from langstring import Controller
from langstring import Converter
from langstring import MultiLangString
from langstring import MultiLangStringFlag


@pytest.mark.parametrize(
    "mls_dict, flags, expected",
    [
        (
            {"en": {"Hello"}, "es": {"Hola"}},
            {MultiLangStringFlag.PRINT_WITH_QUOTES: False, MultiLangStringFlag.PRINT_WITH_LANG: True},
            ["Hello@en", "Hola@es"],
        ),
        (
            {"en": {"hello"}, "es": {"hola"}},
            {MultiLangStringFlag.PRINT_WITH_QUOTES: False, MultiLangStringFlag.PRINT_WITH_LANG: False},
            ["hello", "hola"],
        ),
        (
            {"en": {"HELLO"}, "es": {"HOLA"}},
            {MultiLangStringFlag.PRINT_WITH_QUOTES: True, MultiLangStringFlag.PRINT_WITH_LANG: True},
            ['"HELLO"@en', '"HOLA"@es'],
        ),
        (
            {"en": {"Hello 😊"}, "fr": {"Bonjour"}},
            {MultiLangStringFlag.PRINT_WITH_QUOTES: False, MultiLangStringFlag.PRINT_WITH_LANG: True},
            ["Bonjour@fr", "Hello 😊@en"],
        ),
        (
            {"en": {"Hello"}, "es": {"Hola"}},
            {MultiLangStringFlag.PRINT_WITH_QUOTES: True, MultiLangStringFlag.PRINT_WITH_LANG: False},
            ['"Hello"', '"Hola"'],
        ),
        (
            {"en": {"HELLO"}, "es": {"Hola"}, "fr": {"Bonjour"}},
            {MultiLangStringFlag.PRINT_WITH_QUOTES: False, MultiLangStringFlag.PRINT_WITH_LANG: True},
            ["Bonjour@fr", "HELLO@en", "Hola@es"],
        ),
        (
            {"en": {"hello"}, "fr": {"bonjour"}},
            {MultiLangStringFlag.PRINT_WITH_QUOTES: True, MultiLangStringFlag.PRINT_WITH_LANG: False},
            ['"bonjour"', '"hello"'],
        ),
        (
            {"en": {"Hello World"}, "es": {"Hola Mundo"}},
            {MultiLangStringFlag.PRINT_WITH_QUOTES: False, MultiLangStringFlag.PRINT_WITH_LANG: True},
            ["Hello World@en", "Hola Mundo@es"],
        ),
        (
            {"en": {"Hello 😊"}, "es": {"Hola 😃"}},
            {MultiLangStringFlag.PRINT_WITH_QUOTES: True, MultiLangStringFlag.PRINT_WITH_LANG: True},
            ['"Hello 😊"@en', '"Hola 😃"@es'],
        ),
        (
            {"en": {"你好"}, "zh": {"世界"}},
            {MultiLangStringFlag.PRINT_WITH_QUOTES: False, MultiLangStringFlag.PRINT_WITH_LANG: True},
            ["世界@zh", "你好@en"],
        ),
        (
            {"en": {"Hello\nWorld"}, "es": {"Hola\nMundo"}},
            {MultiLangStringFlag.PRINT_WITH_QUOTES: True, MultiLangStringFlag.PRINT_WITH_LANG: True},
            ['"Hello\nWorld"@en', '"Hola\nMundo"@es'],
        ),
    ],
)
def test_from_multilangstring_to_strings_various_flags_effects(mls_dict: dict, flags: dict, expected: list) -> None:
    """Test the from_multilangstring_to_strings method with various flags effects.

    :param mls_dict: Dictionary representing the MultiLangString object.
    :param flags: Dictionary of flags and their values.
    :param expected: Expected list of string representations.
    :raises AssertionError: If the conversion does not return the expected string value.
    """
    multilangstring = MultiLangString(mls_dict)
    for flag, value in flags.items():
        Controller.set_flag(flag, value)
    result = Converter.from_multilangstring_to_strings(multilangstring)
    assert result == expected, f"Expected '{expected}', got '{result}'"


@pytest.mark.parametrize(
    "mls_dict, expected",
    [
        ({"en": {"Hello"}, "es": {"Hola"}}, ["Hello@en", "Hola@es"]),
        ({"en": {"你好"}, "zh": {"世界"}}, ["世界@zh", "你好@en"]),
        ({"en": {"Hello😊"}}, ["Hello😊@en"]),
        ({"en": {"HELLO"}, "es": {"HOLA"}}, ["HELLO@en", "HOLA@es"]),
        ({"en": {"Hello "}, "es": {" Hola"}}, [" Hola@es", "Hello @en"]),
        ({"en": {"HELLO"}, "ru": {"ПРИВЕТ"}}, ["HELLO@en", "ПРИВЕТ@ru"]),
        ({"en": {"Hello"}, "jp": {"こんにちは"}}, ["Hello@en", "こんにちは@jp"]),
        ({"en": {"Hello😊"}}, ["Hello😊@en"]),
    ],
)
def test_from_multilangstring_to_strings_operation_on_itself(mls_dict: dict, expected: list) -> None:
    """Test the from_multilangstring_to_strings method by performing the conversion twice.

    :param mls_dict: Dictionary representing the initial MultiLangString object.
    :param expected: Expected list of string representations after two conversions.
    :raises AssertionError: If the conversion does not return the expected string value.
    """
    Controller.set_flag(MultiLangStringFlag.PRINT_WITH_QUOTES, False)
    Controller.set_flag(MultiLangStringFlag.PRINT_WITH_LANG, True)
    multilangstring = MultiLangString(mls_dict)

    first_result = Converter.from_multilangstring_to_strings(multilangstring)
    second_multilangstring = MultiLangString({s.split("@")[1]: {s.split("@")[0]} for s in first_result})
    second_result = Converter.from_multilangstring_to_strings(second_multilangstring)

    assert first_result == expected, f"First conversion mismatch: {first_result} != {expected}"
    assert second_result == expected, f"Second conversion mismatch: {second_result} != {expected}"


@pytest.mark.parametrize(
    "mls_dict, expected",
    [
        ({}, []),
        ({"en": set()}, []),
        ({"en": {""}, "es": {"Hola"}}, ['""@en', '"Hola"@es']),
        ({"en": {"Hello\nWorld"}, "es": {"Hola\nMundo"}}, ['"Hello\nWorld"@en', '"Hola\nMundo"@es']),
        ({"en": {"\n\n"}, "es": {"\t\t"}}, ['"\t\t"@es', '"\n\n"@en']),
        ({"en": {" "}, "es": {" "}}, ['" "@en', '" "@es']),
        ({"en": {"HELLO"}, "es": {"HOLA"}, "fr": {"BONJOUR"}}, ['"BONJOUR"@fr', '"HELLO"@en', '"HOLA"@es']),
        ({"en": {""}, "fr": {""}}, ['""@en', '""@fr']),
    ],
)
def test_from_multilangstring_to_strings_edge_cases(mls_dict: dict, expected: list):
    """Test the from_multilangstring_to_strings method with edge cases.

    :param mls_dict: Dictionary representing the MultiLangString object.
    :param expected: Expected list of string representations.
    :raises AssertionError: If the conversion does not return the expected string value.
    """
    Controller.reset_flags()
    multilangstring = MultiLangString(mls_dict)
    result = Converter.from_multilangstring_to_strings(multilangstring)
    assert result == expected, f"Expected '{expected}', got '{result}'"


# Test invalid types
@pytest.mark.parametrize(
    "invalid_input",
    [
        None,
        123,
        "invalid",
        45.67,
        [1, 2, 3],
        (4, 5, 6),
        {"valid_key": ["invalid_value"]},
    ],
)
def test_from_multilangstring_to_strings_invalid_type(invalid_input):
    """Test the from_multilangstring_to_strings method with invalid input types.

    :param invalid_input: Invalid input to test.
    :raises TypeError: If the input type is invalid.
    """
    with pytest.raises(TypeError, match="Invalid argument with value"):
        Converter.from_multilangstring_to_strings(invalid_input)


# Test default and null inputs
def test_from_multilangstring_to_strings_default():
    """Test the from_multilangstring_to_strings method with default input.

    :raises AssertionError: If the conversion does not return the expected string value.
    """
    multilangstring = MultiLangString()
    expected = []
    result = Converter.from_multilangstring_to_strings(multilangstring)
    assert result == expected, f"Expected '{expected}', got '{result}'"


# Edge cases with unusual but valid inputs
@pytest.mark.parametrize(
    "mls_dict, expected",
    [
        ({"en": {""}, "es": {"Hola"}}, ['""@en', '"Hola"@es']),
        ({"": {"Hello"}, "es": {"Hola"}}, ['"Hello"@', '"Hola"@es']),
        ({"en": {" "}, "es": {" "}}, ['" "@en', '" "@es']),
    ],
)
def test_from_multilangstring_to_strings_unusual_valid(mls_dict: dict, expected: list):
    """Test the from_multilangstring_to_strings method with unusual but valid inputs.

    :param mls_dict: Dictionary representing the MultiLangString object.
    :param expected: Expected list of string representations.
    :raises AssertionError: If the conversion does not return the expected string value.
    """
    multilangstring = MultiLangString(mls_dict)
    result = Converter.from_multilangstring_to_strings(multilangstring)
    assert result == expected, f"Expected '{expected}', got '{result}'"


# Test edge cases with empty strings and special characters
@pytest.mark.parametrize(
    "mls_dict, expected",
    [
        ({"en": {"\n", "\n\n"}}, ['"\n\n"@en', '"\n"@en']),
        ({"en": {"\t", "\t\t"}}, ['"\t\t"@en', '"\t"@en']),
    ],
)
def test_from_multilangstring_to_strings_special_characters(mls_dict: dict, expected: list):
    """Test the from_multilangstring_to_strings method with special character inputs.

    :param mls_dict: Dictionary representing the MultiLangString object.
    :param expected: Expected list of string representations.
    :raises AssertionError: If the conversion does not return the expected string value.
    """
    multilangstring = MultiLangString(mls_dict)
    result = Converter.from_multilangstring_to_strings(multilangstring)
    assert result == expected, f"Expected '{expected}', got '{result}'"


# Operation on itself with default and null inputs
def test_from_multilangstring_to_strings_operation_on_itself_default():
    """Test the from_multilangstring_to_strings method by performing the conversion twice with default input.

    :raises AssertionError: If the conversion does not return the expected string value.
    """
    Controller.set_flag(MultiLangStringFlag.PRINT_WITH_QUOTES, False)
    Controller.set_flag(MultiLangStringFlag.PRINT_WITH_LANG, True)
    multilangstring = MultiLangString()

    first_result = Converter.from_multilangstring_to_strings(multilangstring)
    second_multilangstring = MultiLangString({s.split("@")[1]: {s.split("@")[0]} for s in first_result})
    second_result = Converter.from_multilangstring_to_strings(second_multilangstring)

    expected = []
    assert first_result == expected, f"First conversion mismatch: {first_result} != {expected}"
    assert second_result == expected, f"Second conversion mismatch: {second_result} != {expected}"

    # Test invalid values
    @pytest.mark.parametrize(
        "mls_dict, expected_error",
        [
            ({"en": None}, TypeError),
            ({"en": 123}, TypeError),
            ({"en": [1, 2, 3]}, TypeError),
        ],
    )
    def test_from_multilangstring_to_strings_invalid_values(mls_dict: dict, expected_error: type):
        """Test the from_multilangstring_to_strings method with invalid values.

        :param mls_dict: Dictionary representing the MultiLangString object.
        :param expected_error: Expected error type.
        :raises AssertionError: If the input value is invalid and does not raise the expected error.
        """
        with pytest.raises(expected_error, match="Invalid argument with value"):
            MultiLangString(mls_dict)


# Operation on itself with default and null inputs
def test_from_multilangstring_to_strings_operation_on_itself_null():
    """Test the from_multilangstring_to_strings method by performing the conversion twice with null input.

    :raises AssertionError: If the conversion does not return the expected string value.
    """
    Controller.set_flag(MultiLangStringFlag.PRINT_WITH_QUOTES, False)
    Controller.set_flag(MultiLangStringFlag.PRINT_WITH_LANG, True)
    multilangstring = MultiLangString(None)

    first_result = Converter.from_multilangstring_to_strings(multilangstring)
    second_multilangstring = MultiLangString({s.split("@")[1]: {s.split("@")[0]} for s in first_result})
    second_result = Converter.from_multilangstring_to_strings(second_multilangstring)

    expected = []
    assert first_result == expected, f"First conversion mismatch: {first_result} != {expected}"
    assert second_result == expected, f"Second conversion mismatch: {second_result} != {expected}"
