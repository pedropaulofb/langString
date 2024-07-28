import pytest
from langstring import MultiLangString


@pytest.mark.parametrize(
    "other,expected",
    [
        ("A string", False),
        (123, False),
        ([], False),
        ({}, False),
        (True, False),
        (None, False),
        ("", False),
        ("\n", False),
        (" ", False),
    ],
)
def test_eq_with_various_non_multilangstring_objects(other, expected):
    mls = MultiLangString({"en": {"Hello"}})
    assert (mls == other) is expected, f"Expected MultiLangString to be not equal to {type(other)}"
    assert (mls != other) is not expected, f"Expected MultiLangString to be not equal to {type(other)}"


# Test case for case-insensitive language key comparison
@pytest.mark.parametrize(
    "lang_case,expected",
    [
        ({"EN": {"Hello"}}, True),
        ({"en": {"Hello"}, "ES": {"Hola"}}, False),
        ({"eN": {"Hello"}}, True),
        ({"EN": {" HELLO "}}, False),
        ({"en ": {"Hello"}}, False),
    ],
)
def test_eq_case_insensitive_language_keys(lang_case, expected):
    mls1 = MultiLangString({"en": {"Hello"}})
    mls2 = MultiLangString(lang_case)
    assert (mls1 == mls2) is expected, "Case-insensitive language key comparison failed"
    assert (mls1 != mls2) is not expected, "Case-insensitive language key comparison failed"


@pytest.mark.parametrize(
    "content1,content2,expected",
    [
        ({"en": {"Hello"}}, {"en": {"Hello"}}, True),
        ({"fr": {"Bonjour"}, "es": {"Hola"}}, {"fr": {"Bonjour"}, "es": {"Hola"}}, True),
        ({"en": {"Good morning"}, "de": {"Guten Morgen"}}, {"en": {"Good morning"}, "de": {"Guten Morgen"}}, True),
        ({"en": {" "}}, {"en": {" "}}, True),
        ({"en": {""}}, {"en": {""}}, True),
    ],
)
def test_eq_identical_content(content1, content2, expected):
    mls1 = MultiLangString(content1)
    mls2 = MultiLangString(content2)
    assert (mls1 == mls2) is expected, "MultiLangString instances with identical content should match the expectation"
    assert (
        mls1 != mls2
    ) is not expected, "MultiLangString instances with identical content should match the expectation"


@pytest.mark.parametrize(
    "content1,content2,expected",
    [
        ({"en": {"Hello"}}, {"en": {"Goodbye"}}, False),
        ({"fr": {"Bonjour"}}, {"fr": {"Bonsoir"}}, False),
        ({"en": {"Hello"}}, {"de": {"Hallo"}}, False),
        ({"en": {"Hello "}}, {"en": {"Hello"}}, False),
        ({"en": {"Hello"}}, {"en": {" Hello"}}, False),
        ({"en": {"HELLO"}}, {"en": {"hello"}}, False),
    ],
)
def test_eq_different_content(content1, content2, expected):
    mls1 = MultiLangString(content1)
    mls2 = MultiLangString(content2)
    assert (mls1 == mls2) is expected, "MultiLangString instances with different content should not be equal"
    assert (mls1 != mls2) is not expected, "MultiLangString instances with different content should not be equal"


@pytest.mark.parametrize(
    "content1,content2,expected",
    [
        ({"en": {"Hello"}}, {"en": {"Hello"}, "es": {"Hola"}}, False),
        ({"fr": {"Bonjour"}}, {"fr": {"Bonjour"}, "de": {"Guten Tag"}}, False),
        ({"en": {"Good morning"}}, {"en": {"Good morning"}, "it": {"Buongiorno"}}, False),
        ({"gr": {"Γειά"}}, {"gr": {"Γειά"}, "en": {"Hello"}}, False),
        ({"ru": {"Привет"}}, {"ru": {"Привет"}, "es": {"Hola"}}, False),
    ],
)
def test_eq_additional_languages(content1, content2, expected):
    mls1 = MultiLangString(content1)
    mls2 = MultiLangString(content2)
    assert (mls1 == mls2) is expected, "Instances with additional languages should not be considered equal"
    assert (mls1 != mls2) is not expected, "Instances with additional languages should not be considered equal"


@pytest.mark.parametrize(
    "content1,content2,expected",
    [
        ({"en": {"Hello"}}, {"en": {"Hello", "Goodbye"}}, False),
        ({"fr": {"Bonjour"}}, {"fr": {"Bonjour", "Au revoir"}}, False),
        ({"es": {"Hola"}}, {"es": {"Hola", "Adiós"}}, False),
        ({"en": {"Hello", "Hello world"}}, {"en": {"Hello", "Hello world", "Goodbye"}}, False),
        ({"en": {"😀"}}, {"en": {"😀", "😂"}}, False),
        ({"en": {"Special &*()"}}, {"en": {"Special &*()", "Additional @#!"}}, False),
    ],
)
def test_eq_additional_texts_same_language(content1, content2, expected):
    mls1 = MultiLangString(content1)
    mls2 = MultiLangString(content2)
    assert (mls1 == mls2) is expected, "Instances with additional texts in the same language should not be equal"
    assert (mls1 != mls2) is not expected, "Instances with additional texts in the same language should not be equal"


@pytest.mark.parametrize(
    "content,expected",
    [
        ({}, True),  # Comparing empty MultiLangString instances
    ],
)
def test_eq_empty_content(content, expected):
    mls1 = MultiLangString(content)
    mls2 = MultiLangString(content)
    assert (mls1 == mls2) is expected, "Empty MultiLangString instances should be considered equal"


def test_eq_operation_on_itself():
    content = {"en": {"Hello"}}
    mls = MultiLangString(content)
    assert mls == mls, "A MultiLangString instance should be equal to itself"


@pytest.mark.parametrize(
    "pref_lang1,pref_lang2,expected",
    [
        ("en", "fr", True),
        ("es", "de", True),
        ("ru", "gr", True),
        ("en", "en", True),
    ],
)
def test_eq_different_pref_lang_same_content(pref_lang1, pref_lang2, expected):
    content = {"en": {"Hello"}, "fr": {"Bonjour"}, "es": {"Hola"}, "de": {"Hallo"}, "ru": {"Привет"}, "gr": {"Γειά"}}
    mls1 = MultiLangString(content, pref_lang=pref_lang1)
    mls2 = MultiLangString(content, pref_lang=pref_lang2)
    assert (
        mls1 == mls2
    ) is expected, "MultiLangString instances with different pref_lang but identical content should be equal"
