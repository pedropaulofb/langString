import pytest
from langstring import LangString
from langstring import MultiLangString
from langstring import SetLangString


@pytest.mark.parametrize(
    "arg, expected_result",
    [
        (
            LangString("Bonjour", "fr"),
            {"en": {"Hello", "World"}, "fr": set(), "es": {"Hola", "Adios"}},
        ),  # Discard LangString
        (
            SetLangString({"Hola"}, "es"),
            {"en": {"Hello", "World"}, "fr": {"Bonjour"}, "es": {"Adios"}},
        ),  # Discard SetLangString
        (
            SetLangString({"Hola", "Adios"}, "es"),
            {"en": {"Hello", "World"}, "fr": {"Bonjour"}, "es": set()},
        ),  # Discard SetLangString
        (("Adios", "es"), {"en": {"Hello", "World"}, "fr": {"Bonjour"}, "es": {"Hola"}}),  # Discard tuple
    ],
)
def test_discard_various_args_off(arg, expected_result):
    """
    Test the `discard` method with various types of arguments to ensure correct functionality across supported input types.

    :param arg: Argument to discard, which could be a string, LangString, SetLangString, or tuple.
    :param expected_result: Expected state of the MultiLangString instance after the discard operation.
    """
    mls = MultiLangString({"en": {"Hello", "World"}, "fr": {"Bonjour"}, "es": {"Hola", "Adios"}})
    mls.discard(arg)
    assert mls.mls_dict == expected_result, f"Expected dictionary did not match after discarding {arg}."


@pytest.mark.parametrize(
    "arg, expected_result",
    [
        (
            LangString("Bonjour", "fr"),
            {"en": {"Hello", "World"}, "es": {"Hola", "Adios"}},
        ),  # Discard LangString
        (
            SetLangString({"Hola"}, "es"),
            {"en": {"Hello", "World"}, "fr": {"Bonjour"}, "es": {"Adios"}},
        ),  # Discard SetLangString
        (
            SetLangString({"Hola", "Adios"}, "es"),
            {"en": {"Hello", "World"}, "fr": {"Bonjour"}},
        ),  # Discard SetLangString
        (("Adios", "es"), {"en": {"Hello", "World"}, "fr": {"Bonjour"}, "es": {"Hola"}}),  # Discard tuple
    ],
)
def test_discard_various_args_on(arg, expected_result):
    """
    Test the `discard` method with various types of arguments to ensure correct functionality across supported input types.

    :param arg: Argument to discard, which could be a string, LangString, SetLangString, or tuple.
    :param expected_result: Expected state of the MultiLangString instance after the discard operation.
    """
    mls = MultiLangString({"en": {"Hello", "World"}, "fr": {"Bonjour"}, "es": {"Hola", "Adios"}})
    mls.discard(arg, clean_empty=True)
    assert mls.mls_dict == expected_result, f"Expected dictionary did not match after discarding {arg}."


def test_discard_with_invalid_type():
    """
    Test the `discard` method raises a TypeError when an invalid argument type is passed.
    """
    mls = MultiLangString({"en": {"Hello"}})
    with pytest.raises(TypeError, match="Argument with value '.+' must be of type"):
        mls.discard(123)  # Invalid type argument


@pytest.mark.parametrize(
    "arg, expected_result, test_case_description",
    [
        (
            SetLangString(set(), "en"),
            {"en": {"Hello", "World"}, "fr": {"Bonjour"}, "es": {"Hola", "Adios"}},
            "Discarding empty SetLangString does nothing",
        ),
    ],
)
def test_discard_edge_cases(arg, expected_result, test_case_description):
    """
    Test the `discard` method with edge cases like None, empty string, and empty SetLangString.

    :param arg: Argument to discard, could be None, an empty string, or an empty SetLangString.
    :param expected_result: Expected state of the MultiLangString instance after the discard operation.
    :param test_case_description: Description of the test case being executed.
    """
    mls = MultiLangString({"en": {"Hello", "World"}, "fr": {"Bonjour"}, "es": {"Hola", "Adios"}})
    mls.discard(arg)
    assert mls.mls_dict == expected_result, f"After {test_case_description}, expected dictionary did not match."


def test_discard_with_none():
    """
    Test that passing None as an argument to `discard` raises a TypeError.
    """
    mls = MultiLangString({"en": {"Hello", "World"}, "fr": {"Bonjour"}, "es": {"Hola", "Adios"}})
    with pytest.raises(TypeError, match="Argument with value 'None' must be of type"):
        mls.discard(None)  # Passing None should raise TypeError


# Test case for discarding a non-empty string in a non-default language when the clean_empty arg is off.
(
    LangString("World", "en"),
    {"en": {"Hello"}, "fr": {"Bonjour"}, "es": {"Hola", "Adios"}},
    "Discarding 'World' from 'en' with CLEAN_EMPTY_LANG off",
),

# Test case for discarding a non-empty SetLangString in a non-default language when the clean_empty arg is off.
(
    SetLangString({"Adios"}, "es"),
    {"en": {"Hello", "World"}, "fr": {"Bonjour"}, "es": {"Hola"}},
    "Discarding 'Adios' from 'es' with CLEAN_EMPTY_LANG off",
),

# Test case for discarding an existing tuple in a non-default language when the clean_empty arg is off.
(
    ("Hola", "es"),
    {"en": {"Hello", "World"}, "fr": {"Bonjour"}, "es": {"Adios"}},
    "Discarding tuple ('Hola', 'es') with CLEAN_EMPTY_LANG off",
),


