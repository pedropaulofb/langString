import pytest

from langstring import Converter
from langstring import LangString
from langstring import MultiLangString
from tests.conftest import TYPEERROR_MSG_SINGULAR


@pytest.mark.parametrize(
    "mls_dict, expected_output",
    [
        (
            {"en": {"Hello"}, "fr": {"Bonjour"}, "es": {"Hola"}},
            [
                LangString(text="Hello", lang="en"),
                LangString(text="Bonjour", lang="fr"),
                LangString(text="Hola", lang="es"),
            ],
        ),
        ({"de": {"Hallo"}, "it": {"Ciao"}}, [LangString(text="Hallo", lang="de"), LangString(text="Ciao", lang="it")]),
        (
            {"gr": {"Γειά"}, "ru": {"Привет"}},
            [LangString(text="Γειά", lang="gr"), LangString(text="Привет", lang="ru")],
        ),
        (
            {"emoji": {"😊"}, "special": {"@#&*"}},
            [LangString(text="😊", lang="emoji"), LangString(text="@#&*", lang="special")],
        ),
    ],
)
def test_convert_multilangstring_to_langstrings_basic(mls_dict, expected_output):
    """
    Test conversion of MultiLangString with multiple languages to a list of LangString objects using parametrization.
    """
    mls = MultiLangString(mls_dict=mls_dict)
    result = Converter.from_multilangstring_to_langstrings(mls)
    assert all(isinstance(item, LangString) for item in result), "All items in result should be LangString instances."
    assert len(result) == len(
        expected_output
    ), "Result should contain the same number of LangString instances as expected."
    for langstring in expected_output:
        assert langstring in result, f"Expected LangString {langstring} not found in result."


@pytest.mark.parametrize(
    "languages, expected_texts",
    [
        (["en"], ["Hello"]),
        (["fr"], ["Bonjour"]),
        (["es", "fr"], ["Hola", "Bonjour"]),
        (None, ["Hello", "Bonjour", "Hola"]),  # None to signify no language filtering
    ],
)
def test_convert_multilangstring_with_language_filtering(languages, expected_texts):
    """
    Test conversion of a MultiLangString with filtering by languages.
    """
    mls = MultiLangString(mls_dict={"en": {"Hello"}, "fr": {"Bonjour"}, "es": {"Hola"}})
    result = Converter.from_multilangstring_to_langstrings(mls, languages=languages)
    result_texts = [ls.text for ls in result]
    assert sorted(result_texts) == sorted(
        expected_texts
    ), "Filtered conversion should only include specified languages."


def test_convert_empty_multilangstring():
    """
    Test conversion of an empty MultiLangString to an empty list of LangString objects.
    """
    mls = MultiLangString()
    result = Converter.from_multilangstring_to_langstrings(mls)
    assert result == [], "Converting an empty MultiLangString should result in an empty list."


@pytest.mark.parametrize(
    "invalid_input",
    ["Not a MultiLangString", 123, [], ({"not": "a dictionary"},), (True,), (None,), True],
)
def test_convert_multilangstring_to_langstrings_type_error(invalid_input):
    """
    Test that passing a non-MultiLangString object raises a TypeError, using parametrization for various types.
    """
    with pytest.raises(TypeError, match=TYPEERROR_MSG_SINGULAR):
        Converter.from_multilangstring_to_langstrings(invalid_input)


def test_convert_multilangstring_to_langstrings_with_invalid_languages_param():
    """
    Test that passing an invalid type for the languages parameter raises a TypeError.
    """
    mls = MultiLangString(mls_dict={"en": {"Hello"}})
    with pytest.raises(TypeError, match="Invalid argument with value 'en'. Expected 'list', but got 'str'."):
        Converter.from_multilangstring_to_langstrings(mls, languages="en")  # Incorrect type for languages parameter


@pytest.mark.parametrize(
    "mls_dict, languages, expected_count",
    [
        ({"en": ["Hello", "Goodbye"], "fr": ["Bonjour", "Au revoir"]}, None, 4),
        ({}, ["en"], 0),
        ({"en": []}, ["en"], 0),
        (
            {"en": ["Hello"], "en": ["Hello again"]},
            ["en"],
            1,
        ),  # Duplicate keys in dict not possible, but for illustration
        ({"spaces": {" Hello ", "World "}, "empty": {""}, "mixedCase": {"Hello", "WORLD"}}, None, 5),
        ({"en": {" Hello"}, "fr": {"Bonjour "}}, None, 2),
        ({"en": {"Hello"}, "cyrl": {"Привет"}, "gr": {"Γειά σου"}}, ["cyrl", "gr"], 2),
        ({"with spaces": {"Hello"}}, None, 1),
    ],
)
def test_convert_multilangstring_to_langstrings_edge_cases(mls_dict, languages, expected_count):
    """
    Test conversion of MultiLangString considering unusual or edge cases.
    """
    mls = MultiLangString(mls_dict={lang: set(texts) for lang, texts in mls_dict.items()})
    result = Converter.from_multilangstring_to_langstrings(mls, languages=languages)
    assert len(result) == expected_count, f"Expected {expected_count} LangStrings, got {len(result)}."


@pytest.mark.parametrize(
    "mls_input, modification",
    [
        (MultiLangString(mls_dict={"en": {"Hello"}}), lambda x: x.add_langstring(LangString("Goodbye", "en"))),
        (MultiLangString(), lambda x: None),
    ],
)
def test_convert_modified_multilangstring_to_langstrings(mls_input, modification):
    """
    Test conversion after modifying the MultiLangString object.
    """
    modification(mls_input)  # Apply modification
    result = Converter.from_multilangstring_to_langstrings(mls_input)
    assert isinstance(result, list) and all(
        isinstance(ls, LangString) for ls in result
    ), "Result should be a list of LangString instances."


@pytest.mark.parametrize(
    "mls_dict_modification, expected_result_texts",
    [
        # Assuming None values are not intended based on your class definitions.
        (lambda mls: mls.add_langstring(LangString(text="Goodbye", lang="en")), ["Hello", "Goodbye"]),
        (lambda mls: mls.add_langstring(LangString(text="Hola", lang="es")), ["Hello", "Hola"]),
        (lambda mls: mls.add_langstring(LangString(text="   trimmed  ", lang="en")), ["Hello", "   trimmed  "]),
        (lambda mls: mls.add_langstring(LangString(text="Привет", lang="ru")), ["Hello", "Привет"]),
        (lambda mls: mls.add_langstring(LangString(text="😊", lang="emoji")), ["Hello", "😊"]),
    ],
)
def test_convert_multilangstring_modification_during_iteration(mls_dict_modification, expected_result_texts):
    """
    Test the method with a MultiLangString object that is modified before conversion.
    """
    mls = MultiLangString({"en": {"Hello"}})
    mls_dict_modification(mls)  # Apply modification function to mls
    result = Converter.from_multilangstring_to_langstrings(mls)
    result_texts = [ls.text for ls in result]
    assert sorted(result_texts) == sorted(
        expected_result_texts
    ), "The conversion result does not match the expected texts after modification."
