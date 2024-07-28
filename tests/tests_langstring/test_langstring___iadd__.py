import pytest
from langstring import Controller
from langstring import LangStringFlag
from langstring.langstring import LangString


@pytest.mark.parametrize(
    "initial_text, add_text, expected_text",
    [
        ("Hello", " World", "Hello World"),
        ("Bonjour", " le monde", "Bonjour le monde"),
    ],
)
@pytest.mark.parametrize("strict", [True, False])
def test_iadd_langstring_with_string(initial_text, add_text, expected_text, strict):
    """Test in-place addition of a string to a LangString object."""
    Controller.set_flag(LangStringFlag.METHODS_MATCH_TYPES, strict)
    lang_str = LangString(initial_text, "en")
    if strict:
        with pytest.raises(TypeError, match="Strict mode is enabled. Operand must be of type LangString"):
            lang_str += add_text
    else:
        lang_str += add_text
        assert lang_str.text == expected_text and lang_str.lang == "en"


@pytest.mark.parametrize(
    "initial_text, initial_lang, add_text, add_lang, expected_text, expected_lang",
    [
        ("Hello", "en", " World", "en", "Hello World", "en"),
        ("Hola", "es", " Mundo", "es", "Hola Mundo", "es"),
    ],
)
@pytest.mark.parametrize("strict", [True, False])
def test_iadd_two_langstrings_same_lang(
    initial_text, initial_lang, add_text, add_lang, expected_text, expected_lang, strict
):
    """Test in-place addition of two LangString objects with the same language."""
    Controller.set_flag(LangStringFlag.METHODS_MATCH_TYPES, strict)
    lang_str1 = LangString(initial_text, initial_lang)
    lang_str2 = LangString(add_text, add_lang)
    lang_str1 += lang_str2
    assert lang_str1.text == expected_text and lang_str1.lang == expected_lang


@pytest.mark.parametrize(
    "strip_lang_flag, should_raise_error",
    [
        (True, False),
        (False, True),
    ],
)
@pytest.mark.parametrize("strict", [True, False])
def test_iadd_langstrings_with_strip_lang_effect(strip_lang_flag, should_raise_error, strict):
    """Test in-place addition of LangString objects with language tags affected by the STRIP_LANG flag."""
    Controller.set_flag(LangStringFlag.METHODS_MATCH_TYPES, strict)
    Controller.set_flag(LangStringFlag.STRIP_LANG, strip_lang_flag)

    lang_str1 = LangString("Hello", "en")
    lang_str2 = LangString("Bonjour", " en")

    if should_raise_error:
        with pytest.raises(
            ValueError, match="Operation cannot be performed. Incompatible languages between LangString"
        ):
            lang_str1 += lang_str2
    else:
        lang_str1 += lang_str2
        assert lang_str1.text == "HelloBonjour" and lang_str1.lang == "en"


@pytest.mark.parametrize(
    "initial_lang, add_lang, expected_error",
    [
        ("en", "en", False),
        ("en", "EN", False),
        ("en", " en", True),  # Leading space in add_lang, should raise error if STRIP_LANG is False
        ("en", "en-us", True),  # Different language tags, should raise error
    ],
)
@pytest.mark.parametrize("strict", [True, False])
def test_iadd_langstrings_case_insensitive_and_strip_lang(initial_lang, add_lang, expected_error, strict):
    """Test in-place addition of LangString objects with case-insensitive language tags and STRIP_LANG flag effect."""
    Controller.set_flag(LangStringFlag.METHODS_MATCH_TYPES, strict)
    Controller.set_flag(LangStringFlag.STRIP_LANG, not expected_error)
    lang_str1 = LangString("Hello", initial_lang)
    lang_str2 = LangString("World", add_lang)

    if expected_error:
        with pytest.raises(
            ValueError, match="Operation cannot be performed. Incompatible languages between LangString"
        ):
            lang_str1 += lang_str2
    else:
        lang_str1 += lang_str2
        assert lang_str1.text == "HelloWorld" and lang_str1.lang == initial_lang.lower()


@pytest.mark.parametrize(
    "initial_text, add_obj, expected_text, expected_error",
    [
        ("Hello", None, "", TypeError),
        ("", LangString("", "en"), "", None),
        ("Hello", LangString("", "en"), "Hello", None),
        ("Hello", LangString("World", "en"), "HelloWorld", None),
    ],
)
@pytest.mark.parametrize("strict", [True, False])
def test_iadd_langstring_with_various_values(initial_text, add_obj, expected_text, expected_error, strict):
    """Test in-place addition of LangString with various values including empty and None."""
    Controller.set_flag(LangStringFlag.METHODS_MATCH_TYPES, strict)
    lang_str = LangString(initial_text, "en")
    if expected_error:
        with pytest.raises(expected_error):
            lang_str += add_obj
    else:
        lang_str += add_obj
        assert lang_str.text == expected_text


@pytest.mark.parametrize(
    "strip_text_flag, initial_text, add_text, expected_text",
    [
        (True, "Hello ", "World", "HelloWorld"),
        (False, "Hello ", "World", "Hello World"),
    ],
)
@pytest.mark.parametrize("strict", [True, False])
def test_iadd_langstrings_with_strip_text_effect(strip_text_flag, initial_text, add_text, expected_text, strict):
    """Test in-place addition of LangString objects with STRIP_TEXT flag effect."""
    Controller.set_flag(LangStringFlag.METHODS_MATCH_TYPES, strict)
    Controller.set_flag(LangStringFlag.STRIP_TEXT, strip_text_flag)
    lang_str1 = LangString(initial_text, "en")
    lang_str2 = LangString(add_text, "en")
    lang_str1 += lang_str2
    assert lang_str1.text == expected_text
