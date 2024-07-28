import pytest
from langstring import Converter
from langstring import MultiLangString
from langstring import SetLangString
from tests.conftest import TYPEERROR_MSG_SINGULAR


@pytest.mark.parametrize(
    "texts, lang, expected_texts",
    [
        ({"Hello", "World"}, "en", {"Hello", "World"}),
        ({"Hello", "Hello", "World"}, "en", {"Hello", "World"}),
        ({"Hola", "Mundo"}, "es", {"Hola", "Mundo"}),
        (set(), "en", set()),  # Empty set of texts
        ({"   Leading and trailing spaces   "}, "en", {"   Leading and trailing spaces   "}),
        ({"MixedCASE", "lowercase", "UPPERCASE"}, "en", {"MixedCASE", "lowercase", "UPPERCASE"}),
        ({"Γειά", "σου", "Κόσμε"}, "el", {"Γειά", "σου", "Κόσμε"}),  # Greek characters
        ({"Привет", "мир"}, "ru", {"Привет", "мир"}),  # Cyrillic characters
        ({"Hello😊", "World🌍"}, "en", {"Hello😊", "World🌍"}),  # Emojis
        ({"Special&*()[]Characters"}, "en", {"Special&*()[]Characters"}),
        ({"Text with spaces", "Textwithnospaces"}, "en", {"Text with spaces", "Textwithnospaces"}),
        ({"Hello", "World"}, "en-US", {"Hello", "World"}),  # Language tag with subtag
        ({"こんにちは", "世界"}, "ja", {"こんにちは", "世界"}),  # Japanese characters
        ({"Hello", "Hello"}, "en", {"Hello"}),  # Duplicate texts
        (
            {"Complex-Language-Tag-With-Many-Subtags"},
            "en-GB-oed",
            {"Complex-Language-Tag-With-Many-Subtags"},
        ),  # Complex language tag
        ({"Καλημέρα", "Κόσμε", "😊"}, "el", {"Καλημέρα", "Κόσμε", "😊"}),  # Mixed characters and emojis in Greek
        ({"   Multiple   spaces   "}, "en", {"   Multiple   spaces   "}),  # Texts with multiple spaces
    ],
)
def test_from_setlangstring_to_multilangstring_valid(texts, lang, expected_texts):
    """
    Test the `from_setlangstring_to_multilangstring` method with various valid inputs to ensure correct conversion.

    :param texts: A set of strings representing texts in the SetLangString.
    :param lang: The language tag for these texts.
    :param expected_texts: The expected set of texts in the resulting MultiLangString.
    """
    set_lang_str = SetLangString(texts=texts, lang=lang)
    result = Converter.from_setlangstring_to_multilangstring(set_lang_str)

    assert isinstance(result, MultiLangString), "Conversion should result in a MultiLangString instance."
    assert result.mls_dict.get(lang) == expected_texts, f"Expected texts for '{lang}' were not found in the result."


@pytest.mark.parametrize(
    "input, error_type",
    [
        (123, TypeError),
        ("not a SetLangString instance", TypeError),
        (None, TypeError),
        ([], TypeError),
        ([SetLangString()], TypeError),
    ],
)
def test_from_setlangstring_to_multilangstring_invalid(input, error_type):
    """
    Test the `from_setlangstring_to_multilangstring` method with various invalid inputs to ensure proper error handling.

    :param input: The input to be tested, which is expected to cause an error.
    :param error_type: The type of error expected.
    """
    with pytest.raises(error_type, match=TYPEERROR_MSG_SINGULAR):
        Converter.from_setlangstring_to_multilangstring(input)


@pytest.mark.parametrize(
    "texts, lang",
    [
        ({f"test{i}" for i in range(1000)}, "en"),  # Large number of texts
        ({"Hello", "Bonjour", "Hola"}, "en-es-fr"),  # Unconventional but valid language code
        ({" "}, "en"),  # Texts with only a space
        ({""}, "en"),  # Empty string as text
        ({"Hello World"}, "   en  "),  # Lang with leading and trailing spaces
        ({"Text\nwith\nnewlines"}, "en"),  # Text with newlines
        ({"Hello", "hello", "HELLO"}, "en"),  # Case sensitivity in texts
    ],
)
def test_from_setlangstring_to_multilangstring_edge_cases(texts, lang):
    """
    Test `from_setlangstring_to_multilangstring` with edge cases including a large number of texts and unusual language codes.

    :param texts: A set of strings representing texts in the SetLangString.
    :param lang: The language tag for these texts, including unconventional but potentially valid codes.
    """
    set_lang_str = SetLangString(texts=texts, lang=lang)
    result = Converter.from_setlangstring_to_multilangstring(set_lang_str)

    assert isinstance(result, MultiLangString), "Conversion should result in a MultiLangString instance."
    assert result.mls_dict.get(lang) == texts, f"Expected texts for '{lang}' were not found in the result."
