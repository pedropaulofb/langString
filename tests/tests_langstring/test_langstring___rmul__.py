import pytest
from langstring import LangString
from tests.conftest import TYPEERROR_MSG_SINGULAR


@pytest.mark.parametrize(
    "original_text, multiplier, expected_text",
    [("Hello", 3, "HelloHelloHello"), ("", 5, ""), ("Test", 0, ""), ("😊", 2, "😊😊"), ("123", 3, "123123123")],
)
def test_rmul_with_various_multipliers(original_text: str, multiplier: int, expected_text: str) -> None:
    """
    Test the `__rmul__` method for right multiplying LangString with various integer multipliers.

    :param original_text: The original text of the LangString.
    :param multiplier: The integer multiplier.
    :param expected_text: The expected text after right multiplication.
    """
    lang_string = LangString(original_text, "en")
    result = multiplier * lang_string
    assert (
        result.text == expected_text
    ), f"Expected text after right multiplication: '{expected_text}', got: '{result.text}'"


@pytest.mark.parametrize("invalid_multiplier", ["a", 1.5, None, [2], {"multiplier": 2}])
def test_rmul_with_invalid_multiplier(invalid_multiplier) -> None:
    """
    Test the `__rmul__` method with invalid multipliers for right multiplication.

    :param invalid_multiplier: An invalid multiplier type.
    """
    lang_string = LangString("Hello", "en")
    with pytest.raises(TypeError, match=TYPEERROR_MSG_SINGULAR):
        _ = invalid_multiplier * lang_string


@pytest.mark.parametrize(
    "original_text, large_multiplier",
    [
        ("Text", 10000),  # Large multiplier
        ("🌍🚀", 1000),  # Large multiplier with emojis
    ],
)
def test_rmul_with_large_multiplier(original_text: str, large_multiplier: int) -> None:
    """
    Test the `__rmul__` method with unusually large multipliers for right multiplication.

    :param original_text: The original text of the LangString.
    :param large_multiplier: A large integer multiplier.
    """
    lang_string = LangString(original_text, "en")
    result = large_multiplier * lang_string
    assert len(result.text) == len(original_text) * large_multiplier, "Length mismatch after large right multiplication"


@pytest.mark.parametrize(
    "original_text, unicode_multiplier",
    [
        ("こんにちは", 3),  # Multiplying Unicode text
        ("♠♥♦♣", 2),  # Multiplying special characters
    ],
)
def test_rmul_with_unicode_and_special_characters(original_text: str, unicode_multiplier: int) -> None:
    """
    Test the `__rmul__` method with Unicode and special characters for right multiplication.

    :param original_text: The original text of the LangString.
    :param unicode_multiplier: An integer multiplier.
    """
    lang_string = LangString(original_text, "en")
    result = unicode_multiplier * lang_string
    assert (
        result.text == original_text * unicode_multiplier
    ), "Incorrect right multiplication with Unicode/special chars"
