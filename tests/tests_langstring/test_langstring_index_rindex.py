import pytest
from langstring import LangString

index_methods_to_test = ["index", "rindex"]


class StringMethodFindIndexTestCase:
    def __init__(self, input_string, sub, start=0, end=None):
        self.input_string = input_string
        self.sub = sub
        self.start = start
        self.end = end

    def get_expected_output(self, method_name):
        method = getattr(self.input_string, method_name)
        return method(self.sub, self.start, self.end)


index_rindex_test_cases = [
    # Basic cases (similar to find and rfind)
    StringMethodFindIndexTestCase("hello world", "world"),
    StringMethodFindIndexTestCase("hello world", "hello"),
    StringMethodFindIndexTestCase("hello world", "o", 4),
    StringMethodFindIndexTestCase("hello world", "o", 0, 5),
    StringMethodFindIndexTestCase("repeat repeat repeat", "repeat", 7),
    StringMethodFindIndexTestCase("unicode 😊 test", "😊"),
    StringMethodFindIndexTestCase("case-sensitive", "Case"),
    # ValueError scenarios
    StringMethodFindIndexTestCase("hello world", "notfound"),
    StringMethodFindIndexTestCase("hello world", "world", 0, 5),
    # Edge cases
    StringMethodFindIndexTestCase("", "", 0, -1),
    StringMethodFindIndexTestCase("   ", " ", 0, -1),
    StringMethodFindIndexTestCase("hello", "o", 5, 3),
    StringMethodFindIndexTestCase("hello", "hello", 100, 200),
    StringMethodFindIndexTestCase("hello world", "lo wo", 0, -1),
    StringMethodFindIndexTestCase("special characters !@#", "!@", 0, -1),
    StringMethodFindIndexTestCase("hello", "", 0, -1),  # Empty substring
    StringMethodFindIndexTestCase("hello", " ", 0, -1),  # Substring is a space
    StringMethodFindIndexTestCase("hello", "l", 3, 4),  # Narrow range
    StringMethodFindIndexTestCase("hello", "l", -1, 2),  # Invalid range
    StringMethodFindIndexTestCase("hello", "l", 10, 20),  # Range outside the string
    # Edge cases for find, rfind, index, rindex
    StringMethodFindIndexTestCase("a", "a", 0, -1),  # Single character string
    StringMethodFindIndexTestCase(" ", " ", 0, -1),  # Space as string and substring
    StringMethodFindIndexTestCase("hello", "hello world", 0, -1),  # Substring longer than string
    StringMethodFindIndexTestCase("hello", "e", -2, -1),  # Negative indices
    StringMethodFindIndexTestCase("hello", "e", -20, 20),  # Large negative and positive indices
    StringMethodFindIndexTestCase("hello", "e", 1, 1),  # Start and end are the same
    StringMethodFindIndexTestCase("hello", "e", 2, 1),  # Start is greater than end
    StringMethodFindIndexTestCase("hello", "l", 3, 5),  # Substring at the end of the range
    StringMethodFindIndexTestCase("hello", "h", 0, 1),  # Substring at the start of the range
    StringMethodFindIndexTestCase("😊😊😊", "😊", 0, -1),  # Repeated unicode characters
    StringMethodFindIndexTestCase("😊😊😊", "😊", 1, 2),  # Unicode character in a specific range
    StringMethodFindIndexTestCase("", "", 0, -1),  # Empty string and empty 'sub'
    StringMethodFindIndexTestCase("hello", "hello", 0, 0),  # 'start' and 'end' at the same position
    StringMethodFindIndexTestCase("hello", "o", 5, 3),  # 'start' greater than 'end'
    StringMethodFindIndexTestCase("hello", "hello", 100, 200),  # Very large 'start' and 'end'
    StringMethodFindIndexTestCase("hello world", "lo wo", 0, -1),  # Multi-character substring
    StringMethodFindIndexTestCase("hello 😊 world", "😊", 0, -1),  # Unicode character as substring
    StringMethodFindIndexTestCase("hello world", "world", None, None),  # None for both start and end
    StringMethodFindIndexTestCase("hello world", "hello", 0, None),  # None for end
    StringMethodFindIndexTestCase("hello world", "world", None, 5),  # None for start
    StringMethodFindIndexTestCase("repeat repeat repeat", "repeat", None, 10),  # None for start, specific end
    StringMethodFindIndexTestCase("unicode 😊 test", "😊", 8, None),  # Specific start, None for end]
]


@pytest.mark.parametrize(
    "test_case, method", [(tc, m) for tc in index_rindex_test_cases for m in index_methods_to_test]
)
def test_string_methods_index_rindex(test_case, method):
    lang_string = LangString(test_case.input_string, "en")
    if test_case.get_expected_output("find") == -1:
        with pytest.raises(ValueError):
            getattr(lang_string, method)(test_case.sub, test_case.start, test_case.end)
    else:
        expected_output = test_case.get_expected_output(method)
        result = getattr(lang_string, method)(test_case.sub, test_case.start, test_case.end)
        assert (
            result == expected_output
        ), f"{method}('{test_case.sub}', {test_case.start}, {test_case.end}) failed for '{test_case.input_string}'"


# Additional test cases for invalid types
invalid_type_test_cases = [
    (123, 0, -1),  # Non-string 'sub'
    ("hello", "start", -1),  # Non-integer 'start'
    ("hello", 0, "end"),  # Non-integer 'end'
    (123, 0, 5),  # Integer as 'sub'
    (True, 0, 5),  # Boolean as 'sub'
    ([], 0, 5),  # List as 'sub'
    ({}, 0, 5),  # Dictionary as 'sub'
    ("hello", "start", 5),  # Non-integer 'start'
    ("hello", 0, "end"),  # Non-integer 'end'
    ("hello", 3.14, 5),  # Float as 'start'
    ("hello", 0, 3.14),  # Float as 'end'
    ("hello", [1], 5),  # List as 'start'
    ("hello", 0, [1]),  # List as 'end'
    ("hello", {}, 5),  # Dictionary as 'start'
    ("hello", 0, {}),  # Dictionary as 'end'
]


@pytest.mark.parametrize("sub, start, end", invalid_type_test_cases)
@pytest.mark.parametrize("method", index_methods_to_test)
def test_string_methods_invalid_types(sub, start, end, method):
    lang_string = LangString("hello world", "en")
    with pytest.raises(TypeError):
        getattr(lang_string, method)(sub, start, end)
