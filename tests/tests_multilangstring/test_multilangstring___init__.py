import pytest
from langstring import Controller
from langstring import MultiLangString
from langstring import MultiLangStringFlag
from tests.conftest import TYPEERROR_MSG_SINGULAR


@pytest.mark.parametrize(
    "input_dict, pref_lang, expected_dict, expected_pref_lang",
    [
        ({"en": {"Hello"}, "fr": {"Bonjour"}}, "en", {"en": {"Hello"}, "fr": {"Bonjour"}}, "en"),
        (
            {"en": {"Hello"}, "En": {"World"}, "fr": {"Bonjour"}},
            "en",
            {"en": {"Hello", "World"}, "fr": {"Bonjour"}},
            "en",
        ),
        (
            {"EN": {"Hello"}, "En": {"World"}, "fr": {"Bonjour"}},
            "en",
            {"en": {"Hello", "World"}, "fr": {"Bonjour"}},
            "en",
        ),
        ({}, "en", {}, "en"),
        (None, "en", {}, "en"),
        ({}, None, {}, "en"),
        (None, None, {}, "en"),
        ({"en": {"Hello"}, "es": {"Hola"}}, "en", {"en": {"Hello"}, "es": {"Hola"}}, "en"),
    ],
)
def test_multilangstring_init_valid(input_dict: dict, pref_lang: str, expected_dict: dict, expected_pref_lang: str):
    """Tests MultiLangString initialization with valid inputs.

    :param input_dict: Dictionary containing language code keys and string values.
    :param pref_lang: Preferred language code.
    :param expected_dict: Expected dictionary after initialization.
    :param expected_pref_lang: Expected preferred language after initialization.
    """
    mls = MultiLangString(mls_dict=input_dict, pref_lang=pref_lang)
    assert mls.mls_dict == expected_dict, "Initialized mls_dict does not match expected dictionary"
    assert mls.pref_lang == expected_pref_lang, "Initialized pref_lang does not match expected preferred language"


@pytest.mark.parametrize(
    "input_dict, pref_lang",
    [
        (123, "en"),
        ("not a dict", None),
        ([("en", "Hello")], "en"),
    ],
)
def test_multilangstring_init_invalid_type(input_dict: dict, pref_lang: str):
    """Tests MultiLangString initialization with invalid types for `mls_dict`.

    :param input_dict: Invalid type for the dictionary parameter.
    :param pref_lang: Preferred language code.
    """
    with pytest.raises(TypeError, match=TYPEERROR_MSG_SINGULAR):
        MultiLangString(mls_dict=input_dict, pref_lang=pref_lang)


@pytest.mark.parametrize(
    "input_dict, pref_lang",
    [
        ({"en": {"Hello"}, "fr": {123}}, "en"),
        ({"en": {None}, "fr": {123}}, "en"),
        ({"en": {None}, "fr": None}, "en"),
        ({"en": {None}, "fr": {None}}, "en"),
        ({"en": {"Hello"}, "fr": 123}, "en"),
        ({"en": "Hello", "fr": {123}}, "en"),
        ({"en": "Hello", "es": {"Hola"}}, "en"),
        ({"en": None, "es": {"Hola"}}, "en"),
    ],
)
def test_multilangstring_init_invalid_dict_values(input_dict: dict, pref_lang: str):
    """Tests MultiLangString initialization with invalid values in the dictionary.

    :param input_dict: Dictionary containing invalid values.
    :param pref_lang: Preferred language code.
    """
    with pytest.raises(TypeError, match=TYPEERROR_MSG_SINGULAR):
        MultiLangString(mls_dict=input_dict, pref_lang=pref_lang)


@pytest.mark.parametrize(
    "input_dict, pref_lang",
    [
        ({123: {"Hello", "World"}, "pt": {"Olá", "Mundo"}}, "en"),
        ({None: {"Hello", "World"}, "pt": {"Olá", "Mundo"}}, "en"),
        ({"en": {"Hello", "World"}, None: {""}}, "en"),
    ],
)
def test_multilangstring_init_invalid_dict_keys(input_dict: dict, pref_lang: str):
    """Tests MultiLangString initialization with invalid values in the dictionary.

    :param input_dict: Dictionary containing invalid values.
    :param pref_lang: Preferred language code.
    """
    with pytest.raises(TypeError, match=TYPEERROR_MSG_SINGULAR):
        MultiLangString(mls_dict=input_dict, pref_lang=pref_lang)


@pytest.mark.parametrize(
    "input_dict, pref_lang",
    [
        ({"en": {"Hello", "World"}, "pt": {"Olá", "Mundo"}}, 123),
        ({"en": {"Hello", "World"}, "pt": {"Olá", "Mundo"}}, ["a"]),
        ({"en": {"Hello", "World"}, "pt": {"Olá", "Mundo"}}, {"a": "b"}),
    ],
)
def test_multilangstring_init_invalid_pref_lang(input_dict: dict, pref_lang: str):
    """Tests MultiLangString initialization with invalid values in the dictionary.

    :param input_dict: Dictionary containing invalid values.
    :param pref_lang: Preferred language code.
    """
    with pytest.raises(TypeError, match=TYPEERROR_MSG_SINGULAR):
        MultiLangString(mls_dict=input_dict, pref_lang=pref_lang)


