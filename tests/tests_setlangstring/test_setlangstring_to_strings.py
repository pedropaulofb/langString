import pytest
from langstring.setlangstring import SetLangString


@pytest.mark.parametrize(
    "texts, lang, expected_strings",
    [
        ({"Hello", "World"}, "en", ['"Hello"@en', '"World"@en']),
        (set(), "en", []),
        ({"こんにちは", "世界"}, "ja", ['"こんにちは"@ja', '"世界"@ja']),
        ({"Hello"}, "", ['"Hello"@']),
    ],
)
def test_to_strings_basic(texts: set[str], lang: str, expected_strings: list[str]):
    """Test the basic functionality of to_strings method in SetLangString without any flags."""
    set_lang_string = SetLangString(texts, lang)
    assert sorted(set_lang_string.to_strings()) == sorted(
        expected_strings
    ), "to_strings did not return the expected list of strings."


@pytest.mark.parametrize(
    "texts, lang",
    [
        ({"Hello", "World"}, "en"),
        ({"こんにちは", "世界"}, "ja"),
    ],
)
def test_to_strings_immutable(texts, lang):
    """Ensure that the to_strings method does not mutate the SetLangString instance."""
    set_lang_string = SetLangString(texts, lang)
    before_texts = set_lang_string.texts.copy()
    before_lang = set_lang_string.lang
    set_lang_string.to_strings()  # Call the method to potentially mutate the instance
    assert (
        set_lang_string.texts == before_texts and set_lang_string.lang == before_lang
    ), "to_strings method mutated the SetLangString instance."


@pytest.mark.parametrize(
    "texts, lang, print_quotes, separator, print_lang, expected_strings",
    [
        ({"Hello", "World"}, "en", True, "@", True, ['"Hello"@en', '"World"@en']),
        ({"Hello", "World"}, "en", False, "@", True, ["Hello@en", "World@en"]),
        ({"Hello", "World"}, "en", True, "@", False, ['"Hello"', '"World"']),
        (set(), "en", True, "@", True, []),
        ({"こんにちは", "世界"}, "ja", True, "@", True, ['"こんにちは"@ja', '"世界"@ja']),
        ({"Hello"}, "", True, "@", True, ['"Hello"@']),
        ({"Hello", "World"}, "en", False, "#", True, ["Hello#en", "World#en"]),
        ({"Hello", "World"}, "en", True, "#", False, ['"Hello"', '"World"']),
    ],
)
def test_to_strings_with_options(texts, lang, print_quotes, separator, print_lang, expected_strings):
    """Test the to_strings method with various formatting options."""
    set_lang_string = SetLangString(texts, lang)
    result = set_lang_string.to_strings(print_quotes=print_quotes, separator=separator, print_lang=print_lang)
    assert sorted(result) == sorted(
        expected_strings
    ), "to_strings did not return the expected list of strings with given formatting options."


@pytest.mark.parametrize(
    "initial_texts, lang, expected_output",
    [
        ({"Hello", "World"}, "en", ['"Hello"@en', '"World"@en']),
        ({"One"}, "en", ['"One"@en']),
        (set(), "en", []),
    ],
)
def test_to_strings_without_flags(initial_texts, lang, expected_output):
    """Test `to_strings` without any SetLangStringFlag flags affecting output."""
    set_lang_string = SetLangString(initial_texts, lang)
    result = set_lang_string.to_strings()
    assert sorted(result) == sorted(
        expected_output
    ), "The to_strings method output did not match the expected output without any flags."


@pytest.mark.parametrize(
    "initial_texts, lang, expected_output, print_quotes, separator, print_lang",
    [
        # Default formatting
        ({"Hello", "World"}, "en", ['"Hello"@en', '"World"@en'], True, "@", True),
        # Without quotes
        ({"Hello", "World"}, "en", ["Hello@en", "World@en"], False, "@", True),
        # Without lang
        ({"Hello", "World"}, "en", ['"Hello"', '"World"'], True, "@", False),
        # Without quotes and lang
        ({"Hello", "World"}, "en", ["Hello", "World"], False, "@", False),
        # Custom separator
        ({"Hello", "World"}, "en", ['"Hello"#en', '"World"#en'], True, "#", True),
        # Empty set
        (set(), "en", [], True, "@", True),
    ],
)
def test_to_strings_various_configurations(initial_texts, lang, expected_output, print_quotes, separator, print_lang):
    """Test `to_strings` with various configurations."""
    set_lang_string = SetLangString(initial_texts, lang)
    result = set_lang_string.to_strings(print_quotes=print_quotes, separator=separator, print_lang=print_lang)
    assert sorted(result) == sorted(
        expected_output
    ), "The to_strings method output did not match the expected output with given configurations."


