from enum import Enum
from typing import Optional
from unittest.mock import patch

import pytest
from langstring import Controller
from langstring import GlobalFlag
from langstring import LangStringFlag
from langstring.utils.validators import FlagValidator


@pytest.mark.parametrize(
    "flag_type,lang,expected,msg",
    [
        (LangStringFlag, None, "", "Expected no error when lang is None"),
        (LangStringFlag, "", "", "Expected no error when lang is an empty string"),
        (LangStringFlag, "en", "en", "Expected lang 'en' to be valid"),
        (LangStringFlag, "EN", "EN", "Expected lang 'EN' to be valid"),
        (LangStringFlag, "   ", "   ", "Expected lang with spaces only to be valid"),
        (LangStringFlag, "123", "123", "Expected numeric lang to be valid"),
        (LangStringFlag, "русский", "русский", "Expected Cyrillic lang to be valid"),
        (LangStringFlag, "Ελληνικά", "Ελληνικά", "Expected Greek lang to be valid"),
        (LangStringFlag, "emoji 😊", "emoji 😊", "Expected lang with emoji to be valid"),
        (LangStringFlag, "!@#$%^&*()", "!@#$%^&*()", "Expected lang with special characters to be valid"),
        (LangStringFlag, "mixED CaSe", "mixED CaSe", "Expected lang with mixed case to be valid"),
        (LangStringFlag, "   en   ", "   en   ", "Expected lang with spaces before and after to be valid"),
    ],
)
def test_validate_flags_lang_basic(flag_type: type[Enum], lang: Optional[str], expected: str, msg: str) -> None:
    """Test basic functionality of validate_flags_lang without any flags enabled.

    :param flag_type: The type of flag to use for validation.
    :type flag_type: type[Enum]
    :param lang: The language string to validate.
    :type lang: Optional[str]
    :param expected: The expected output.
    :type expected: str
    :param msg: Assertion message in case of failure.
    :type msg: str
    """
    assert FlagValidator.validate_flags_lang(flag_type, lang) == expected, msg


@pytest.mark.parametrize(
    "flag_type,lang,msg",
    [
        (
            LangStringFlag,
            None,
            r"Invalid 'lang' value received \('None'\)\. 'LangStringFlag\.DEFINED_LANG' is enabled\. Expected non-empty 'str' or 'str' with non-space characters\.",
        ),
        (
            LangStringFlag,
            "",
            r"Invalid 'lang' value received \(''\)\. 'LangStringFlag\.DEFINED_LANG' is enabled\. Expected non-empty 'str' or 'str' with non-space characters\.",
        ),
        (
            LangStringFlag,
            "   ",
            r"Invalid 'lang' value received \('   '\)\. 'LangStringFlag\.DEFINED_LANG' is enabled\. Expected non-empty 'str' or 'str' with non-space characters\.",
        ),
    ],
)
def test_validate_flags_lang_defined_lang(flag_type: type[Enum], lang: Optional[str], msg: str) -> None:
    """Test validate_flags_lang with DEFINED_LANG flag enabled.

    :param flag_type: The type of flag to use for validation.
    :type flag_type: type[Enum]
    :param lang: The language string to validate.
    :type lang: Optional[str]
    :param msg: Assertion message in case of failure.
    :type msg: str
    :raises: ValueError
    """
    Controller.set_flag(flag_type.DEFINED_LANG, True)
    with pytest.raises(ValueError, match=msg):
        FlagValidator.validate_flags_lang(flag_type, lang)
    Controller.set_flag(flag_type.DEFINED_LANG, False)


