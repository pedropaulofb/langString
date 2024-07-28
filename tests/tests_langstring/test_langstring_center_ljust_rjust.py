import copy

import pytest
from langstring import LangString

methods_to_test = ["center", "ljust", "rjust"]


class StringMethodSingleArgTestCase:
    def __init__(self, input_string, method_arg, method_arg2=None):
        self.input_string = input_string
        self.method_arg = method_arg
        self.method_arg2 = method_arg2

    def get_expected_output(self, method_name):
        method = getattr(self.input_string, method_name)
        if self.method_arg2 is not None:
            return method(self.method_arg, self.method_arg2)
        return method(self.method_arg)


# Test cases for methods with one or two arguments
test_cases = [
    StringMethodSingleArgTestCase("hello", 10),
    StringMethodSingleArgTestCase("world", 8, "*"),
    StringMethodSingleArgTestCase("text", 5, " "),
    StringMethodSingleArgTestCase("python", 10, "-"),
    StringMethodSingleArgTestCase("", 5, "*"),
    StringMethodSingleArgTestCase("short", 20, "="),  # Longer width with fill character
    StringMethodSingleArgTestCase("longer text example", 10),  # Width shorter than text
    StringMethodSingleArgTestCase("boundary", 8, "-"),  # Width equal to text length
    StringMethodSingleArgTestCase("multi\nline\ntext", 15),  # Multi-line text
    StringMethodSingleArgTestCase("🌟star🌟", 10, "✨"),  # Unicode characters and fill
    StringMethodSingleArgTestCase("12345", 10, "0"),  # Numeric string with fill
    StringMethodSingleArgTestCase("    spaced    ", 20, "."),  # Text with leading/trailing spaces
    StringMethodSingleArgTestCase("edge-case", 0),  # Zero width
    StringMethodSingleArgTestCase("emptyfill", 10, None),  # Empty string as fill character
    StringMethodSingleArgTestCase("no-fill", 10),  # No fill character provided
    StringMethodSingleArgTestCase("hello", -10, "*"),  # Negative width
    StringMethodSingleArgTestCase("world", True, "*"),  # Boolean True as width
    StringMethodSingleArgTestCase("text", 10, None),  # None as fill character
    StringMethodSingleArgTestCase("python", 10, None),  # Empty string as fill character
]


@pytest.mark.parametrize("test_case, method", [(tc, m) for tc in test_cases for m in methods_to_test])
def test_string_methods_single_arg(test_case, method):
    lang_string = LangString(test_case.input_string, "en")
    lang_string_before = copy.deepcopy(lang_string)
    expected_output = test_case.get_expected_output(method)
    if test_case.method_arg2 is not None:
        result = getattr(lang_string, method)(test_case.method_arg, test_case.method_arg2)
    else:
        result = getattr(lang_string, method)(test_case.method_arg)
    assert (
        result.text == expected_output
    ), f"{method}({test_case.method_arg}, {test_case.method_arg2}) failed for '{test_case.input_string}'"
    assert lang_string_before == lang_string, "The original LangString cannot be modified by the called method."


# Test cases for invalid argument types
invalid_arg_test_cases = [
    ("str", " "),  # String as first arg
    ([], " "),  # List as first arg
    ({}, " "),  # Dictionary as first arg
    (3.14, " "),  # Float as first arg
    (None, " "),  # None as first arg
    (10, 5),  # Integer as second arg
    (10, []),  # List as second arg
    (10, {}),  # Dictionary as second arg
    (10, 3.14),  # Float as second arg
    (10, "xx"),  # More than one character as second arg
    (10, "😊😊"),  # Unicode characters as second arg
    # ... other invalid cases ...
]


@pytest.mark.parametrize("invalid_arg1, invalid_arg2", invalid_arg_test_cases)
@pytest.mark.parametrize("method", methods_to_test)
def test_string_methods_invalid_args(invalid_arg1, invalid_arg2, method):
    lang_string = LangString("hello", "en")
    with pytest.raises(TypeError):
        if invalid_arg2 is not None:
            getattr(lang_string, method)(invalid_arg1, invalid_arg2)
        else:
            getattr(lang_string, method)(invalid_arg1)


@pytest.mark.parametrize("method", methods_to_test)
@pytest.mark.parametrize("invalid_fillchar", ["", "  ", "xx", "😊😊", "ab"])
def test_string_methods_invalid_fillchar(method, invalid_fillchar):
    lang_string = LangString("hello", "en")
    with pytest.raises(TypeError, match="The fill character must be exactly one character long"):
        getattr(lang_string, method)(10, invalid_fillchar)


@pytest.mark.parametrize("method", methods_to_test)
@pytest.mark.parametrize("invalid_fillchar", [123, None, True, ["*"], {"*": 1}])
def test_invalid_fillchar_types(method, invalid_fillchar):
    lang_string = LangString("hello", "en")
    with pytest.raises(TypeError, match="The fill character must be a unicode character, not"):
        getattr(lang_string, method)(10, invalid_fillchar)
