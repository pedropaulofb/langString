import pytest
from langstring import MultiLangString
from tests.conftest import TYPEERROR_MSG_SINGULAR


@pytest.mark.parametrize(
    "print_quotes, separator, print_lang, expected_output",
    [
        (True, "@", True, ['"Hello"@en', '"Hola"@es']),
        (False, "@", True, ["Hello@en", "Hola@es"]),
        (True, "-", False, ['"Hello"', '"Hola"']),
        (False, "-", False, ["Hello", "Hola"]),
        (True, " ", True, ['"Hello" en', '"Hola" es']),  # Space as separator
        (False, "_", False, ["Hello", "Hola"]),  # Underscore as separator, no lang, no quotes
        (True, "", True, ['"Hello"en', '"Hola"es']),  # No separator with language
        (False, "@", False, ["Hello", "Hola"]),  # No quotes, no language despite separator
        (True, "@", False, ['"Hello"', '"Hola"']),  # Quotes without language
    ],
)
def test_to_strings_with_various_options(print_quotes, separator, print_lang, expected_output):
    """Test the to_strings method with various combinations of options.

    :param print_quotes: Boolean to include quotes in output.
    :param separator: String separator between text and language.
    :param print_lang: Boolean to include language in output.
    :param expected_output: Expected list of strings output.
    """
    mls = MultiLangString({"en": {"Hello"}, "es": {"Hola"}})
    assert (
        mls.to_strings(print_quotes=print_quotes, separator=separator, print_lang=print_lang) == expected_output
    ), "to_strings does not produce the expected output with various options"


@pytest.mark.parametrize(
    "langs, expected_output",
    [
        (["en"], ['"Hello"@en']),
        ([], []),
        (["de"], []),
        (["en", "es"], ['"Hello"@en', '"Hola"@es']),  # Multiple languages
        (["ru"], []),  # Non-existent language
        (["en", "non-existent"], ['"Hello"@en']),  # Mix of existent and non-existent languages
        # Assuming your implementation treats language codes in a case-insensitive manner
        (["EN", "ES"], ['"Hello"@EN', '"Hola"@ES']),  # Both upper case, matching entries in a case-insensitive manner
        (["eN", "Es"], ['"Hello"@eN', '"Hola"@Es']),  # Mixed case, matching entries in a case-insensitive manner
    ],
)
def test_to_strings_with_langs_option(langs, expected_output):
    """Test the to_strings method with langs option specifying which languages to include.

    :param langs: List of languages to include in output.
    :param expected_output: Expected list of strings output.
    """
    mls = MultiLangString({"en": {"Hello"}, "es": {"Hola"}})
    assert (
        mls.to_strings(langs=langs, print_quotes=True, separator="@") == expected_output
    ), "to_strings does not produce the expected output with langs option"


@pytest.mark.parametrize(
    "invalid_param, value",
    [
        ("print_quotes", "not_a_boolean"),
        ("separator", 123),
        ("langs", "not_a_list"),
        ("langs", [123]),
        ("print_lang", "not_a_boolean"),
        ("separator", True),
        ("langs", {"en", "es"}),  # Passing a set instead of list
        ("langs", [123, "en"]),  # Mix of valid and invalid types within list
    ],
)
def test_to_strings_with_invalid_parameters(invalid_param, value):
    """Test the to_strings method with invalid parameter values, expecting TypeError.

    :param invalid_param: Name of the parameter being tested.
    :param value: Invalid value to test for the parameter.
    """
    mls = MultiLangString({"en": {"Hello"}, "es": {"Hola"}})
    with pytest.raises(TypeError, match=TYPEERROR_MSG_SINGULAR):
        kwargs = {invalid_param: value}
        mls.to_strings(**kwargs)


def test_to_strings_with_valid_none_parameter():
    """Test the to_strings method with invalid parameter values, expecting TypeError.

    :param invalid_param: Name of the parameter being tested.
    :param value: Invalid value to test for the parameter.
    """
    mls = MultiLangString({"en": {"Hello"}, "es": {"Hola"}})
    assert mls.to_strings(None) == ['"Hello"@en', '"Hola"@es']
    assert mls.to_strings() == ['"Hello"@en', '"Hola"@es']


@pytest.mark.parametrize(
    "separator",
    [
        (", "),  # Unusual separator
        (""),  # No separator
    ],
)
def test_to_strings_with_unusual_separators(separator):
    """Test the to_strings method with unusual but valid separators.
    :param separator: Unusual separator string.
    """
    mls = MultiLangString({"en": {"Hello"}})
    expected_output = [f'"Hello"{separator}en'] if separator else ['"Hello"en']
    assert (
        mls.to_strings(print_quotes=True, separator=separator, print_lang=True) == expected_output
    ), f"to_strings does not handle unusual separator '{separator}' correctly"


@pytest.mark.parametrize(
    "print_lang",
    [
        (None),  # Explicit None should default to controller flag
    ],
)
def test_to_strings_with_explicit_none_for_print_lang(print_lang):
    """Test the to_strings method with explicit None for print_lang, expecting default behavior.
    :param print_lang: Explicit None value for print_lang.
    """
    mls = MultiLangString({"en": {"Hello"}})
    # Assuming Controller.get_flag(MultiLangStringFlag.PRINT_WITH_LANG) returns True as default
    expected_output = ['"Hello"@en']
    assert (
        mls.to_strings(print_quotes=True, print_lang=print_lang) == expected_output
    ), "to_strings does not revert to default behavior with explicit None for print_lang"


