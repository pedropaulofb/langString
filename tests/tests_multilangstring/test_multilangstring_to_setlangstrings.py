import pytest
from langstring import MultiLangString
from langstring import SetLangString
from tests.conftest import TYPEERROR_MSG_SINGULAR


@pytest.mark.parametrize(
    "mls_dict, langs, expected",
    [
        ({"en": {"Hello"}, "es": {"Hola"}}, ["en"], [SetLangString({"Hello"}, "en")]),
        (
            {"en": {"Hello", "Hi"}, "fr": {"Bonjour"}},
            ["en", "fr"],
            [SetLangString({"Hello", "Hi"}, "en"), SetLangString({"Bonjour"}, "fr")],
        ),
        (
            {"de": {"Hallo"}, "es": {"Hola"}, "fr": {"Bonjour"}},
            ["es", "de"],
            [SetLangString({"Hola"}, "es"), SetLangString({"Hallo"}, "de")],
        ),
        ({"en": {"Hello"}, "es": {"Hola"}}, [], []),
        ({"en": {"Hello"}, "es": {"Hola"}}, None, [SetLangString({"Hello"}, "en"), SetLangString({"Hola"}, "es")]),
        ({"en": {" "}, "es": {"   "}}, ["en", "es"], [SetLangString({" "}, "en"), SetLangString({"   "}, "es")]),
        ({"en": {"Hello world"}, "es": {"Hola mundo"}}, ["en"], [SetLangString({"Hello world"}, "en")]),
        (
            {"ru": {"Привет"}, "gr": {"Γειά"}},
            ["ru", "gr"],
            [SetLangString({"Привет"}, "ru"), SetLangString({"Γειά"}, "gr")],
        ),
        (
            {"en": {"HELLO"}, "es": {"hola"}},
            ["en", "es"],
            [SetLangString({"HELLO"}, "en"), SetLangString({"hola"}, "es")],
        ),
        (
            {"en": {"Hello😀"}, "es": {"Hola😃"}},
            ["en", "es"],
            [SetLangString({"Hello😀"}, "en"), SetLangString({"Hola😃"}, "es")],
        ),
        (
            {"en": {"Hello-world"}, "es": {"Hola_mundo"}},
            ["en", "es"],
            [SetLangString({"Hello-world"}, "en"), SetLangString({"Hola_mundo"}, "es")],
        ),
        ({"": {"NoLangText"}, "en": {"Hello"}, "es": {"Hola"}}, [""], [SetLangString({"NoLangText"}, "")]),
        (
            {"": {"NoLangText1", "NoLangText2"}, "en": {"Hello"}},
            [""],
            [SetLangString({"NoLangText1", "NoLangText2"}, "")],
        ),
        (
            {"": {"NoLangText"}, "en": {"Hello"}, "es": {"Hola"}},
            ["", "en"],
            [SetLangString({"NoLangText"}, ""), SetLangString({"Hello"}, "en")],
        ),
        ({"": {"OnlyNoLangText"}}, None, [SetLangString({"OnlyNoLangText"}, "")]),
        # Testing with an empty string alongside non-existent and valid language codes.
        (
            {"": {"NoLang"}, "en": {"Hello"}, "es": {"Hola"}},
            ["", "xx", "en"],
            [SetLangString({"NoLang"}, ""), SetLangString({"Hello"}, "en")],
        ),
    ],
)
def test_to_setlangstrings_with_valid_langs_parametrized(mls_dict, langs, expected):
    """
    Parametrized test of the `to_setlangstrings` method with various valid inputs.

    :param mls_dict: Dictionary to initialize MultiLangString object.
    :param langs: List of language codes to pass to the `to_setlangstrings` method.
    :param expected: Expected result, a list of SetLangString objects.
    """
    mls = MultiLangString(mls_dict)
    result = mls.to_setlangstrings(langs=langs)
    assert len(result) == len(expected) and all(
        isinstance(item, SetLangString) for item in result
    ), "Expected a list of SetLangString objects."
    for res, exp in zip(result, expected):
        assert (
            res.lang == exp.lang and res.texts == exp.texts
        ), f"Expected SetLangString with lang '{exp.lang}' and texts {exp.texts}, got lang '{res.lang}' and texts {res.texts}."


@pytest.mark.parametrize(
    "langs, expected_exception",
    [
        (123, TypeError),
        ("en", TypeError),
        ([None], TypeError),
        ([{"not": "a lang code"}], TypeError),
        ([123], TypeError),  # List with an invalid type
        (["en", 123], TypeError),  # Mixed valid and invalid types
    ],
)
def test_to_setlangstrings_with_invalid_langs_type(langs, expected_exception):
    """
    Test to_setlangstrings with invalid 'langs' parameter types.

    :param langs: Invalid 'langs' inputs to test.
    :param expected_exception: The type of exception expected from the test.
    :return: Asserts that TypeError is raised with an appropriate message.
    """
    mls = MultiLangString({"en": {"Hello"}})
    with pytest.raises(expected_exception, match=TYPEERROR_MSG_SINGULAR):
        mls.to_setlangstrings(langs=langs)


def test_to_setlangstrings_with_none_langs():
    """
    Test to_setlangstrings method with 'langs' parameter set to None.

    :param: None
    :return: Asserts that all SetLangString objects are returned when 'langs' is None.
    """
    mls = MultiLangString({"en": {"Hello"}, "es": {"Hola"}})
    result = mls.to_setlangstrings(langs=None)
    assert len(result) == 2 and all(
        isinstance(item, SetLangString) for item in result
    ), "Expected a list of all SetLangString objects when 'langs' is None."
