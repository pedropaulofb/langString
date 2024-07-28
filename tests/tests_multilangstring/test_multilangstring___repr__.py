import pytest
from langstring import MultiLangString


@pytest.mark.parametrize(
    "mls_dict, expected_repr",
    [
        ({}, "MultiLangString(mls_dict={}, pref_lang='en')"),
        ({"en": {"Hello", "World"}}, "MultiLangString(mls_dict={'en': {'Hello', 'World'}}, pref_lang='en')"),
        (
            {"en": {"Hello", "World"}, "en": {"Hello", "World"}},
            "MultiLangString(mls_dict={'en': {'Hello', 'World'}}, pref_lang='en')",
        ),
        ({"en": {"Hello"}, "en": {"World"}}, "MultiLangString(mls_dict={'en': {'Hello', 'World'}}, pref_lang='en')"),
        (
            {"fr": {"Bonjour"}, "es": {"Hola", "Adiós"}},
            "MultiLangString(mls_dict={'fr': {'Bonjour'}, 'es': {'Hola', 'Adiós'}}, pref_lang='en')",
        ),
        # Test with special characters and emojis
        ({"🌐": {"Hello", "🌎"}}, "MultiLangString(mls_dict={'🌐': {'Hello', '🌎'}}, pref_lang='en')"),
        # Test with spaces and mixed cases in language codes
        (
            {"  en  ": {"Spacing"}, "FR": {"Majuscule"}},
            "MultiLangString(mls_dict={'  en  ': {'Spacing'}, 'FR': {'Majuscule'}}, pref_lang='en')",
        ),
        # Cyrillic characters in the language code and texts
        ({"рус": {"Привет", "Мир"}}, "MultiLangString(mls_dict={'рус': {'Привет', 'Мир'}}, pref_lang='en')"),
        ({"long": {"a" * 1000}}, "MultiLangString(mls_dict={'long': {'" + "a" * 1000 + "'}}, pref_lang='en')"),
        (
            {"nested": {"{'inner': 'value'}"}},
            "MultiLangString(mls_dict={'nested': {\"{'inner': 'value'}\"}}, pref_lang='en')",
        ),
        # Empty sets for languages
        ({"empty": set()}, "MultiLangString(mls_dict={'empty': set()}, pref_lang='en')"),
        # Mixed case language codes with actual text
        ({"MiXeD": {"Mixed Case"}}, "MultiLangString(mls_dict={'MiXeD': {'Mixed Case'}}, pref_lang='en')"),
        # Languages with spaces before, after, and inside, with actual texts
        ({" before": {"Before Space"}}, "MultiLangString(mls_dict={' before': {'Before Space'}}, pref_lang='en')"),
        ({"after ": {"After Space"}}, "MultiLangString(mls_dict={'after ': {'After Space'}}, pref_lang='en')"),
        ({" inside ": {"Inside Space"}}, "MultiLangString(mls_dict={' inside ': {'Inside Space'}}, pref_lang='en')"),
        # Different charset with Greek and Cyrillic, emojis, and special characters in texts
        (
            {"Ελληνικά": {"Καλημέρα", "Γειά σου"}},
            "MultiLangString(mls_dict={'Ελληνικά': {'Καλημέρα', 'Γειά σου'}}, pref_lang='en')",
        ),
        (
            {"русский": {"Здравствуйте", "Привет"}},
            "MultiLangString(mls_dict={'русский': {'Здравствуйте', 'Привет'}}, pref_lang='en')",
        ),
        ({"symbols": {"@#$%", "&*()"}}, "MultiLangString(mls_dict={'symbols': {'@#$%', '&*()'}}, pref_lang='en')"),
        # Test with only emojis in language code and texts
        ({"😀": {"😁", "😂"}}, "MultiLangString(mls_dict={'😀': {'😁', '😂'}}, pref_lang='en')"),
        # Test with a mix of different cases, spaces, special characters in one
        (
            {"  🌐 MiXeD 😀 ": {"Hello 🌎", "World 🌍"}},
            "MultiLangString(mls_dict={'  🌐 MiXeD 😀 ': {'Hello 🌎', 'World 🌍'}}, pref_lang='en')",
        ),
    ],
)
def test_repr_output(mls_dict: dict, expected_repr: str):
    """Test the `__repr__` method of the MultiLangString class provides the expected string representation.

    This test constructs a MultiLangString object from a dictionary, converts it to its string representation using
    `__repr__`, and then ensures that the string can be converted back to a dictionary that matches the original
    dictionary used to create the MultiLangString object, ignoring the order of items in sets.

    :param mls_dict: The dictionary representing the internal structure of the MultiLangString instance to test.
    :param expected_repr: The expected string representation of the MultiLangString instance.
    """
    mls = MultiLangString(mls_dict)
    actual_repr = repr(mls)
    actual_mls_dict = eval(actual_repr).mls_dict
    for key in mls_dict:
        assert mls_dict[key] == actual_mls_dict[key], f"Mismatch for language '{key}'."
