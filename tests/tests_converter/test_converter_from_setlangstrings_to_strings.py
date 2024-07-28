import pytest
from langstring import Converter
from langstring import SetLangString
from tests.conftest import TYPEERROR_MSG_SINGULAR


@pytest.mark.parametrize(
    "input_setlangstrings, expected_output",
    [
        ([SetLangString({"Hello", "World"}, "en")], ['"Hello"@en', '"World"@en']),
        ([SetLangString(set(), "en")], []),
        ([SetLangString({" "}, "en")], ['" "@en']),
        ([SetLangString({"HELLO", "WORLD"}, "en")], ['"HELLO"@en', '"WORLD"@en']),
        ([SetLangString({"Hello1", "WorLd2"}, "en")], ['"Hello1"@en', '"WorLd2"@en']),
        ([SetLangString({"Γειά", "Κόσμος"}, "el")], ['"Γειά"@el', '"Κόσμος"@el']),
        ([SetLangString({"Привет", "Мир"}, "ru")], ['"Мир"@ru', '"Привет"@ru']),
        ([SetLangString({"😊", "🚀"}, "emoji")], ['"😊"@emoji', '"🚀"@emoji']),
        ([SetLangString({" Hello ", " World "}, "en")], ['" Hello "@en', '" World "@en']),
        ([SetLangString({"hElLo@#%", "WoRlD&*()"}, "en")], ['"WoRlD&*()"@en', '"hElLo@#%"@en']),
    ],
)
def test_from_setlangstrings_to_strings_valid_inputs(input_setlangstrings, expected_output):
    """Test the `from_setlangstrings_to_strings` method with valid SetLangString inputs.

    :param input_setlangstrings: A SetLangString instance to convert.
    :param expected_output: The expected list of strings after conversion.
    :type input_setlangstrings: SetLangString
    :type expected_output: list
    :return: None
    """
    result = Converter.from_setlangstrings_to_strings(input_setlangstrings)
    assert result == expected_output, "Conversion from SetLangString to strings did not produce the expected output."


@pytest.mark.parametrize(
    "input_value", [None, 123, ["a", "list", "of", "strings"], {"a", "set", "of", "strings"}, True, "string"]
)
def test_from_setlangstrings_to_strings_invalid_inputs(input_value):
    """Test the `from_setlangstrings_to_strings` method with invalid input types.

    :param input_value: An invalid input value to the method.
    :type input_value: Any
    :raises TypeError: If input_value is not an instance of SetLangString.
    :return: None
    """
    with pytest.raises(TypeError, match=TYPEERROR_MSG_SINGULAR):
        Converter.from_setlangstrings_to_strings(input_value)


@pytest.mark.parametrize(
    "input_setlangstrings, expected_contains",
    [
        ([SetLangString({"Hello, World!", "@#$%^&*()"}, "en")], ['"Hello, World!"@en', '"@#$%^&*()"@en']),
        (
            [SetLangString({"Hello?!", "#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"}, "en")],
            ['"Hello?!"@en', '"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~"@en'],
        ),
    ],
)
def test_from_setlangstrings_to_strings_special_characters(input_setlangstrings, expected_contains):
    """Test the `from_setlangstrings_to_strings` method with SetLangString inputs containing special characters.

    :param input_setlangstrings: A SetLangString instance containing special characters.
    :param expected_contains: A list of strings that should be contained in the output.
    :type input_setlangstrings: SetLangString
    :type expected_contains: list
    :return: None
    """
    result = Converter.from_setlangstrings_to_strings(input_setlangstrings)
    for expected in expected_contains:
        assert expected in result, f"Expected '{expected}' to be in the conversion result."


@pytest.mark.parametrize(
    "input_setlangstrings",
    [
        ([SetLangString({"Hello"}, "en"), SetLangString({"Bonjour"}, "fr")]),
    ],
)
def test_from_setlangstrings_to_strings_multiple_languages(input_setlangstrings):
    """Test the `from_setlangstrings_to_strings` method with SetLangString inputs containing multiple languages.

    :param input_setlangstrings: A list of SetLangString instances containing different languages.
    :type input_setlangstrings: List[SetLangString]
    :return: None
    """
    result = Converter.from_setlangstrings_to_strings(input_setlangstrings)
    assert all(isinstance(item, str) for item in result), "Not all items in the result are strings."
    assert '"Hello"@en' in result and '"Bonjour"@fr' in result, "Expected multilingual output not found."


@pytest.mark.parametrize(
    "input_setlangstrings, print_lang, print_quotes, separator, expected_output",
    [
        ([SetLangString({"Hello"}, "en")], True, True, ";", ['"Hello";en']),
        ([SetLangString({"Hello", "World"}, "en")], False, False, ",", ["Hello", "World"]),
        ([SetLangString({"Hello"}, "en")], True, False, "-", ["Hello-en"]),
        (
            [SetLangString({"Hello", "Bonjour"}, "en"), SetLangString({"Hola"}, "es")],
            True,
            True,
            "@",
            ['"Bonjour"@en', '"Hello"@en', '"Hola"@es'],
        ),
        # Test with default values for print_lang, print_quotes, and separator not explicitly set (assuming defaults).
        ([SetLangString({"Hello", "World"}, "en")], True, True, " ", ['"Hello" en', '"World" en']),
        # Edge case with empty string as separator and defaults for print_lang and print_quotes.
        ([SetLangString({"Hello", "World"}, "en")], True, True, "", ['"Hello"en', '"World"en']),
        # Unusual but valid usage: non-standard character as separator with defaults for print_lang and print_quotes.
        ([SetLangString({"A", "B"}, "en")], True, True, "###", ['"A"###en', '"B"###en']),
    ],
)
def test_from_setlangstrings_to_strings_with_params(
    input_setlangstrings, print_lang, print_quotes, separator, expected_output
):
    """Test the `from_setlangstrings_to_strings` method considering print_lang, print_quotes, and separator.

    :param input_setlangstrings: A list of SetLangString instances to convert.
    :param print_lang: Boolean to indicate if language should be printed.
    :param print_quotes: Boolean to indicate if quotes should be used.
    :param separator: String to be used as separator between texts.
    :param expected_output: The expected list of strings after conversion.
    :type input_setlangstrings: List[SetLangString]
    :type print_lang: bool
    :type print_quotes: bool
    :type separator: str
    :type expected_output: list
    :return: None
    """
    result = Converter.from_setlangstrings_to_strings(
        input_setlangstrings, print_lang=print_lang, print_quotes=print_quotes, separator=separator
    )
    assert result == expected_output, "Conversion did not produce the expected output with given parameters."
