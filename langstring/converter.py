"""
The `converter` module provides a utility class for converting between different string types used in language \
processing.

The `Converter` class facilitates conversions between `LangString`, `SetLangString`, and `MultiLangString` objects.
These objects represent various ways of handling language-tagged strings, which are common in applications dealing with
multilingual data. The `Converter` class methods enable seamless and efficient transformations of these string types,
ensuring compatibility and ease of use in various language processing tasks.

Classes:
    Converter: Provides methods for converting between `LangString`, `SetLangString`, and `MultiLangString`.

Usage:
    The `Converter` class is used as a utility and should not be instantiated. Instead, its class methods are called
    directly to perform conversions. For example, `Converter.to_langstring(arg_obj)` where `arg_obj` could
    be an instance of `SetLangString` or `MultiLangString`.

Examples:
    # Convert a string to a LangString using the 'manual' method:
    >>> langstring = Converter.from_string_to_langstring("manual", "Hello", "en")
    >>> print(langstring)  #Output: "Hello"@en

    # Convert a list of strings to a list of LangStrings using the 'parse' method:
    >>> langstrings = Converter.from_strings_to_langstrings("parse", ["Hello@en", "Bonjour@fr"], separator="@")
    >>> for ls in langstrings:
    >>>     print(ls)  #Output: "Hello"@en
    >>>                #        "Bonjour"@fr

    # Convert a SetLangString to a MultiLangString:
    >>> setlangstring = SetLangString({"Hello", "Hi"}, "en")
    >>> multilangstring = Converter.from_setlangstring_to_multilangstring(setlangstring)
    >>> print(multilangstring)  #Output: {'Hello', 'Hi'}@en

Note:
    The module assumes that the argument objects are well-formed instances of their respective classes. Error handling
    is provided for type mismatches, but not for malformed objects.

This module is part of a larger package dealing with language processing and RDF data manipulation, providing
foundational tools for handling multilingual text data in various formats.
"""

from typing import Optional

from .langstring import LangString
from .multilangstring import MultiLangString
from .setlangstring import SetLangString
from .utils.non_instantiable import NonInstantiable
from .utils.validators import TypeValidator


