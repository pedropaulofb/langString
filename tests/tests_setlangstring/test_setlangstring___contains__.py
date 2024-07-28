import pytest
from langstring import Controller
from langstring import LangString
from langstring import SetLangString
from langstring import SetLangStringFlag
from tests.conftest import TYPEERROR_MSG_PLURAL


def calculate_expected_result(texts, lang, element, strict_mode):
    # Check for type compatibility
    if not isinstance(element, (str, LangString)):
        return TypeError

    # Check for language compatibility
    if isinstance(element, LangString):
        if element.lang != lang:
            return ValueError
        return element.text in texts

    # Check for strict mode and type of element
    if strict_mode and not isinstance(element, LangString):
        return TypeError

    # For string elements
    return element in texts


# Test cases for the __contains__ method
@pytest.mark.parametrize(
    "texts, lang, element",
    [
        # String in SetLangString
        ({"hello", "world"}, "en", "hello"),
        # String not in SetLangString
        ({"hello", "world"}, "en", "goodbye"),
        # LangString with same language in SetLangString
        ({"hello", "world"}, "en", LangString("hello", "en")),
        # LangString with same language not in SetLangString
        ({"hello", "world"}, "en", LangString("goodbye", "en")),
        # LangString with different language
        ({"hello", "world"}, "en", LangString("hello", "fr")),
        # Non-string, non-LangString type
        ({"hello", "world"}, "en", 5),
        # Empty SetLangString
        (set(), "en", "hello"),
        # Checking with empty string
        ({"hello", "world"}, "en", ""),
        # Special characters in SetLangString
        ({"!", "@"}, "en", "!"),
        # Emoji in SetLangString
        ({"😊", "😂"}, "en", "😊"),
        # Mixed content in SetLangString
        ({"hello", "1", "😊"}, "en", "1"),
    ],
)
@pytest.mark.parametrize("strict_mode", [True, False])
def test_setlangstring_contains(texts, lang, element, strict_mode):
    Controller.set_flag(SetLangStringFlag.METHODS_MATCH_TYPES, strict_mode)
    expected_result = calculate_expected_result(texts, lang, element, strict_mode)
    set_lang_string = SetLangString(texts=texts, lang=lang)

    if isinstance(expected_result, type) and issubclass(expected_result, Exception):
        with pytest.raises(expected_result):
            _ = element in set_lang_string
    else:
        assert (
            element in set_lang_string
        ) == expected_result, (
            f"Containment check failed for element '{element}' in SetLangString with texts {texts} and lang '{lang}'"
        )


# Additional test cases for the __contains__ method
@pytest.mark.parametrize(
    "texts, lang, element",
    [
        # Null value (None) as element
        ({"hello", "world"}, "en", None),
        # Empty LangString with same language
        ({"hello", "world"}, "en", LangString("", "en")),
        # LangString with empty text but different language
        ({"hello", "world"}, "en", LangString("", "fr")),
        # SetLangString with mixed types and checking for a non-existent complex string
        ({"hello", "1", "😊"}, "en", "hello world"),
    ],
)
@pytest.mark.parametrize("strict_mode", [True, False])
def test_setlangstring_contains_additional(texts, lang, element, strict_mode):
    Controller.set_flag(SetLangStringFlag.METHODS_MATCH_TYPES, strict_mode)
    expected_result = calculate_expected_result(texts, lang, element, strict_mode)
    set_lang_string = SetLangString(texts=texts, lang=lang)

    if isinstance(expected_result, type) and issubclass(expected_result, Exception):
        with pytest.raises(expected_result):
            _ = element in set_lang_string
    else:
        assert (
            element in set_lang_string
        ) == expected_result, (
            f"Containment check failed for element '{element}' in SetLangString with texts {texts} and lang '{lang}'"
        )


@pytest.mark.parametrize("element", [123, 45.67, None, True, [], {}, set()])
def test_contains_with_invalid_elements(element):
    """
    Test that the `__contains__` method returns False for invalid element types.

    :param element: An element of invalid type.
    :type element: Any
    :raises AssertionError: If the assertion fails.
    """
    set_lang_str = SetLangString({"Hello", "World"}, "en")
    with pytest.raises(TypeError, match=TYPEERROR_MSG_PLURAL):
        element in set_lang_str


def test_contains_with_valid_langstring():
    """
    Test that the `__contains__` method returns True for a LangString with the same language tag and text in the set.

    :raises AssertionError: If the assertion fails.
    """
    set_lang_str = SetLangString({"Hello", "World"}, "en")
    lang_str = LangString("Hello", "en")
    assert lang_str in set_lang_str, "LangString with same language tag and text should be in the set"


def test_contains_with_valid_string():
    """
    Test that the `__contains__` method returns True for a valid string in the set.

    :raises AssertionError: If the assertion fails.
    """
    set_lang_str = SetLangString({"Hello", "World"}, "en")
    assert "Hello" in set_lang_str, "String 'Hello' should be in the set"
    assert "Python" not in set_lang_str, "String 'Python' should not be in the set"
