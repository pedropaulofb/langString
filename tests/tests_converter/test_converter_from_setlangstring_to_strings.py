import pytest
from langstring import Converter
from langstring import LangString
from langstring import SetLangString
from tests.conftest import TYPEERROR_MSG_SINGULAR


@pytest.mark.parametrize(
    "texts, lang, print_quotes, separator, print_lang, expected",
    [
        ({"Hello", "World"}, "en", False, "@", False, ["Hello", "World"]),
        ({"Hello", "World"}, "en", True, "@", False, ['"Hello"', '"World"']),
        ({"Hello", "World"}, "en", False, "@", True, ["Hello@en", "World@en"]),
        ({"Hello", "World"}, "en", True, "@", True, ['"Hello"@en', '"World"@en']),
        (set(), "en", True, "@", True, []),
        ({"Emoji", "👍"}, "emoji", True, "~", True, ['"Emoji"~emoji', '"👍"~emoji']),
        ({"Mixed", "123"}, "num", False, "#", True, ["Mixed#num", "123#num"]),
    ],
)
def test_from_setlangstring_to_strings_variations(
    texts: set, lang: str, print_quotes: bool, separator: str, print_lang: bool, expected: list[str]
) -> None:
    """
    Test the `from_setlangstring_to_strings` method with various combinations of inputs and flags to ensure it
    correctly formats the strings according to the given parameters.

    :param texts: A set of texts to initialize the SetLangString object.
    :param lang: The language tag to be associated with the SetLangString object.
    :param print_quotes: Flag indicating whether the output strings should be enclosed in quotes.
    :param separator: The separator to be used between the text and the language tag in the output strings.
    :param print_lang: Flag indicating whether the language tag should be included in the output strings.
    :param expected: The expected list of formatted strings.
    """
    set_lang_string = SetLangString(texts=texts, lang=lang)
    result = Converter.from_setlangstring_to_strings(
        set_lang_string, print_quotes=print_quotes, separator=separator, print_lang=print_lang
    )
    assert sorted(result) == sorted(expected), (
        f"Expected {expected} but got {result} with configuration "
        f"(print_quotes={print_quotes}, separator='{separator}', "
        f"print_lang={print_lang})."
    )


@pytest.mark.parametrize(
    "invalid_input",
    [123, 1.2, LangString("a", "b"), "not a SetLangString", None, {}, []],
)
def test_from_setlangstring_to_strings_invalid_input(invalid_input):
    """Test from_setlangstring_to_strings with various invalid input types.

    :param invalid_input: The invalid input to test.
    :param expected_error: The expected error message.
    """
    with pytest.raises(TypeError, match=TYPEERROR_MSG_SINGULAR):
        Converter.from_setlangstring_to_strings(invalid_input)
