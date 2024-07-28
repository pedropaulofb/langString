import pytest
from langstring import LangString
from langstring import MultiLangString
from tests.conftest import TYPEERROR_MSG_SINGULAR


@pytest.mark.parametrize(
    "init_data, langstring_text, langstring_lang, clean_empty, expected_exists",
    [
        ({"en": {"test1"}, "de": {"test2"}}, "test1", "en", False, True),
        ({"en": {"test1"}, "de": {"test2"}}, "test2", "de", True, False),
        ({"en": {"test1", "test2"}}, "test1", "en", True, True),
        ({"en": {""}}, "", "en", True, False),
        ({"en": {"Test1"}, "de": {"Test2"}}, "Test1", "en", False, True),
        ({"en": {"Test1"}, "de": {"Test2"}}, "Test1", "en", True, False),
        ({"en": {" test1 "}, "de": {"test2"}}, " test1 ", "en", True, False),
        ({"el": {"δοκιμή"}}, "δοκιμή", "el", False, True),
        ({"ru": {"тест"}}, "тест", "ru", True, False),
        ({"en": {"😊"}}, "😊", "en", True, False),
        ({"en": {"test@#"}}, "test@#", "en", True, False),
        ({"En": {"test@#"}}, "test@#", "en", True, False),
        ({"en": {"test@#"}}, "test@#", "En", True, False),
        ({"none": {"test1"}}, "test1", "none", False, True),
        ({"int": {"42"}}, "42", "int", True, False),
    ],
)
def test_remove_langstring_valid_cases(init_data, langstring_text, langstring_lang, clean_empty, expected_exists):
    """Test removing LangStrings from MultiLangString for valid scenarios.

    :param init_data: Initial data for MultiLangString instance.
    :param langstring_text: Text of the LangString to be removed.
    :param langstring_lang: Language of the LangString to be removed.
    :param clean_empty: Specifies whether to clean up empty language entries.
    :param expected_exists: Boolean indicating if the language should still exist in the MultiLangString.
    """
    mls = MultiLangString(init_data)
    ls = LangString(langstring_text, langstring_lang)
    mls.remove_langstring(ls, clean_empty=clean_empty)
    assert (langstring_lang in mls.mls_dict) is expected_exists, "LangString removal did not match expected outcome."


@pytest.mark.parametrize(
    "init_data, langstring_to_remove",
    [
        ({"en": {"test1"}}, LangString("nonexistent", "en")),
        ({"en": set()}, LangString("test1", "en")),
        ({"en": {"test1"}}, LangString("", "en")),
        ({"en": {"test1"}}, LangString("😊", "en")),
        ({"en": {"test1"}}, LangString("test@#", "en")),
    ],
)
def test_remove_langstring_value_error(init_data, langstring_to_remove):
    """
    Test removing LangStrings from MultiLangString for scenarios expected to fail with ValueError.

    :param init_data: Initial data for MultiLangString instance.
    :param langstring_to_remove: LangString instance to be removed.
    """
    mls = MultiLangString(init_data)
    with pytest.raises(ValueError, match="Entry .+ not found in the MultiLangString."):
        mls.remove_langstring(langstring_to_remove), "Expected exception was not raised."


# TypeError test for remove_langstring with invalid types
@pytest.mark.parametrize(
    "init_data, langstring_to_remove",
    [
        ({"en": {"test1"}}, None),
        ({"en": {"test1"}}, "LangString"),
        ({"en": {"test1"}}, True),
        ({"en": {"test1"}}, {}),
    ],
)
def test_remove_langstring_type_error(init_data, langstring_to_remove):
    """
    Test removing LangStrings from MultiLangString for scenarios expected to fail with TypeError.

    :param init_data: Initial data for MultiLangString instance.
    :param langstring_to_remove: LangString instance to be removed.
    """
    mls = MultiLangString(init_data)
    with pytest.raises(TypeError, match=TYPEERROR_MSG_SINGULAR):
        mls.remove_langstring(langstring_to_remove), "Expected exception was not raised."
