langstring.multilangstring
==========================

.. py:module:: langstring.multilangstring

.. autoapi-nested-parse::

   The multilangstring module provides the MultiLangString class to manage and manipulate multilingual text strings.

   This module is designed to store, retrieve, and handle text strings in multiple languages, offering a flexible
   and efficient way to manage multilingual content in various applications. The MultiLangString class uses a dictionary
   to store text entries associated with language tags, allowing the representation and manipulation of text in
   different languages. It supports adding new entries, removing entries, and retrieving entries based on specific
   languages or across all languages. Additionally, the class allows setting a preferred language, which can be used
   as a default for operations involving text retrieval.

   The module integrates seamlessly with other components like `LangString` and `SetLangString`, enabling robust
   multilingual text management and operations. It ensures that user interaction is as intuitive as possible, while
   offering extensive functionality for handling multilingual text data.

   :Example:

       mls = MultiLangString({"en": {"Hello", "World"}, "fr": {"Bonjour", "Monde"}}, "en")

       # Add a new entry
       mls.add_entry("Hola", "es")
       print(mls)  # Output: {'Hello', 'World'}@en, {'Hola'}@es, {'Bonjour', 'Monde'}@fr

       # Retrieve texts in a specific language
       english_texts = mls["en"]
       print(english_texts)  # Output: {'Hello', 'World'}

       # Remove an entry
       mls.remove_entry("Hello", "en")
       print(mls)  # Output: {'World'}@en, {'Hola'}@es, {'Bonjour', 'Monde'}@fr

   Modules:
       controller: Provides control flags that influence the behavior of the MultiLangString class.
       flags: Defines the MultiLangStringFlag class with various control flags for the MultiLangString class.
       langstring: Provides the LangString class used within the MultiLangString class.
       setlangstring: Provides the SetLangString class used within the MultiLangString class.
       utils.validators: Provides validation methods used within the MultiLangString class.



Classes
-------

.. autoapisummary::

   langstring.multilangstring.MultiLangString


Module Contents
---------------

