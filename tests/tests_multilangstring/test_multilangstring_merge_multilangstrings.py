import pytest
from langstring import MultiLangString
from tests.conftest import TYPEERROR_MSG_SINGULAR


@pytest.mark.parametrize(
    "inputs,expected",
    [
        (
            [{"en": {"Hello"}, "fr": {"Bonjour"}}, {"de": {"Hallo"}, "en": {"Hi"}}],
            {"en": {"Hello", "Hi"}, "fr": {"Bonjour"}, "de": {"Hallo"}},
        ),
        (
            [{"en": {"Good morning"}}, {"en": {"Good evening"}, "es": {"Buenas noches"}}],
            {"en": {"Good morning", "Good evening"}, "es": {"Buenas noches"}},
        ),
        (
            [{"it": {"Buongiorno"}}, {"it": {"Buonasera"}, "de": {"Guten Abend"}}],
            {"it": {"Buongiorno", "Buonasera"}, "de": {"Guten Abend"}},
        ),
        (
            [{"en": {" "}, "fr": {" Bonjour"}}, {"de": {"Hallo "}, "en": {"Hi"}}],
            {"en": {" ", "Hi"}, "fr": {" Bonjour"}, "de": {"Hallo "}},
        ),
        (
            [{"ru": {"Привет"}, "el": {"Γειά σου"}}, {"ru": {"Здравствуйте"}, "el": {"Καλημέρα"}}],
            {"ru": {"Привет", "Здравствуйте"}, "el": {"Γειά σου", "Καλημέρα"}},
        ),
        (
            [{"emoji": {"👋"}, "special": {"#hello"}}, {"emoji": {"😊"}, "special": {"$greeting"}}],
            {"emoji": {"👋", "😊"}, "special": {"#hello", "$greeting"}},
        ),
        (
            [{"EN": {"HELLO"}}, {"en": {"world"}}],
            {"EN": {"HELLO", "world"}},
        ),
        (
            [{"fr": {"bonjour"}}, {"FR": {"BONSOIR"}, "Fr": {"salut"}}],
            {"fr": {"bonjour", "BONSOIR", "salut"}},
        ),
        (
            [{"mixCase": {"This"}}, {"mixCase": {"is"}, "MIXCASE": {"Mixed"}}],
            {"mixCase": {"This", "is", "Mixed"}},
        ),
    ],
)
def test_merge_multilangstrings_with_valid_inputs(inputs, expected):
    """Test merging MultiLangString instances with varied valid inputs.

    :param inputs: List of dictionaries representing MultiLangString contents to be merged.
    :param expected: Dictionary with the expected content after merging.
    """
    mls_instances = [MultiLangString(content) for content in inputs]
    result = MultiLangString.merge_multilangstrings(mls_instances)
    # Correcting the assertion to compare sets of texts for each language
    assert all(
        result.mls_dict.get(lang, set()) == expected.get(lang, set()) for lang in expected
    ), "Merged MultiLangString does not match expected content."


@pytest.mark.parametrize(
    "invalid_element",
    [
        123,
        "string",
        [],
        None,
        {"not_a_list"},
        {"en": "Hello, world!"},
        True,
        False,
    ],
)
def test_merge_multilangstrings_with_invalid_type(invalid_element):
    """Test merging MultiLangString instances with varied invalid types in the list.

    :param invalid_element: Tuple containing an invalid element to include in the list and the expected exception message.
    """
    with pytest.raises(TypeError, match=TYPEERROR_MSG_SINGULAR):
        MultiLangString.merge_multilangstrings([invalid_element])


def test_merge_multilangstrings_with_empty_list():
    """Test merging MultiLangString instances with an empty list.

    :return: A new, empty MultiLangString instance.
    """
    result = MultiLangString.merge_multilangstrings([])
    assert result.mls_dict == {}, "Merged MultiLangString from an empty list should be empty."


@pytest.mark.parametrize("invalid_input", [None, 123, "test", object()])
def test_merge_multilangstrings_with_invalid_list_input(invalid_input):
    """Test merging MultiLangString instances with invalid list input types.

    :param invalid_input: Invalid input to test.
    :raises TypeError: If the input is not a list.
    """
    with pytest.raises(TypeError, match=TYPEERROR_MSG_SINGULAR):
        MultiLangString.merge_multilangstrings(invalid_input)


@pytest.mark.parametrize(
    "inputs,expected",
    [
        # Merging with itself
        (
            [{"en": {"Hello"}}],
            {"en": {"Hello"}},
        ),
        # Merging where one instance contains an empty set for a language
        (
            [{"en": {"Hello"}}, {"en": set(), "fr": {"Bonjour"}}],
            {"en": {"Hello"}, "fr": {"Bonjour"}},
        ),
        (
            [{"upper": {"HELLO"}}, {"upper": {"WORLD"}}],
            {"upper": {"HELLO", "WORLD"}},
        ),
        (
            [{"mixed": {"Hello"}}, {"mixed": {"hello"}}],
            {"mixed": {"Hello", "hello"}},
        ),
        (
            [{"spaces": {" leading"}}, {"spaces": {"trailing "}}],
            {"spaces": {" leading", "trailing "}},
        ),
    ],
)
def test_merge_multilangstrings_unusual_but_valid(inputs, expected):
    """Test merging MultiLangString instances in unusual but valid scenarios.

    :param inputs: List of dictionaries representing MultiLangString contents to be merged.
    :param expected: Dictionary with the expected content after merging.
    """
    mls_instances = [MultiLangString(content) for content in inputs]
    result = MultiLangString.merge_multilangstrings(mls_instances)
    assert all(
        result.mls_dict.get(lang, set()) == expected.get(lang, set()) for lang in expected
    ), "Merged MultiLangString does not match expected content in unusual but valid scenarios."
