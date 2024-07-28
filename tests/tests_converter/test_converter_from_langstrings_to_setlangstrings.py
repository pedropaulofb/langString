import pytest
from langstring import Converter
from langstring import LangString
from langstring import SetLangString
from tests.conftest import TYPEERROR_MSG_SINGULAR


@pytest.mark.parametrize(
    "input_langstrings, expected_output",
    [
        ([], []),
        ([LangString("Hello", "en")], [SetLangString(texts={"Hello"}, lang="en")]),
        ([LangString("Hello", "en"), LangString("World", "en")], [SetLangString(texts={"Hello", "World"}, lang="en")]),
        (
            [LangString("Hello", "en"), LangString("Hola", "es")],
            [SetLangString(texts={"Hello"}, lang="en"), SetLangString(texts={"Hola"}, lang="es")],
        ),
        (
            [LangString("  Hello  ", "en"), LangString("World!", "en")],
            [SetLangString(texts={"  Hello  ", "World!"}, lang="en")],
        ),
        ([LangString("Привет", "ru"), LangString("Мир", "ru")], [SetLangString(texts={"Привет", "Мир"}, lang="ru")]),
        ([LangString("😀", "emoji"), LangString("🌍", "emoji")], [SetLangString(texts={"😀", "🌍"}, lang="emoji")]),
        ([LangString("", "en"), LangString(" ", "en")], [SetLangString(texts={"", " "}, lang="en")]),
        (
            [LangString("Hello", "en"), LangString("hello", "en"), LangString("Hello", "en")],
            [SetLangString(texts={"Hello", "hello"}, lang="en")],
        ),
        ([LangString("a" * 1000, "en") for _ in range(1000)], [SetLangString(texts={"a" * 1000}, lang="en")]),
        ([LangString("Hello", "En"), LangString("World", "eN")], [SetLangString(texts={"Hello", "World"}, lang="en")]),
        (
            [LangString("Hello", " en "), LangString("World", "en")],
            [SetLangString(texts={"World"}, lang="en"), SetLangString(texts={"Hello"}, lang=" en ")],
        ),
        (
            [LangString(" Text ", "en "), LangString("Text", " en")],
            [SetLangString(texts={" Text "}, lang="en "), SetLangString(texts={"Text"}, lang=" en")],
        ),
        (
            [LangString("SameText", ""), LangString("SameText", " ")],
            [SetLangString(texts={"SameText"}, lang=""), SetLangString(texts={"SameText"}, lang=" ")],
        ),
        (
            [LangString("Special@Lang", "@@"), LangString("AnotherText", "@@")],
            [SetLangString(texts={"Special@Lang", "AnotherText"}, lang="@@")],
        ),
        (
            [LangString(str(i), "en") for i in range(1000)],
            [SetLangString(texts={str(i) for i in range(1000)}, lang="en")],
        ),
        # Duplicate texts with different languages
        (
            [LangString("Duplicate", "en"), LangString("Duplicate", "es")],
            [SetLangString(texts={"Duplicate"}, lang="en"), SetLangString(texts={"Duplicate"}, lang="es")],
        ),
    ],
)
def test_from_langstrings_to_setlangstrings_valid(
    input_langstrings: list[LangString], expected_output: list[SetLangString]
) -> None:
    """Test from_langstrings_to_setlangstrings with valid inputs, ensuring language codes are normalized."""
    result = Converter.from_langstrings_to_setlangstrings(input_langstrings)
    assert len(result) == len(expected_output), "Number of SetLangString objects does not match expected output."

    for expected_sls in expected_output:
        # This time, we also include the language code in our match criteria
        matching_sls = next(
            (
                sls
                for sls in result
                if sls.texts == expected_sls.texts and sls.lang.strip().lower() == expected_sls.lang.strip().lower()
            ),
            None,
        )

        assert (
            matching_sls is not None
        ), f"Expected SetLangString with texts {expected_sls.texts} and lang '{expected_sls.lang}' not found in result."


