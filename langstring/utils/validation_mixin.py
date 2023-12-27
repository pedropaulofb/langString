"""This module defines the ValidationMixin class.

The ValidationMixin provides validation functionalities for LangString and MultiLangString classes.
It includes methods to validate argument types, ensure text and language requirements, and check the validity of
language tags based on configurable control flags.

The mixin is designed to be used with classes that handle language strings and need to enforce specific validation
rules. It leverages control flags from a control class (like LangStringControl or MultiLangStringControl) to
determine the validation behavior.

Classes:
    ValidationMixin: A mixin class providing validation methods for LangString and MultiLangString classes.

Example Usage:
    class LangString(ValidationMixin):
        # LangString implementation
        ...

    class MultiLangString(ValidationMixin):
        # MultiLangString implementation
        ...
"""
from abc import abstractmethod

from langcodes import tag_is_valid
from loguru import logger


class ValidationMixin:
    """A mixin class that provides validation methods for classes handling language strings.

    It ensures that the text and language arguments meet specific criteria, such as type correctness, non-emptiness,
    and language tag validity. The validation rules are determined by control flags from a control class.
    """

    @abstractmethod
    def _get_control_and_flags_type(self) -> None:
        """Abstract method that must be implemented by subclasses.

        It should return the control class and its flags enumeration used for validation.

        This method is intended to be overridden in subclasses to return a tuple containing the specific control
        class and the corresponding flags enumeration. These are used for configuring and validating instances of
        the subclass. The exact types of the control class and flags enumeration will depend on the subclass.

        Subclasses should return:
            - The control class that manages configuration flags.
            - The flags enumeration that defines these flags.
        """

    def _validate_arguments_types(self) -> None:
        """Validate the types of the 'text' and 'lang' arguments.

        Ensures that 'text' is a string and 'lang' is either a string or None. Raises a TypeError if the types do not
        match the expected types. Additionally, checks if 'text' is not None.

        :raises TypeError: If 'text' is not a string or if 'lang' is provided and is not a string or None.
        :raises ValueError: If 'text' is None.
        """
        if not isinstance(self.text, str):
            raise TypeError(f"Expected 'text' to be of type str, but got {type(self.text).__name__}.")
        if self.lang is not None and not isinstance(self.lang, str):
            raise TypeError(f"Expected 'lang' to be of type str, but got {type(self.lang).__name__}.")

        # Text field cannot be empty
        if self.text is None:
            raise ValueError(f"{self.__class__.__name__}'s 'text' field cannot be None.")

    def _validate_ensure_text(self) -> None:
        """Validate the 'text' argument based on the ENSURE_TEXT control flag.

        Checks if the 'text' field is empty and raises a ValueError or logs a warning depending on the ENSURE_TEXT and
        VERBOSE_MODE flags set in the control class.

        :raises ValueError: If ENSURE_TEXT is enabled and 'text' is an empty string.
        """
        control, flags = self._get_control_and_flags_type()

        if self.text == "":
            if control.get_flag(flags.VERBOSE_MODE):
                warning_msg = f"{self.__class__.__name__}'s 'text' field received empty string."
                logger.warning(warning_msg)
            if control.get_flag(flags.ENSURE_TEXT):
                raise ValueError(
                    f"ENSURE_TEXT enabled: {self.__class__.__name__}'s 'text' field cannot receive empty string."
                )

    def _validate_ensure_any_lang(self) -> None:
        """Validate the 'lang' argument based on the ENSURE_ANY_LANG and ENSURE_VALID_LANG control flags.

        Checks if the 'lang' field is empty and raises a ValueError or logs a warning depending on the ENSURE_ANY_LANG,
        ENSURE_VALID_LANG, and VERBOSE_MODE flags set in the control class.

        :raises ValueError: If ENSURE_ANY_LANG or ENSURE_VALID_LANG is enabled and 'lang' is an empty string.
        """
        control, flags = self._get_control_and_flags_type()

        if self.lang == "":
            if control.get_flag(flags.VERBOSE_MODE):
                warning_msg = f"{self.__class__.__name__}'s 'lang' field received empty string."
                logger.warning(warning_msg)
            if control.get_flag(flags.ENSURE_ANY_LANG):
                raise ValueError(
                    f"ENSURE_ANY_LANG enabled: {self.__class__.__name__}'s 'lang' field cannot receive empty string."
                )
            if control.get_flag(flags.ENSURE_VALID_LANG):
                raise ValueError(
                    f"ENSURE_VALID_LANG enabled: {self.__class__.__name__}'s 'lang' field cannot receive empty string."
                )

    def _validate_ensure_valid_lang(self) -> None:
        """Validate the language tag for its validity.

        This method checks if the language tag is valid. If the tag is invalid, it raises a warning or an error
        depending on the control flags set in the control class.

        :raises ValueError: If ENSURE_VALID_LANG is enabled and the language tag is invalid.
        """
        control, flags = self._get_control_and_flags_type()

        if self.lang and not tag_is_valid(self.lang):
            if control.get_flag(flags.VERBOSE_MODE):
                warning_msg = f"Invalid language tag '{self.lang}' used."
                logger.warning(warning_msg)
            if control.get_flag(flags.ENSURE_VALID_LANG):
                raise ValueError(
                    f"ENSURE_VALID_LANG enabled: {self.__class__.__name__}'s 'lang' field cannot be invalid."
                )
