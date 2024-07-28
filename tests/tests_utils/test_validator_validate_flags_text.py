from enum import Enum
from typing import Any

import pytest
from langstring import Controller
from langstring import LangStringFlag
from langstring.utils.validators import FlagValidator


def test_validate_flags_text_strip_text_enabled() -> None:
    """Test validate_flags_text with STRIP_TEXT flag enabled.

    :raises AssertionError: If the transformation does not meet the expected outcome.
    """
    Controller.set_flag(LangStringFlag.STRIP_TEXT, True)
    text = "  sample text  "
    expected = "sample text"
    assert (
        FlagValidator.validate_flags_text(LangStringFlag, text) == expected
    ), "Expected text to be stripped of leading and trailing spaces."


def test_validate_flags_text_strip_text_disabled() -> None:
    """Test validate_flags_text with STRIP_TEXT flag disabled.

    :raises AssertionError: If the transformation does not meet the expected outcome.
    """
    Controller.set_flag(LangStringFlag.STRIP_TEXT, False)
    text = "  sample text  "
    expected = "  sample text  "
    assert (
        FlagValidator.validate_flags_text(LangStringFlag, text) == expected
    ), "Expected text to remain unchanged when STRIP_TEXT flag is disabled."


@pytest.mark.parametrize(
    "flag_type,text,msg",
    [
        (
            LangStringFlag,
            "   ",
            r"Invalid 'text' value received \('   '\)\. 'LangStringFlag\.DEFINED_TEXT' is enabled\. "
            r"Expected non-empty 'str' or 'str' with non-space characters\.",
        ),
        (
            LangStringFlag,
            "",
            r"Invalid 'text' value received \(''\)\. 'LangStringFlag\.DEFINED_TEXT' is enabled\. "
            r"Expected non-empty 'str' or 'str' with non-space characters\.",
        ),
        (
            LangStringFlag,
            "\n   \n",
            r"Invalid 'text' value received \('\n   \n'\)\. 'LangStringFlag\.DEFINED_TEXT' is enabled\. "
            r"Expected non-empty 'str' or 'str' with non-space characters\.",
        ),
        (
            LangStringFlag,
            "    ",
            r"Invalid 'text' value received \('    '\)\. 'LangStringFlag\.DEFINED_TEXT' is enabled\. "
            r"Expected non-empty 'str' or 'str' with non-space characters\.",
        ),
        (
            LangStringFlag,
            "\t",
            r"Invalid 'text' value received \('\t'\)\. 'LangStringFlag\.DEFINED_TEXT' is enabled\. "
            r"Expected non-empty 'str' or 'str' with non-space characters\.",
        ),
        (
            LangStringFlag,
            "\n\t ",
            r"Invalid 'text' value received \('\n\t '\)\. 'LangStringFlag\.DEFINED_TEXT' is enabled\. "
            r"Expected non-empty 'str' or 'str' with non-space characters\.",
        ),
    ],
)
def test_validate_flags_text_defined_text_invalid(flag_type: type[Enum], text: str, msg: str) -> None:
    """Test validate_flags_text raises ValueError when DEFINED_TEXT is enabled and text is invalid.

    :param flag_type: The type of flag to use for validation.
    :type flag_type: type[Enum]
    :param text: The text string to validate.
    :type text: str
    :param msg: Assertion message in case of failure.
    :type msg: str
    :raises ValueError: If DEFINED_TEXT is enabled and the text is invalid.
    """
    Controller.set_flag(flag_type.DEFINED_TEXT, True)
    with pytest.raises(ValueError, match=msg):
        FlagValidator.validate_flags_text(flag_type, text)


def test_validate_flags_text_defined_text_valid() -> None:
    """Test validate_flags_text with DEFINED_TEXT flag enabled and valid text.

    :raises AssertionError: If the transformation does not meet the expected outcome.
    """
    Controller.set_flag(LangStringFlag.DEFINED_TEXT, True)
    text = "valid text"
    assert (
        FlagValidator.validate_flags_text(LangStringFlag, text) == text
    ), "Expected valid text to remain unchanged when DEFINED_TEXT flag is enabled."


