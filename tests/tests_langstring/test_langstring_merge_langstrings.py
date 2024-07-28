import pytest
from langstring import LangString
from tests.conftest import TYPEERROR_MSG_SINGULAR


@pytest.mark.parametrize(
    "input_data, expected_output",
    [
        # Adjusted test cases for individual strings instead of sets
        ([LangString("a", "EN"), LangString("a", "en")], [LangString("a", "en")]),
        ([LangString("a", "EN"), LangString("a", "EN")], [LangString("a", "EN")]),
        ([LangString("hello", "En"), LangString("hello", "EN")], [LangString("hello", "en")]),
        (
            [LangString("hello", "EN"), LangString("world", "EN")],
            [LangString("hello", "EN"), LangString("world", "EN")],
        ),
        (
            [LangString("hello", "EN"), LangString("world", "En")],
            [LangString("hello", "EN"), LangString("world", "En")],
        ),
        (
            [LangString("hello", "EN"), LangString("hello", "EN")],
            [LangString("hello", "EN")],
        ),
        (
            [LangString("hello", "EN"), LangString("hello", "eN")],
            [LangString("hello", "en")],
        ),
        ([LangString(" Καλημέρα", "en")], [LangString(" Καλημέρα", "en")]),  # Spaces before, Greek characters
        (
            [LangString("🚀", "emoji"), LangString("🌟", "emoji")],
            [LangString("🚀", "emoji"), LangString("🌟", "emoji")],
        ),  # Emojis
        (
            [LangString("data", " DE "), LangString("science", " de ")],
            [LangString("data", " DE "), LangString("science", " de ")],
        ),  # Spaces in lang
        (
            [LangString("Привет", "ru"), LangString("Мир", "RU")],
            [LangString("Привет", "ru"), LangString("Мир", "RU")],
        ),  # Cyrillic
        (
            [LangString("!@#$%^&*()", "spec"), LangString("{}[]:;\"'<>?,./", "spec")],
            [LangString("!@#$%^&*()", "spec"), LangString("{}[]:;\"'<>?,./", "spec")],
        ),  # Special chars
        (
            [LangString("hello", ""), LangString("world", "")],
            [LangString("hello", ""), LangString("world", "")],
        ),  # Empty lang value
        (
            [LangString("A", "en"), LangString("a", "en")],
            [LangString("A", "en"), LangString("a", "en")],
        ),  # Case sensitivity in content
        (
            [LangString("A", "En"), LangString("a", "en")],
            [LangString("A", "En"), LangString("a", "en")],
        ),  # Case sensitivity in content
        (
            [LangString("A", "EN"), LangString("a", "EN")],
            [LangString("A", "EN"), LangString("a", "EN")],
        ),  # Case sensitivity in content
        (
            [LangString("hello", "en"), LangString("HELLO", "en")],
            [LangString("hello", "en"), LangString("HELLO", "en")],
        ),  # Different content, same lang
        # Preserve original casing if texts differ
        (
            [LangString("text", "DE"), LangString("more text", "DE")],
            [LangString("text", "DE"), LangString("more text", "DE")],
        ),
        (
            [LangString("text", "DE"), LangString("more text", "de")],
            [LangString("text", "DE"), LangString("more text", "de")],
        ),
        # Merge with original casing if texts and casings are identical
        ([LangString("text", "DE"), LangString("text", "DE")], [LangString("text", "DE")]),
        # Merge with original casing if texts and casings are identical
        ([LangString(" text", "DE"), LangString("text", "dE")], [LangString(" text", "DE"), LangString("text", "dE")]),
        # Casefold language tag if there are case variations among duplicates
        ([LangString("text", "De"), LangString("text", "DE")], [LangString("text", "de")]),
        # Testing leading/trailing spaces in texts
        (
            [LangString("    ", "en"), LangString("Empty spaces", "EN")],
            [LangString("    ", "en"), LangString("Empty spaces", "EN")],
        ),
        # Greek characters, mixed case, preserving individual instances
        (
            [LangString("Γειά σου κόσμε", "el"), LangString("Καλημέρα", "EL")],
            [LangString("Γειά σου κόσμε", "el"), LangString("Καλημέρα", "EL")],
        ),
        # Cyrillic characters, mixed case, preserving individual instances
        ([LangString("Привет", "ru"), LangString("Мир", "RU")], [LangString("Привет", "ru"), LangString("Мир", "RU")]),
        # Emojis in texts, mixed case, preserving individual instances
        (
            [LangString("👋", "emoji"), LangString("😊", "EMOJI")],
            [LangString("👋", "emoji"), LangString("😊", "EMOJI")],
        ),
    ],
)
def test_merge_langstrings_success(input_data, expected_output):
    """Adapted test to verify merge_langstrings successfully merges LangStrings following specific rules about text content and language tag casing."""
    result = LangString.merge_langstrings(input_data)
    assert len(result) == len(
        expected_output
    ), f"Expected {len(expected_output)} LangString instances, got {len(result)}."
    for res, exp in zip(result, expected_output):
        assert (
            res.text == exp.text and res.lang == exp.lang
        ), f"Expected LangString with text '{exp.text}' and lang '{exp.lang}', got text '{res.text}' and lang '{res.lang}'."


@pytest.mark.parametrize(
    "invalid_input",
    [
        # Incorrect types, not LangString instance
        ([{"a"}, "EN"]),
        ("Not a list",),
        ([LangString("a", "en"), "Random String"]),  # Mixed with incorrect type
    ],
)
def test_merge_langstrings_type_error(invalid_input):
    """Test `merge_langstrings` raises TypeError with invalid input types."""
    with pytest.raises(TypeError, match=TYPEERROR_MSG_SINGULAR):
        LangString.merge_langstrings(invalid_input)


def test_merge_langstrings_empty_input():
    """Test `merge_langstrings` with an empty list input returns an empty list."""
    result = LangString.merge_langstrings([])
    assert result == [], "Expected empty list as output when merging an empty input list."


@pytest.mark.parametrize(
    "input_data",
    [
        (None),
        ([None]),
    ],
)
def test_merge_langstrings_null_input(input_data):
    """Test merge_langstrings handling of null inputs."""
    with pytest.raises(TypeError, match=TYPEERROR_MSG_SINGULAR):
        LangString.merge_langstrings(input_data)