@pytest.mark.parametrize(
    "flag_type,lang,expected,msg",
    [
        (LangStringFlag, "  en  ", "en", "Expected 'en' when lang is '  en  ' and STRIP_LANG is enabled"),
        (LangStringFlag, "EN", "en", "Expected 'en' when lang is 'EN' and LOWERCASE_LANG is enabled"),
        (
            LangStringFlag,
            "  ΕΛΛΗΝΙΚΆ  ",
            "ελληνικά",
            "Expected 'ελληνικά' when lang is '  ΕΛΛΗΝΙΚΆ  ' and STRIP_LANG and LOWERCASE_LANG are enabled",
        ),
        (
            LangStringFlag,
            "  РУССКИЙ  ",
            "русский",
            "Expected 'русский' when lang is '  РУССКИЙ  ' and STRIP_LANG and LOWERCASE_LANG are enabled",
        ),
        (
            LangStringFlag,
            " Emoji 😊 ",
            "emoji 😊",
            "Expected 'emoji 😊' when lang is ' Emoji 😊 ' and STRIP_LANG and LOWERCASE_LANG are enabled",
        ),
        (
            LangStringFlag,
            "  MixED CaSe  ",
            "mixed case",
            "Expected 'mixed case' when lang is '  MixED CaSe  ' and STRIP_LANG and LOWERCASE_LANG are enabled",
        ),
    ],
)
def test_validate_flags_lang_strip_lowercase(flag_type: type[Enum], lang: str, expected: str, msg: str) -> None:
    """Test validate_flags_lang with STRIP_LANG and LOWERCASE_LANG flags enabled.

    :param flag_type: The type of flag to use for validation.
    :type flag_type: type[Enum]
    :param lang: The language string to validate.
    :type lang: str
    :param expected: The expected output.
    :type expected: str
    :param msg: Assertion message in case of failure.
    :type msg: str
    """
    Controller.set_flag(flag_type.STRIP_LANG, True)
    Controller.set_flag(flag_type.LOWERCASE_LANG, True)
    assert FlagValidator.validate_flags_lang(flag_type, lang) == expected, msg
    Controller.set_flag(flag_type.STRIP_LANG, False)
    Controller.set_flag(flag_type.LOWERCASE_LANG, False)


def test_validate_flags_lang_import_error() -> None:
    """Test validate_flags_lang raises ImportError when VALID_LANG is enabled and langcodes is not installed.

    :raises: ImportError
    """
    Controller.set_flag(LangStringFlag.VALID_LANG, True)
    Controller.set_flag(GlobalFlag.ENFORCE_EXTRA_DEPEND, True)

    import builtins

    original_import = builtins.__import__

    def mocked_import(name, *args):
        if name == "langcodes":
            raise ImportError("No module named 'langcodes'")
        return original_import(name, *args)

    with patch("builtins.__import__", side_effect=mocked_import):
        with pytest.raises(ImportError, match=r"VALID_LANG functionality requires the 'langcodes' library"):
            FlagValidator.validate_flags_lang(LangStringFlag, "en")

    Controller.set_flag(LangStringFlag.VALID_LANG, False)
    Controller.set_flag(GlobalFlag.ENFORCE_EXTRA_DEPEND, False)


@pytest.mark.parametrize(
    "flag_type,lang,msg",
    [
        (
            LangStringFlag,
            "invalid-lang",
            r"Invalid 'lang' value received \('invalid-lang'\)\. 'LangStringFlag\.VALID_LANG' is enabled\. Expected valid language code\.",
        ),
        (
            LangStringFlag,
            "  invalid-lang  ",
            r"Invalid 'lang' value received \('  invalid-lang  '\)\. 'LangStringFlag\.VALID_LANG' is enabled\. Expected valid language code\.",
        ),
        (
            LangStringFlag,
            "русский-invalid",
            r"Invalid 'lang' value received \('русский-invalid'\)\. 'LangStringFlag\.VALID_LANG' is enabled\. Expected valid language code\.",
        ),
        (
            LangStringFlag,
            "Ελληνικά-invalid",
            r"Invalid 'lang' value received \('Ελληνικά-invalid'\)\. 'LangStringFlag\.VALID_LANG' is enabled\. Expected valid language code\.",
        ),
        (
            LangStringFlag,
            "emoji-invalid 😊",
            r"Invalid 'lang' value received \('emoji-invalid 😊'\)\. 'LangStringFlag\.VALID_LANG' is enabled\. Expected valid language code\.",
        ),
        (
            LangStringFlag,
            "!@#$%^&*-invalid",
            r"Invalid 'lang' value received \('!@#\$%\^&\*-invalid'\)\. 'LangStringFlag\.VALID_LANG' is enabled\. Expected valid language code\.",
        ),
    ],
)
def test_validate_flags_lang_invalid(flag_type: type[Enum], lang: str, msg: str) -> None:
    """Test validate_flags_lang raises ValueError when VALID_LANG is enabled and lang is invalid.

    :param flag_type: The type of flag to use for validation.
    :type flag_type: type[Enum]
    :param lang: The language string to validate.
    :type lang: str
    :param msg: Assertion message in case of failure.
    :type msg: str
    :raises: ValueError
    """
    Controller.set_flag(flag_type.VALID_LANG, True)
    with pytest.raises(ValueError, match=msg):
        FlagValidator.validate_flags_lang(flag_type, lang)
    Controller.set_flag(flag_type.VALID_LANG, False)


