import copy

import pytest
from langstring import LangString

split_methods_to_test = ["split", "rsplit"]


class StringMethodSplitTestCase:
    def __init__(self, input_string, sep=None, maxsplit=-1):
        self.input_string = input_string
        self.sep = sep
        self.maxsplit = maxsplit

    def get_expected_output(self, method_name):
        method = getattr(self.input_string, method_name)
        return method(self.sep, self.maxsplit)


split_test_cases = [
    StringMethodSplitTestCase("1,2,3", ",", -1),
    StringMethodSplitTestCase("1 2 3", None, -1),
    StringMethodSplitTestCase("1,2,3", ",", -2),
    StringMethodSplitTestCase("1 2 3", None, -2),
    StringMethodSplitTestCase("1,2,3", ",", -5),
    StringMethodSplitTestCase("1 2 3", None, -5),
    StringMethodSplitTestCase("1,2,,3,", ",", -1),
    StringMethodSplitTestCase("   1   2   3   ", None, -1),
    StringMethodSplitTestCase("1<>2<>3", "<>", -1),
    StringMethodSplitTestCase("hello world", " ", 1),
    StringMethodSplitTestCase("hello world", " ", 0),
    StringMethodSplitTestCase("hello", " ", -1),
    StringMethodSplitTestCase("", ",", -1),  # Edge case: empty input string
    StringMethodSplitTestCase("   \t\n  ", None, -1),  # Only whitespace
    StringMethodSplitTestCase(",start", ",", -1),  # Separator at start
    StringMethodSplitTestCase("end,", ",", -1),  # Separator at end
    StringMethodSplitTestCase("Mixed \t\n Whitespace", None, -1),  # Mixed whitespace
    StringMethodSplitTestCase("No separator here", ",", -1),  # No separator
    StringMethodSplitTestCase("\nNew\nLine\nSeparator", "\n", -1),  # Newline separator
    StringMethodSplitTestCase("Multiple,,,Consecutive,,", ",", 2),  # Multiple consecutive separators
    # Edge cases
    StringMethodSplitTestCase("   ", None, -1),  # Only spaces
    StringMethodSplitTestCase("a b c d e", None, 2),  # Split with default separator and limited splits
    StringMethodSplitTestCase("1,2,,3,,", ",", 2),  # Consecutive separators
    StringMethodSplitTestCase("1,,2,,3", ",", -1),  # Empty strings due to consecutive separators
    StringMethodSplitTestCase("1<>2<>3<>", "<>", -1),  # Separator at the end
    StringMethodSplitTestCase("1<>2<>3<>", "<>", 1),  # Maxsplit with separator at the end
    StringMethodSplitTestCase("1<>2<>3<>", "<>", 0),  # No split
    StringMethodSplitTestCase("hello", None, -1),  # No separator provided
    StringMethodSplitTestCase("hello", " ", -1),  # Empty separator (should raise an error)
    # Unusual, but valid usage
    StringMethodSplitTestCase("1 2 3 4 5", " ", 3),  # Valid separator with limited splits
    StringMethodSplitTestCase("1,2,3,4,5", ",", 100),  # Maxsplit larger than possible splits
    StringMethodSplitTestCase("word", "word", -1),  # Separator is the entire string
    StringMethodSplitTestCase("word", "o", -1),  # Single character separator
    StringMethodSplitTestCase("😊Start😊Middle😊End😊", "😊", -1),  # Unicode character as separator
    # Testing default maxsplit (-1)
    StringMethodSplitTestCase("1,2,3", ","),  # Default maxsplit
    StringMethodSplitTestCase("1 2 3", None),  # Default maxsplit with None separator
    StringMethodSplitTestCase("1,2,,3,", ","),  # Default maxsplit with consecutive separators
    StringMethodSplitTestCase("hello world", " "),  # Default maxsplit with space separator
    StringMethodSplitTestCase("multi\nline\ntext", "\n"),  # Default maxsplit with newline separator
    StringMethodSplitTestCase("1<>2<>3", "<>"),  # Default maxsplit with multi-character separator
    StringMethodSplitTestCase("no-separator", "x"),  # Default maxsplit with no occurrences of separator
]


@pytest.mark.parametrize("test_case, method", [(tc, m) for tc in split_test_cases for m in split_methods_to_test])
def test_string_methods_split(test_case, method):
    lang_string = LangString(test_case.input_string, "en")
    lang_string_before = copy.deepcopy(lang_string)
    expected_output = [LangString(part, "en") for part in test_case.get_expected_output(method)]
    result = getattr(lang_string, method)(test_case.sep, test_case.maxsplit)
    assert (
        result == expected_output
    ), f"{method}('{test_case.sep}', {test_case.maxsplit}) failed for '{test_case.input_string}'"
    assert lang_string_before == lang_string, "The original LangString should not be modified by the method."


invalid_split_arg_test_cases = [
    # Invalid separator types
    (123, -1),  # Integer as separator
    (True, -1),  # Boolean as separator
    ([], -1),  # List as separator
    ({}, -1),  # Dictionary as separator
    # Invalid maxsplit types
    (None, "str"),  # String as maxsplit
    (None, 3.14),  # Float as maxsplit
    (None, []),  # List as maxsplit
    (None, {}),  # Dictionary as maxsplit
    (" ", "multi-char"),  # Multi-character string as maxsplit
    (5, -1),  # Non-string, non-None separator
]


@pytest.mark.parametrize("invalid_sep, invalid_maxsplit", invalid_split_arg_test_cases)
@pytest.mark.parametrize("method", split_methods_to_test)
def test_string_methods_split_invalid_args(invalid_sep, invalid_maxsplit, method):
    lang_string = LangString("hello world", "en")
    with pytest.raises(TypeError):
        getattr(lang_string, method)(invalid_sep, invalid_maxsplit)


@pytest.mark.parametrize("method", split_methods_to_test)
def test_string_methods_split_empty_separator(method):
    lang_string = LangString("hello world", "en")
    with pytest.raises(ValueError, match="empty separator"):
        getattr(lang_string, method)("", -1)
