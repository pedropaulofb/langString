import pytest
from langstring import LangString


class ReplaceTestCase:
    def __init__(self, input_string, old, new, count):
        self.input_string = input_string
        self.old = old
        self.new = new
        self.count = count
        self.expected_output = input_string.replace(old, new, count)


replace_test_cases = [
    ReplaceTestCase("hello world", "world", "universe", -1),
    ReplaceTestCase("hello hello", "hello", "hi", 1),
    ReplaceTestCase("hello", "l", "L", -1),
    ReplaceTestCase("hello", "x", "X", -1),  # 'old' not in string
    ReplaceTestCase("", "a", "b", -1),  # Empty string
    ReplaceTestCase("hello", "", "-", -1),  # Empty 'old'
    ReplaceTestCase("hello", "o", "", -1),  # Empty 'new'
    ReplaceTestCase("hello", "o", "O", 0),  # Count is 0
    ReplaceTestCase("hello world world", "world", "universe", 1),
    ReplaceTestCase("こんにちは", "に", "ニ", -1),  # Unicode characters
    ReplaceTestCase("😊😊😊", "😊", "🙂", 2),  # Emojis
    ReplaceTestCase("banana", "na", "NA", -1),
    ReplaceTestCase("123123", "123", "321", -1),
    ReplaceTestCase("hello", "l", "l", -1),
    ReplaceTestCase("short", "sh", "longerPrefix", -1),
    ReplaceTestCase("repeat repeat repeat", "repeat", "word", 2),
    ReplaceTestCase("overlapping", "app", "APP", -1),
    ReplaceTestCase("negative count", "e", "E", -5),
    ReplaceTestCase("an old string", "old", "new", True),
    ReplaceTestCase("an old string", "old", "new", False),
]


@pytest.mark.parametrize("test_case", replace_test_cases)
def test_replace(test_case: ReplaceTestCase) -> None:
    """
    Test the replace method of LangString.
    """
    lang_string = LangString(test_case.input_string, "en")
    result = lang_string.replace(test_case.old, test_case.new, test_case.count)
    assert isinstance(result, LangString), "Result should be a LangString instance"
    assert (
        result.text == test_case.expected_output
    ), f"replace('{test_case.old}', '{test_case.new}', {test_case.count}) failed for '{test_case.input_string}'"
    assert result.lang == "en", "Language tag should remain unchanged"


# Test cases for invalid argument types
invalid_arg_test_cases = [
    # Non-string 'old'
    (123, "new", -1),
    (True, "new", -1),
    ([], "new", -1),
    ({}, "new", -1),
    (None, "new", -1),
    # Non-string 'new'
    ("old", 123, -1),
    ("old", False, -1),
    ("old", [], -1),
    ("old", {}, -1),
    ("old", None, -1),
    # Non-integer 'count'
    ("old", "new", "count"),
    ("old", "new", 1.5),
    ("old", "new", []),
    ("old", "new", {}),
    ("old", "new", None),
    # Combining invalid 'old', 'new', and 'count'
    (123, 456, "count"),
    (True, None, []),
    ([], {}, 1.5),
]


@pytest.mark.parametrize("old, new, count", invalid_arg_test_cases)
def test_replace_invalid_args(old, new, count):
    lang_string = LangString("hello", "en")
    with pytest.raises(TypeError):
        lang_string.replace(old, new, count)