@pytest.mark.parametrize(
    "flag_type,lang,expected,msg",
    [
        (LangStringFlag, "a" * 1000, "a" * 1000, "Expected lang to be valid for very long strings"),
        (LangStringFlag, " !@#$%^&*()_+ ", " !@#$%^&*()_+ ", "Expected lang to be valid for special characters"),
        (LangStringFlag, "emoji 😊 emoji", "emoji 😊 emoji", "Expected lang to be valid for lang with multiple emojis"),
    ],
)
def test_validate_flags_lang_edge_cases(flag_type: type[Enum], lang: str, expected: str, msg: str) -> None:
    """Test validate_flags_lang with edge cases.

    :param flag_type: The type of flag to use for validation.
    :type flag_type: type[Enum]
    :param lang: The language string to validate.
    :type lang: str
    :param expected: The expected output.
    :type expected: str
    :param msg: Assertion message in case of failure.
    :type msg: str
    """
    assert FlagValidator.validate_flags_lang(flag_type, lang) == expected, msg


@pytest.mark.parametrize(
    "flag_type,flags_combination,lang,expected,msg",
    [
        (
            LangStringFlag,
            [LangStringFlag.STRIP_LANG, LangStringFlag.LOWERCASE_LANG],
            "  EN  ",
            "en",
            "Expected 'en' when STRIP_LANG and LOWERCASE_LANG are enabled",
        ),
        (
            LangStringFlag,
            [LangStringFlag.DEFINED_LANG, LangStringFlag.VALID_LANG],
            "en",
            "en",
            "Expected 'en' when DEFINED_LANG and VALID_LANG are enabled",
        ),
        # Issue: The `langcodes` library's `tag_is_valid` function may not correctly validate certain known valid language tags.
        # (LangStringFlag, [LangStringFlag.STRIP_LANG, LangStringFlag.LOWERCASE_LANG, LangStringFlag.VALID_LANG], "  ΕΛΛΗΝΙΚΆ  ", "ελληνικά",
        #  "Expected 'ελληνικά' when STRIP_LANG, LOWERCASE_LANG, and VALID_LANG are enabled"),
        # (LangStringFlag, [LangStringFlag.STRIP_LANG, LangStringFlag.LOWERCASE_LANG, LangStringFlag.VALID_LANG], "  РУССКИЙ  ", "русский",
        #  "Expected 'русский' when STRIP_LANG, LOWERCASE_LANG, and VALID_LANG are enabled"),
        # (LangStringFlag, [LangStringFlag.STRIP_LANG, LangStringFlag.LOWERCASE_LANG, LangStringFlag.VALID_LANG], " emoji 😊 ", "emoji 😊",
        #  "Expected 'emoji 😊' when STRIP_LANG, LOWERCASE_LANG, and VALID_LANG are enabled"),
    ],
)
def test_validate_flags_lang_unusual_usage(
    flag_type: type[Enum], flags_combination: list, lang: str, expected: str, msg: str
) -> None:
    """Test validate_flags_lang with unusual but valid flag combinations.

    :param flag_type: The type of flag to use for validation.
    :type flag_type: type[Enum]
    :param flags_combination: List of flags to enable for validation.
    :type flags_combination: list
    :param lang: The language string to validate.
    :type lang: str
    :param expected: The expected output.
    :type expected: str
    :param msg: Assertion message in case of failure.
    :type msg: str
    """
    for flag in flags_combination:
        Controller.set_flag(flag, True)
    assert FlagValidator.validate_flags_lang(flag_type, lang) == expected, msg
    for flag in flags_combination:
        Controller.set_flag(flag, False)


