import pytest
from langstring import Controller
from langstring import MultiLangString
from langstring import MultiLangStringFlag
from langstring import SetLangString
from tests.conftest import TYPEERROR_MSG_SINGULAR


@pytest.mark.parametrize(
    "initial_dict, setlangstring, expected_dict",
    [
        # Adding a new SetLangString to an empty MultiLangString
        ({}, SetLangString(texts={"Hello", "World"}, lang="en"), {"en": {"Hello", "World"}}),
        # Adding a SetLangString to an existing language with existing texts
        (
            {"en": {"Hello"}},
            SetLangString(texts={"World", "Greetings"}, lang="en"),
            {"en": {"Hello", "World", "Greetings"}},
        ),
        # Adding a SetLangString in a new language
        (
            {"en": {"Hello"}},
            SetLangString(texts={"Bonjour", "Salut"}, lang="fr"),
            {"en": {"Hello"}, "fr": {"Bonjour", "Salut"}},
        ),
    ],
)
def test_add_setlangstring(initial_dict: dict, setlangstring: SetLangString, expected_dict: dict):
    """Tests adding a SetLangString object to the MultiLangString.

    :param initial_dict: Initial state of mls_dict in MultiLangString.
    :param setlangstring: The SetLangString object to be added.
    :param expected_dict: Expected state of mls_dict after adding the SetLangString.
    """
    mls = MultiLangString(mls_dict=initial_dict)
    mls.add_setlangstring(setlangstring)
    assert mls.mls_dict == expected_dict, "The SetLangString was not added correctly."


@pytest.mark.parametrize(
    "invalid_setlangstring",
    [
        123,
        "not a SetLangString",
        None,
    ],
)
def test_add_setlangstring_invalid_type(invalid_setlangstring):
    """Tests adding an invalid type as SetLangString to the MultiLangString, expecting a TypeError.

    :param invalid_setlangstring: Invalid SetLangString object to be added.
    :param match_message: Expected error message or pattern.
    """
    mls = MultiLangString()
    with pytest.raises(TypeError, match=TYPEERROR_MSG_SINGULAR):
        mls.add_setlangstring(invalid_setlangstring)


@pytest.mark.parametrize(
    "lang1, lang2, expected_dict1, expected_dict2",
    [
        ("en", "es", {"en": set()}, {"en": set(), "es": set()}),
    ],
)
def test_add_setlangstring_empty_texts(lang1, lang2, expected_dict1, expected_dict2):
    mls = MultiLangString()
    mls.add_setlangstring(SetLangString(texts=set(), lang=lang1))
    assert mls.mls_dict == expected_dict1, "Empty SetLangString was not handled correctly."
    mls.add_setlangstring(SetLangString(texts=set(), lang=lang2))
    assert mls.mls_dict == expected_dict2, "Empty SetLangString was not handled correctly."


def test_add_setlangstring_with_flag_effect():
    Controller.set_flag(MultiLangStringFlag.LOWERCASE_LANG, True)
    mls = MultiLangString()
    mls.add_setlangstring(SetLangString(texts={"HELLO", "WORLD"}, lang="EN"))
    assert mls.mls_dict == {"en": {"HELLO", "WORLD"}}, "Flag effect not applied correctly."


@pytest.mark.parametrize(
    "texts, lang, expected_dict",
    [
        ({"  ", "\t"}, "en", {"en": {"  ", "\t"}}),  # Whitespace and tab character
    ],
)
def test_add_setlangstring_unusual_valid_texts(texts, lang, expected_dict):
    mls = MultiLangString()
    mls.add_setlangstring(SetLangString(texts=texts, lang=lang))
    assert mls.mls_dict == expected_dict, "Unusual but valid texts not handled correctly."