.. py:class:: MultiLangString(mls_dict = None, pref_lang = 'en')

   A class for managing multilingual text strings with various language tags.

   This class provides functionality for storing, retrieving, and manipulating text strings in multiple languages.
   It uses a dictionary to maintain text entries associated with language tags, allowing efficient handling of
   multilingual content. The MultiLangString class supports operations like adding new entries, removing entries,
   and retrieving entries in specific languages or across all languages. Additionally, it allows setting a preferred
   language, which can be used as a default for text retrieval operations.

   The behavior of this class is influenced by control flags set in the Controller, which can enforce constraints
   like valid language tags and non-empty text entries. The class integrates seamlessly with other components like
   LangString and SetLangString, providing a comprehensive solution for managing multilingual text data.

   :ivar mls_dict: A dictionary representing the internal structure of the MultiLangString, where keys are language
                   codes and values are sets of text entries.
   :vartype mls_dict: Optional[dict[str, set[str]]]
   :ivar pref_lang: The preferred language for this MultiLangString. Defaults to "en".
   :vartype pref_lang: str


   .. py:property:: mls_dict
      :type: dict[str, set[str]]

      Get the dictionary representing the internal structure of the MultiLangString.

      :return: The dictionary where keys are language codes and values are sets of text entries.
      :rtype: dict[str, set[str]]



   .. py:property:: pref_lang
      :type: str

      Get the preferred language for this MultiLangString.

      :return: The preferred language as a string.
      :rtype: str



   .. py:method:: add(arg)

      Add an element to the MultiLangString.

      This method determines the type of the argument and calls the appropriate add method.

      :param arg: The element to add, which can be a tuple of (text, language), LangString, SetLangString,
                  or MultiLangString.
      :type arg: Union[tuple[str, str], LangString, SetLangString, MultiLangString]
      :raises TypeError: If the argument is not of a supported type.

      :Example:
      >>> mls = MultiLangString()
      >>> mls.add(("Hello", "en"))
      >>> mls.add(LangString("Bonjour", "fr"))
      >>> print(mls)  # Output: {'Hello'}@en, {'Bonjour'}@fr



   .. py:method:: add_entry(text, lang)

      Add a text entry to the MultiLangString under a specified language.

      Validates the provided text and language against the current flag settings before adding. If the specified
      language does not exist in the mls_dict, a new set for that language is created. The text is then added to
      this set. If the language already exists, the text is added to the existing set for that language.

      :param text: The text to be added to the MultiLangString.
      :type text: str
      :param lang: The language under which the text should be added. If not specified, defaults to an empty string.
      :type lang: str

      :Example:
      >>> mls = MultiLangString()
      >>> mls.add_entry("Hello", "en")
      >>> mls.add_entry("Bonjour", "fr")
      >>> print(mls)  # Output: {'Hello'}@en, {'Bonjour'}@fr



   .. py:method:: add_text_in_pref_lang(text)

      Add a text entry to the preferred language.

      :param text: The text to be added to the preferred language.
      :type text: str

      :Example:
      >>> mls = MultiLangString(pref_lang="en")
      >>> mls.add_text_in_pref_lang("Hello")
      >>> print(mls)  # Output: {'Hello'}@en



   .. py:method:: add_langstring(langstring)

      Add a LangString to the MultiLangString.

      :param langstring: The LangString object to be added, representing a text in a specific language.
      :type langstring: LangString

      :Example:
      >>> mls = MultiLangString()
      >>> langstring = LangString("Hello", "en")
      >>> mls.add_langstring(langstring)
      >>> print(mls)  # Output: {'Hello'}@en



   .. py:method:: add_setlangstring(setlangstring)

      Add a SetLangString to the MultiLangString.

      This method adds all text entries from a SetLangString to the MultiLangString under the specified language.

      :param setlangstring: The SetLangString object to be added, representing a text in a specific language.
      :type setlangstring: SetLangString

      :Example:
      >>> mls = MultiLangString()
      >>> setlangstring = SetLangString({"Hello", "Hi"}, "en")
      >>> mls.add_setlangstring(setlangstring)
      >>> print(mls)  # Output: {'Hello', 'Hi'}@en



   .. py:method:: add_multilangstring(multilangstring)

      Add a MultiLangString to the MultiLangString.

      This method adds all text entries from another MultiLangString to the current MultiLangString.

      :param multilangstring: The MultiLangString object to be added.
      :type multilangstring: MultiLangString

      :Example:
      >>> mls1 = MultiLangString()
      >>> mls2 = MultiLangString({"en": {"Hello"}, "fr": {"Bonjour"}})
      >>> mls1.add_multilangstring(mls2)
      >>> print(mls1)  # Output: {'Hello'}@en, {'Bonjour'}@fr



   .. py:method:: add_empty_lang(lang)

      Add an empty language to the MultiLangString.

      This method adds an empty set for the specified language to the MultiLangString if it does not already exist.

      :param lang: The language to add.
      :type lang: str

      :Example:
      >>> mls = MultiLangString()
      >>> mls.add_empty_lang("en")
      >>> print(mls)  # Output: {}@en



   .. py:method:: discard(arg, clean_empty = False)

      Discard an entry, LangString, SetLangString, or MultiLangString from the MultiLangString.

      This method discards the specified entry from the MultiLangString. It can handle tuples, LangString,
      SetLangString, or MultiLangString objects. Optionally, it can remove empty language entries after discarding.

      :param arg: The entry to discard, which can be a tuple, LangString, SetLangString, or MultiLangString.
      :type arg: Union[tuple[str, str], LangString, SetLangString, MultiLangString]
      :param clean_empty: If True, remove empty language entries after discarding. Defaults to False.
      :type clean_empty: bool

      :Example:
      >>> mls = MultiLangString({"en": {"Hello"}, "fr": {"Bonjour"}})
      >>> mls.discard(("Hello", "en"))
      >>> print(mls)  # Output: {}@en, {'Bonjour'}@fr
      >>> lang_str = LangString("Bonjour", "fr")
      >>> mls.discard(lang_str)
      >>> print(mls)  # Output: {}@en, {}@fr



   .. py:method:: discard_entry(text, lang, clean_empty = False)

      Discard a text entry from a specified language in the MultiLangString.

      This method removes the specified text entry from the set associated with the given language.
      If the set becomes empty and clean_empty is True, the language entry is removed.

      :param text: The text to discard.
      :type text: str
      :param lang: The language of the text to discard.
      :type lang: str
      :param clean_empty: If True, remove the language entry if it becomes empty. Defaults to False.
      :type clean_empty: bool

      :Example:
      >>> mls = MultiLangString({"en": {"Hello", "World"}, "fr": {"Bonjour"}})
      >>> mls.discard_entry("Hello", "en")
      >>> print(mls)  # Output: {'World'}@en, {'Bonjour'}@fr
      >>> mls.discard_entry("World", "en", clean_empty=True)
      >>> print(mls)  # Output: {'Bonjour'}@fr



   .. py:method:: discard_text_in_pref_lang(text, clean_empty = False)

      Discard a text entry from the preferred language.

      This method removes the specified text entry from the set associated with the preferred language.
      If the set becomes empty and clean_empty is True, the language entry is removed.

      :param text: The text to discard.
      :type text: str
      :param clean_empty: If True, remove the language entry if it becomes empty. Defaults to False.
      :type clean_empty: bool

      :Example:
      >>> mls = MultiLangString({"en": {"Hello", "World"}, "fr": {"Bonjour"}})
      >>> mls.discard_text_in_pref_lang("Hello")
      >>> print(mls)  # Output: {'World'}@en, {'Bonjour'}@fr
      >>> mls.discard_text_in_pref_lang("World", clean_empty=True)
      >>> print(mls)  # Output: {'Bonjour'}@fr



   .. py:method:: discard_langstring(langstring, clean_empty = False)

      Discard a LangString from the MultiLangString.

      This method removes the specified LangString from the set associated with its language.
      If the set becomes empty and clean_empty is True, the language entry is removed.

      :param langstring: The LangString object to discard.
      :type langstring: LangString
      :param clean_empty: If True, remove the language entry if it becomes empty. Defaults to False.
      :type clean_empty: bool

      :Example:
      >>> mls = MultiLangString({"en": {"Hello", "World"}, "fr": {"Bonjour"}})
      >>> lang_str = LangString("Hello", "en")
      >>> mls.discard_langstring(lang_str)
      >>> print(mls)  # Output: {'World'}@en, {'Bonjour'}@fr
      >>> lang_str = LangString("World", "en")
      >>> mls.discard_langstring(lang_str, clean_empty=True)
      >>> print(mls)  # Output: {'Bonjour'}@fr



   .. py:method:: discard_setlangstring(setlangstring, clean_empty = False)

      Discard a SetLangString from the MultiLangString.

      This method removes the specified SetLangString from the sets associated with its language.
      If the set becomes empty and clean_empty is True, the language entry is removed.

      :param setlangstring: The SetLangString object to discard.
      :type setlangstring: SetLangString
      :param clean_empty: If True, remove the language entry if it becomes empty. Defaults to False.
      :type clean_empty: bool

      :Example:
      >>> mls = MultiLangString({"en": {"Hello", "World"}, "fr": {"Bonjour"}})
      >>> set_lang_str = SetLangString({"Hello", "World"}, "en")
      >>> mls.discard_setlangstring(set_lang_str)
      >>> print(mls)  # Output: {}@en, {'Bonjour'}@fr
      >>> set_lang_str = SetLangString({"Bonjour"}, "fr")
      >>> mls.discard_setlangstring(set_lang_str, clean_empty=True)
      >>> print(mls)  # Output: {}@en



   .. py:method:: discard_multilangstring(multilangstring, clean_empty = False)

      Discard a MultiLangString from the current MultiLangString.

      This method removes the specified MultiLangString from the sets associated with its languages.
      If a set becomes empty and clean_empty is True, the language entry is removed.

      :param multilangstring: The MultiLangString object to discard.
      :type multilangstring: MultiLangString
      :param clean_empty: If True, remove empty language entries after discarding. Defaults to False.
      :type clean_empty: bool

      :Example:
      >>> mls = MultiLangString({"en": {"Hello", "World"}, "fr": {"Bonjour", "Salut"}})
      >>> mls_to_discard = MultiLangString({"en": {"Hello"}, "fr": {"Salut"}})
      >>> mls.discard_multilangstring(mls_to_discard)
      >>> print(mls)  # Output: {'World'}@en, {'Bonjour'}@fr
      >>> mls_to_discard = MultiLangString({"en": {"World"}, "fr": {"Bonjour"}})
      >>> mls.discard_multilangstring(mls_to_discard, clean_empty=True)
      >>> print(mls)  # Output: {}



   .. py:method:: discard_lang(lang)

      Discard all entries for a specified language.

      This method removes all entries associated with the given language from the MultiLangString.

      :param lang: The language to discard.
      :type lang: str

      :Example:
      >>> mls = MultiLangString({"en": {"Hello", "World"}, "fr": {"Bonjour", "Salut"}})
      >>> mls.discard_lang("en")
      >>> print(mls)  # Output: {'Bonjour', 'Salut'}@fr
      >>> mls.discard_lang("fr")
      >>> print(mls)  # Output: {}



   .. py:method:: remove(arg, clean_empty = False)

      Remove an entry, LangString, SetLangString, or MultiLangString from the MultiLangString.

      This method removes the specified entry from the MultiLangString. It can handle tuples, LangString,
      SetLangString, or MultiLangString objects. Optionally, it can remove empty language entries after removing.

      :param arg: The entry to remove, which can be a tuple, LangString, SetLangString, or MultiLangString.
      :type arg: Union[tuple[str, str], LangString, SetLangString, MultiLangString]
      :param clean_empty: If True, remove empty language entries after removing. Defaults to False.
      :type clean_empty: bool

      :Example:
      >>> mls = MultiLangString({"en": {"Hello"}, "fr": {"Bonjour"}})
      >>> mls.remove(("Hello", "en"))
      >>> print(mls)  # Output: {}@en, {'Bonjour'}@fr
      >>> lang_str = LangString("Bonjour", "fr")
      >>> mls.remove(lang_str)
      >>> print(mls)  # Output: {}@en, {}@fr



   .. py:method:: remove_entry(text, lang, clean_empty = False)

      Remove a single entry from the set of a given language key in the dictionary.

      If the specified language key exists and the text is in its set, the text is removed. If this results in an
      empty set for the language, the language key is also removed from the dictionary.

      :param text: The text to be removed.
      :type text: str
      :param lang: The language key from which the text should be removed.
      :type lang: str
      :param clean_empty: If True, remove the language entry if it becomes empty. Defaults to False.
      :type clean_empty: bool

      :Example:
      >>> mls = MultiLangString({"en": {"Hello", "World"}, "fr": {"Bonjour"}})
      >>> mls.remove_entry("Hello", "en")
      >>> print(mls)  # Output: {'World'}@en, {'Bonjour'}@fr
      >>> mls.remove_entry("World", "en", clean_empty=True)
      >>> print(mls)  # Output: {'Bonjour'}@fr



   .. py:method:: remove_text_in_pref_lang(text, clean_empty = False)

      Remove a text entry from the preferred language.

      This method removes the specified text entry from the set associated with the preferred language.
      If the set becomes empty and clean_empty is True, the language entry is removed.

      :param text: The text to remove.
      :type text: str
      :param clean_empty: If True, remove the language entry if it becomes empty. Defaults to False.
      :type clean_empty: bool

      :Example:
      >>> mls = MultiLangString({"en": {"Hello", "World"}, "fr": {"Bonjour"}})
      >>> mls.remove_text_in_pref_lang("Hello")
      >>> print(mls)  # Output: {'World'}@en, {'Bonjour'}@fr
      >>> mls.remove_text_in_pref_lang("World", clean_empty=True)
      >>> print(mls)  # Output: {'Bonjour'}@fr



   .. py:method:: remove_langstring(langstring, clean_empty = False)

      Remove a LangString from the MultiLangString.

      This method removes the specified LangString from the set associated with its language.
      If the set becomes empty and clean_empty is True, the language entry is removed.

      :param langstring: The LangString object to remove.
      :type langstring: LangString
      :param clean_empty: If True, remove the language entry if it becomes empty. Defaults to False.
      :type clean_empty: bool

      :Example:
      >>> mls = MultiLangString({"en": {"Hello", "World"}, "fr": {"Bonjour"}})
      >>> lang_str = LangString("Hello", "en")
      >>> mls.remove_langstring(lang_str)
      >>> print(mls)  # Output: {'World'}@en, {'Bonjour'}@fr
      >>> lang_str = LangString("World", "en")
      >>> mls.remove_langstring(lang_str, clean_empty=True)
      >>> print(mls)  # Output: {'Bonjour'}@fr



   .. py:method:: remove_setlangstring(setlangstring, clean_empty = False)

      Remove a SetLangString from the MultiLangString.

      This method removes the specified SetLangString from the sets associated with its language.
      If the set becomes empty and clean_empty is True, the language entry is removed.

      :param setlangstring: The SetLangString object to remove.
      :type setlangstring: SetLangString
      :param clean_empty: If True, remove the language entry if it becomes empty. Defaults to False.
      :type clean_empty: bool

      :Example:
      >>> mls = MultiLangString({"en": {"Hello", "World"}, "fr": {"Bonjour"}})
      >>> set_lang_str = SetLangString({"Hello", "World"}, "en")
      >>> mls.remove_setlangstring(set_lang_str)
      >>> print(mls)  # Output: {}@en, {'Bonjour'}@fr
      >>> set_lang_str = SetLangString({"Bonjour"}, "fr")
      >>> mls.remove_setlangstring(set_lang_str, clean_empty=True)
      >>> print(mls)  # Output: {}@en



   .. py:method:: remove_multilangstring(multilangstring, clean_empty = False)

      Remove a MultiLangString from the current MultiLangString.

      This method removes the specified MultiLangString from the sets associated with its languages.
      If a set becomes empty and clean_empty is True, the language entry is removed.

      :param multilangstring: The MultiLangString object to remove.
      :type multilangstring: MultiLangString
      :param clean_empty: If True, remove empty language entries after removing. Defaults to False.
      :type clean_empty: bool

      :Example:
      >>> mls = MultiLangString({"en": {"Hello", "World"}, "fr": {"Bonjour", "Salut"}})
      >>> mls_to_remove = MultiLangString({"en": {"Hello"}, "fr": {"Salut"}})
      >>> mls.remove_multilangstring(mls_to_remove)
      >>> print(mls)  # Output: {'World'}@en, {'Bonjour'}@fr
      >>> mls_to_remove = MultiLangString({"en": {"World"}, "fr": {"Bonjour"}})
      >>> mls.remove_multilangstring(mls_to_remove, clean_empty=True)
      >>> print(mls)  # Output: {}



   .. py:method:: remove_lang(lang)

      Remove all entries of a given language from the dictionary.

      If the specified language key exists, it and all its associated texts are removed from the dictionary.

      :param lang: The language key to be removed along with all its texts.
      :type lang: str

      :Example:
      >>> mls = MultiLangString({"en": {"Hello", "World"}, "fr": {"Bonjour", "Salut"}})
      >>> mls.remove_lang("en")
      >>> print(mls)  # Output: {'Bonjour', 'Salut'}@fr
      >>> mls.remove_lang("fr")
      >>> print(mls)  # Output: {}



   .. py:method:: remove_empty_langs()

      Remove all empty language entries from the dictionary.

      This method checks for languages that have no associated text entries and removes them from the dictionary.

      :Example:
      >>> mls = MultiLangString({"en": {"Hello"}, "fr": set()})
      >>> mls.remove_empty_langs()
      >>> print(mls)  # Output: {'Hello'}@en



   .. py:method:: to_strings(langs = None, print_quotes = None, separator = '@', print_lang = None)

      Convert the MultiLangString to a list of formatted strings.

      This method converts the text entries of the MultiLangString into a list of strings,
      optionally formatted with quotes and language tags.
      The resulting list of strings is sorted to generate a deterministic output.

      :param langs: A list of languages to include in the output. If None, includes all languages.
      :type langs: Optional[list[str]]
      :param print_quotes: If True, wraps the text in quotes. Defaults to the controller flag.
      :type print_quotes: Optional[bool]
      :param separator: The separator between the text and the language tag. Defaults to "@".
      :type separator: str
      :param print_lang: If True, includes the language tag in the output. Defaults to the controller flag.
      :type print_lang: Optional[bool]
      :return: A sorted list of formatted strings.
      :rtype: list[str]

      :Example:
      >>> mls = MultiLangString({"en": {"Hello", "World"}, "fr": {"Bonjour"}})
      >>> strings = mls.to_strings()
      >>> print(strings)  # Output: ['"Bonjour"@fr', '"Hello"@en', '"World"@en']
      >>> strings = mls.to_strings(print_quotes=False, print_lang=False)
      >>> print(strings)  # Output: ['Bonjour', 'Hello', 'World']



   .. py:method:: to_langstrings(langs = None)

      Convert the MultiLangString to a list of LangString objects.

      This method converts the text entries of the MultiLangString into a list of LangString objects.

      :param langs: A list of languages to include in the output. If None, includes all languages.
      :type langs: Optional[list[str]]
      :return: A list of LangString objects.
      :rtype: list[LangString]

      :Example:
      >>> mls = MultiLangString({"en": {"Hello", "World"}, "fr": {"Bonjour"}})
      >>> langstrings = mls.to_langstrings()
      >>> for langstring in langstrings:
      ...     print(langstring)
      ...
      # Output:   "Hello"@en
      #           "World"@en
      #           "Bonjour"@fr



   .. py:method:: to_setlangstrings(langs = None)

      Convert the MultiLangString to a list of SetLangString objects.

      This method converts the text entries of the MultiLangString into a list of SetLangString objects.

      :param langs: A list of languages to include in the output. If None, includes all languages.
      :type langs: Optional[list[str]]
      :return: A list of SetLangString objects.
      :rtype: list[SetLangString]

      :Example:
      >>> mls = MultiLangString({"en": {"Hello", "World"}, "fr": {"Bonjour"}})
      >>> setlangstrings = mls.to_setlangstrings()
      >>> for setlangstring in setlangstrings:
      ...     print(setlangstring)
      ...
      >>> # Output:   {'Hello', 'World'}@en
      >>> #           {'Bonjour'}@fr



   .. py:method:: count_entries_of_lang(lang)

      Count the number of text entries for a given language.

      This method returns the number of text entries associated with the specified language.

      :param lang: The language to count the entries for.
      :type lang: str
      :return: The number of text entries for the specified language.
      :rtype: int

      :Example:
      >>> mls = MultiLangString({"en": {"Hello", "World"}, "fr": {"Bonjour"}})
      >>> count = mls.count_entries_of_lang("en")
      >>> print(count)  # Output: 2
      >>> count = mls.count_entries_of_lang("fr")
      >>> print(count)  # Output: 1



   .. py:method:: count_entries_per_lang()

      Return the number of text entries for each language.

      This method returns a dictionary with language codes as keys and the counts of text entries as values.

      :return: A dictionary with language codes as keys and counts of text entries as values.
      :rtype: dict[str, int]

      :Example:
      >>> mls = MultiLangString({"en": {"Hello", "World"}, "fr": {"Bonjour"}})
      >>> counts = mls.count_entries_per_lang()
      >>> print(counts)  # Output: {'en': 2, 'fr': 1}



   .. py:method:: count_entries_total()

      Return the total number of text entries across all languages.

      This method returns the total count of text entries in the MultiLangString.

      :return: The total number of text entries.
      :rtype: int

      :Example:
      >>> mls = MultiLangString({"en": {"Hello", "World"}, "fr": {"Bonjour"}})
      >>> total_count = mls.count_entries_total()
      >>> print(total_count)  # Output: 3



   .. py:method:: count_langs_total()

      Count the total number of languages in the MultiLangString.

      This method returns the number of unique languages in the MultiLangString.

      :return: The total number of languages.
      :rtype: int

      :Example:
      >>> mls = MultiLangString({"en": {"Hello", "World"}, "fr": {"Bonjour"}})
      >>> total_langs = mls.count_langs_total()
      >>> print(total_langs)  # Output: 2



   .. py:method:: contains(arg)

      Check if the MultiLangString contains the specified entry, LangString, SetLangString, or MultiLangString.

      This method checks if the specified entry is present in the MultiLangString. It can handle tuples, LangString,
      SetLangString, or MultiLangString objects.

      :param arg: The entry to check, which can be a tuple, LangString, SetLangString, or MultiLangString.
      :type arg: Union[tuple[str, str], LangString, SetLangString, MultiLangString]
      :return: True if the entry is present, False otherwise.
      :rtype: bool

      :Example:
      >>> mls = MultiLangString({"en": {"Hello"}, "fr": {"Bonjour"}})
      >>> result = mls.contains(("Hello", "en"))
      >>> print(result)  # Output: True
      >>> lang_str = LangString("Bonjour", "fr")
      >>> result = mls.contains(lang_str)
      >>> print(result)  # Output: True
      >>> set_lang_str = SetLangString({"Hello"}, "en")
      >>> result = mls.contains(set_lang_str)
      >>> print(result)  # Output: True
      >>> mls_to_check = MultiLangString({"en": {"Hello"}, "fr": {"Bonjour"}})
      >>> result = mls.contains(mls_to_check)
      >>> print(result)  # Output: True



   .. py:method:: contains_entry(text, lang)

      Check if a specific text entry exists in a given language.

      This method checks if the specified text entry is present in the set associated with the given language.

      :param text: The text entry to check.
      :type text: str
      :param lang: The language of the text entry.
      :type lang: str
      :return: True if the text entry is present, False otherwise.
      :rtype: bool

      :Example:
      >>> mls = MultiLangString({"en": {"Hello"}, "fr": {"Bonjour"}})
      >>> result = mls.contains_entry("Hello", "en")
      >>> print(result)  # Output: True
      >>> result = mls.contains_entry("Bonjour", "fr")
      >>> print(result)  # Output: True
      >>> result = mls.contains_entry("Hello", "fr")
      >>> print(result)  # Output: False



   .. py:method:: contains_lang(lang)

      Check if a specific language exists in the MultiLangString.

      This method checks if the specified language is present in the MultiLangString.

      :param lang: The language to check.
      :type lang: str
      :return: True if the language is present, False otherwise.
      :rtype: bool

      :Example:
      >>> mls = MultiLangString({"en": {"Hello"}, "fr": {"Bonjour"}})
      >>> result = mls.contains_lang("en")
      >>> print(result)  # Output: True
      >>> result = mls.contains_lang("fr")
      >>> print(result)  # Output: True
      >>> result = mls.contains_lang("es")
      >>> print(result)  # Output: False



   .. py:method:: contains_text_in_pref_lang(text)

      Check if a specific text exists in the preferred language.

      This method checks if the specified text entry is present in the set associated with the preferred language.

      :param text: The text entry to check.
      :type text: str
      :return: True if the text entry is present in the preferred language, False otherwise.
      :rtype: bool

      :Example:
      >>> mls = MultiLangString({"en": {"Hello"}, "fr": {"Bonjour"}})
      >>> result = mls.contains_text_in_pref_lang("Hello")
      >>> print(result)  # Output: True
      >>> result = mls.contains_text_in_pref_lang("Bonjour")
      >>> print(result)  # Output: False



   .. py:method:: contains_text_in_any_lang(text)

      Check if a specific text exists in any language.

      This method checks if the specified text entry is present in the sets associated with any language
      in the MultiLangString.

      :param text: The text entry to check.
      :type text: str
      :return: True if the text entry is present in any language, False otherwise.
      :rtype: bool

      :Example:
      >>> mls = MultiLangString({"en": {"Hello"}, "fr": {"Bonjour"}})
      >>> result = mls.contains_text_in_any_lang("Hello")
      >>> print(result)  # Output: True
      >>> result = mls.contains_text_in_any_lang("Bonjour")
      >>> print(result)  # Output: True
      >>> result = mls.contains_text_in_any_lang("Hola")
      >>> print(result)  # Output: False



   .. py:method:: contains_langstring(langstring)

      Check if the given LangString's text and language are part of this MultiLangString.

      This method checks if the specified LangString is present in the set associated with its language.

      :param langstring: A LangString object to check.
      :type langstring: LangString
      :return: True if the LangString's text is found within the specified language's set; otherwise, False.
      :rtype: bool

      :Example:
      >>> mls = MultiLangString({"en": {"Hello"}, "fr": {"Bonjour"}})
      >>> lang_str = LangString("Hello", "en")
      >>> result = mls.contains_langstring(lang_str)
      >>> print(result)  # Output: True
      >>> lang_str = LangString("Hola", "es")
      >>> result = mls.contains_langstring(lang_str)
      >>> print(result)  # Output: False



   .. py:method:: contains_setlangstring(setlangstring)

      Check if all texts and the language of a SetLangString are part of this MultiLangString.

      This method checks if the specified SetLangString's language exists and all its texts are found within the
      specified language's set.

      :param setlangstring: A SetLangString object to check.
      :type setlangstring: SetLangString
      :return: True if the SetLangString's language exists and all its texts are found within the specified
               language's set; otherwise, False.
      :rtype: bool

      :Example:
      >>> mls = MultiLangString({"en": {"Hello", "World"}, "fr": {"Bonjour"}})
      >>> set_lang_str = SetLangString({"Hello"}, "en")
      >>> result = mls.contains_setlangstring(set_lang_str)
      >>> print(result)  # Output: True
      >>> set_lang_str = SetLangString({"Bonjour"}, "fr")
      >>> result = mls.contains_setlangstring(set_lang_str)
      >>> print(result)  # Output: True
      >>> set_lang_str = SetLangString({"Hola"}, "es")
      >>> result = mls.contains_setlangstring(set_lang_str)
      >>> print(result)  # Output: False



   .. py:method:: contains_multilangstring(multilangstring)

      Check if the current instance contains all languages and texts of another MultiLangString instance.

      This method checks if all languages and their respective texts in the specified MultiLangString are contained
      in this instance.

      :param multilangstring: The MultiLangString instance to check against.
      :type multilangstring: MultiLangString
      :return: True if all languages and their respective texts in `multilangstring` are contained in this instance,
               False otherwise.
      :rtype: bool

      :Example:
      >>> mls = MultiLangString({"en": {"Hello", "World"}, "fr": {"Bonjour"}})
      >>> mls_to_check = MultiLangString({"en": {"Hello"}, "fr": {"Bonjour"}})
      >>> result = mls.contains_multilangstring(mls_to_check)
      >>> print(result)  # Output: True
      >>> mls_to_check = MultiLangString({"en": {"Hello"}, "fr": {"Salut"}})
      >>> result = mls.contains_multilangstring(mls_to_check)
      >>> print(result)  # Output: False



   .. py:method:: get_langs(casefold = False)

      Return a list of all languages in the MultiLangString.

      This method returns a list of all language codes present in the MultiLangString. If casefold is True,
      the language codes are returned in lowercase.

      :param casefold: If True, return the language codes in lowercase. Defaults to False.
      :type casefold: bool
      :return: A list of language codes.
      :rtype: list[str]

      :Example:
      >>> mls = MultiLangString({"en": {"Hello"}, "fr": {"Bonjour"}})
      >>> langs = mls.get_langs()
      >>> print(langs)  # Output: ['en', 'fr']
      >>> langs_casefolded = mls.get_langs(casefold=True)
      >>> print(langs_casefolded)  # Output: ['en', 'fr']



   .. py:method:: get_texts()

      Return a sorted list of all texts in the MultiLangString.

      This method returns a list of all text entries present in the MultiLangString, sorted in alphabetical order.

      :return: A sorted list of text entries.
      :rtype: list[str]

      :Example:
      >>> mls = MultiLangString({"en": {"Hello", "World"}, "fr": {"Bonjour"}})
      >>> texts = mls.get_texts()
      >>> print(texts)  # Output: ['Bonjour', 'Hello', 'World']



   .. py:method:: get_langstring(text, lang)

      Retrieve a LangString from the MultiLangString.

      This method returns a LangString object if the specified text and language are present in the MultiLangString.
      If the text and language are not found, it returns a LangString with only the language set.

      :param text: The text entry to retrieve.
      :type text: str
      :param lang: The language of the text entry.
      :type lang: str
      :return: A LangString object with the specified text and language, or a LangString with only the language if
               not found.
      :rtype: LangString

      :Example:
      >>> mls = MultiLangString({"en": {"Hello"}, "fr": {"Bonjour"}})
      >>> lang_str = mls.get_langstring("Hello", "en")
      >>> print(lang_str)  # Output: "Hello"@en
      >>> lang_str = mls.get_langstring("Hola", "es")
      >>> print(lang_str)  # Output: ""@es



   .. py:method:: get_setlangstring(lang)

      Retrieve a SetLangString from the MultiLangString.

      This method returns a SetLangString object if the specified language is present in the MultiLangString.
      If the language is not found, it returns an empty SetLangString with the language set.

      :param lang: The language to retrieve the SetLangString for.
      :type lang: str
      :return: A SetLangString object with the texts for the specified language, or an empty SetLangString
               if not found.
      :rtype: SetLangString

      :Example:
      >>> mls = MultiLangString({"en": {"Hello", "World"}, "fr": {"Bonjour"}})
      >>> set_lang_str = mls.get_setlangstring("en")
      >>> print(set_lang_str)  # Output: {'Hello', 'World'}@en
      >>> set_lang_str = mls.get_setlangstring("es")
      >>> print(set_lang_str)  # Output: {}es



   .. py:method:: get_multilangstring(langs)

      Retrieve a MultiLangString containing only the specified languages.

      This method returns a new MultiLangString object containing only the specified languages and their texts
      from the current MultiLangString.

      :param langs: A list of languages to include in the new MultiLangString.
      :type langs: list[str]
      :return: A new MultiLangString object with the specified languages and their texts.
      :rtype: MultiLangString

      :Example:
      >>> mls = MultiLangString({"en": {"Hello", "World"}, "fr": {"Bonjour"}, "es": {"Hola"}})
      >>> new_mls = mls.get_multilangstring(["en", "es"])
      >>> print(new_mls)  # Output: {'Hello', 'World'}@en, {'Hola'}@es



   .. py:method:: pop_langstring(text, lang)

      Remove and return a LangString from the MultiLangString.

      This method removes the specified text entry and its language from the MultiLangString,
      and returns it as a LangString object. If the entry is not found, it returns None.

      :param text: The text entry to remove.
      :type text: str
      :param lang: The language of the text entry.
      :type lang: str
      :return: The removed LangString object, or None if the entry was not found.
      :rtype: Optional[LangString]

      :Example:
      >>> mls = MultiLangString({"en": {"Hello"}, "fr": {"Bonjour"}})
      >>> lang_str = mls.pop_langstring("Hello", "en")
      >>> print(lang_str)  # Output: "Hello"@en
      >>> print(mls)  # Output: {}@en, {'Bonjour'}@fr,
      >>> lang_str = mls.pop_langstring("Hola", "es")
      >>> print(lang_str)  # Output: None
      >>> print(mls)  # Output: {}@en, {'Bonjour'}@fr



   .. py:method:: pop_setlangstring(lang)

      Remove and return a SetLangString from the MultiLangString.

      This method removes all text entries associated with the specified language from the MultiLangString,
      and returns them as a SetLangString object. If the language is not found, it returns None.

      :param lang: The language to remove the SetLangString for.
      :type lang: str
      :return: The removed SetLangString object, or None if the language was not found.
      :rtype: Optional[SetLangString]

      :Example:
      >>> mls = MultiLangString({"en": {"Hello", "World"}, "fr": {"Bonjour"}})
      >>> set_lang_str = mls.pop_setlangstring("en")
      >>> print(set_lang_str)  # Output: {'Hello', 'World'}@en
      >>> print(mls)  # Output: {'Bonjour'}@fr
      >>> set_lang_str = mls.pop_setlangstring("es")
      >>> print(set_lang_str)  # Output: None
      >>> print(mls)  # Output: {'Bonjour'}@fr



   .. py:method:: pop_multilangstring(langs)

      Remove and return a MultiLangString containing the specified languages.

      This method removes all text entries associated with the specified languages from the MultiLangString,
      and returns them as a new MultiLangString object.

      :param langs: A list of languages to remove.
      :type langs: list[str]
      :return: A new MultiLangString object with the specified languages and their texts.
      :rtype: MultiLangString

      :Example:
      >>> mls = MultiLangString({"en": {"Hello", "World"}, "fr": {"Bonjour"}, "es": {"Hola"}})
      >>> new_mls = mls.pop_multilangstring(["en", "es"])
      >>> print(new_mls)  # Output: {'Hello', 'World'}@en, {'Hola'}@es
      >>> print(mls)  # Output: {'Bonjour'}@fr



   .. py:method:: has_pref_lang_entries()

      Check if there are any entries in the preferred language.

      This method checks whether there are any text entries in the MultiLangString for the preferred language.

      :return: True if there are entries in the preferred language, False otherwise.
      :rtype: bool

      :Example:
      >>> mls = MultiLangString({"en": {"Hello"}, "fr": {"Bonjour"}})
      >>> has_entries = mls.has_pref_lang_entries()
      >>> print(has_entries)  # Output: True
      >>> mls.pop_setlangstring("en")
      >>> has_entries = mls.has_pref_lang_entries()
      >>> print(has_entries)  # Output: False



   .. py:method:: __contains__(lang)

      Check if a language is in the MultiLangString.

      This method mimics the behavior of the 'in' operator for dictionaries, allowing users to check if a language
      exists in the MultiLangString.

      :param lang: The language code to check for.
      :type lang: str
      :return: True if the language is present, False otherwise.
      :rtype: bool

      :Example:
      >>> mls = MultiLangString({"en": {"Hello"}, "fr": {"Bonjour"}})
      >>> print("en" in mls)  # Output: True
      >>> print("es" in mls)  # Output: False



   .. py:method:: __delitem__(lang)

      Allow deletion of language entries.

      This method mimics the behavior of the 'del' operator for dictionaries, allowing users to delete a language
      entry from the MultiLangString.

      :param lang: The language code to delete.
      :type lang: str
      :raises KeyError: If the language is not found in the MultiLangString.

      :Example:
      >>> mls = MultiLangString({"en": {"Hello"}, "fr": {"Bonjour"}})
      >>> del mls["en"]
      >>> print(mls)  # Output: {'Bonjour'}@fr
      >>> del mls["es"]  # Raises KeyError



   .. py:method:: __eq__(other)

      Check equality of this MultiLangString with another MultiLangString.

      This method mimics the behavior of the '==' operator for dictionaries, allowing users to compare two
      MultiLangString objects for equality based on their mls_dict attributes.
      The pref_lang attribute is not considered in the equality check.

      :param other: Another object to compare with.
      :type other: object
      :return: True if both MultiLangString objects have the same mls_dict, False otherwise.
      :rtype: bool

      :Example:
      >>> mls1 = MultiLangString({"en": {"Hello"}, "fr": {"Bonjour"}})
      >>> mls2 = MultiLangString({"en": {"Hello"}, "fr": {"Bonjour"}})
      >>> print(mls1 == mls2)  # Output: True
      >>> mls3 = MultiLangString({"en": {"Hi"}, "fr": {"Salut"}})
      >>> print(mls1 == mls3)  # Output: False



   .. py:method:: __getitem__(lang)

      Allow retrieval of entries by language.

      This method mimics the behavior of the dictionary 'getitem' method, allowing users to retrieve the set of
      text entries associated with a specified language code from the MultiLangString.
      Raises KeyError if the language is not found.

      :param lang: The language code to retrieve entries for.
      :type lang: str
      :return: A set of text entries associated with the specified language.
      :rtype: set[str]
      :raises KeyError: If the language is not found in the MultiLangString.

      :Example:
      >>> mls = MultiLangString({"en": {"Hello", "World"}, "fr": {"Bonjour"}})
      >>> print(mls["en"])  # Output: {'Hello', 'World'}
      >>> print(mls["es"])  # Raises KeyError



   .. py:method:: __hash__()

      Generate a hash value for a MultiLangString object.

      This method mimics the behavior of the dictionary 'hash' method, allowing users to obtain a hash value
      for the MultiLangString. The hash is computed based on the 'mls_dict' attribute, ensuring that
      MultiLangString objects with the same content will have the same hash value.
      I.e., the pref_lang attribute is not considered in the hash creation.

      :return: The hash value of the MultiLangString object.
      :rtype: int

      :Example:
      >>> mls1 = MultiLangString({"en": {"Hello", "World"}, "fr": {"Bonjour"}}, pref_lang="en")
      >>> mls2 = MultiLangString({"en": {"Hello", "World"}, "fr": {"Bonjour"}}, pref_lang="pt")
      >>> print(hash(mls1) == hash(mls2))  # Output: True



   .. py:method:: __iter__()

      Allow iteration over the dictionary keys (language codes).

      This method mimics the behavior of the dictionary 'iter' method, allowing users to iterate over the
      language codes present in the MultiLangString.

      :return: An iterator over the language codes.
      :rtype: iterator

      :Example:
      >>> mls = MultiLangString({"en": {"Hello"}, "fr": {"Bonjour"}})
      >>> for lang in mls:
      >>>     print(lang)
      >>> # Output:   en
      >>> #           fr



   .. py:method:: __len__()

      Return the number of languages in the dictionary.

      This method mimics the behavior of the dictionary 'len' method, allowing users to get the number of
      language entries present in the MultiLangString.

      :return: The number of language entries.
      :rtype: int

      :Example:
      >>> mls = MultiLangString({"en": {"Hello"}, "fr": {"Bonjour"}})
      >>> print(len(mls))  # Output: 2



   .. py:method:: __repr__()

      Return a detailed string representation of the MultiLangString object.

      This method provides a more verbose string representation of the MultiLangString, which includes the full
      dictionary of language strings and the preferred language, making it useful for debugging.

      :return: A detailed string representation of the MultiLangString.
      :rtype: str

      :Example:
      >>> mls = MultiLangString({"en": {"Hello"}, "fr": {"Bonjour"}})
      >>> print(repr(mls))  # Output: 'MultiLangString(mls_dict={'en': {'Hello'}, 'fr': {'Bonjour'}}, pref_lang='en')'



   .. py:method:: __reversed__()

      Return a reverse iterator over the dictionary keys.

      This method allows for iterating over the language codes in the MultiLangString in reverse order.

      :return: A reverse iterator over the dictionary keys.
      :rtype: reverse_iterator

      :Example:
      >>> mls = MultiLangString({"en": {"Hello"}, "fr": {"Bonjour"}})
      >>> reversed_langs = list(reversed(mls))
      >>> print(reversed_langs)  # Output: ['fr', 'en']



   .. py:method:: __setitem__(lang, texts)

      Allow setting entries by language.

      This method allows for setting the text entries for a given language in the MultiLangString, mimicking
      dictionary behavior. If the language does not exist, it is added.

      :param lang: The language code.
      :type lang: str
      :param texts: A set of text entries to associate with the language.
      :type texts: set[str]

      :Example:
      >>> mls = MultiLangString()
      >>> mls["en"] = {"Hello", "World"}
      >>> mls["es"] = {"Hola"}
      >>> print(mls)  # Output: {'Hello', 'World'}@en, {'Hola'}@es
      >>> mls["en"] = {"Bye"}
      >>> print(mls)  # Output: {'Bye'}@en, {'Hola'}@es



   .. py:method:: __str__()

      Return a string representation of the MultiLangString, including language tags.

      This method provides a concise string representation of the MultiLangString, listing each text entry with its
      associated language tag. The output is sorted alphabetically by language and then by text within each language.

      :return: A string representation of the MultiLangString with language tags.
      :rtype: str

      :Example:
      >>> mls = MultiLangString({"en": {"World", "Hello"}, "fr": {"Bonjour"}})
      >>> print(mls)  # Output: {'Hello', 'World'}@en, {'Bonjour'}@fr



   .. py:method:: merge_multilangstrings(multilangstrings)
      :staticmethod:


      Merge multiple MultiLangString instances into a single MultiLangString.

      This static method takes a list of MultiLangString instances and merges them into a single
      MultiLangString. The resulting MultiLangString contains all languages and texts from the provided
      instances. If the list is empty, an empty MultiLangString is returned.

      :param multilangstrings: A list of MultiLangString instances to merge.
      :type multilangstrings: list[MultiLangString]
      :return: A new MultiLangString containing all languages and texts from the provided instances.
      :rtype: MultiLangString

      :Example:
      >>> mls1 = MultiLangString({"en": {"Hello"}, "fr": {"Bonjour"}})
      >>> mls2 = MultiLangString({"es": {"Hola"}, "en": {"World"}})
      >>> merged_mls = MultiLangString.merge_multilangstrings([mls1, mls2])
      >>> print(merged_mls)  # Output: {'Hello', 'World'}@en, {'Hola'}@es, {'Bonjour'}@fr