def test_validate_flags_text_optional_none() -> None:
    """Test validate_flags_text with text as None.

    :raises AssertionError: If the transformation does not meet the expected outcome.
    """
    Controller.set_flag(LangStringFlag.DEFINED_TEXT, False)  # Ensure DEFINED_TEXT is not enabled
    text = None
    assert FlagValidator.validate_flags_text(LangStringFlag, text) == "", "Expected None to return empty string."


def test_validate_flags_text_none_with_defined_text() -> None:
    """Test validate_flags_text raises ValueError when DEFINED_TEXT is enabled and text is None.

    :raises ValueError: If text is None when DEFINED_TEXT is enabled.
    """
    Controller.set_flag(LangStringFlag.DEFINED_TEXT, True)  # Enable DEFINED_TEXT
    text = None
    with pytest.raises(
        ValueError,
        match="Invalid 'text' value received \('None'\)\. 'LangStringFlag\.DEFINED_TEXT' is enabled\. Expected non-empty 'str' or 'str' with non-space characters\.",
    ):
        FlagValidator.validate_flags_text(LangStringFlag, text)


@pytest.mark.parametrize(
    "flag_type,text,expected,msg",
    [
        (
            LangStringFlag,
            "  Text with spaces  ",
            "Text with spaces",
            "Expected text to be stripped of leading and trailing spaces when STRIP_TEXT is enabled.",
        ),
        (
            LangStringFlag,
            "\nText with newline\n",
            "Text with newline",
            "Expected text to be stripped of leading and trailing newline when STRIP_TEXT is enabled.",
        ),
        (
            LangStringFlag,
            "  Mixed CASE text  ",
            "Mixed CASE text",
            "Expected text to be stripped of leading and trailing spaces when STRIP_TEXT is enabled.",
        ),
        (
            LangStringFlag,
            "Text with special characters!@# ",
            "Text with special characters!@#",
            "Expected text to be stripped of leading and trailing spaces when STRIP_TEXT is enabled.",
        ),
        (
            LangStringFlag,
            "Text with emoji 😊 ",
            "Text with emoji 😊",
            "Expected text to be stripped of leading and trailing spaces when STRIP_TEXT is enabled.",
        ),
        (
            LangStringFlag,
            "   ΕΛΛΗΝΙΚΆ   ",
            "ΕΛΛΗΝΙΚΆ",
            "Expected text to be stripped of leading and trailing spaces when STRIP_TEXT is enabled.",
        ),
        (
            LangStringFlag,
            "   РУССКИЙ   ",
            "РУССКИЙ",
            "Expected text to be stripped of leading and trailing spaces when STRIP_TEXT is enabled.",
        ),
    ],
)
def test_validate_flags_text_strip_text_various(flag_type: type[Enum], text: str, expected: str, msg: str) -> None:
    """Test validate_flags_text with STRIP_TEXT flag enabled for various text formats.

    :param flag_type: The type of flag to use for validation.
    :type flag_type: type[Enum]
    :param text: The text string to validate.
    :type text: str
    :param expected: The expected output.
    :type expected: str
    :param msg: Assertion message in case of failure.
    :type msg: str
    :raises AssertionError: If the transformation does not meet the expected outcome.
    """
    Controller.set_flag(flag_type.STRIP_TEXT, True)
    assert FlagValidator.validate_flags_text(flag_type, text) == expected, msg


