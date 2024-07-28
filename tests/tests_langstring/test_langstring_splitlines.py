import pytest
from langstring import LangString
from tests.conftest import TYPEERROR_MSG_SINGULAR


class SplitLinesTestCase:
    def __init__(self, input_string: str, keepends: bool) -> None:
        self.input_string = input_string
        self.keepends = keepends
        self.expected_output = input_string.splitlines(keepends)


splitlines_test_cases = [
    SplitLinesTestCase("Hello\nWorld", False),
    SplitLinesTestCase("Hello\nWorld", True),
    SplitLinesTestCase("One\nTwo\nThree", False),
    SplitLinesTestCase("One\nTwo\nThree", True),
    SplitLinesTestCase("No newline", False),
    SplitLinesTestCase("", False),
    SplitLinesTestCase("Line with \n newline", False),
    SplitLinesTestCase("Multiple\n\nNewlines", False),
    SplitLinesTestCase("Ends with newline\n", False),
    SplitLinesTestCase("Ends with newline\n", True),
    SplitLinesTestCase("\nStarts with newline", False),
    SplitLinesTestCase("Unicode\nこんにちは", False),
    SplitLinesTestCase("Emoji 😊\nNewline", False),
    SplitLinesTestCase("\n\n", False),  # Only newlines
    SplitLinesTestCase("\nStarts and ends\n", False),
    SplitLinesTestCase("Mixed\r\nNewlines\nHere", False),
    SplitLinesTestCase("Multiple\n\nNewlines\n\n", False),
]


@pytest.mark.parametrize("test_case", splitlines_test_cases)
def test_splitlines(test_case: SplitLinesTestCase) -> None:
    """
    Test the splitlines method of LangString.

    :param test_case: A test case instance containing input string, keepends flag, and expected output.
    """
    lang_string = LangString(test_case.input_string, "en")
    result = lang_string.splitlines(test_case.keepends)
    assert isinstance(result, list), "Result should be a list"
    assert all(isinstance(item, LangString) for item in result), "All items in result should be LangString instances"
    assert [
        item.text for item in result
    ] == test_case.expected_output, f"splitlines({test_case.keepends}) failed for '{test_case.input_string}'"


# Additional test cases for splitlines method
additional_splitlines_test_cases = [
    SplitLinesTestCase("\n\n", False),  # Only newlines
    SplitLinesTestCase("\nStarts and ends\n", False),
    SplitLinesTestCase("Mixed\r\nNewlines\nHere", False),
    SplitLinesTestCase("Multiple\n\nNewlines\n\n", False),
]


@pytest.mark.parametrize("test_case", additional_splitlines_test_cases)
def test_additional_splitlines(test_case: SplitLinesTestCase) -> None:
    lang_string = LangString(test_case.input_string, "en")
    result = lang_string.splitlines(test_case.keepends)
    assert [
        item.text for item in result
    ] == test_case.expected_output, f"splitlines({test_case.keepends}) failed for '{test_case.input_string}'"


# Test cases with invalid keepends values
invalid_keepends_test_cases = [
    ("Hello\nWorld", 123),
    ("Hello\nWorld", "string"),
    ("Hello\nWorld", None),
    ("Hello\nWorld", []),
    ("Hello\nWorld", {}),
]


@pytest.mark.parametrize("input_string, keepends", invalid_keepends_test_cases)
def test_splitlines_invalid_keepends(input_string: str, keepends: any) -> None:
    """
    Test the splitlines method of LangString with invalid keepends values.

    :param input_string: The input string to split.
    :param keepends: The invalid keepends value to test.
    """
    lang_string = LangString(input_string, "en")
    with pytest.raises(TypeError, match=TYPEERROR_MSG_SINGULAR):
        lang_string.splitlines(keepends)