class Converter(metaclass=NonInstantiable):
    """
    A utility class for converting between different string types used in language processing.

    This class provides methods to convert between `LangString`, `SetLangString`, and `MultiLangString` types.
    It is designed to be non-instantiable as it serves as a utility class with class methods only.

    Examples:
        # Convert a string to a LangString using the 'manual' method:
        >>> langstring = Converter.from_string_to_langstring("manual", "Hello", "en")
        >>> print(langstring)  #Output: "Hello"@en

        # Convert a list of strings to a list of LangStrings using the 'parse' method:
        >>> langstrings = Converter.from_strings_to_langstrings("parse", ["Hello@en", "Bonjour@fr"], separator="@")
        >>> for ls in langstrings:
        >>>     print(ls)  #Output: "Hello"@en
        >>>                #        "Bonjour"@fr

        # Convert a SetLangString to a MultiLangString:
        >>> setlangstring = SetLangString({"Hello", "Hi"}, "en")
        >>> multilangstring = Converter.from_setlangstring_to_multilangstring(setlangstring)
        >>> print(multilangstring)  #Output: {'Hello', 'Hi'}@en
    """

    # ---------------------------------------------
    # Strings' Conversion Methods
    # ---------------------------------------------

    @classmethod
    def from_string_to_langstring(
        cls, method: str, input_string: str, lang: Optional[str] = None, separator: str = "@"
    ) -> LangString:
        """
        Convert a string to a LangString using the specified method.

        :param method: The method to use for conversion ('manual' or 'parse').
        :type method: str
        :param input_string: The text to be converted.
        :type input_string: str
        :param lang: The language code (used only with 'manual' method).
        :type lang: Optional[str]
        :param separator: The separator used to split the text and language (used only with 'parse' method).
        :type separator: str
        :return: A LangString object with the converted text and language.
        :rtype: LangString
        :raises ValueError: If the method is unknown.

        Examples:
            # Convert a string to a LangString using the 'manual' method:
            >>> langstring = Converter.from_string_to_langstring("manual", "Hello", "en")
            >>> print(langstring)  # Output: "Hello"@en

            # Convert a string to a LangString using the 'parse' method:
            >>> langstring = Converter.from_string_to_langstring("parse", "Hello@en")
            >>> print(langstring)  # Output: "Hello"@en
        """
        TypeValidator.validate_type_single(input_string, str)
        TypeValidator.validate_type_single(method, str)
        TypeValidator.validate_type_single(lang, str, optional=True)
        TypeValidator.validate_type_single(separator, str)

        if method == "manual":
            return cls.from_string_to_langstring_manual(input_string, lang)

        if method == "parse":
            return cls.from_string_to_langstring_parse(input_string, separator)

        raise ValueError(f"Unknown method: {method}. Valid methods are 'manual' and 'parse'.")

    @TypeValidator.validate_type_decorator
    @staticmethod
    def from_string_to_langstring_manual(input_string: Optional[str], lang: Optional[str]) -> LangString:
        """
        Convert a string to a LangString with the specified language.

        :param input_string: The text to be converted.
        :type input_string: str
        :param lang: The language code.
        :type lang: Optional[str]
        :return: A LangString object with the provided text and language.
        :rtype: LangString

        Examples:
            # Convert a string to a LangString with the specified language:
            >>> langstring = Converter.from_string_to_langstring_manual("Hello", "en")
            >>> print(langstring)  # Output: "Hello"@en
        """
        return LangString(text=input_string or "", lang=lang or "")

    @TypeValidator.validate_type_decorator
    @staticmethod
    def from_string_to_langstring_parse(input_string: str, separator: str = "@") -> LangString:
        """
        Convert a string to a LangString by parsing it with the given separator.

        This function splits the input string into text and language components based on the last occurrence of the
        specified separator. If the separator is not found, the entire string is considered as text and lang is set
        to "" (empty string).

        :param input_string: The text to be converted.
        :type input_string: str
        :param separator: The separator used to split the text and language.
        :type separator: str
        :return: A LangString object with the parsed text and language.
        :rtype: LangString

        Examples:
            # Convert a string to a LangString by parsing it with the given separator:
            >>> langstring = Converter.from_string_to_langstring_parse("Hello@en", "@")
            >>> print(langstring)  # Output: "Hello"@en

            # Convert a string to a LangString with no separator found:
            >>> langstring = Converter.from_string_to_langstring_parse("Hello", "@")
            >>> print(langstring)  # Output: "Hello"@
        """
        if separator not in input_string:
            text, lang = input_string, ""
        elif separator == "":
            text, lang = input_string, ""
        else:
            text, lang = input_string.rsplit(separator, 1)

        return LangString(text=text, lang=lang)

    @classmethod
    def from_strings_to_langstrings(
        cls, method: str, strings: list[str], lang: Optional[str] = None, separator: str = "@"
    ) -> list[LangString]:
        """
        Convert a list of strings to a list of LangStrings using the specified method.

        :param method: The method to use for conversion ('manual' or 'parse').
        :type method: str
        :param strings: List of strings to be converted.
        :type strings: list[str]
        :param lang: The language code for 'manual' method.
        :type lang: Optional[str]
        :param separator: The separator used in 'parse' method.
        :type separator: str
        :return: A list of LangString objects.
        :rtype: list[LangString]
        :raises ValueError: If an unknown method is specified.
        :raises TypeError: If the input types are incorrect.

        Examples:
            # Convert a list of strings to a list of LangStrings using the 'manual' method:
            >>> langstrings = Converter.from_strings_to_langstrings("manual", ["Hello", "Hi"], "en")
            >>> for ls in langstrings:
            >>>     print(ls)  # Output: "Hello"@en
            >>>                #         "Hi"@en

            # Convert a list of strings to a list of LangStrings using the 'parse' method:
            >>> langstrings = Converter.from_strings_to_langstrings("parse", ["Hello@en", "Bonjour@fr"], separator="@")
            >>> for ls in langstrings:
            >>>     print(ls)  # Output: "Hello"@en
            >>>                #         "Bonjour"@fr
        """
        TypeValidator.validate_type_iterable(strings, list, str)
        TypeValidator.validate_type_single(method, str)
        TypeValidator.validate_type_single(lang, str, optional=True)
        TypeValidator.validate_type_single(separator, str)

        langstrings = []
        for string in strings:
            langstring = cls.from_string_to_langstring(method, string, lang, separator)
            langstrings.append(langstring)

        return langstrings

    @classmethod
    def from_strings_to_setlangstring(cls, strings: list[str], lang: Optional[str] = None) -> SetLangString:
        """
        Convert a list of strings to a SetLangString using the 'manual' method.

        :param strings: List of strings to be converted.
        :type strings: list[str]
        :param lang: Language code for the 'manual' method. Optional.
        :type lang: Optional[str]
        :return: A SetLangString object.
        :rtype: SetLangString

        Examples:
            # Convert a list of strings to a SetLangString using the 'manual' method:
            >>> setlangstring = Converter.from_strings_to_setlangstring(["Hello", "Hi"], "en")
            >>> print(setlangstring)  # Output: {'Hello', 'Hi'}@en
        """
        TypeValidator.validate_type_iterable(strings, list, str)
        TypeValidator.validate_type_single(lang, str, optional=True)

        return SetLangString(set(strings), lang=lang or "")

    @classmethod
    def from_strings_to_multilangstring(
        cls, method: str, strings: list[str], lang: Optional[str] = None, separator: str = "@"
    ) -> MultiLangString:
        """
        Convert a list of strings to a MultiLangString using the specified method.

        :param method: Method to use for conversion ("manual", or "parse").
        :type method: str
        :param strings: List of strings to be converted.
        :type strings: list[str]
        :param lang: Language code for the "manual" method. Optional.
        :type lang: Optional[str]
        :param separator: Separator for the "parse" method. Default is "@".
        :type separator: str
        :return: A MultiLangString object.
        :rtype: MultiLangString

        Examples:
            # Convert a list of strings to a MultiLangString using the 'manual' method:
            >>> multilangstring = Converter.from_strings_to_multilangstring("manual", ["Hello", "Hi"], "en")
            >>> print(multilangstring)  # Output: {'Hello', 'Hi'}@en

            # Convert a list of strings to a MultiLangString using the 'parse' method:
            >>> multilangstring = Converter.from_strings_to_multilangstring("parse", ["Hello@en", "Bonjour@fr"],
                                                                                                        separator="@")
            >>> print(multilangstring)  # Output: {'Hello', 'Bonjour'}@en,fr
        """
        TypeValidator.validate_type_single(method, str)
        TypeValidator.validate_type_iterable(strings, list, str)
        TypeValidator.validate_type_single(lang, str, optional=True)
        TypeValidator.validate_type_single(separator, str)

        multilangstring = MultiLangString()

        for string in strings:
            langstring = cls.from_string_to_langstring(method, string, lang, separator)
            multilangstring.add_langstring(langstring)

        return multilangstring

    # ---------------------------------------------
    # LangStrings' Conversion Methods
    # ---------------------------------------------

    @TypeValidator.validate_type_decorator
    @staticmethod
    def from_langstring_to_string(
        arg: LangString, print_quotes: Optional[bool] = None, separator: str = "@", print_lang: Optional[bool] = None
    ) -> str:
        """
        Convert a LangString to a string.

        :param arg: The LangString to be converted.
        :type arg: LangString
        :param print_quotes: Whether to include quotes around the text in the output.
        :type print_quotes: Optional[bool]
        :param separator: The separator to use between text and language.
        :type separator: str
        :param print_lang: Whether to include the language in the output.
        :type print_lang: Optional[bool]
        :return: The string representation of the LangString.
        :rtype: str

        Examples:
            # Convert a LangString to a string with quotes and language:
            >>> langstring = LangString("Hello", "en")
            >>> string = Converter.from_langstring_to_string(langstring, print_quotes=True, separator="@")
            >>> print(string)  # Output: "Hello"@en

            # Convert a LangString to a string without quotes and language:
            >>> string = Converter.from_langstring_to_string(langstring, print_quotes=False, separator="@",
                                                                                                    print_lang=False)
            >>> print(string)  # Output: "Hello"
        """
        return arg.to_string(print_quotes=print_quotes, separator=separator, print_lang=print_lang)

    @staticmethod
    def from_langstrings_to_strings(
        arg: list[LangString],
        print_quotes: Optional[bool] = None,
        separator: str = "@",
        print_lang: Optional[bool] = None,
    ) -> list[str]:
        """
        Convert a list of LangStrings to a list of strings.

        :param arg: List of LangStrings to be converted.
        :type arg: list[LangString]
        :param print_quotes: Whether to include quotes around the text in the output.
        :type print_quotes: Optional[bool]
        :param separator: The separator to use between text and language.
        :type separator: str
        :param print_lang: Whether to include the language in the output.
        :type print_lang: Optional[bool]
        :return: A list of string representations of the LangStrings.
        :rtype: list[str]

        Examples:
            # Convert a list of LangStrings to a list of strings with quotes and language:
            >>> langstrings = [LangString("Hello", "en"), LangString("Bonjour", "fr")]
            >>> strings = Converter.from_langstrings_to_strings(langstrings, print_quotes=True, separator="@")
            >>> for s in strings:
            >>>     print(s)  # Output: "Hello"@en
            >>>                #         "Bonjour"@fr

            # Convert a list of LangStrings to a list of strings without quotes and language:
            >>> strings = Converter.from_langstrings_to_strings(langstrings, print_quotes=False, separator="@",
                                                                                                    print_lang=False)
            >>> for s in strings:
            >>>     print(s)  # Output: "Hello"
            >>>                #         "Bonjour"
        """
        TypeValidator.validate_type_iterable(arg, list, LangString)
        TypeValidator.validate_type_single(print_quotes, bool, optional=True)
        TypeValidator.validate_type_single(separator, str)
        TypeValidator.validate_type_single(print_lang, bool, optional=True)

        strings = []
        for langstring in arg:
            strings.append(langstring.to_string(print_quotes=print_quotes, separator=separator, print_lang=print_lang))
        return strings

    @TypeValidator.validate_type_decorator
    @staticmethod
    def from_langstring_to_setlangstring(arg: LangString) -> SetLangString:
        """
        Convert a LangString to a SetLangString.

        This method creates a SetLangString from a LangString. The resulting SetLangString contains the text of the
        LangString in a set and retains its language.

        :param arg: The LangString to be converted.
        :type arg: LangString
        :return: A SetLangString containing the text from the arg LangString.
        :rtype: SetLangString
        :raises TypeError: If the arg is not of type LangString.

        Examples:
            # Convert a LangString to a SetLangString:
            >>> langstring = LangString("Hello", "en")
            >>> setlangstring = Converter.from_langstring_to_setlangstring(langstring)
            >>> print(setlangstring)  # Output: {'Hello'}@en
        """
        return SetLangString(texts={arg.text}, lang=arg.lang)

    @staticmethod
    def from_langstrings_to_setlangstring(arg: list[LangString]) -> SetLangString:
        """
        Convert a list of LangStrings to a SetLangString.

        This method merges a list of LangStrings into a single SetLangString. The resulting SetLangString contains
        all the unique texts from the LangStrings and retains a common language if all LangStrings have the same
        language.

        :param arg: The list of LangStrings to be converted.
        :type arg: list[LangString]
        :return: A SetLangString containing the texts from the list of LangStrings.
        :rtype: SetLangString
        :raises ValueError: If the LangStrings have different languages.
        :raises TypeError: If the input types are incorrect.

        Examples:
            # Convert a list of LangStrings to a SetLangString:
            >>> langstrings = [LangString("Hello", "en"), LangString("Hi", "en")]
            >>> setlangstring = Converter.from_langstrings_to_setlangstring(langstrings)
            >>> print(setlangstring)  # Output: {'Hello', 'Hi'}@en
        """
        TypeValidator.validate_type_iterable(arg, list, LangString)
        merged_langstrings = LangString.merge_langstrings(arg)

        new_texts = set()
        new_lang = set()

        for langstring in merged_langstrings:
            new_texts.add(langstring.text)
            new_lang.add(langstring.lang)

        if len(new_lang) > 1:
            raise ValueError("The conversion can only be performed from LangStrings with the same language.")

        final_lang = "" if not len(new_lang) else new_lang.pop()

        return SetLangString(texts=new_texts, lang=final_lang)

    @classmethod
    def from_langstrings_to_setlangstrings(cls, arg: list[LangString]) -> list[SetLangString]:
        """
        Convert a list of LangStrings to a list of SetLangStrings.

        This method merges a list of LangStrings into multiple SetLangStrings based on their languages. Each
        SetLangString contains all the unique texts for a specific language from the LangStrings.

        :param arg: The list of LangStrings to be converted.
        :type arg: list[LangString]
        :return: A list of SetLangStrings, each containing texts of a specific language from the LangStrings.
        :rtype: list[SetLangString]
        :raises TypeError: If the input types are incorrect.

        Examples:
            # Convert a list of LangStrings to a list of SetLangStrings:
            >>> langstrings = [LangString("Hello", "en"), LangString("Bonjour", "fr")]
            >>> setlangstrings = Converter.from_langstrings_to_setlangstrings(langstrings)
            >>> for sls in setlangstrings:
            >>>     print(sls)  # Output: {'Hello'}@en
            >>>                 #         {'Bonjour'}@fr
        """
        TypeValidator.validate_type_iterable(arg, list, LangString)

        merged_lagnstrings = LangString.merge_langstrings(arg)

        setlangstrings = []
        for langstring in merged_lagnstrings:
            setlangstrings.append(cls.from_langstrings_to_setlangstring([langstring]))

        return SetLangString.merge_setlangstrings(setlangstrings)

    @TypeValidator.validate_type_decorator
    @staticmethod
    def from_langstring_to_multilangstring(arg: LangString) -> MultiLangString:
        """
        Convert a LangString to a MultiLangString.

        This method takes a single LangString and converts it into a MultiLangString. The resulting MultiLangString
        contains the text and language of the arg LangString.

        :param arg: The LangString to be converted.
        :type arg: LangString
        :return: A MultiLangString containing the text and language from the arg LangString.
        :rtype: MultiLangString
        :raises TypeError: If the arg is not of type LangString.

        Examples:
            # Convert a LangString to a MultiLangString:
            >>> langstring = LangString("Hello", "en")
            >>> multilangstring = Converter.from_langstring_to_multilangstring(langstring)
            >>> print(multilangstring)  # Output: {'Hello'}@en
        """
        new_mls_dict: dict[str, set[str]] = {arg.lang: {arg.text}}
        return MultiLangString(mls_dict=new_mls_dict, pref_lang=arg.lang)

    @staticmethod
    def from_langstrings_to_multilangstring(arg: list[LangString]) -> MultiLangString:
        """
        Convert a list of LangStrings to a MultiLangString.

        This method merges a list of LangStrings into a single MultiLangString. The resulting MultiLangString
        contains all the unique texts and languages from the LangStrings.

        :param arg: The list of LangStrings to be converted.
        :type arg: list[LangString]
        :return: A MultiLangString containing the texts and languages from the list of LangStrings.
        :rtype: MultiLangString
        :raises TypeError: If the input types are incorrect.

        Examples:
            # Convert a list of LangStrings to a MultiLangString:
            >>> langstrings = [LangString("Hello", "en"), LangString("Bonjour", "fr")]
            >>> multilangstring = Converter.from_langstrings_to_multilangstring(langstrings)
            >>> print(multilangstring)  # Output: {'Hello'}@en, {'Bonjour'}@fr
        """
        TypeValidator.validate_type_iterable(arg, list, LangString)
        new_mls = MultiLangString()
        merged_langstrings = LangString.merge_langstrings(arg)

        for langstring in merged_langstrings:
            new_mls.add_langstring(langstring)

        return new_mls

    # ---------------------------------------------
    # SetLangStrings' Conversion Methods
    # ---------------------------------------------

    @TypeValidator.validate_type_decorator
    @staticmethod
    def from_setlangstring_to_string(arg: SetLangString) -> str:
        """
        Convert a SetLangString to a string.

        :param arg: The SetLangString to be converted.
        :type arg: SetLangString
        :return: The string representation of the SetLangString.
        :rtype: str

        Examples:
            # Convert a SetLangString to a string:
            >>> setlangstring = SetLangString({"Hello", "Hi"}, "en")
            >>> string = Converter.from_setlangstring_to_string(setlangstring)
            >>> print(string)  # Output: {'Hello', 'Hi'}@en
        """
        return arg.__str__()

    @TypeValidator.validate_type_decorator
    @staticmethod
    def from_setlangstring_to_strings(
        arg: SetLangString, print_quotes: Optional[bool] = None, separator: str = "@", print_lang: Optional[bool] = None
    ) -> list[str]:
        """
        Convert a SetLangString to a list of strings.

        :param arg: The SetLangString to be converted.
        :type arg: SetLangString
        :param print_quotes: Whether to include quotes around the text in the output.
        :type print_quotes: Optional[bool]
        :param separator: The separator to use between text and language.
        :type separator: str
        :param print_lang: Whether to include the language in the output.
        :type print_lang: Optional[bool]
        :return: A list of string representations of the SetLangString.
        :rtype: list[str]

        Examples:
            # Convert a SetLangString to a list of strings with quotes and language:
            >>> setlangstring = SetLangString({"Hello", "Hi"}, "en")
            >>> strings = Converter.from_setlangstring_to_strings(setlangstring, print_quotes=True, separator="@")
            >>> for s in strings:
            >>>     print(s)  # Output: "Hello"@en
            >>>                #         "Hi"@en

            # Convert a SetLangString to a list of strings without quotes and language:
            >>> strings = Converter.from_setlangstring_to_strings(setlangstring, print_quotes=False, separator="@",
                                                                                                    print_lang=False)
            >>> for s in strings:
            >>>     print(s)  # Output: Hello
            >>>                #         Hi
        """
        return arg.to_strings(print_quotes=print_quotes, separator=separator, print_lang=print_lang)

    @staticmethod
    def from_setlangstrings_to_strings(
        arg: list[SetLangString],
        print_quotes: Optional[bool] = None,
        separator: str = "@",
        print_lang: Optional[bool] = None,
    ) -> list[str]:
        """
        Convert a list of SetLangStrings to a list of strings.

        :param arg: List of SetLangStrings to be converted.
        :type arg: list[SetLangString]
        :param print_quotes: Whether to include quotes around the text in the output.
        :type print_quotes: Optional[bool]
        :param separator: The separator to use between text and language.
        :type separator: str
        :param print_lang: Whether to include the language in the output.
        :type print_lang: Optional[bool]
        :return: A list of string representations of the SetLangStrings.
        :rtype: list[str]

        Examples:
            # Convert a list of SetLangStrings to a list of strings with quotes and language:
            >>> setlangstrings = [SetLangString({"Hello"}, "en"), SetLangString({"Bonjour"}, "fr")]
            >>> strings = Converter.from_setlangstrings_to_strings(setlangstrings, print_quotes=True, separator="@")
            >>> for s in strings:
            >>>     print(s)  # Output: "Hello"@en
            >>>                #         "Bonjour"@fr

            # Convert a list of SetLangStrings to a list of strings without quotes and language:
            >>> strings = Converter.from_setlangstrings_to_strings(setlangstrings, print_quotes=False, separator="@",
                                                                                                    print_lang=False)
            >>> for s in strings:
            >>>     print(s)  # Output: Hello
            >>>                #         Bonjour
        """
        TypeValidator.validate_type_iterable(arg, list, SetLangString)
        TypeValidator.validate_type_single(print_quotes, bool, optional=True)
        TypeValidator.validate_type_single(separator, str)
        TypeValidator.validate_type_single(print_lang, bool, optional=True)

        merged_setlangstrings = SetLangString.merge_setlangstrings(arg)

        strings = []
        for setlangstring in merged_setlangstrings:
            strings.extend(
                setlangstring.to_strings(print_quotes=print_quotes, separator=separator, print_lang=print_lang)
            )
        return strings

    @TypeValidator.validate_type_decorator
    @staticmethod
    def from_setlangstring_to_langstrings(arg: SetLangString) -> list[LangString]:
        """
        Convert a SetLangString to a list of LangStrings.

        This method takes a SetLangString and converts it into a list of LangStrings, each containing one of the texts
        from the SetLangString and its associated language.

        :param arg: The SetLangString to be converted.
        :type arg: SetLangString
        :return: A list of LangStrings, each corresponding to a text in the arg SetLangString.
        :rtype: list[LangString]
        :raises TypeError: If the arg is not of type SetLangString.

        Examples:
            # Convert a SetLangString to a list of LangStrings:
            >>> setlangstring = SetLangString({"Hello", "Hi"}, "en")
            >>> langstrings = Converter.from_setlangstring_to_langstrings(setlangstring)
            >>> for ls in langstrings:
            >>>     print(ls)  # Output: "Hi"@en
            >>>                #         "Hello"@en

        Note:
            The order of elements in the output list is not guaranteed, as sets do not maintain order.
        """
        return arg.to_langstrings()

    @staticmethod
    def from_setlangstrings_to_langstrings(arg: list[SetLangString]) -> list[LangString]:
        """
        Convert a list of SetLangStrings to a list of LangStrings.

        This method merges a list of SetLangStrings into a single list of LangStrings. Each LangString in the output
        list corresponds to one of the texts in the SetLangStrings, retaining their associated languages.

        :param arg: The list of SetLangStrings to be converted.
        :type arg: list[SetLangString]
        :return: A list of LangStrings, each corresponding to a text in the SetLangStrings.
        :rtype: list[LangString]
        :raises TypeError: If the input types are incorrect.

        Examples:
            # Convert a list of SetLangStrings to a list of LangStrings:
            >>> setlangstrings = [SetLangString({"Hello"}, "en"), SetLangString({"Bonjour"}, "fr")]
            >>> langstrings = Converter.from_setlangstrings_to_langstrings(setlangstrings)
            >>> for ls in langstrings:
            >>>     print(ls)  # Output: "Hello"@en
            >>>                #         "Bonjour"@fr
        """
        TypeValidator.validate_type_iterable(arg, list, SetLangString)
        merged_setlangstrings = SetLangString.merge_setlangstrings(arg)

        langstrings = []
        for setlangstring in merged_setlangstrings:
            langstrings.extend(setlangstring.to_langstrings())
        return langstrings

    @TypeValidator.validate_type_decorator
    @staticmethod
    def from_setlangstring_to_multilangstring(arg: SetLangString) -> MultiLangString:
        """
        Convert a SetLangString to a MultiLangString.

        This method creates a MultiLangString from a SetLangString. The resulting MultiLangString contains all texts
        from the SetLangString, associated with its language.

        :param arg: The SetLangString to be converted.
        :type arg: SetLangString
        :return: A MultiLangString containing all texts from the arg SetLangString.
        :rtype: MultiLangString
        :raises TypeError: If the arg is not of type SetLangString.

        Examples:
            # Convert a SetLangString to a MultiLangString:
            >>> setlangstring = SetLangString({"Hello", "Hi"}, "en")
            >>> multilangstring = Converter.from_setlangstring_to_multilangstring(setlangstring)
            >>> print(multilangstring)  # Output: {'Hello', 'Hi'}@en
        """
        new_mls = MultiLangString()
        new_mls.add_setlangstring(arg)
        return new_mls

    @staticmethod
    def from_setlangstrings_to_multilangstring(arg: list[SetLangString]) -> MultiLangString:
        """
        Convert a list of SetLangString objects to a MultiLangString object.

        If there are different casings for the same lang tag among the SetLangString objects in the input list,
        the casefolded version of the lang tag is used. If only a single case is used, that case is adopted.

        :param arg: List of SetLangString instances to be converted.
        :type arg: list[SetLangString]
        :return: A MultiLangString instance with aggregated texts under normalized language tags.
        :rtype: MultiLangString
        :raises TypeError: If the input types are incorrect.

        Examples:
            # Convert a list of SetLangStrings to a MultiLangString:
            >>> setlangstrings = [SetLangString({"Hello"}, "en"), SetLangString({"Bonjour"}, "fr")]
            >>> multilangstring = Converter.from_setlangstrings_to_multilangstring(setlangstrings)
            >>> print(multilangstring)  # Output: {'Hello'}@en, {'Bonjour'}@fr
        """
        TypeValidator.validate_type_iterable(arg, list, SetLangString)
        merged_setlangstrings = SetLangString.merge_setlangstrings(arg)

        multilangstring = MultiLangString()
        for setlangstring in merged_setlangstrings:
            multilangstring.add_setlangstring(setlangstring)
        return multilangstring

    # ---------------------------------------------
    # MultiLangStrings' Conversion Methods
    # ---------------------------------------------

    @TypeValidator.validate_type_decorator
    @staticmethod
    def from_multilangstring_to_string(arg: MultiLangString) -> str:
        """
        Convert a MultiLangString to a string.

        :param arg: The MultiLangString to be converted.
        :type arg: MultiLangString
        :return: The string representation of the MultiLangString.
        :rtype: str

        Examples:
            # Convert a MultiLangString to a string:
            >>> multilangstring = MultiLangString(mls_dict={"en": {"Hello", "Hi"}, "fr": {"Bonjour"}})
            >>> string = Converter.from_multilangstring_to_string(multilangstring)
            >>> print(string)  # Output: {'Hello', 'Hi'}@en, {'Bonjour'}@fr
        """
        return arg.__str__()

    @TypeValidator.validate_type_decorator
    @staticmethod
    def from_multilangstring_to_strings(
        arg: MultiLangString,
        langs: Optional[list[str]] = None,
        print_quotes: Optional[bool] = None,
        separator: str = "@",
        print_lang: Optional[bool] = None,
    ) -> list[str]:
        """
        Convert a MultiLangString to a list of strings.

        The method sorts the output strings both by language and by text within each language.

        :param arg: The MultiLangString to be converted.
        :type arg: MultiLangString
        :param langs: List of languages to include in the output. If None, all languages are included.
        :type langs: Optional[list[str]]
        :param print_quotes: Whether to include quotes around the text in the output.
        :type print_quotes: Optional[bool]
        :param separator: The separator to use between text and language.
        :type separator: str
        :param print_lang: Whether to include the language in the output.
        :type print_lang: Optional[bool]
        :return: A list of string representations of the MultiLangString.
        :rtype: list[str]

        Examples:
            # Convert a MultiLangString to a list of strings with quotes and language:
            >>> multilangstring = MultiLangString(mls_dict={"en": {"Hello", "Hi"}, "fr": {"Bonjour"}})
            >>> strings = Converter.from_multilangstring_to_strings(multilangstring, print_quotes=True, separator="@")
            >>> for s in strings:
            >>>     print(s)  # Output: "Bonjour"@fr
            >>>                #         "Hello"@en
            >>>                #         "Hi"@en

            # Convert a MultiLangString to a list of strings without quotes and language:
            >>> strings = Converter.from_multilangstring_to_strings(multilangstring, print_quotes=False, separator="@",
                                                                                                    print_lang=False)
            >>> for s in strings:
            >>>     print(s)  # Output: Bonjour
            >>>                #         Hello
            >>>                #         Hi

        Note:
            The output strings are sorted by language and by text within each language.
        """
        return arg.to_strings(langs=langs, print_quotes=print_quotes, separator=separator, print_lang=print_lang)

    @staticmethod
    def from_multilangstrings_to_strings(
        arg: list[MultiLangString],
        languages: Optional[list[str]] = None,
        print_quotes: bool = True,
        separator: str = "@",
        print_lang: bool = True,
    ) -> list[str]:
        """
        Convert a list of MultiLangStrings to a list of strings.

        The method sorts the output strings both by language and by text within each language.

        :param arg: List of MultiLangStrings to be converted.
        :type arg: list[MultiLangString]
        :param languages: List of languages to include in the output. If None, all languages are included.
        :type languages: Optional[list[str]]
        :param print_quotes: Whether to include quotes around the text in the output.
        :type print_quotes: bool
        :param separator: The separator to use between text and language.
        :type separator: str
        :param print_lang: Whether to include the language in the output.
        :type print_lang: bool
        :return: A list of string representations of the MultiLangStrings.
        :rtype: list[str]

        Examples:
            # Convert a list of MultiLangStrings to a list of strings with quotes and language:
            >>> mls1 = MultiLangString(mls_dict={"en": {"Hello"}, "fr": {"Bonjour"}})
            >>> mls2 = MultiLangString(mls_dict={"en": {"Hi"}, "fr": {"Salut"}})
            >>> strings = Converter.from_multilangstrings_to_strings([mls1, mls2], print_quotes=True, separator="@")
            >>> for s in strings:
            >>>     print(s)  # Output: "Bonjour"@fr
            >>>                #         "Hello"@en
            >>>                #         "Hi"@en
            >>>                #         "Salut"@fr

            # Convert a list of MultiLangStrings to a list of strings without quotes and language:
            >>> strings = Converter.from_multilangstrings_to_strings([mls1, mls2], print_quotes=False, separator="@",
                                                                                                    print_lang=False)
            >>> for s in strings:
            >>>     print(s)  # Output: Bonjour
            >>>                #         Hello
            >>>                #         Hi
            >>>                #         Salut

        Note:
            The output strings are sorted by language and by text within each language.
        """
        TypeValidator.validate_type_iterable(arg, list, MultiLangString)
        # Other argument types are already validated in the 'to_strings' method.

        unified_mls = MultiLangString.merge_multilangstrings(arg)

        return unified_mls.to_strings(
            langs=languages, print_quotes=print_quotes, separator=separator, print_lang=print_lang
        )

    @staticmethod
    def from_multilangstring_to_langstrings(
        arg: MultiLangString, languages: Optional[list[str]] = None
    ) -> list[LangString]:
        """
        Convert a MultiLangString to a list of LangStrings.

        This method takes a MultiLangString and converts it into a list of LangStrings, each representing one of the
        texts in the MultiLangString along with its associated language.

        :param arg: The MultiLangString to be converted.
        :type arg: MultiLangString
        :param languages: List of languages to include in the output. If None, all languages are included.
        :type languages: Optional[list[str]]
        :return: A list of LangStrings, each corresponding to a text in the arg MultiLangString.
        :rtype: list[LangString]
        :raises TypeError: If the arg is not of type MultiLangString.

        Examples:
            # Convert a MultiLangString to a list of LangStrings:
            >>> multilangstring = MultiLangString(mls_dict={"en": {"Hi", "Hello"}, "fr": {"Bonjour"}})
            >>> langstrings = Converter.from_multilangstring_to_langstrings(multilangstring)
            >>> for ls in langstrings:
            >>>     print(ls)  # Output: "Hi"@en
            >>>                #         "Hello"@en
            >>>                #         "Bonjour"@fr

        Note:
            The output strings are in the order of insertion within each language.
        """
        TypeValidator.validate_type_single(arg, MultiLangString)
        TypeValidator.validate_type_iterable(languages, list, str, optional=True)
        return arg.to_langstrings(langs=languages)

    @staticmethod
    def from_multilangstrings_to_langstrings(
        arg: list[MultiLangString], languages: Optional[list[str]] = None
    ) -> list[LangString]:
        """
        Convert a list of MultiLangStrings to a list of LangStrings.

        This method takes a list of MultiLangStrings and converts them into a list of LangStrings,
        each representing one of the texts in the MultiLangStrings along with its associated language.

        :param arg: List of MultiLangStrings to be converted.
        :type arg: list[MultiLangString]
        :param languages: List of languages to include in the output. If None, all languages are included.
        :type languages: Optional[list[str]]
        :return: A list of LangStrings, each corresponding to a text in the MultiLangStrings.
        :rtype: list[LangString]
        :raises TypeError: If any of the arguments are not of the expected type.

        Examples:
            # Convert a list of MultiLangStrings to a list of LangStrings:
            >>> mls1 = MultiLangString(mls_dict={"en": {"Hello", "Hi"}, "fr": {"Bonjour"}})
            >>> mls2 = MultiLangString(mls_dict={"en": {"Hey"}, "fr": {"Salut"}})
            >>> langstrings = Converter.from_multilangstrings_to_langstrings([mls1, mls2])
            >>> for ls in langstrings:
            >>>     print(ls)  # Output could vary as texts within each language may not be sorted. Possible outputs:
            >>>                #         "Hello"@en
            >>>                #         "Hi"@en
            >>>                #         "Hey"@en
            >>>                #         "Bonjour"@fr
            >>>                #         "Salut"@fr
        """
        TypeValidator.validate_type_iterable(arg, list, MultiLangString)
        TypeValidator.validate_type_iterable(languages, list, str, optional=True)

        unified_mls = MultiLangString.merge_multilangstrings(arg)

        return unified_mls.to_langstrings(langs=languages)

    @staticmethod
    def from_multilangstring_to_setlangstrings(
        arg: MultiLangString, languages: Optional[list[str]] = None
    ) -> list[SetLangString]:
        """
        Convert a MultiLangString to a list of SetLangStrings.

        This method creates a list of SetLangStrings from a MultiLangString. Each SetLangString in the list contains
        texts of a single language from the MultiLangString.

        :param arg: The MultiLangString to be converted.
        :type arg: MultiLangString
        :param languages: List of languages to include in the output. If None, all languages are included.
        :type languages: Optional[list[str]]
        :return: A list of SetLangStrings, each containing texts of a single language from the arg MultiLangString.
        :rtype: list[SetLangString]
        :raises TypeError: If the arg is not of type MultiLangString.

        Examples:
            # Convert a MultiLangString to a list of SetLangStrings:
            >>> multilangstring = MultiLangString(mls_dict={"en": {"Hello", "Hi"}, "fr": {"Bonjour", "Salut"}})
            >>> setlangstrings = Converter.from_multilangstring_to_setlangstrings(multilangstring)
            >>> for sls in setlangstrings:
            >>>     print(sls)  # Output: {'Hello', 'Hi'}@en
            >>>                #         {'Bonjour', 'Salut'}@fr

        Note:
            The texts within each language are sorted.
        """
        TypeValidator.validate_type_single(arg, MultiLangString)
        TypeValidator.validate_type_iterable(languages, list, str, optional=True)
        return arg.to_setlangstrings(langs=languages)

    @staticmethod
    def from_multilangstrings_to_setlangstrings(
        arg: list[MultiLangString], languages: Optional[list[str]] = None
    ) -> list[SetLangString]:
        """
        Convert a list of MultiLangString objects to a list of SetLangString objects.

        This method creates a list of SetLangStrings from multiple MultiLangStrings. Each SetLangString in the list
        contains texts of a single language from the merged MultiLangStrings.

        :param arg: List of MultiLangStrings to be converted.
        :type arg: list[MultiLangString]
        :param languages: List of languages to include in the output. If None, all languages are included.
        :type languages: Optional[list[str]]
        :return: A list of SetLangStrings, each containing texts of a single language from the merged MultiLangStrings.
        :rtype: list[SetLangString]
        :raises TypeError: If any of the arguments are not of the expected type.

        Examples:
            # Convert a list of MultiLangStrings to a list of SetLangStrings:
            >>> mls1 = MultiLangString(mls_dict={"en": {"Hello"}, "fr": {"Bonjour"}})
            >>> mls2 = MultiLangString(mls_dict={"en": {"Hi"}, "fr": {"Salut"}})
            >>> setlangstrings = Converter.from_multilangstrings_to_setlangstrings([mls1, mls2])
            >>> for sls in setlangstrings:
            >>>     print(sls)  # Output: {'Hello', 'Hi'}@en
            >>>                #         {'Bonjour', 'Salut'}@fr

        Note:
            The texts within each language are sorted.
        """
        TypeValidator.validate_type_iterable(arg, list, MultiLangString)
        TypeValidator.validate_type_iterable(languages, list, str, optional=True)

        unified_mls = MultiLangString.merge_multilangstrings(arg)

        return unified_mls.to_setlangstrings(langs=languages)