@pytest.mark.parametrize(
    "texts, lang, print_quotes, expected_output",
    [
        ({"Hello", "World"}, "en", True, ['"Hello"@en', '"World"@en']),
        ({"Hello", "World"}, "en", False, ["Hello@en", "World@en"]),
    ],
)
def test_to_strings_print_quotes(texts, lang, print_quotes, expected_output):
    """Test the effect of the print_quotes parameter on the to_strings output."""
    set_lang_string = SetLangString(texts, lang)
    result = set_lang_string.to_strings(print_quotes=print_quotes)
    assert sorted(result) == sorted(expected_output), "Incorrect handling of print_quotes parameter."


@pytest.mark.parametrize(
    "texts, lang, separator, expected_output",
    [
        ({"Hello", "World"}, "en", "@", ['"Hello"@en', '"World"@en']),
        ({"Hello", "World"}, "en", "#", ['"Hello"#en', '"World"#en']),
    ],
)
def test_to_strings_separator(texts, lang, separator, expected_output):
    """Test the effect of the separator parameter on the to_strings output."""
    set_lang_string = SetLangString(texts, lang)
    result = set_lang_string.to_strings(separator=separator)
    assert sorted(result) == sorted(expected_output), "Incorrect handling of separator parameter."


@pytest.mark.parametrize(
    "texts, lang, print_lang, expected_output",
    [
        ({"Hello", "World"}, "en", True, ['"Hello"@en', '"World"@en']),
        ({"Hello", "World"}, "en", False, ['"Hello"', '"World"']),
    ],
)
def test_to_strings_print_lang(texts, lang, print_lang, expected_output):
    """Test the effect of the print_lang parameter on the to_strings output."""
    set_lang_string = SetLangString(texts, lang)
    result = set_lang_string.to_strings(print_lang=print_lang)
    assert sorted(result) == sorted(expected_output), "Incorrect handling of print_lang parameter."


@pytest.mark.parametrize(
    "texts, lang, print_quotes, separator, print_lang, expected_output, custom_case",
    [
        ({"Hello", "World"}, "en", True, "@", True, ['"Hello"@en', '"World"@en'], "Default case with quotes and lang"),
        ({"Hello", "World"}, "en", False, "@", True, ["Hello@en", "World@en"], "Without quotes"),
        ({"Hello", "World"}, "en", True, "@", False, ['"Hello"', '"World"'], "Without lang"),
        ({"Hello", "World"}, "en", True, "##", True, ['"Hello"##en', '"World"##en'], "Custom separator"),
        (set(), "en", True, "@", True, [], "Empty set"),
    ],
)
def test_to_strings_detailed_cases(texts, lang, print_quotes, separator, print_lang, expected_output, custom_case):
    """Test to_strings method with detailed case-specific configurations."""
    set_lang_string = SetLangString(texts, lang)
    result = set_lang_string.to_strings(print_quotes=print_quotes, separator=separator, print_lang=print_lang)
    assert sorted(result) == sorted(expected_output), f"{custom_case} failed: Unexpected output."


@pytest.mark.parametrize(
    "texts, lang, print_quotes, separator, print_lang, expected_output",
    [
        # Testing strings with separator in the text
        ({"Hello@World", "Test"}, "en", True, "@", True, ['"Hello@World"@en', '"Test"@en']),
        # Testing strings with special characters
        ({"Hello#World", "Test$"}, "en", True, "@", True, ['"Hello#World"@en', '"Test$"@en']),
        # Testing strings with leading/trailing spaces
        ({" Hello ", "World "}, "en", True, "@", True, ['" Hello "@en', '"World "@en']),
        # Testing with a multi-character separator
        ({"Multi", "Separator"}, "en", True, "##", True, ['"Multi"##en', '"Separator"##en']),
        # Testing without quotes and with a special separator
        ({"NoQuotes", "SpecialSep"}, "en", False, "#", True, ["NoQuotes#en", "SpecialSep#en"]),
        # Testing the independence of print_quotes and print_lang
        ({"Independence", "Test"}, "en", False, "@", False, ["Independence", "Test"]),
    ],
)
def test_to_strings_advanced_customization(texts, lang, print_quotes, separator, print_lang, expected_output):
    """Test `to_strings` with advanced customization options to cover edge cases and unusual but valid usages."""
    set_lang_string = SetLangString(texts, lang)
    result = set_lang_string.to_strings(print_quotes=print_quotes, separator=separator, print_lang=print_lang)
    assert sorted(result) == sorted(expected_output), "Advanced customization cases failed: Unexpected output."


@pytest.mark.parametrize(
    "texts, lang, print_quotes, expected_output",
    [
        # Testing the impact of the print_quotes parameter
        ({"QuoteTest"}, "en", False, ["QuoteTest@en"]),
        # Ensuring quotes are handled correctly
        ({"'SingleQuotes'", '"DoubleQuotes"'}, "en", True, ['""DoubleQuotes""@en', "\"'SingleQuotes'\"@en"]),
    ],
)
def test_to_strings_quote_handling(texts, lang, print_quotes, expected_output):
    """Test how `to_strings` handles quotes in strings."""
    set_lang_string = SetLangString(texts, lang)
    result = set_lang_string.to_strings(print_quotes=print_quotes)
    assert sorted(result) == sorted(expected_output), "Quote handling cases failed: Unexpected output."
