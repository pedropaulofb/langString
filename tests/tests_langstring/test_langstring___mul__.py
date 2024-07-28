import pytest
from langstring import LangString
from tests.conftest import TYPEERROR_MSG_SINGULAR


@pytest.mark.parametrize(
    "original_text, multiplier, expected_text",
    [("Hello", 3, "HelloHelloHello"), ("", 5, ""), ("Test", 0, ""), ("😊", 2, "😊😊"), ("123", 3, "123123123")],
)
def test_mul_with_various_multipliers(original_text: str, multiplier: int, expected_text: str) -> None:
    """
    Test the `__mul__` method for multiplying LangString with various integer multipliers.

    :param original_text: The original text of the LangString.
    :param multiplier: The integer multiplier.
    :param expected_text: The expected text after multiplication.
    """
    lang_string = LangString(original_text, "en")
    result = lang_string * multiplier
    assert result.text == expected_text, f"Expected text after multiplication: '{expected_text}', got: '{result.text}'"


@pytest.mark.parametrize("invalid_multiplier", ["a", 1.5, None, [2], {"multiplier": 2}])
def test_mul_with_invalid_multiplier(invalid_multiplier) -> None:
    """
    Test the `__mul__` method with invalid multipliers.

    :param invalid_multiplier: An invalid multiplier type.
    """
    lang_string = LangString("Hello", "en")
    with pytest.raises(TypeError, match=TYPEERROR_MSG_SINGULAR):
        _ = lang_string * invalid_multiplier


@pytest.mark.parametrize(
    "original_text, large_multiplier",
    [
        ("Text", 10000),  # Large multiplier
        ("🌍🚀", 1000),  # Large multiplier with emojis
    ],
)
def test_mul_with_large_multiplier(original_text: str, large_multiplier: int) -> None:
    """
    Test the `__mul__` method with unusually large multipliers.

    :param original_text: The original text of the LangString.
    :param large_multiplier: A large integer multiplier.
    """
    lang_string = LangString(original_text, "en")
    result = lang_string * large_multiplier
    assert len(result.text) == len(original_text) * large_multiplier, "Length mismatch after large multiplication"


@pytest.mark.parametrize(
    "original_text, unicode_multiplier",
    [
        ("こんにちは", 3),  # Multiplying Unicode text
        ("♠♥♦♣", 2),  # Multiplying special characters
    ],
)
def test_mul_with_unicode_and_special_characters(original_text: str, unicode_multiplier: int) -> None:
    """
    Test the `__mul__` method with Unicode and special characters.

    :param original_text: The original text of the LangString.
    :param unicode_multiplier: An integer multiplier.
    """
    lang_string = LangString(original_text, "en")
    result = lang_string * unicode_multiplier
    assert result.text == original_text * unicode_multiplier, "Incorrect multiplication with Unicode/special chars"
