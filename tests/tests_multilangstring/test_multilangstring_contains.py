import pytest
from langstring import LangString
from langstring import MultiLangString
from langstring import SetLangString


@pytest.mark.parametrize(
    "arg, expected",
    [
        (("Hello", "en"), True),  # Tuple with text and language
        (LangString("Hello", "en"), True),  # LangString object
        (SetLangString({"Hello"}, "en"), True),  # SetLangString object
        # Assuming MultiLangString.contains_multilangstring is properly implemented and checks for any overlap.
        (MultiLangString({"en": {"Hello"}}), True),  # MultiLangString object
        (("Hola", "en"), False),  # Text not present
        (("Hello", "de"), False),  # Language not present
        # Null checks
        ((None, "en"), pytest.raises(TypeError)),  # Null text with valid language
        (("Hello", None), pytest.raises(TypeError)),  # Valid text with null language
        ((None, None), pytest.raises(TypeError)),  # Both text and language are null
        # Empty checks
        (("", "en"), False),  # Empty text with valid language
        (("Hello", ""), False),  # Valid text with empty language
        # Invalid types for tuple
        ((123, "en"), pytest.raises(TypeError)),  # Non-string text
        (("Hello", 123), pytest.raises(TypeError)),  # Non-string language
        # Operation on itself
        ((MultiLangString({"en": {"Hello", "Hi"}}), True)),  # MultiLangString containing itself
        # Unusual but valid usage
        ((("LongText" * 1000, "en"), False)),  # Extremely long text
        # Invalid argument type
        (("Just a string",), pytest.raises(TypeError, match="Argument .* must be of type 'tuple\\[str,str\\]'")),
        # Case sensitivity checks
        (("hello", "en"), False),  # Case sensitivity check
        # Exact match vs. partial match
        (("Hello world", "en"), False),  # Assuming exact match is required
        # Special characters and punctuation
        (("Hello!", "en"), False),  # Text with punctuation not present
        # Numeric texts
        (("123", "en"), False),  # Numeric string
        # Testing with multiple languages in a single MultiLangString instance
        ((MultiLangString({"en": {"Hello"}, "es": {"Hola"}}), False)),  # MultiLangString with multiple languages
        # Testing with an empty MultiLangString
        ((MultiLangString({}), True)),  # Empty MultiLangString
        # Uncommon language codes
        (("Hello", "xx"), False),  # Uncommon/invalid language code
    ],
)
def test_contains(arg, expected):
    """
    Test the `contains` method with various types of arguments.

    :param arg: Argument to be passed to the contains method. Can be a tuple, LangString, SetLangString, or MultiLangString.
    :param expected: Expected result or exception raised.
    """
    mls = MultiLangString({"en": {"Hello", "Hi"}, "de": {"Hallo", "Guten Tag"}})
    if isinstance(expected, bool):
        assert mls.contains(arg) == expected, f"Expected {expected} for argument '{arg}'."
    else:
        with expected:
            mls.contains(arg)
