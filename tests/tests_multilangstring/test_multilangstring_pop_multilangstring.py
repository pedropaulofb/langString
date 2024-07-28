import pytest
from langstring import MultiLangString
from tests.conftest import TYPEERROR_MSG_SINGULAR


@pytest.mark.parametrize(
    "initial_data, langs_to_pop, expected_result_data, expected_remaining_data",
    [
        # Popping existing languages
        (
            {"en": {"Hello", "World"}, "fr": {"Bonjour", "Monde"}},
            ["en"],
            {"en": {"Hello", "World"}},
            {"fr": {"Bonjour", "Monde"}},
        ),
        # Popping non-existing language
        ({"en": {"Hello"}}, ["de"], {}, {"en": {"Hello"}}),
        # Popping with an empty list
        ({"en": {"Hello"}, "fr": {"Bonjour"}}, [], {}, {"en": {"Hello"}, "fr": {"Bonjour"}}),
        # Mixed existing and non-existing languages
        (
            {"en": {"Hello", "World"}, "fr": {"Bonjour", "Monde"}, "es": {"Hola", "Mundo"}},
            ["fr", "de"],
            {"fr": {"Bonjour", "Monde"}},
            {"en": {"Hello", "World"}, "es": {"Hola", "Mundo"}},
        ),
        # Languages with special characters and emojis
        (
            {"emoji": {"🙂", "🚀"}, "ru": {"Привет", "Мир"}},
            ["emoji", "ru"],
            {"emoji": {"🙂", "🚀"}, "ru": {"Привет", "Мир"}},
            {},
        ),
        (
            {"gr": {"Γειά", "Κόσμος"}, "ru": {"Привет", "Мир"}},
            ["gr", "ru"],
            {"gr": {"Γειά", "Κόσμος"}, "ru": {"Привет", "Мир"}},
            {},
        ),
        ({"EN": {"Hello"}, "fr ": {"Bonjour"}}, ["EN", "fr "], {"EN": {"Hello"}, "fr ": {"Bonjour"}}, {}),
    ],
)
def test_pop_multilangstring_parametrized(initial_data, langs_to_pop, expected_result_data, expected_remaining_data):
    """
    Test the pop_multilangstring method with various scenarios including existing and non-existing languages,
    special character sets, and edge cases.
    :param initial_data: Initial data to populate the MultiLangString with.
    :param langs_to_pop: Languages to pop from the MultiLangString.
    :param expected_result_data: Expected data in the returned MultiLangString after popping.
    :param expected_remaining_data: Expected remaining data in the original MultiLangString after popping.
    """
    mls = MultiLangString(initial_data)
    popped_mls = mls.pop_multilangstring(langs_to_pop)
    assert {
        lang: popped_mls.mls_dict[lang] for lang in langs_to_pop if lang in popped_mls.mls_dict
    } == expected_result_data, "The popped MultiLangString does not match the expected result."
    assert (
        mls.mls_dict == expected_remaining_data
    ), "The remaining data in the original MultiLangString after popping does not match the expected remaining data."


@pytest.mark.parametrize(
    "langs_to_pop, expected_exception",
    [
        (None, TypeError),
        ("en", TypeError),
        (123, TypeError),
        (True, TypeError),
        (["en", 1], TypeError),
        ([1, "en"], TypeError),
    ],
)
def test_pop_multilangstring_invalid_input(langs_to_pop, expected_exception):
    """
    Test the pop_multilangstring method with invalid input types for langs parameter.
    :param langs_to_pop: Invalid type for langs parameter.
    :param expected_exception: Expected exception type.
    """
    mls = MultiLangString({"en": {"Hello", "World"}})
    with pytest.raises(expected_exception, match=TYPEERROR_MSG_SINGULAR):
        mls.pop_multilangstring(langs_to_pop)
