from typing import Any
import pytest
from langstring import LangString


class FormatMapTestCase:
    def __init__(self, input_string: str, mapping: Any, lang: str):
        self.input_string = input_string
        self.mapping = mapping
        self.lang = lang


# Valid cases for comparison
valid_format_map_test_cases = [
    FormatMapTestCase("Hello, {name}", {"name": "Alice"}, "en"),
    FormatMapTestCase("Value: {value}", {"value": 42}, "en"),
    FormatMapTestCase("Template string", {"key": [1, 2, 3]}, "en"),  # Non-primitive type as value
    FormatMapTestCase("Template string", {"not": {"allowed": "value"}}, "en"),  # Nested dictionary
    FormatMapTestCase("Template string", {complex(1, 2): "value"}, "en"),  # Complex number as key
    FormatMapTestCase("Template string", {"key": lambda x: x}, "en"),  # Function as value
]

# Invalid cases
invalid_format_map_test_cases = [
    FormatMapTestCase("Template string", [("key", "value")], "en"),  # List instead of dictionary
    FormatMapTestCase("Template string", 123, "en"),  # Integer instead of dictionary
]


@pytest.mark.parametrize("test_case", valid_format_map_test_cases)
def test_format_map_valid_cases(test_case: FormatMapTestCase):
    """
    Test the format_map method of LangString with valid cases.

    :param test_case: A test case instance containing input string, mapping, lang, and expected output.
    """
    lang_string = LangString(test_case.input_string, test_case.lang)
    result = lang_string.format_map(test_case.mapping)
    assert isinstance(result, LangString), "Result should be a LangString instance"
    expected_output = test_case.input_string.format_map(test_case.mapping)
    assert (
        result.text == expected_output
    ), f"Format_map method failed for input {test_case.input_string} with mapping {test_case.mapping}"
    assert result.lang == test_case.lang, "Language tag should remain unchanged"


@pytest.mark.parametrize("test_case", invalid_format_map_test_cases)
def test_format_map_invalid_cases(test_case: FormatMapTestCase):
    """
    Test the format_map method of LangString with invalid cases.

    :param test_case: A test case instance containing input string, mapping, lang, and expected output.
    """
    lang_string = LangString(test_case.input_string, test_case.lang)
    with pytest.raises(TypeError, match="Invalid argument|Invalid key in mapping|Invalid value in mapping"):
        lang_string.format_map(test_case.mapping)
