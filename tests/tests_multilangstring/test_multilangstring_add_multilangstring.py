import pytest
from langstring import MultiLangString
from tests.conftest import TYPEERROR_MSG_SINGULAR


@pytest.mark.parametrize(
    "initial_contents, adding_contents, expected_result",
    [
        # Test adding MultiLangString with the same language
        ({"en": {"Hello"}}, {"en": {"World"}}, {"en": {"Hello", "World"}}),
        # Test adding MultiLangString with empty langs:
        (
            {"en": {"Hello"}},
            {"es": set(), "fr": set(), "pt": set()},
            {"en": {"Hello"}, "es": set(), "fr": set(), "pt": set()},
        ),
        # Test adding MultiLangString with different languages
        ({"en": {"Hello"}}, {"fr": {"Bonjour"}}, {"en": {"Hello"}, "fr": {"Bonjour"}}),
        # Test adding MultiLangString with overlapping text in the same language
        ({"en": {"Hello", "World"}}, {"en": {"World", "Universe"}}, {"en": {"Hello", "World", "Universe"}}),
        # Test adding MultiLangString with same contents
        ({"en": {"Hello"}}, {"en": {"Hello"}}, {"en": {"Hello"}}),
        # Test adding MultiLangString with empty contents
        ({"en": {"Hello"}}, {}, {"en": {"Hello"}}),
        # Test adding empty MultiLangString to non-empty MultiLangString
        ({}, {"en": {"Hello"}}, {"en": {"Hello"}}),
        # Test adding MultiLangString with multiple languages
        ({"en": {"Hello"}}, {"fr": {"Bonjour"}, "es": {"Hola"}}, {"en": {"Hello"}, "fr": {"Bonjour"}, "es": {"Hola"}}),
    ],
)
def test_add_multilangstring_various_scenarios(initial_contents, adding_contents, expected_result):
    """
    Test `add_multilangstring` method across various scenarios, including adding contents in the same language,
    different languages, and overlapping contents.

    :param initial_contents: Initial contents of the MultiLangString instance.
    :param adding_contents: Contents to be added, represented as a dictionary.
    :param expected_result: Expected contents of the MultiLangString after addition.
    """
    mls_initial = MultiLangString(initial_contents)
    mls_adding = MultiLangString(adding_contents)
    mls_initial.add_multilangstring(mls_adding)
    assert mls_initial.mls_dict == expected_result, "MultiLangString contents did not match expected after addition."


def test_add_multilangstring_to_itself():
    """
    Test adding a MultiLangString to itself.
    """
    contents = {"en": {"Hello"}}
    mls = MultiLangString(contents)
    mls.add_multilangstring(mls)
    expected = {"en": {"Hello"}}  # Assuming idempotent behavior
    assert mls.mls_dict == expected, "Adding a MultiLangString to itself should not change its contents."


def test_add_multilangstring_with_none():
    mls = MultiLangString()
    with pytest.raises(TypeError, match=TYPEERROR_MSG_SINGULAR):
        mls.add_multilangstring(None)


def test_add_empty_multilangstring_to_empty():
    mls1 = MultiLangString()
    mls2 = MultiLangString()
    mls1.add_multilangstring(mls2)
    assert mls1.mls_dict == {}, "Adding an empty MultiLangString should not change the original MultiLangString."


@pytest.mark.parametrize("invalid_arg", ["string", ["list"], 123])
def test_add_multilangstring_with_invalid_type(invalid_arg):
    mls = MultiLangString()
    with pytest.raises(TypeError, match=TYPEERROR_MSG_SINGULAR):
        mls.add_multilangstring(invalid_arg)


def test_add_multilangstring_with_overlapping_content():
    mls1 = MultiLangString({"en": {"Hello"}})
    mls2 = MultiLangString({"en": {"Hello", "World"}})
    mls1.add_multilangstring(mls2)
    assert mls1.mls_dict == {"en": {"Hello", "World"}}, "Overlapping content should be merged correctly."


def test_add_multilangstring_with_clean_empty_lang_flag_effect():
    """
    Test the behavior of add_multilangstring method when clean_empty arg is set.
    This test assumes that when CLEAN_EMPTY_LANG is True, adding a MultiLangString that results in empty language entries
    should remove those entries.
    """
    # Setup initial MultiLangString with some languages
    mls1a = MultiLangString({"en": {"Hello"}, "fr": set()})
    mls1b = MultiLangString({"en": {"Hello"}, "fr": set()})
    mls2 = MultiLangString({"en": {"World"}})

    # Perform the add operation
    mls1a.add_multilangstring(mls2)
    mls2.add_multilangstring(mls1b)

    expected_result = {"en": {"Hello", "World"}, "fr": set()}

    assert mls1a.mls_dict == expected_result, "Did not remove empty language entries as expected."
    assert mls2.mls_dict == expected_result, "Did not remove empty language entries as expected."
