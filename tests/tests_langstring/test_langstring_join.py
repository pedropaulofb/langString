from typing import Iterable

import pytest
from langstring import LangString


class JoinTestCase:
    def __init__(self, separator: str, iterable: Iterable[str], lang: str):
        self.separator = separator
        self.iterable = iterable
        self.lang = lang
        self.expected_output = separator.join(iterable)


join_test_cases = [
    JoinTestCase(" ", ["hello", "world"], "en"),  # Joining words with space
    JoinTestCase("-", ["2023", "01", "16"], "en"),  # Joining date parts
    JoinTestCase("", ["a", "b", "c"], "en"),  # Joining without separator
    JoinTestCase("\n", ["line1", "line2"], "en"),  # Joining lines with newline
    JoinTestCase(",", ["apple", "banana", "cherry"], "en"),  # Joining with comma
    JoinTestCase("😊", ["emoji", "test"], "en"),  # Joining with emoji
    JoinTestCase("separator", [], "en"),  # Joining empty iterable
    JoinTestCase("x", ["single"], "en"),  # Single element iterable
    JoinTestCase(" ", ["こんにちは", "世界"], "ja"),  # Unicode characters
    # Existing valid cases...
    JoinTestCase("-", ["hello", "world"], "en"),  # Joining with a string
    JoinTestCase("-", {"key1": "value1", "key2": "value2"}, "en"),  # Joining with a dictionary
    JoinTestCase("-", LangString("hello", "en"), "en"),  # Joining with a LangString object
    # Additional valid cases...
    JoinTestCase(" ", ["single"], "en"),  # Single element iterable
    JoinTestCase(",", ["1", "2", "3"], "en"),  # Numeric strings
    JoinTestCase("\n", ["Line 1", "Line 2"], "en"),  # Multiline strings
    JoinTestCase("", ["", "", ""], "en"),  # Empty strings
    # Default cases
    JoinTestCase("-", [], "en"),  # Joining with an empty list
    JoinTestCase("-", (), "en"),  # Joining with an empty tuple
    # Edge case with long strings
    JoinTestCase("-", ["a" * 10000, "b" * 10000], "en"),  # Very long strings
    # Unusual but valid cases
    JoinTestCase("-", ["    ", "   "], "en"),  # Strings with only whitespace
    JoinTestCase("-", ["", "", ""], "en"),  # Empty strings
]


@pytest.mark.parametrize("test_case", join_test_cases)
def test_join(test_case: JoinTestCase) -> None:
    separator_lang_string = LangString(test_case.separator, test_case.lang)
    result = separator_lang_string.join(test_case.iterable)
    assert isinstance(result, LangString), "Result should be a LangString instance"
    assert (
        result.text == test_case.expected_output
    ), f"join({test_case.iterable}) failed for separator '{test_case.separator}'"
    assert result.lang == test_case.lang, "Language tag should remain unchanged"


# Test cases for invalid iterable types
invalid_iterable_test_cases = [
    123,  # Integer
    1.5,  # Float
    True,  # Boolean
    complex(1, 2),  # Complex number
    (1, 2, 3),  # Tuple
    [1, 2, 3],  # List of integers
    slice(0, 5),  # Slice object
    ["hello", 123, "world"],  # Mixed string and integer
]


@pytest.mark.parametrize("invalid_iterable", invalid_iterable_test_cases)
def test_join_invalid_iterable(invalid_iterable: Iterable[str]) -> None:
    lang_string = LangString("-", "en")
    with pytest.raises(TypeError):
        lang_string.join(invalid_iterable)
