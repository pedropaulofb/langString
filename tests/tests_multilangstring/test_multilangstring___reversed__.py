import pytest
from langstring import MultiLangString


@pytest.mark.parametrize(
    "mls, expected_reversed_keys",
    [
        (MultiLangString(), []),
        (MultiLangString({"en": {"Hello"}}), ["en"]),
        (MultiLangString({"en": {"Hello"}, "es": {"Hola"}, "fr": {"Bonjour"}}), ["fr", "es", "en"]),
        (MultiLangString({"en": {"Hello"}, "es": {"Hola"}, "fr": {"Bonjour"}, "EN": {"World"}}), ["fr", "es", "en"]),
        (MultiLangString({"en": {"Hello"}, "EN": {"Hi"}, "en-GB": {"Hello, mate"}}), ["en-GB", "en"]),
        (MultiLangString({"1": {"One"}, "2": {"Two"}, "3": {"Three"}}), ["3", "2", "1"]),
        (MultiLangString({"a": {"A"}, "b": set(), "c": {"C"}}), ["c", "b", "a"]),
        (MultiLangString({"😀": {"Emoji 1"}, "🤔": {"Emoji 2"}, "😂": {"Emoji 3"}}), ["😂", "🤔", "😀"]),
        (
            MultiLangString({" space before": {"Space"}, "space after ": {"Space"}, " normal ": {"Normal"}}),
            [" normal ", "space after ", " space before"],
        ),
        (
            MultiLangString({"uppercase": {"UPPER"}, "lowercase": {"lower"}, "MixedCase": {"Mixed"}}),
            ["MixedCase", "lowercase", "uppercase"],
        ),
        # Testing with an empty MultiLangString instance
        (MultiLangString(), []),
        # Testing with a single language to ensure basic functionality
        (MultiLangString({"en": {"Hello"}}), ["en"]),
        # Testing with multiple languages to ensure correct reversed order
        (MultiLangString({"en": {"Hello"}, "es": {"Hola"}, "de": {"Hallo"}}), ["de", "es", "en"]),
        # Testing with languages added in non-alphabetical order to verify it's truly reversing the insertion order
        (MultiLangString({"de": {"Hallo"}, "en": {"Hello"}, "es": {"Hola"}}), ["es", "en", "de"]),
        # Testing with empty values to ensure they are handled correctly
        (MultiLangString({"en": set(), "es": set()}), ["es", "en"]),
        # Testing with unusual but valid usage including different character sets, emojis, and special characters
        (MultiLangString({"😀": {"Emoji"}, "α": {"Alpha"}, "!@#$": {"Special chars"}}), ["!@#$", "α", "😀"]),
        (MultiLangString({"   ": {"Space as key"}}), ["   "]),
        (
            MultiLangString({"lowercase": {"lower"}, "UPPERCASE": {"UPPER"}, "MixedCase": {"Mixed"}}),
            ["MixedCase", "UPPERCASE", "lowercase"],
        ),
        (
            MultiLangString({"русский": {"Привет"}, "ελληνικά": {"Γειά"}, "日本語": {"こんにちは"}}),
            ["日本語", "ελληνικά", "русский"],
        ),
        (
            MultiLangString({"surrounding spaces ": {" space "}, " inner spaces ": {"inner  spaces"}}),
            [" inner spaces ", "surrounding spaces "],
        ),
        (MultiLangString({"": {"Empty key"}, " ": {"Single space key"}}), [" ", ""]),
        (MultiLangString({"multiple": {"value1", "value2"}, "single": {"value"}}), ["single", "multiple"]),
        (
            MultiLangString({"same keys different case": {"Value1"}, "Same Keys Different Case": {"Value2"}}),
            ["same keys different case"],
        ),
    ],
)
def test_reversed_keys(mls: MultiLangString, expected_reversed_keys: list[str]) -> None:
    """Test the __reversed__ method to ensure it returns the language keys in the correct reversed order.

    :param mls: The MultiLangString instance to test.
    :param expected_reversed_keys: The expected list of keys (language codes) to be returned by the reversed iterator.
    :return: None
    """
    reversed_keys = list(reversed(mls))
    assert (
        reversed_keys == expected_reversed_keys
    ), f"Expected reversed keys {expected_reversed_keys}, but got {reversed_keys}"
