import pytest
from langstring import MultiLangString


@pytest.mark.parametrize(
    "mls, expected_keys",
    [
        (MultiLangString(), []),
        (MultiLangString({"en": {"Hello"}}), ["en"]),
        (MultiLangString({"en": {"Hello"}, "es": {"Hola"}}), ["en", "es"]),
        (MultiLangString({"EN": {"Hello"}, "es": {"Hola"}, "en": {"World"}}), ["en", "es"]),
        (MultiLangString({"en": {"Hello"}, "EN": {"Hi"}}), ["en"]),
        (MultiLangString({"": {"Empty key"}}), [""]),
        (MultiLangString({"GR": {"Γειά σου"}, "RU": {"Привет"}}), ["GR", "RU"]),
        (MultiLangString({"en": set()}), ["en"]),
        (MultiLangString({"😀": {"Emoji key"}}), ["😀"]),
        (MultiLangString({" special*chars! ": {"Special characters in key"}}), [" special*chars! "]),
        (MultiLangString({"en": {" Hello "}, "es": {" Hola "}}), ["en", "es"]),
    ],
)
def test_iter_keys(mls: MultiLangString, expected_keys: list[str]) -> None:
    """Test the __iter__ method to ensure it returns the correct language keys.

    :param mls: The MultiLangString instance to test.
    :param expected_keys: The expected list of keys (language codes) to be returned by the iterator.
    :return: None
    """
    keys = list(iter(mls))
    assert keys == expected_keys, f"Expected keys {expected_keys}, but got {keys}"


@pytest.mark.parametrize(
    "mls, expected_order",
    [
        (MultiLangString({"a": {"A"}, "b": {"B"}, "c": {"C"}}), ["a", "b", "c"]),
        (MultiLangString({"c": {"C"}, "a": {"A"}, "b": {"B"}}), ["c", "a", "b"]),
        (MultiLangString({" z ": {"Z"}, " a ": {"A"}}), [" z ", " a "]),
        (MultiLangString({"α": {"Alpha"}, "β": {"Beta"}}), ["α", "β"]),
        (MultiLangString({"1": {"One"}, "2": {"Two"}}), ["1", "2"]),
        (MultiLangString({"😀": {"Emoji 1"}, "🤔": {"Emoji 2"}}), ["😀", "🤔"]),
        (
            MultiLangString({" special*chars! ": {"Special 1"}, " another*chars! ": {"Special 2"}}),
            [" special*chars! ", " another*chars! "],
        ),
    ],
)
def test_iter_order(mls: MultiLangString, expected_order: list[str]) -> None:
    """Test the __iter__ method to ensure that the iteration order follows the insertion order.

    :param mls: The MultiLangString instance to test.
    :param expected_order: The expected iteration order of keys (language codes).
    :return: None
    """
    order = list(iter(mls))
    assert order == expected_order, f"Expected iteration order {expected_order}, but got {order}"