@pytest.mark.parametrize(
    "flag_type,lang,expected,msg",
    [
        (
            LangStringFlag,
            "  ΕΛΛΗΝΙΚΆ  ",
            "ελληνικά",
            "Expected 'ελληνικά' when STRIP_LANG and LOWERCASE_LANG flags are enabled.",
        ),
        (
            LangStringFlag,
            "\nΕΛΛΗΝΙΚΆ\n",
            "ελληνικά",
            "Expected 'ελληνικά' when STRIP_LANG and LOWERCASE_LANG flags are enabled.",
        ),
        (
            LangStringFlag,
            "\tΕΛΛΗΝΙΚΆ\t",
            "ελληνικά",
            "Expected 'ελληνικά' when STRIP_LANG and LOWERCASE_LANG flags are enabled.",
        ),
        (
            LangStringFlag,
            "\rΕΛΛΗΝΙΚΆ\r",
            "ελληνικά",
            "Expected 'ελληνικά' when STRIP_LANG and LOWERCASE_LANG flags are enabled.",
        ),
        (
            LangStringFlag,
            "\fΕΛΛΗΝΙΚΆ\f",
            "ελληνικά",
            "Expected 'ελληνικά' when STRIP_LANG and LOWERCASE_LANG flags are enabled.",
        ),
    ],
)
def test_validate_flags_lang_whitespace_characters(
    flag_type: type[Enum], lang: Optional[str], expected: str, msg: str
) -> None:
    """Test validate_flags_lang with various whitespace characters.

    :param flag_type: The type of flag to use for validation.
    :type flag_type: type[Enum]
    :param lang: The language string to validate.
    :type lang: Optional[str]
    :param expected: The expected output.
    :type expected: str
    :param msg: Assertion message in case of failure.
    :type msg: str
    :raises AssertionError: If the transformation does not meet the expected outcome.
    """
    Controller.set_flag(flag_type.STRIP_LANG, True)
    Controller.set_flag(flag_type.LOWERCASE_LANG, True)
    assert FlagValidator.validate_flags_lang(flag_type, lang) == expected, msg


class MockFlag(Enum):
    STRIP_TEXT = 1
    DEFINED_TEXT = 2
    VALID_LANG = 3
    STRIP_LANG = 4
    LOWERCASE_LANG = 5
    DEFINED_LANG = 6


def test_validate_flags_lang_warns_if_langcodes_missing(monkeypatch):
    """Test FlagValidator.validate_flags_lang warns if 'langcodes' is missing."""

    def mock_get_flag(flag):
        if flag == MockFlag.VALID_LANG:
            return True
        return False

    def mock_import_langcodes(name, globals=None, locals=None, fromlist=(), level=0):
        if name == "langcodes":
            raise ImportError("No module named 'langcodes'")
        return original_import(name, globals, locals, fromlist, level)

    original_import = __import__
    monkeypatch.setattr(Controller, "get_flag", mock_get_flag)
    monkeypatch.setattr("builtins.__import__", mock_import_langcodes)

    with pytest.warns(
        UserWarning, match="Language validation skipped. VALID_LANG functionality requires the 'langcodes' library."
    ):
        FlagValidator.validate_flags_lang(MockFlag, "en")
