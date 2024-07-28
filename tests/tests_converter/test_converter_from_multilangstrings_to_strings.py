import pytest
from langstring import Converter
from langstring import MultiLangString
from tests.conftest import TYPEERROR_MSG_SINGULAR


@pytest.mark.parametrize(
    "input_data,expected_output",
    [
        ([MultiLangString({"en": {"Hello"}, "fr": {"Bonjour"}})], ['"Bonjour"@fr', '"Hello"@en']),
        ([MultiLangString({"en": {"Hello", "Hi"}, "fr": {"Bonjour"}})], ['"Bonjour"@fr', '"Hello"@en', '"Hi"@en']),
        (
            [MultiLangString({"es": {"Hola"}, "fr": {"Bonjour"}, "en": {"Hello"}})],
            ['"Bonjour"@fr', '"Hello"@en', '"Hola"@es'],
        ),
        ([MultiLangString({"en": {" "}, "fr": {" "}})], ['" "@en', '" "@fr']),
        ([MultiLangString({"gr": {"Γειά"}, "ru": {"Привет"}})], ['"Γειά"@gr', '"Привет"@ru']),
        ([MultiLangString({"en": {"Hello😊"}})], ['"Hello😊"@en']),
        ([MultiLangString({"en": {"Hello"}, "empty": set()})], ['"Hello"@en']),
    ],
)
def test_from_multilangstrings_to_strings_success(input_data: list[MultiLangString], expected_output: list[str]):
    """Test the successful conversion of a list of MultiLangString instances to a unified string representation.

    :param input_data: The list of MultiLangString instances to be converted.
    :param expected_output: The expected list of string outputs after conversion, each tagged with its language.
    """
    result = Converter.from_multilangstrings_to_strings(input_data)
    assert result == expected_output, f"Expected {expected_output} but got {result}"


@pytest.mark.parametrize(
    "input_data",
    [
        123,
        "NotAMultiLangString",
    ],
)
def test_from_multilangstrings_to_strings_type_error(input_data):
    """Test the method raises a TypeError with appropriate message for invalid input types.

    :param input_data: The input data expected to raise TypeError upon conversion attempt.
    :param exception_message: The expected error message.
    """
    with pytest.raises(TypeError, match=TYPEERROR_MSG_SINGULAR):
        Converter.from_multilangstrings_to_strings(input_data)


def test_from_multilangstrings_to_strings_empty_input():
    """Test the method's behavior with an empty list of MultiLangString instances."""
    empty_mls = [MultiLangString({})]
    result = Converter.from_multilangstrings_to_strings(empty_mls)
    assert result == [], "Expected an empty list for an empty list of MultiLangString inputs"


@pytest.mark.parametrize(
    "input_data,expected_output",
    [
        ([MultiLangString({"en": set()})], []),
        ([MultiLangString({"en": {" "}})], ['" "@en']),
        ([MultiLangString({"en": {""}})], ['""@en']),
        (
            [MultiLangString({"en": {" leading space"}, "fr": {"trailing space "}})],
            ['" leading space"@en', '"trailing space "@fr'],
        ),
        ([MultiLangString({"mixed": {"UPPER lower"}})], ['"UPPER lower"@mixed']),
        ([MultiLangString({"special": {"@#$%"}})], ['"@#$%"@special']),
    ],
)
def test_from_multilangstrings_to_strings_edge_cases(input_data: list[MultiLangString], expected_output: list[str]):
    """Test the method's handling of edge cases, such as empty sets or spaces as inputs within MultiLangString instances.

    :param input_data: The list of MultiLangString instances to be converted, representing edge cases.
    :param expected_output: The expected list of string outputs after conversion, each potentially tagged with its language.
    """
    result = Converter.from_multilangstrings_to_strings(input_data)
    assert result == expected_output, f"Expected {expected_output} but got {result}"


@pytest.mark.parametrize(
    "input_data, expected_exception",
    [
        (None, TypeError),  # Assuming the method should raise TypeError for None input
    ],
)
def test_from_multilangstrings_to_strings_none_input(input_data, expected_exception):
    """Test the method raises an exception for None input."""
    with pytest.raises(expected_exception, match=TYPEERROR_MSG_SINGULAR):
        Converter.from_multilangstrings_to_strings(input_data)


@pytest.mark.parametrize(
    "input_data, print_quotes, print_langs, separator, expected_output",
    [
        # Test print_quotes effect
        ([MultiLangString({"en": {"Hello"}})], False, True, "; ", ["Hello; en"]),
        ([MultiLangString({"en": {"Hello"}})], True, True, "; ", ['"Hello"; en']),
        # Test print_langs effect
        ([MultiLangString({"en": {"Hello"}})], True, False, "; ", ['"Hello"']),
        # Test separator effect with corrected handling for output separation
        ([MultiLangString({"en": {"Hello", "Hi"}})], True, False, ", ", ['"Hello"', '"Hi"']),
    ],
)
def test_from_multilangstrings_to_strings_optional_params(
    input_data: list[MultiLangString], print_quotes: bool, print_langs: bool, separator: str, expected_output: list[str]
):
    """Test the effects of optional parameters on the method's output.

    :param input_data: The list of MultiLangString instances to be converted.
    :param print_quotes: Flag to control quoting of output strings.
    :param print_langs: Flag to control inclusion of language tags in output.
    :param separator: String used to separate multiple entries in a single language.
    :param expected_output: The expected list of string outputs after conversion.
    """
    result = Converter.from_multilangstrings_to_strings(
        input_data, print_quotes=print_quotes, print_lang=print_langs, separator=separator
    )
    assert result == expected_output, f"Expected {expected_output} but got {result}"


@pytest.mark.parametrize(
    "input_data, print_quotes, print_langs, separator, expected_output",
    [
        # Correct behavior for toggling language tags with 'print_langs'
        ([MultiLangString({"en": {"Hello"}})], False, False, "; ", ["Hello"]),  # Without language tag
        ([MultiLangString({"en": {"Hello"}})], True, False, "; ", ['"Hello"']),  # Quotes without language tag
        # Adding cases to existing parameterization
        ([MultiLangString({"en": {"Hello world"}})], False, False, ";", ["Hello world"]),
        ([MultiLangString({"en": {"   "}})], True, True, "; ", ['"   "; en']),
        ([MultiLangString({"cy": {"Helo"}, "en": {"Hello"}})], True, False, " & ", ['"Hello"', '"Helo"']),
        ([MultiLangString({"special": {"*&^%$#@!"}})], True, True, " - ", ['"*&^%$#@!" - special']),
        ([MultiLangString({"emoji": {"😊👍"}, "text": {"hello"}})], False, True, "/", ["hello/text", "😊👍/emoji"]),
    ],
)
def test_from_multilangstrings_to_strings_flags_effect_corrected(
    input_data: list[MultiLangString], print_quotes: bool, print_langs: bool, separator: str, expected_output: list[str]
):
    """Test to verify the actual effects of optional parameters, especially 'print_langs'."""
    result = Converter.from_multilangstrings_to_strings(
        input_data, print_quotes=print_quotes, print_lang=print_langs, separator=separator
    )
    assert result == expected_output, f"Expected {expected_output} but got {result}"
