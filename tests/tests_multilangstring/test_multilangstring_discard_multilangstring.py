import pytest
from langstring import MultiLangString
from tests.conftest import TYPEERROR_MSG_SINGULAR


@pytest.mark.parametrize(
    "initial_contents, discarding_contents, expected_result",
    [
        # Test discarding MultiLangString with the same language
        ({"en": {"Hello", "World"}}, {"en": {"World"}}, {"en": {"Hello"}}),
        # Test discarding MultiLangString with different languages
        ({"en": {"Hello"}, "fr": {"Bonjour"}}, {"fr": {"Bonjour"}}, {"en": {"Hello"}, "fr": set()}),
        # Test discarding MultiLangString with non-overlapping text
        ({"en": {"Hello", "World"}}, {"en": {"Universe"}}, {"en": {"Hello", "World"}}),
        # Test discarding MultiLangString that results in empty content
        ({"en": {"Hello"}}, {"en": {"Hello"}}, {"en": set()}),
        # Test discarding empty MultiLangString does nothing
        ({"en": {"Hello"}}, {}, {"en": {"Hello"}}),
        # Test discarding MultiLangString with multiple languages
        (
            {"en": {"Hello"}, "fr": {"Bonjour"}, "es": {"Hola"}},
            {"fr": {"Bonjour"}, "es": {"Hola"}},
            {"en": {"Hello"}, "fr": set(), "es": set()},
        ),
    ],
)
def test_discard_multilangstring_various_scenarios(initial_contents, discarding_contents, expected_result):
    """
    Test `discard_multilangstring` method across various scenarios, including discarding contents in the same language,
    different languages, and non-overlapping contents.

    :param initial_contents: Initial contents of the MultiLangString instance.
    :param discarding_contents: Contents to be discarded, represented as a dictionary.
    :param expected_result: Expected contents of the MultiLangString after discarding.
    """
    mls_initial = MultiLangString(initial_contents)
    mls_discarding = MultiLangString(discarding_contents)
    mls_initial.discard_multilangstring(mls_discarding)
    assert mls_initial.mls_dict == expected_result, "MultiLangString contents did not match expected after discarding."


def test_discard_multilangstring_self():
    """
    Test discarding a MultiLangString from itself.
    """
    contents = {"en": {"Hello", "World"}}
    mls = MultiLangString(contents)
    mls.discard_multilangstring(mls)
    expected = {"en": set()}  # Expect all contents to be discarded
    assert mls.mls_dict == expected, "Discarding a MultiLangString from itself should remove all its contents."


def test_discard_multilangstring_with_none():
    mls = MultiLangString({"en": {"Hello"}})
    with pytest.raises(TypeError, match=TYPEERROR_MSG_SINGULAR):
        mls.discard_multilangstring(None)


@pytest.mark.parametrize("invalid_input", [123, "string", [1, 2, 3], {"a": 1}])
def test_discard_multilangstring_with_invalid_type(invalid_input):
    mls = MultiLangString({"en": {"Hello"}})
    with pytest.raises(TypeError, match=TYPEERROR_MSG_SINGULAR):
        mls.discard_multilangstring(invalid_input)


def test_discard_non_empty_from_empty_multilangstring():
    mls1 = MultiLangString()
    mls2 = MultiLangString({"en": {"Hello"}})
    mls1.discard_multilangstring(mls2)
    assert mls1.mls_dict == {}, "Discarding from an empty MultiLangString should not change it."


def test_discard_completely_different_multilangstring():
    mls1 = MultiLangString({"en": {"Goodbye"}})
    mls2 = MultiLangString({"fr": {"Bonjour"}})
    mls1.discard_multilangstring(mls2)
    expected_result = {"en": {"Goodbye"}}
    assert mls1.mls_dict == expected_result, "Discarding unrelated MultiLangString should not affect the original."


@pytest.mark.parametrize(
    "initial_contents, discarding_contents, expected_result",
    [
        (
            {"en": {"Hello", "World"}, "fr": {"Bonjour"}},
            {"en": {"Goodbye"}, "fr": {"Salut"}},
            {"en": {"Hello", "World"}, "fr": {"Bonjour"}},
        ),
    ],
)
def test_discard_multilangstring_overlapping_languages_different_texts(
    initial_contents, discarding_contents, expected_result
):
    mls_initial = MultiLangString(initial_contents)
    mls_discarding = MultiLangString(discarding_contents)
    mls_initial.discard_multilangstring(mls_discarding)
    assert (
        mls_initial.mls_dict == expected_result
    ), "Discarding did not work as expected for overlapping languages with different texts."


@pytest.mark.parametrize(
    "initial_contents, discarding_contents, expected_result",
    [
        (
            {"en": {"Hello", "World"}, "fr": {"Bonjour"}, "es": {"Hola"}},
            {"fr": {"Bonjour"}},
            {"en": {"Hello", "World"}, "fr": set(), "es": {"Hola"}},
        ),
    ],
)
def test_discard_multilangstring_subset_languages(initial_contents, discarding_contents, expected_result):
    mls_initial = MultiLangString(initial_contents)
    mls_discarding = MultiLangString(discarding_contents)
    mls_initial.discard_multilangstring(mls_discarding)
    assert mls_initial.mls_dict == expected_result, "Discarding did not work as expected for subset of languages."