@pytest.mark.parametrize(
    "flag_type,text,msg",
    [
        (
            LangStringFlag,
            123,
            r"Invalid argument with value '123'\. Expected 'str', but got 'int'\.",
        ),
        (
            LangStringFlag,
            ["list"],
            r"Invalid argument with value '\['list'\]'\. Expected 'str', but got 'list'\.",
        ),
        (
            LangStringFlag,
            {"set"},
            r"Invalid argument with value '\{'set'\}'\. Expected 'str', but got 'set'\.",
        ),
        (
            LangStringFlag,
            {"key": "value"},
            r"Invalid argument with value '\{'key': 'value'\}'\. Expected 'str', but got 'dict'\.",
        ),
    ],
)
def test_validate_flags_text_invalid_types(flag_type: type[Enum], text: Any, msg: str) -> None:
    """Test validate_flags_text raises TypeError when text is of invalid type.

    :param flag_type: The type of flag to use for validation.
    :type flag_type: type[Enum]
    :param text: The text to validate.
    :type text: Any
    :param msg: Assertion message in case of failure.
    :type msg: str
    :raises TypeError: If the text is of invalid type.
    """
    Controller.set_flag(flag_type.DEFINED_TEXT, True)
    with pytest.raises(TypeError, match=msg):
        FlagValidator.validate_flags_text(flag_type, text)


@pytest.mark.parametrize(
    "flag_type,text,expected,msg",
    [
        (
            LangStringFlag,
            "  text with spaces  ",
            "text with spaces",
            "Expected text to be stripped of leading and trailing spaces when STRIP_TEXT is enabled.",
        ),
        (
            LangStringFlag,
            "\ntext with newline\n",
            "text with newline",
            "Expected text to be stripped of leading and trailing newline when STRIP_TEXT is enabled.",
        ),
    ],
)
def test_validate_flags_text_strip_text_enabled(flag_type: type[Enum], text: str, expected: str, msg: str) -> None:
    """Test validate_flags_text with STRIP_TEXT flag enabled for various text formats.

    :param flag_type: The type of flag to use for validation.
    :type flag_type: type[Enum]
    :param text: The text to validate.
    :type text: str
    :param expected: The expected output.
    :type expected: str
    :param msg: Assertion message in case of failure.
    :type msg: str
    :raises AssertionError: If the transformation does not meet the expected outcome.
    """
    Controller.set_flag(flag_type.STRIP_TEXT, True)
    assert FlagValidator.validate_flags_text(flag_type, text) == expected, msg


def test_validate_flags_text_none_with_defined_text_enabled() -> None:
    """Test validate_flags_text raises ValueError when DEFINED_TEXT is enabled and text is None.

    :raises ValueError: If text is None when DEFINED_TEXT is enabled.
    """
    Controller.set_flag(LangStringFlag.DEFINED_TEXT, True)
    text = None
    with pytest.raises(
        ValueError,
        match=r"Invalid 'text' value received \('None'\)\. 'LangStringFlag\.DEFINED_TEXT' is enabled\. "
        r"Expected non-empty 'str' or 'str' with non-space characters\.",
    ):
        FlagValidator.validate_flags_text(LangStringFlag, text)


def test_validate_flags_text_strip_text_effects() -> None:
    """Test validate_flags_text with STRIP_TEXT flag to see its effects on text.

    :raises AssertionError: If the transformation does not meet the expected outcome.
    """
    Controller.set_flag(LangStringFlag.STRIP_TEXT, True)
    text = " text with spaces "
    expected = "text with spaces"
    assert (
        FlagValidator.validate_flags_text(LangStringFlag, text) == expected
    ), "Expected text to be stripped of spaces."


def test_validate_flags_text_defined_text_empty_string() -> None:
    """Test validate_flags_text raises ValueError when DEFINED_TEXT is enabled and text is an empty string.

    :raises ValueError: If text is an empty string when DEFINED_TEXT is enabled.
    """
    Controller.set_flag(LangStringFlag.DEFINED_TEXT, True)
    text = ""
    with pytest.raises(
        ValueError,
        match=r"Invalid 'text' value received \(''\)\. 'LangStringFlag\.DEFINED_TEXT' is enabled\. "
        r"Expected non-empty 'str' or 'str' with non-space characters\.",
    ):
        FlagValidator.validate_flags_text(LangStringFlag, text)