def test_to_strings_on_empty_MultiLangString():
    """Test the to_strings method on an empty MultiLangString instance."""
    mls = MultiLangString()
    assert mls.to_strings() == [], "to_strings should return an empty list when called on an empty MultiLangString"


@pytest.mark.parametrize(
    "input_langs, test_langs, expected_output",
    [
        # Case-insensitive handling: Adjust expected outputs to reflect normalized language codes
        ({"en": {"Hello"}, "ES": {"Hola"}}, ["EN", "es"], ['"Hello"@EN', '"Hola"@es']),  # Case-insensitive match
        ({"EN": {"Hello"}, "es": {"Hola"}}, ["en", "ES"], ['"Hello"@en', '"Hola"@ES']),  # Case-insensitive match
        ({"EN": {"Hello"}, "es": {"Hola"}}, ["en", "ES"], ['"Hello"@en', '"Hola"@ES']),  # Case-insensitive match
        ({"eN": {"Hello"}, "Es": {"Hola"}}, ["EN", "es"], ['"Hello"@EN', '"Hola"@es']),  # Case-insensitive match
    ],
)
def test_to_strings_with_case_sensitivity(input_langs, test_langs, expected_output):
    """Test the to_strings method considering different cases in langs argument and MultiLangString dict's lang.
    :param input_langs: Dict of language-text pairs for initializing MultiLangString, with case variations.
    :param test_langs: Languages to test with the langs argument, with case variations.
    :param expected_output: Expected list of strings output, assuming case-insensitive handling.
    """
    mls = MultiLangString(input_langs)
    actual_output = mls.to_strings(langs=test_langs, print_quotes=True, separator="@")
    assert sorted(actual_output) == sorted(
        expected_output
    ), "to_strings does not handle language case sensitivity correctly"


@pytest.mark.parametrize(
    "langs, expected_output",
    [
        (["xx"], ['"Hello"@xx']),  # Fictional/uncommon language code
        (["xy"], []),  # Non-existent language in the MultiLangString
        (["XX"], ['"Hello"@XX']),  # Upper case fictional/uncommon language code
        (["x-x"], ['"Greetings"@x-x']),  # Language code with subtag
        (["x_X"], ['"Salutations"@x_X']),  # Language code with underscore
    ],
)
def test_to_strings_with_uncommon_langs(langs, expected_output):
    """Test handling of uncommon or fictional language codes."""
    mls = MultiLangString({"xx": {"Hello"}, "x-x": {"Greetings"}, "x_X": {"Salutations"}})
    assert mls.to_strings(langs=langs, print_quotes=True, separator="@") == expected_output


@pytest.mark.parametrize(
    "texts, langs, expected_output",
    [
        ({"utf8": {"こんにちは"}}, ["utf8"], ['"こんにちは"@utf8']),  # UTF-8 encoded text
        ({"emoji": {"🚀"}}, ["emoji"], ['"🚀"@emoji']),  # Emoji as text
        ({"special": {"çå∂"}}, ["special"], ['"çå∂"@special']),  # Special characters
    ],
)
def test_to_strings_with_text_encodings(texts, langs, expected_output):
    """Test handling of text with different encodings."""
    mls = MultiLangString(texts)
    assert mls.to_strings(langs=langs, print_quotes=True, separator="@") == expected_output


@pytest.mark.parametrize(
    "langs, expected_output",
    [
        (["en-US"], ['"Hello"@en-US']),  # Language tag with subtag
        (["zh-Hant"], ['"你好"@zh-Hant']),  # Traditional Chinese
        (["pt-BR"], ['"Olá"@pt-BR']),  # Brazilian Portuguese
        (["fr-CA"], ['"Salut"@fr-CA']),  # Canadian French
        (["en-GB"], ['"Hello"@en-GB']),  # British English
        (["es-419"], ['"Hola"@es-419']),  # Latin American Spanish
    ],
)
def test_to_strings_with_lang_subtags(langs, expected_output):
    """Test handling of language tags that include subtags."""
    mls = MultiLangString(
        {
            "en-US": {"Hello"},
            "zh-Hant": {"你好"},
            "pt-BR": {"Olá"},
            "fr-CA": {"Salut"},
            "en-GB": {"Hello"},
            "es-419": {"Hola"},
        }
    )
    assert mls.to_strings(langs=langs, print_quotes=True, separator="@") == expected_output


@pytest.mark.parametrize(
    "texts, print_lang, expected_output",
    [
        # Testing with empty language code and print_lang=True
        ({"": {"Text with no language"}}, True, ['"Text with no language"@']),
    ],
)
def test_to_strings_with_empty_lang_code(texts, print_lang, expected_output):
    """Test handling of texts with an empty language code."""
    mls = MultiLangString(texts)
    assert (
        mls.to_strings(print_quotes=True, print_lang=print_lang) == expected_output
    ), "to_strings does not correctly handle empty language codes."