def test_multilangstring_init_no_args():
    """Tests MultiLangString initialization without arguments, assuming defaults are set."""
    mls = MultiLangString()
    assert mls.mls_dict == {}, "Initialized mls_dict should be empty by default"
    assert mls.pref_lang == "en", "Initialized pref_lang should be 'en' by default"


@pytest.mark.parametrize(
    "input_dict",
    [({"en": {"a" * 10000}}), ({"en": {f"value{k}" for k in range(1000)}})],  # Test with a very long string
)
def test_multilangstring_init_edge_cases(input_dict: dict):
    """Tests MultiLangString initialization with edge case inputs.

    :param input_dict: Dictionary for edge case testing.
    """
    mls = MultiLangString(mls_dict=input_dict)
    assert len(mls.mls_dict) == len(input_dict), "Initialized mls_dict size does not match input dictionary size"


def test_multilangstring_init_with_lowercase_lang_flag():
    """Tests MultiLangString initialization with LOWERCASE_LANG flag effect."""
    # Set the LOWERCASE_LANG flag to True
    Controller.set_flag(MultiLangStringFlag.LOWERCASE_LANG, True)
    input_dict = {"EN": {"Hello"}, "FR": {"Bonjour"}}
    mls = MultiLangString(mls_dict=input_dict)
    # Expecting languages to be converted to lowercase if LOWERCASE_LANG flag is set
    for lang in mls.mls_dict.keys():
        assert lang.islower(), "Language codes should be lowercase when LOWERCASE_LANG flag is True"


def test_multilangstring_init_with_strip_text_flag():
    """Tests MultiLangString initialization with STRIP_TEXT flag effect."""
    # Set the STRIP_TEXT flag to True
    Controller.set_flag(MultiLangStringFlag.STRIP_TEXT, True)
    input_dict = {"en": {"  Hello  "}, "fr": {"  Bonjour  "}}
    mls = MultiLangString(mls_dict=input_dict)
    # Expecting text to be stripped if STRIP_TEXT flag is set
    for texts in mls.mls_dict.values():
        for text in texts:
            assert (
                text == text.strip()
            ), "Text should be stripped of leading and trailing spaces when STRIP_TEXT flag is True"


@pytest.mark.parametrize(
    "input_dict, expected_dict",
    [
        ({"en": {"Hello"}, "EN": {"World"}}, {"en": {"Hello", "World"}}),
        ({"FR": {"Salut"}, "fr": {"Bonjour"}, "Fr": {"Au revoir"}}, {"fr": {"Salut", "Bonjour", "Au revoir"}}),
        ({"es": {"Hola"}, "ES": {"Adiós"}, "Es": {"Buenos días"}}, {"es": {"Hola", "Adiós", "Buenos días"}}),
        ({"en": {""}, "EN": {"World", ""}}, {"en": {"", "World"}}),
        ({"": {"Empty key"}, "  ": {"Whitespace key"}}, {"": {"Empty key"}, "  ": {"Whitespace key"}}),
        ({"GR": {"Γειά σου"}, "gr": {"Καλημέρα"}, "Gr": {"Καλησπέρα"}}, {"gr": {"Γειά σου", "Καλημέρα", "Καλησπέρα"}}),
        ({"RU": {"Привет"}, "ru": {"Здравствуйте"}}, {"ru": {"Привет", "Здравствуйте"}}),
        ({"emoji": {"😀", "😃"}, "EMOJI": {"😄", "😁"}}, {"emoji": {"😀", "😃", "😄", "😁"}}),
        (
            {"special": {"!@#$%", "^&*()"}, "SPECIAL": {"_+{}:", "<>?~"}},
            {"special": {"!@#$%", "^&*()", "_+{}:", "<>?~"}},
        ),
        (
            {"mixedCASE": {"Case Insensitive"}, "MixedCase": {"Merging Test"}},
            {"mixedcase": {"Case Insensitive", "Merging Test"}},
        ),
        (
            {" leading ": {"Leading spaces"}, "leading ": {"Trimming"}},
            {" leading ": {"Leading spaces"}, "leading ": {"Trimming"}},
        ),
        ({"trailing": {"Trailing spaces "}, "Trailing": {"Merging"}}, {"trailing": {"Trailing spaces ", "Merging"}}),
        (
            {"inner  spaces": {"Inner spaces"}, "Inner  Spaces": {"Are preserved"}},
            {"inner  spaces": {"Inner spaces", "Are preserved"}},
        ),
        (
            {"ja": {"こんにちは"}, "JA": {"こんばんは"}, "Ja": {"おはようございます"}},
            {"ja": {"こんにちは", "こんばんは", "おはようございます"}},
        ),
        (
            {"de": {"Guten Tag"}, "DE": {"Guten Morgen", "Guten Abend"}},
            {"de": {"Guten Tag", "Guten Morgen", "Guten Abend"}},
        ),
    ],
)
def test_multilangstring_language_merging(input_dict: dict, expected_dict: dict):
    mls = MultiLangString(mls_dict=input_dict)
    assert mls.mls_dict == expected_dict, "Languages with different cases should be merged correctly"
