"""The langstring module provides the LangString class to encapsulate a string with its language information.

This module is designed to work with text strings and their associated language tags, offering functionalities
such as validation of language tags, handling of empty strings and language tags based on control flags, and
logging of warnings for invalid language tags. It utilizes the langcodes library for validating language tags and
the loguru library for logging warnings in case of invalid language tags.

Control flags from the langstring_control module are used to enforce certain behaviors like ensuring non-empty
text and valid language tags. These flags can be set externally to alter the behavior of the LangString class.

:Example:

    # Create a LangString object
    lang_str = LangString("Hello, World!", "en")

    # Print the string representation
    print(lang_str.to_string())  # Output: '"Hello, World!"@en'
"""
import nltk
from langcodes import Language
from nltk.corpus import wordnet

from .flags import LangStringFlag
from .setlangstring import SetLangString
from .utils.validation_base import ValidationBase


class LangString(ValidationBase):
    """A class to encapsulate a string with its language information.

    This class provides functionality to associate a text string with a language tag, offering methods for string
    representation, equality comparison, and hashing. The behavior of this class is influenced by control flags
    from the Controller class, which can enforce non-empty text, valid language tags, and other constraints.

    :ivar text: The text string.
    :vartype text: Optional[str]
    :ivar lang: The language tag of the text.
    :vartype lang: str
    """

    # Ignoring mypy error for practicality: subclasses narrow type for specific use, not affecting functionality.
    def _get_flags_type(self) -> type[LangStringFlag]:  # type: ignore
        """Retrieve the control class and its corresponding flags enumeration used in the LangString class.

        This method provides the specific control class (Controller) and the flags enumeration (LangStringFlag)
        that are used for configuring and validating the LangString instances. It is essential for the functioning of
        the ValidationBase methods, which rely on these control settings.

        :return: A tuple containing the Controller class and the LangStringFlag enumeration.
        :rtype: tuple[type[Controller], type[LangStringFlag]]
        """
        return LangStringFlag

    def __init__(self, text: str = "", lang: str = None) -> None:
        """Initialize a new LangString object with text and an optional language tag.

        The behavior of this method is influenced by control flags set in Controller. For instance, if the
        DEFINED_TEXT flag is enabled, an empty 'text' string will raise a ValueError.

        :param text: The text string, defaults to an empty string.
        :type text: Optional[str]
        :param lang: The language tag of the text.
        :type lang: str
        :raises TypeError: If 'text' is not a string, or 'lang' is not a string or None.
        :raises ValueError: If 'text' is empty and DEFINED_TEXT is enabled; if 'lang' is empty and ENSURE_ANY_LANG is
                            enabled; or if 'lang' is invalid and VALID_LANG is enabled.
        """
        self.text: str = text

        if lang:
            self.lang: str = lang
        else:
            raise ValueError("Language not defined. LangStrings are expected to have an associated language.")

        self._validate_arguments(self.text, self.lang)
        self._validate_ensure_text(self.text)
        self._validate_ensure_any_lang(self.lang)
        self._validate_ensure_valid_lang(self.lang)

    def to_string(self) -> str:
        """Convert the LangString object to a string representation.

        This method is a convenience wrapper for the __str__ method.

        :return: The string representation of the LangString object, including the language tag if present.
        :rtype: str
        """
        return self.__str__()

    def __str__(self) -> str:
        """Define the string representation of the LangString object.

        :return: The string representation of the LangString object. Format: '"text"@lang' or 'text' if lang is None.
        :rtype: str
        """
        if self.lang is None:
            return f"{self.text}"
        return f'"{self.text}"@{self.lang}'

    def __eq__(self, other: object) -> bool:
        """Check equality of this LangString with another object.

        :param other: Another object to compare with.
        :type other: object
        :return: True if 'other' is a LangString object with the same text and language tag, False otherwise.
        :rtype: bool
        """
        if not isinstance(other, LangString):
            return NotImplemented
        return self.text == other.text and self.lang == other.lang

    def __hash__(self) -> int:
        """Generate a hash value for a LangString object.

        :return: The hash value of the LangString object, based on its text and language tag.
        :rtype: int
        """
        return hash((self.text, self.lang))

    def get_synsets(self) -> list[SetLangString]:
        # Check if this is expensive
        nltk.download("omw-1.4", quiet=True)

        synsets_list: list[SetLangString] = []

        std_lang = Language.get(self.lang).to_alpha3()
        synsets = wordnet.synonyms(self.text, lang=std_lang)

        for synset in synsets:
            if synset:
                synsets_list.append(SetLangString(synset, self.lang))

        return synsets_list