# Test for discarding with None, expecting a TypeError, to specifically catch incorrect argument types.
def test_discard_with_none_raises_error():
    """
    Test that passing None as an argument to `discard` method raises a TypeError, ensuring robust input validation.
    """
    mls = MultiLangString({"en": {"Hello", "World"}, "fr": {"Bonjour"}, "es": {"Hola", "Adios"}})
    with pytest.raises(TypeError, match="Argument with value 'None' must be of type"):
        mls.discard(None)  # Passing None should raise TypeError


@pytest.mark.parametrize(
    "initial_contents, discarding_mls_contents, expected_result, description",
    [
        # mls1 has exactly mls2
        (
            {"en": {"Hello", "World"}, "fr": {"Bonjour"}},
            {"en": {"Hello", "World"}, "fr": {"Bonjour"}},
            {"en": set(), "fr": set()},
            "mls1 has exactly mls2",
        ),
        # mls1 has some of mls2
        (
            {"en": {"Hello", "World", "Universe"}, "fr": {"Bonjour", "Salut"}},
            {"en": {"World"}, "fr": {"Bonjour"}},
            {"en": {"Hello", "Universe"}, "fr": {"Salut"}},
            "mls1 has some of mls2",
        ),
        # mls1 has all mls2 and more
        (
            {"en": {"Hello", "World"}, "fr": {"Bonjour", "Salut"}},
            {"en": {"World"}},
            {"en": {"Hello"}, "fr": {"Bonjour", "Salut"}},
            "mls1 has all mls2 and more",
        ),
        # mls1 has none of mls2
        ({"en": {"Hello"}}, {"fr": {"Bonjour"}}, {"en": {"Hello"}}, "mls1 has none of mls2"),
    ],
)
def test_discard_multilangstring_various_scenarios(
    initial_contents, discarding_mls_contents, expected_result, description
):
    """
    Test the `discard` method when receiving a MultiLangString as an argument across various scenarios.

    :param initial_contents: Initial contents of the MultiLangString instance.
    :param discarding_mls_contents: Contents of the MultiLangString to be discarded.
    :param expected_result: Expected contents of the MultiLangString after the discard operation.
    :param description: Description of the test case.
    """
    mls_initial = MultiLangString(initial_contents)
    mls_discarding = MultiLangString(discarding_mls_contents)
    mls_initial.discard(mls_discarding)
    assert (
        mls_initial.mls_dict == expected_result
    ), f"After discarding {description}, expected dictionary did not match."


@pytest.mark.parametrize(
    "initial_contents, discarding_mls_contents, expected_result, description",
    [
        # mls1 has exactly mls2
        (
            {"en": {"Hello", "World"}, "fr": {"Bonjour"}},
            {"en": {"Hello", "World"}, "fr": {"Bonjour"}},
            {},
            "mls1 has exactly mls2",
        ),
        # mls1 has all mls2 and more
        (
            {"en": {"Hello", "World"}, "fr": {"Bonjour", "Salut"}},
            {"en": {"Hello", "World"}},
            {"fr": {"Bonjour", "Salut"}},
            "mls1 has all mls2 and more",
        ),
    ],
)
def test_discard_multilangstring_various_scenarios_on(
    initial_contents, discarding_mls_contents, expected_result, description
):
    """
    Test the `discard` method when receiving a MultiLangString as an argument across various scenarios.

    :param initial_contents: Initial contents of the MultiLangString instance.
    :param discarding_mls_contents: Contents of the MultiLangString to be discarded.
    :param expected_result: Expected contents of the MultiLangString after the discard operation.
    :param description: Description of the test case.
    """
    mls_initial = MultiLangString(initial_contents)
    mls_discarding = MultiLangString(discarding_mls_contents)
    mls_initial.discard(mls_discarding, True)
    assert (
        mls_initial.mls_dict == expected_result
    ), f"After discarding {description}, expected dictionary did not match."


import pytest
from langstring import MultiLangString, LangString, SetLangString


@pytest.mark.parametrize(
    "initial_contents, discarding_contents, clean_empty, expected_contents",
    [
        # Scenario: Discarding a LangString leaves a language empty, with clean_empty=True
        ({"en": {"Hello"}}, LangString("Hello", "en"), True, {}),
        # Scenario: Discarding a SetLangString leaves a language empty, with clean_empty=False
        ({"es": {"Hola", "Adios"}}, SetLangString({"Hola", "Adios"}, "es"), False, {"es": set()}),
        # Scenario: Discarding a tuple from a language not present in the MultiLangString
        ({"fr": {"Bonjour"}}, ("Hello", "en"), True, {"fr": {"Bonjour"}}),  # No effect expected
        # Scenario: Attempting to discard from an empty MultiLangString
        ({}, LangString("Hello", "en"), True, {}),  # No change expected
    ],
)
def test_discard_with_clean_empty(initial_contents, discarding_contents, clean_empty, expected_contents):
    """
    Test discarding entries from a MultiLangString with the clean_empty parameter.
    """
    mls = MultiLangString(initial_contents)
    mls.discard(discarding_contents, clean_empty=clean_empty)
    assert mls.mls_dict == expected_contents, "The resulting contents did not match the expected result."


@pytest.mark.parametrize("invalid_input", [123, ["Hello", "en"], {"text": "Hello", "lang": "en"}, None])
def test_discard_with_invalid_input_type(invalid_input):
    """
    Test discarding with invalid input types raises a TypeError.
    """
    mls = MultiLangString({"en": {"Hello", "World"}})
    with pytest.raises(TypeError, match="Argument .+ must be of type"):
        mls.discard(invalid_input)


def test_discard_from_empty_multilangstring():
    """
    Test discarding from an empty MultiLangString instance.
    """
    mls = MultiLangString()
    mls.discard(LangString("Hello", "en"), clean_empty=True)
    assert mls.mls_dict == {}, "Discarding from an empty MultiLangString should leave it unchanged."