@pytest.mark.parametrize(
    "invalid_input, error_type",
    [
        (None, TypeError),
        ("not a list", TypeError),
        ([123], TypeError),
        ([LangString("Hello", "en"), "not a LangString"], TypeError),
        (["not a LangString", LangString("Hello", "en")], TypeError),
        ({}, TypeError),
        (set(), TypeError),
        (LangString("Hello", "en"), TypeError),
    ],
)
def test_from_langstrings_to_setlangstrings_invalid_input(invalid_input, error_type) -> None:
    """Test from_langstrings_to_setlangstrings with invalid inputs to ensure it raises appropriate errors.

    :param invalid_input: An invalid input to test the method's error handling.
    :param error_type: The type of error expected to be raised.
    :return: None
    """
    with pytest.raises(error_type, match=TYPEERROR_MSG_SINGULAR):
        Converter.from_langstrings_to_setlangstrings(invalid_input)


@pytest.mark.parametrize(
    "input_langstrings, expected_output",
    [
        # Case with different languages but same text
        (
            [LangString("Hello", "en"), LangString("Hello", "es"), LangString("Hello", "fr")],
            [
                SetLangString(texts={"Hello"}, lang="en"),
                SetLangString(texts={"Hello"}, lang="es"),
                SetLangString(texts={"Hello"}, lang="fr"),
            ],
        ),
        # Case with mixed texts and languages
        (
            [
                LangString("Hello", "en"),
                LangString("World", "en"),
                LangString("Hola", "es"),
                LangString("Mundo", "es"),
                LangString("Bonjour", "fr"),
                LangString("Monde", "fr"),
            ],
            [
                SetLangString(texts={"Hello", "World"}, lang="en"),
                SetLangString(texts={"Hola", "Mundo"}, lang="es"),
                SetLangString(texts={"Bonjour", "Monde"}, lang="fr"),
            ],
        ),
        # Case with same text across all languages
        (
            [LangString("Yes", "en"), LangString("Yes", "es"), LangString("Yes", "fr")],
            [
                SetLangString(texts={"Yes"}, lang="en"),
                SetLangString(texts={"Yes"}, lang="es"),
                SetLangString(texts={"Yes"}, lang="fr"),
            ],
        ),
    ],
)
def test_from_langstrings_to_setlangstrings_varied_cases(
    input_langstrings: list[LangString], expected_output: list[SetLangString]
) -> None:
    """Test handling of LangString objects under various scenarios, including same texts with different languages.

    :param input_langstrings: A list of LangString objects to be converted.
    :param expected_output: The expected list of SetLangString objects after conversion, covering various cases.
    :return: None
    """
    result = Converter.from_langstrings_to_setlangstrings(input_langstrings)
    assert len(result) == len(expected_output), "Number of SetLangString objects does not match expected output."
    for set_lang_string in expected_output:
        assert set_lang_string in result, f"Expected SetLangString not found in result for lang: {set_lang_string.lang}"


@pytest.mark.parametrize(
    "input_langstrings, expected_output",
    [
        # Case with two different casings for the same language code
        ([LangString("Hello", "EN"), LangString("World", "en")], [SetLangString(texts={"Hello", "World"}, lang="en")]),
        # Case with multiple different casings for the same language code
        (
            [LangString("a", "eN"), LangString("b", "En"), LangString("c", "EN")],
            [SetLangString(texts={"a", "b", "c"}, lang="en")],
        ),
        # Case with multiple languages and multiple casings
        (
            [LangString("Hello", "EN"), LangString("World", "en"), LangString("Hola", "ES"), LangString("Mundo", "es")],
            [SetLangString(texts={"Hello", "World"}, lang="en"), SetLangString(texts={"Hola", "Mundo"}, lang="es")],
        ),
        # Case with varied casings and a single instance for one language
        (
            [LangString("One", "en"), LangString("Two", "EN"), LangString("Uno", "ES")],
            [SetLangString(texts={"One", "Two"}, lang="en"), SetLangString(texts={"Uno"}, lang="es")],
        ),
    ],
)
def test_from_langstrings_to_setlangstrings_language_casing(
    input_langstrings: list[LangString], expected_output: list[SetLangString]
) -> None:
    """Test handling of different casings for same language codes in from_langstrings_to_setlangstrings.

    Ensures that language codes with different casings are normalized and treated as the same language.

    :param input_langstrings: A list of LangString objects with various casing for language codes.
    :param expected_output: The expected list of SetLangString objects after conversion.
    :return: None
    """
    result = Converter.from_langstrings_to_setlangstrings(input_langstrings)
    assert len(result) == len(expected_output), "Incorrect number of SetLangString objects."
    for set_lang_string in expected_output:
        assert set_lang_string in result, f"Expected SetLangString not found: {set_lang_string}"
