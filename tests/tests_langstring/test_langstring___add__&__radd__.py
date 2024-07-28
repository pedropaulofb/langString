import pytest
from langstring import Controller
from langstring import LangString
from langstring import LangStringFlag
from tests.conftest import TYPEERROR_MSG_PLURAL
from tests.conftest import TYPEERROR_MSG_SINGULAR


# Test cases for adding two LangString objects
@pytest.mark.parametrize(
    "text1, lang1, text2, lang2, expected_text, expected_lang",
    [
        ("Hello", "en", " World", "en", "Hello World", "en"),
        ("Bonjour", "fr", " le monde", "fr", "Bonjour le monde", "fr"),
    ],
)
@pytest.mark.parametrize("strict", [True, False])
def test_add_two_langstrings_same_lang(text1, lang1, text2, lang2, expected_text, expected_lang, strict):
    """Test adding two LangString objects with the same language."""
    Controller.set_flag(LangStringFlag.METHODS_MATCH_TYPES, strict)
    lang_str1 = LangString(text1, lang1)
    lang_str2 = LangString(text2, lang2)
    result = lang_str1 + lang_str2
    assert (
        result.text == expected_text and result.lang == expected_lang
    ), "Adding two LangString objects with the same language should concatenate their texts"


@pytest.mark.parametrize(
    "lang1, lang2",
    [
        ("en", "fr"),
        ("en", " en"),  # Leading space in language tag
        ("en-us", "en"),  # Different regional dialects
        ("en", ""),  # One empty language tag
        ("en-US", "en-GB"),  # Different regional dialects of the same language
    ],
)
@pytest.mark.parametrize("strict", [True, False])
def test_add_two_langstrings_different_lang(lang1, lang2, strict):
    Controller.set_flag(LangStringFlag.METHODS_MATCH_TYPES, strict)
    lang_str1 = LangString("Hello", lang1)
    lang_str2 = LangString("Bonjour", lang2)
    with pytest.raises(
        ValueError,
        match="Operation cannot be performed. Incompatible languages between LangString and LangString object.",
    ):
        _ = lang_str1 + lang_str2


# Test adding LangString and string
@pytest.mark.parametrize(
    "lang_str_text, lang_str_lang, other_text, expected_text",
    [
        ("Hello", "en", " World", "Hello World"),
        ("Hola", "es", " Mundo", "Hola Mundo"),
    ],
)
@pytest.mark.parametrize("strict", [True, False])
def test_add_langstring_and_string(lang_str_text, lang_str_lang, other_text, expected_text, strict):
    Controller.set_flag(LangStringFlag.METHODS_MATCH_TYPES, strict)
    lang_str = LangString(lang_str_text, lang_str_lang)

    if strict:
        with pytest.raises(TypeError):
            _ = lang_str + other_text
    else:
        result = lang_str + other_text
        assert (
            result.text == expected_text and result.lang == lang_str_lang
        ), "Adding a LangString and a string should concatenate the text"


# Test adding string and LangString
@pytest.mark.parametrize(
    "other_text, lang_str_text, lang_str_lang, expected_text",
    [
        ("Welcome ", "to Python", "en", "Welcome to Python"),
        ("Bienvenido ", "al mundo", "es", "Bienvenido al mundo"),
    ],
)
@pytest.mark.parametrize("strict", [True, False])
def test_add_string_and_langstring(other_text, lang_str_text, lang_str_lang, expected_text, strict):
    """Test adding a string to a LangString object."""
    Controller.set_flag(LangStringFlag.METHODS_MATCH_TYPES, strict)
    lang_str = LangString(lang_str_text, lang_str_lang)
    result = other_text + lang_str
    assert result == expected_text, "Adding a string to a LangString should concatenate the text"


# Test adding incompatible types
@pytest.mark.parametrize(
    "lang_str, other",
    [
        (LangString("Hello", "en"), 42),
        (LangString("Hola", "es"), 3.14),
        (LangString("Bonjour", "fr"), None),
    ],
)
@pytest.mark.parametrize("strict", [True, False])
def test_add_incompatible_types(lang_str, other, strict):
    """Test adding incompatible types to a LangString."""
    Controller.set_flag(LangStringFlag.METHODS_MATCH_TYPES, strict)
    with pytest.raises(TypeError, match=TYPEERROR_MSG_PLURAL):
        _ = lang_str + other


# Test adding LangString to itself
@pytest.mark.parametrize("strict", [True, False])
def test_add_langstring_to_itself(strict):
    """Test adding a LangString object to itself."""
    Controller.set_flag(LangStringFlag.METHODS_MATCH_TYPES, strict)
    lang_str = LangString("Repeat ", "en")
    result = lang_str + lang_str
    assert (
        result.text == "Repeat Repeat " and result.lang == "en"
    ), "Adding a LangString to itself should concatenate its text"


# Test adding a string to a LangString object using the __radd__ method
@pytest.mark.parametrize(
    "other_text, lang_str_text, lang_str_lang, expected_text",
    [
        ("Welcome ", "to Python", "en", "Welcome to Python"),
        ("Hola ", "mundo", "es", "Hola mundo"),
    ],
)
@pytest.mark.parametrize("strict", [True, False])
def test_radd_string_to_langstring(other_text, lang_str_text, lang_str_lang, expected_text, strict):
    """Test adding a string to a LangString object using the __radd__ method."""
    Controller.set_flag(LangStringFlag.METHODS_MATCH_TYPES, strict)
    lang_str = LangString(lang_str_text, lang_str_lang)
    result = other_text + lang_str
    assert result == expected_text, "The text after addition should match the expected result"