@pytest.mark.parametrize(
    "initial_contents, discarding_contents, expected_result",
    [
        ({"en": {"Hello"}}, {"en": {"Hello"}, "de": {"Hallo"}}, {"en": set()}),
    ],
)
def test_discard_multilangstring_additional_languages_not_in_original(
    initial_contents, discarding_contents, expected_result
):
    mls_initial = MultiLangString(initial_contents)
    mls_discarding = MultiLangString(discarding_contents)
    mls_initial.discard_multilangstring(mls_discarding)
    assert (
        mls_initial.mls_dict == expected_result
    ), "Discarding did not work as expected when discarding object has additional languages."


import pytest
from langstring import MultiLangString


@pytest.mark.parametrize(
    "initial_contents, discarding_contents, clean_empty, expected_result",
    [
        # Verify clean_empty=True behavior when the preferred language becomes empty
        ({"en": {"Hello"}}, {"en": {"Hello"}}, True, {}),
        # Ensure language remains when clean_empty=False, even if empty
        ({"en": {"Hello"}}, {"en": {"Hello"}}, False, {"en": set()}),
        # Check non-existent preferred language
        ({"fr": {"Bonjour"}}, {"en": {"Hello"}}, True, {"fr": {"Bonjour"}}),
        # Test with mixed language contents
        ({"en": {"Hello", "World"}, "fr": {"Bonjour"}}, {"en": {"World"}}, True, {"en": {"Hello"}, "fr": {"Bonjour"}}),
    ],
)
def test_discard_multilangstring_with_clean_empty(initial_contents, discarding_contents, clean_empty, expected_result):
    """
    Test `discard_multilangstring` method with the `clean_empty` parameter, verifying its effect in various scenarios.

    :param initial_contents: Initial contents of the MultiLangString.
    :param discarding_contents: Contents to be discarded, represented as a MultiLangString.
    :param clean_empty: Determines if empty languages should be removed from `mls_dict`.
    :param expected_result: Expected contents of `mls_dict` after discarding.
    """
    mls_initial = MultiLangString(initial_contents)
    mls_discarding = MultiLangString(discarding_contents)
    mls_initial.discard_multilangstring(mls_discarding, clean_empty=clean_empty)
    assert mls_initial.mls_dict == expected_result, "MultiLangString contents did not match expected after discarding."


@pytest.mark.parametrize(
    "discarding_contents, clean_empty",
    [
        (123, False),
        ("not a MultiLangString", True),
    ],
)
def test_discard_multilangstring_invalid_type(discarding_contents, clean_empty):
    """
    Test discarding with invalid types for `discard_multilangstring` method raises appropriate errors.

    :param discarding_contents: Invalid content to attempt to discard.
    :param clean_empty: Boolean indicating if empty languages should be cleared.
    :param match_error: Expected error message pattern.
    """
    mls = MultiLangString({"en": {"Hello"}})
    with pytest.raises(TypeError, match=TYPEERROR_MSG_SINGULAR):
        mls.discard_multilangstring(discarding_contents, clean_empty=clean_empty)


# Additional pytest tests based on your current test set
import pytest
from langstring import MultiLangString


@pytest.mark.parametrize(
    "initial_contents, discarding_contents, clean_empty, expected_result",
    [
        # Test with clean_empty=True, removing the only text in the preferred language
        ({"en": {"Hello"}}, {"en": {"Hello"}}, True, {}),
        # Test with clean_empty=False, keeping the language even if it becomes empty
        ({"en": {"Hello"}}, {"en": {"Hello"}}, False, {"en": set()}),
        # Test discarding from a language not present, with clean_empty=True
        ({"fr": {"Bonjour"}}, {"en": {"Hello"}}, True, {"fr": {"Bonjour"}}),
        # Test discarding non-existent text, with clean_empty=True
        (
            {"en": {"Hello", "World"}, "fr": {"Bonjour"}},
            {"en": {"Universe"}},
            True,
            {"en": {"Hello", "World"}, "fr": {"Bonjour"}},
        ),
        # Test discarding with an invalid type for the discarding_contents parameter
        ({"en": {"Hello"}}, 123, False, TypeError("Argument '123' must be of type 'MultiLangString', but got")),
    ],
)
def test_discard_multilangstring_with_clean_empty_and_edge_cases(
    initial_contents, discarding_contents, clean_empty, expected_result
):
    mls_initial = MultiLangString(initial_contents)
    if isinstance(expected_result, Exception):
        with pytest.raises(type(expected_result), match=TYPEERROR_MSG_SINGULAR):
            mls_initial.discard_multilangstring(discarding_contents, clean_empty=clean_empty)
    else:
        mls_discarding = (
            MultiLangString(discarding_contents) if not isinstance(discarding_contents, Exception) else None
        )
        mls_initial.discard_multilangstring(mls_discarding, clean_empty=clean_empty)
        assert (
            mls_initial.mls_dict == expected_result
        ), "MultiLangString contents did not match expected after discarding."
