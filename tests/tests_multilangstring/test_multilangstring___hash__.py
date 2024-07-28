import pytest
from langstring import MultiLangString


@pytest.mark.parametrize(
    "mls_dict1,mls_dict2,expected",
    [
        ({"en": {"Hello"}}, {"en": {"Hello"}}, True),
        ({"en": {"Hello"}}, {"EN": {"Hello"}}, True),
        ({" en": {"Hello", "World"}}, {" eN": {"World", "Hello"}}, True),
        ({"en": {"Hello"}}, {"fr": {"Bonjour"}}, False),
        ({"en": {"Hello", "Goodbye"}}, {"en": {"Hello"}, "fr": {"Au revoir"}}, False),
        ({"en": {"Hello", "Goodbye"}}, {"en": {"Goodbye", "Hello"}}, True),
        ({"en": {""}}, {"en": {""}}, True),
        ({"en": {" Hello "}}, {"en": {"Hello"}}, False),
        ({"en": {"Hello"}}, {"en": {"\tHello\t"}}, False),
        ({"en": {"Привет"}}, {"ru": {"Привет"}}, False),  # Cyrillic
        ({"el": {"Γειά"}}, {"el": {"Γειά"}}, True),  # Greek
        ({"en": {"😀"}}, {"en": {"😀"}}, True),
        ({" en": {"😀"}}, {"en": {"😀"}}, False),
        ({"en ": {"😀"}}, {"en": {"😀"}}, False),
        ({"en": {" 😀"}}, {"en": {"😀"}}, False),
        ({"en": {"😀 "}}, {"en": {"😀"}}, False),
        ({"en": {"Hello\nWorld"}}, {"en": {"Hello World"}}, False),
        ({"en": {"Special&*()"}}, {"en": {"Special&*()"}}, True),
        ({"EN": {"Special&*()"}}, {"en": {"Special&*()"}}, True),
        ({"en": {"Case"}}, {"EN": {"case"}}, False),
        ({"": {"Empty key"}}, {"": {"Empty key"}}, True),  # Empty key
    ],
)
def test_hash_equality_for_multi_lang_strings(mls_dict1, mls_dict2, expected):
    """Test if two MultiLangString instances with identical or different contents produce the expected hash equality or inequality.
    :param mls_dict1: First dictionary to initialize MultiLangString instance
    :param mls_dict2: Second dictionary to initialize MultiLangString instance
    :param expected: Expected result; True if hashes should be equal, False otherwise
    """
    mls1 = MultiLangString(mls_dict1)
    mls2 = MultiLangString(mls_dict2)
    assert (hash(mls1) == hash(mls2)) is expected, "Hash equality does not match expected outcome."


def test_hash_consistency_with_modifications():
    """Test that the hash value of a MultiLangString instance changes after modification."""
    mls = MultiLangString({"en": {"Hello"}})
    hash_before = hash(mls)
    mls.add_entry("Bonjour", "fr")
    hash_after = hash(mls)
    assert hash_before != hash_after, "Hash did not change after modifying the MultiLangString."


def test_hash_for_empty_multi_lang_string():
    """Test that an empty MultiLangString instance has a consistent hash value."""
    mls = MultiLangString()
    assert isinstance(hash(mls), int), "Hash of an empty MultiLangString is not an integer."


def test_hash_unusual_but_valid_usage():
    """Test the hash function with unusual but valid dictionary."""
    mls = MultiLangString({"en": {"Hello"}, "en-GB": {"Hello"}, "EN": {"HELLO"}})
    assert isinstance(hash(mls), int), "Hash of a MultiLangString with case variants is not an integer."


@pytest.mark.parametrize(
    "mls_dict, pref_lang1, pref_lang2",
    [
        ({"en": {"Hello"}}, "en", "fr"),
        ({"en": {"Hello"}}, "en", "en"),
        ({"en": {"Hello"}}, "en", "EN"),
        ({"en": {"Hello"}, "fr": {"Bonjour"}}, "en", "fr"),
        ({"en": {"Hello"}, "de": {"Hallo"}}, "de", "en"),
        ({"es": {"Hola"}, "fr": {"Bonjour"}}, "es", "fr"),
        ({"en": {"Hello"}, "fr": {"Bonjour"}, "es": {"Hola"}}, "fr", "es"),
        ({"en": {"Hello"}, "EN": {"HELLO"}}, "en", "EN"),
        ({"ru": {"Привет"}}, "ru", "RU"),
        ({"el": {"Γειά"}}, "el", "EL"),
        ({"en": {"😀"}}, "en", "fr"),
        ({"en": {"Special&*()"}}, "en", "fr"),
    ],
)
def test_hash_equality_ignoring_pref_lang(mls_dict, pref_lang1, pref_lang2):
    """Test that two MultiLangString instances with the same content but different preferred languages produce the expected hash equality.
    :param mls_dict: Dictionary to initialize MultiLangString instance
    :param pref_lang1: Preferred language for the first MultiLangString instance
    :param pref_lang2: Preferred language for the second MultiLangString instance
    :param expected: Expected result; True if hashes should be equal, False otherwise
    """
    mls1 = MultiLangString(mls_dict, pref_lang=pref_lang1)
    mls2 = MultiLangString(mls_dict, pref_lang=pref_lang2)
    assert hash(mls1) == hash(mls2), "Hash equality does not match expected outcome despite pref_lang."