# Test adding an incompatible type to a LangString object using the __radd__ method
@pytest.mark.parametrize(
    "other, lang_str_text, lang_str_lang",
    [
        (123, "text", "en"),
        ([], "text", "en"),
        (None, "text", "en"),
    ],
)
@pytest.mark.parametrize("strict", [True, False])
def test_radd_incompatible_type_to_langstring(other, lang_str_text, lang_str_lang, strict):
    """Test adding an incompatible type to a LangString object using the __radd__ method."""
    Controller.set_flag(LangStringFlag.METHODS_MATCH_TYPES, strict)
    lang_str = LangString(lang_str_text, lang_str_lang)
    with pytest.raises(TypeError, match=TYPEERROR_MSG_SINGULAR):
        _ = other + lang_str


# Test adding empty strings to a LangString object
@pytest.mark.parametrize(
    "other_text, lang_str_text, lang_str_lang, expected_text",
    [
        ("", "text", "en", "text"),
        ("text", "", "en", "text"),
        ("", "", "en", ""),
    ],
)
@pytest.mark.parametrize("strict", [True, False])
def test_add_empty_string_to_langstring(other_text, lang_str_text, lang_str_lang, expected_text, strict):
    """Test adding empty strings to a LangString object."""
    Controller.set_flag(LangStringFlag.METHODS_MATCH_TYPES, strict)
    lang_str = LangString(lang_str_text, lang_str_lang)

    if strict:
        with pytest.raises(TypeError):
            _ = lang_str + other_text
    else:
        result = lang_str + other_text
        assert (
            result.text == expected_text
        ), "The text after addition with an empty string should match the expected result"


# Test adding empty strings to a LangString object using the __radd__ method
@pytest.mark.parametrize(
    "other_text, lang_str_text, lang_str_lang, expected_text",
    [
        ("", "text", "en", "text"),
        ("text", "", "en", "text"),
        ("", "", "en", ""),
    ],
)
@pytest.mark.parametrize("strict", [True, False])
def test_radd_empty_string_to_langstring(other_text, lang_str_text, lang_str_lang, expected_text, strict):
    """Test adding empty strings to a LangString object using the __radd__ method."""
    Controller.set_flag(LangStringFlag.METHODS_MATCH_TYPES, strict)
    lang_str = LangString(lang_str_text, lang_str_lang)
    result = other_text + lang_str
    assert result == expected_text, "The text after addition with an empty string should match the expected result"


@pytest.mark.parametrize(
    "flag_state, text1, text2, expected_result",
    [
        (True, " Hello ", "World ", "HelloWorld"),
        (False, " Hello ", "World ", " Hello World "),
    ],
)
@pytest.mark.parametrize("strict", [True, False])
def test_add_with_strip_text_flag(flag_state, text1, text2, expected_result, strict):
    """Test adding LangString objects with the STRIP_TEXT flag."""
    Controller.set_flag(LangStringFlag.METHODS_MATCH_TYPES, strict)
    Controller.set_flag(LangStringFlag.STRIP_TEXT, flag_state)
    lang_str1 = LangString(text1, "en")
    lang_str2 = LangString(text2, "en")
    result = lang_str1 + lang_str2
    assert result.text == expected_result, "The result should consider the STRIP_TEXT flag state"


@pytest.mark.parametrize(
    "strip_lang_flag, should_raise_error",
    [
        (True, False),  # With STRIP_LANG enabled, addition should succeed
        (False, True),  # With STRIP_LANG disabled, addition should raise an error
    ],
)
@pytest.mark.parametrize("strict", [True, False])
def test_add_langstrings_with_strip_lang_effect(strip_lang_flag, should_raise_error, strict):
    """Test adding two LangString objects with language tags affected by the STRIP_LANG flag."""
    Controller.set_flag(LangStringFlag.METHODS_MATCH_TYPES, strict)
    Controller.set_flag(LangStringFlag.STRIP_LANG, strip_lang_flag)

    lang_str1 = LangString("Hello", "en")
    lang_str2 = LangString("Bonjour", " en")  # Note the leading space in the language tag

    if should_raise_error:
        with pytest.raises(
            ValueError, match="Operation cannot be performed. Incompatible languages between LangString"
        ):
            _ = lang_str1 + lang_str2
    else:
        result = lang_str1 + lang_str2
        assert result.text == "HelloBonjour" and result.lang == "en"


@pytest.mark.parametrize(
    "lang1, lang2, text1, text2, expected_result",
    [
        ("en", "EN", "Hello", "World", "HelloWorld"),
        ("EN", "en", "Hello", "World", "HelloWorld"),
        ("En", "eN", "Hello", "World", "HelloWorld"),
    ],
)
@pytest.mark.parametrize("strict", [True, False])
def test_add_langstring_case_insensitive_lang_tags(lang1, lang2, text1, text2, expected_result, strict):
    """Test adding LangString objects with case-insensitive language tags."""
    Controller.set_flag(LangStringFlag.METHODS_MATCH_TYPES, strict)
    lang_str1 = LangString(text1, lang1)
    lang_str2 = LangString(text2, lang2)
    result = lang_str1 + lang_str2
    assert result.text == expected_result, "The addition should be successful with case-insensitive language tags"
