import pytest
from langstring import Controller
from langstring import LangString
from langstring import LangStringFlag
from tests.conftest import TYPEERROR_MSG_SINGULAR


@pytest.mark.parametrize(
    "input_text, expected_text",
    [
        ("Hello, World!", "Hello, World!"),
        ("", ""),
        (None, ""),
        ("123", "123"),
        ("Special characters: !@#$%^&*()", "Special characters: !@#$%^&*()"),
        ("Unicode 😊", "Unicode 😊"),
    ],
)
def test_text_getter_setter(input_text: str, expected_text: str) -> None:
    """Test the text getter and setter for various inputs.

    :param input_text: The input text to be set.
    :param expected_text: The expected text after setting.
    """
    lang_string = LangString()
    lang_string.text = input_text
    assert lang_string.text == expected_text, f"Text getter/setter failed for input '{input_text}'"


@pytest.mark.parametrize(
    "input_lang, expected_lang",
    [("en", "en"), (None, ""), ("", ""), ("fr", "fr"), ("EN", "EN"), ("zh-CN", "zh-CN"), (None, "")],
)
def test_lang_getter_setter(input_lang: str, expected_lang: str) -> None:
    """Test the lang getter and setter for various inputs.

    :param input_lang: The input language tag to be set.
    :param expected_lang: The expected language tag after setting.
    """
    lang_string = LangString()
    lang_string.lang = input_lang
    assert lang_string.lang == expected_lang, f"Lang getter/setter failed for input '{input_lang}'"


@pytest.mark.parametrize("invalid_text", [123, True, 3.14, ["list"], {"dict": "value"}])
def test_text_setter_invalid_type(invalid_text) -> None:
    """Test the text setter with invalid types.

    :param invalid_text: The invalid text input to be set.
    """
    with pytest.raises(TypeError, match=TYPEERROR_MSG_SINGULAR):
        LangString(text=invalid_text)


@pytest.mark.parametrize("invalid_lang", [123, True, 3.14, ["list"], {"dict": "value"}])
def test_lang_setter_invalid_type(invalid_lang) -> None:
    """Test the lang setter with invalid types.

    :param invalid_lang: The invalid language tag input to be set.
    """
    with pytest.raises(TypeError, match=TYPEERROR_MSG_SINGULAR):
        LangString(lang=invalid_lang)


def test_text_setter_empty_with_flag() -> None:
    """Test the text setter with an empty string when the DEFINED_TEXT flag is enabled."""
    Controller.set_flag(LangStringFlag.DEFINED_TEXT, True)
    with pytest.raises(ValueError, match="Invalid 'text' value received"):
        LangString(text="")


def test_lang_setter_empty_with_flag() -> None:
    """Test the text setter with an empty string when the DEFINED_LANG flag is enabled."""
    Controller.reset_flags()
    Controller.set_flag(LangStringFlag.DEFINED_LANG, True)
    with pytest.raises(ValueError, match="Invalid 'lang' value received"):
        LangString(lang="")


def test_lang_setter_invalid_with_flag() -> None:
    """Test the lang setter with an invalid language tag when the VALID_LANG flag is enabled."""
    Controller.reset_flags()
    Controller.set_flag(LangStringFlag.VALID_LANG, True)
    with pytest.raises(ValueError, match="Invalid 'lang' value received"):
        LangString(lang="invalid-lang")
