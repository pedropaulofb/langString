from typing import Union

import pytest
from langstring import LangString


class GetItemTestCase:
    def __init__(self, input_string, key):
        self.input_string = input_string
        self.key = key
        self.expected_output = self.compute_expected_output()

    def compute_expected_output(self):
        try:
            return self.input_string[self.key]
        except IndexError:
            return IndexError


getitem_test_cases = [
    GetItemTestCase("hello", 1),  # Single character access
    GetItemTestCase("hello", slice(1, 4)),  # Slicing
    GetItemTestCase("hello", slice(None, None, -1)),  # Reverse string
    GetItemTestCase("こんにちは", 2),  # Unicode character access
    GetItemTestCase("😊😊😊", slice(1, 3)),  # Emoji slicing
    GetItemTestCase("hello", -1),  # Negative index
    GetItemTestCase("hello", slice(-4, -1)),  # Negative slicing
    GetItemTestCase("hello", slice(1, 100)),  # Out of range slice end
    GetItemTestCase("hello", slice(-100, 2)),  # Out of range slice start
    GetItemTestCase("hello", slice(2, 2)),  # Slice with no characters
    GetItemTestCase("hello", slice(1, 4, 2)),  # Slicing with step
    GetItemTestCase("hello", slice(None, None, 2)),  # Slicing with positive step
    GetItemTestCase("hello", slice(None, None, -2)),  # Slicing with negative step
    GetItemTestCase("hello", 100),  # Index out of range
    GetItemTestCase("hello", -100),  # Negative index out of range
    GetItemTestCase("hello", 0),  # First character
    GetItemTestCase("hello", -1),  # Last character
    GetItemTestCase("hello", slice(0, 5, 2)),  # Step size 2
    GetItemTestCase("hello", slice(0, 5, -1)),  # Negative step
    GetItemTestCase("hello", slice(2, 2)),  # Same start and end index
    GetItemTestCase("hello", slice(10, 15)),  # Slice beyond string length
    GetItemTestCase("hello", slice(-15, -10)),  # Negative slice beyond string length
    GetItemTestCase("a" * 1000, 999),  # Very long string
    GetItemTestCase("a", 0),  # Single character string
    GetItemTestCase("hello", slice(1, 1)),  # Empty result slice
]


@pytest.mark.parametrize("test_case", getitem_test_cases)
def test_getitem(test_case: GetItemTestCase) -> None:
    lang_string = LangString(test_case.input_string, "en")
    if test_case.expected_output is IndexError:
        with pytest.raises(IndexError):
            lang_string[test_case.key]
    else:
        result = lang_string[test_case.key]
        assert isinstance(result, LangString), "Result should be a LangString instance"
        assert (
            result.text == test_case.expected_output
        ), f"__getitem__({test_case.key}) failed for '{test_case.input_string}'"
        assert result.lang == "en", "Language tag should remain unchanged"


# Test cases for invalid key types
invalid_key_test_cases = [
    "string",  # String key
    None,  # None key
    1.5,  # Float key
    [],  # List key
    {},  # Dictionary key
    complex(1, 2),  # Complex number
    (1, 2),  # Tuple
    slice("a", "b"),  # Non-integer slice indices
    slice(1, 5, "a"),  # Non-integer slice step
    slice(1.5, 3.5),  # Float slice indices
]


@pytest.mark.parametrize("invalid_key", invalid_key_test_cases)
def test_getitem_invalid_key(invalid_key: Union[int, slice]) -> None:
    lang_string = LangString("hello", "en")
    with pytest.raises(TypeError):
        lang_string[invalid_key]
