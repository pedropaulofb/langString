import pytest
from langstring import LangString


class StringMethodPartitionTestCase:
    def __init__(self, input_string, separator):
        self.input_string = input_string
        self.separator = separator

    def get_expected_output(self, method_name):
        method = getattr(self.input_string, method_name)
        return method(self.separator)


partition_test_cases = [
    StringMethodPartitionTestCase("hello world", " "),
    StringMethodPartitionTestCase("hello world", "o"),
    StringMethodPartitionTestCase("hello world", "x"),  # Separator not in string
    StringMethodPartitionTestCase("hello", " "),  # Non-available separator
    StringMethodPartitionTestCase("", " "),  # Empty string
    StringMethodPartitionTestCase("hello😊world", "😊"),
    StringMethodPartitionTestCase("special!characters!test", "!"),
    StringMethodPartitionTestCase("こんにちはworldこんにちは", "こんにちは"),
    StringMethodPartitionTestCase("xhello world", "x"),
    StringMethodPartitionTestCase("hello worldy", "y"),
    StringMethodPartitionTestCase("zhello worldz", "z"),
    StringMethodPartitionTestCase("hello world hello world", " "),
    StringMethodPartitionTestCase("repeat-repeat-repeat", "-"),
    StringMethodPartitionTestCase("abcabcabc", "abc"),
]


@pytest.mark.parametrize(
    "test_case, method", [(tc, m) for tc in partition_test_cases for m in ["partition", "rpartition"]]
)
def test_string_methods_partition(test_case, method):
    lang_string = LangString(test_case.input_string, "en")
    result = getattr(lang_string, method)(test_case.separator)
    assert isinstance(result, tuple), f"{method} should return a tuple"
    assert all(
        isinstance(part, LangString) and part.lang == "en" for part in result
    ), "All parts must be LangString with correct language"
    expected_output = test_case.get_expected_output(method)
    assert all(
        part.text == expected_part for part, expected_part in zip(result, expected_output)
    ), f"{method}({test_case.separator}) failed for '{test_case.input_string}'"


# Test cases for invalid argument types
invalid_arg_test_cases = [
    123,  # Integer
    12.34,  # Float
    [],  # List
    {},  # Dictionary
    True,  # Boolean
    None,  # NoneType
]


@pytest.mark.parametrize("invalid_arg", invalid_arg_test_cases)
@pytest.mark.parametrize("method", ["partition", "rpartition"])
def test_string_methods_partition_invalid_arg(invalid_arg, method):
    lang_string = LangString("hello", "en")
    expected_error_msg = f"must be str, not {type(invalid_arg).__name__}"
    with pytest.raises(TypeError, match=expected_error_msg):
        getattr(lang_string, method)(invalid_arg)


@pytest.mark.parametrize("method", ["partition", "rpartition"])
def test_string_methods_partition_empty_separator(method):
    lang_string = LangString("hello", "en")
    with pytest.raises(ValueError, match="empty separator"):
        getattr(lang_string, method)("")
