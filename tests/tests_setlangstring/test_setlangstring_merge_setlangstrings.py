import pytest
from langstring import SetLangString
from tests.conftest import TYPEERROR_MSG_SINGULAR


@pytest.mark.parametrize(
    "input_data, expected_output",
    [
        ([SetLangString({"a", "b"}, "EN"), SetLangString({"c"}, "en")], [SetLangString({"a", "b", "c"}, "en")]),
        (
            [SetLangString({"x"}, "FR"), SetLangString({"y"}, "fr"), SetLangString({"z"}, "FR")],
            [SetLangString({"x", "y", "z"}, "fr")],
        ),
        ([SetLangString({"hello"}, "en"), SetLangString({"hello"}, "en")], [SetLangString({"hello"}, "en")]),
        ([SetLangString({"hello"}, "EN"), SetLangString({"hello"}, "EN")], [SetLangString({"hello"}, "EN")]),
        ([SetLangString({"hello"}, "En"), SetLangString({"hello"}, "EN")], [SetLangString({"hello"}, "en")]),
        ([SetLangString({"hello"}, "en"), SetLangString({"world"}, "en")], [SetLangString({"hello", "world"}, "en")]),
        ([SetLangString({"hello"}, "En"), SetLangString({"world"}, "EN")], [SetLangString({"hello", "world"}, "en")]),
        ([SetLangString({"hello"}, "EN"), SetLangString({"world"}, "EN")], [SetLangString({"hello", "world"}, "EN")]),
        (
            [SetLangString({"hello"}, "EN"), SetLangString({"world"}, "EN"), SetLangString({"test"}, "EN")],
            [SetLangString({"hello", "world", "test"}, "EN")],
        ),
        (
            [SetLangString({"hello"}, "eN"), SetLangString({"world"}, "EN"), SetLangString({"test"}, "EN")],
            [SetLangString({"hello", "world", "test"}, "en")],
        ),
        (
            [SetLangString({"data"}, "de"), SetLangString({"science"}, "DE"), SetLangString({"rocks"}, "de")],
            [SetLangString({"data", "science", "rocks"}, "de")],
        ),
        ([SetLangString(set(), "en")], [SetLangString(set(), "en")]),  # Testing with empty set
        ([SetLangString({" Καλημέρα"}, "en")], [SetLangString({" Καλημέρα"}, "en")]),  # Spaces before, Greek characters
        (
            [SetLangString({"🚀"}, "emoji"), SetLangString({"🌟"}, "emoji")],
            [SetLangString({"🚀", "🌟"}, "emoji")],
        ),  # Emojis
        (
            [SetLangString({"data"}, " DE "), SetLangString({"science"}, " de ")],
            [SetLangString({"data", "science"}, " de ")],
        ),
        (
            [SetLangString({"Привет"}, "ru"), SetLangString({"Мир"}, "RU")],
            [SetLangString({"Привет", "Мир"}, "ru")],
        ),  # Cyrillic
        (
            [SetLangString({"!@#$%^&*()"}, "spec"), SetLangString({"{}[]:;\"'<>?,./"}, "spec")],
            [SetLangString({"!@#$%^&*()", "{}[]:;\"'<>?,./"}, "spec")],
        ),  # Special chars
        (
            [SetLangString({"hello"}, ""), SetLangString({"world"}, "")],
            [SetLangString({"hello", "world"}, "")],
        ),  # Empty lang value
        # Additional test cases to add to the "input_data, expected_output" parametrization in test_merge_setlangstrings_success
        (
            [SetLangString({"こんにちは"}, "ja"), SetLangString({"さようなら"}, "ja")],
            [SetLangString({"こんにちは", "さようなら"}, "ja")],
        ),  # Japanese characters
        (
            [
                SetLangString({"hello"}, "en"),
                SetLangString({"goodbye"}, "EN"),
                SetLangString({"hello", "goodbye"}, "En"),
            ],
            [SetLangString({"hello", "goodbye"}, "en")],
        ),  # Duplicate content with different cases
        (
            [SetLangString({" "}, "whitespace"), SetLangString({" "}, "whitespace")],
            [SetLangString({" "}, "whitespace")],
        ),  # Whitespace content
        (
            [SetLangString({"mixedCASE"}, "en"), SetLangString({"MIXEDcase"}, "EN")],
            [SetLangString({"mixedCASE", "MIXEDcase"}, "en")],
        ),  # Mixed case content
        (
            [SetLangString({"123"}, "num"), SetLangString({"456"}, "num"), SetLangString({"789"}, "NUM")],
            [SetLangString({"123", "456", "789"}, "num")],
        ),  # Numeric content
        (
            [SetLangString({"", ""}, "empty"), SetLangString({"", ""}, "empty")],
            [SetLangString({"", ""}, "empty")],
        ),  # Empty string content and lang
    ],
)
def test_merge_setlangstrings_success(input_data, expected_output):
    """Test `merge_setlangstrings` successfully merges SetLangStrings with different or same case language tags.

    :param input_data: List of SetLangString instances to be merged.
    :param expected_output: Expected list of SetLangString instances after merge.
    :type input_data: List[SetLangString]
    :type expected_output: List[SetLangString]
    :return: Asserts if the output from merge_setlangstrings matches the expected output.
    """
    result = SetLangString.merge_setlangstrings(input_data)
    assert result == expected_output, "Expected merged SetLangString instances did not match actual result."


@pytest.mark.parametrize(
    "invalid_input",
    [
        ([{"a", "b"}, "EN"]),  # Incorrect type, not SetLangString instance
        ("Not a list",),
        ([SetLangString({"a"}, "en"), "Random String"]),  # Mixed with incorrect type
    ],
)
def test_merge_setlangstrings_type_error(invalid_input):
    """Test `merge_setlangstrings` raises TypeError with invalid input types.

    :param invalid_input: Invalid input to trigger TypeError.
    :type invalid_input: Any
    :raises TypeError: If input to merge_setlangstrings is not a list of SetLangString instances.
    """
    with pytest.raises(TypeError, match=TYPEERROR_MSG_SINGULAR):
        SetLangString.merge_setlangstrings(invalid_input)


def test_merge_setlangstrings_empty_input():
    """Test `merge_setlangstrings` with an empty list input returns an empty list.

    :return: Asserts if the output from merge_setlangstrings is an empty list when given an empty list.
    """
    result = SetLangString.merge_setlangstrings([])
    assert result == [], "Expected empty list as output when merging an empty input list."


def test_merge_setlangstrings_with_itself():
    """Test merging SetLangString instances with themselves to check idempotency."""
    sls = SetLangString({"a"}, "EN")
    result = SetLangString.merge_setlangstrings([sls, sls])
    assert result == [sls], "Merging with itself should be idempotent."


@pytest.mark.parametrize(
    "input_data",
    [
        (None),
        ([None]),
    ],
)
def test_merge_setlangstrings_null_input(input_data):
    """Test merge_setlangstrings handling of null inputs."""
    with pytest.raises(TypeError, match=TYPEERROR_MSG_SINGULAR):
        SetLangString.merge_setlangstrings(input_data)
