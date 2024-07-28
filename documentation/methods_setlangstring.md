# Methods in SetLangString Class

<!-- TOC -->
* [Methods in SetLangString Class](#methods-in-setlangstring-class)
  * [Initialization and Properties](#initialization-and-properties)
  * [SetLangString's Regular Methods](#setlangstrings-regular-methods)
  * [Overwritten Set's Built-in Regular Methods](#overwritten-sets-built-in-regular-methods)
  * [Overwritten Set's Built-in Dunder Methods](#overwritten-sets-built-in-dunder-methods)
  * [Static Methods](#static-methods)
<!-- TOC -->

## Initialization and Properties

- `__init__(self, texts: Optional[Union[set[str], list[str]]] = None, lang: str = "") -> None`
  - Initialize a new SetLangString object with a set of texts and an optional language tag.

- `texts(self) -> set[str]`
  - Get the set of text strings.

- `texts(self, new_texts: Optional[Union[set[str], list[str]]]) -> None`
  - Set the set of text strings with validation based on control flags.

- `lang(self) -> str`
  - Get the language tag.

- `lang(self, new_lang: str) -> None`
  - Set the language tag with validation based on control flags.

## SetLangString's Regular Methods

- `add_langstring(self, langstring: LangString) -> None`
  - Add a LangString object to the set of texts.

- `add_text(self, text: str) -> None`
  - Add a text string to the set of texts.

- `discard_text(self, text: str) -> None`
  - Discard a text string from the set of texts without raising an error if not found.

- `discard_langstring(self, langstring: LangString) -> None`
  - Discard a LangString object from the set of texts without raising an error if not found.

- `remove_langstring(self, langstring: LangString) -> None`
  - Remove a LangString object from the set of texts, raising a KeyError if not found.

- `remove_text(self, text: str) -> None`
  - Remove a text string from the set of texts, raising a KeyError if not found.

- `to_langstrings(self) -> list[LangString]`
  - Convert the set of texts to a list of LangString objects.

- `to_strings(self, print_quotes: Optional[bool] = None, separator: str = "@", print_lang: Optional[bool] = None) -> list[str]`
  - Convert the set of texts to a list of formatted strings.

## Overwritten Set's Built-in Regular Methods

- `add(self, new_element: Union[str, LangString]) -> None`
  - Add a new element to the set of texts.

- `clear(self) -> None`
  - Remove all elements from the set of texts.

- `copy(self) -> "SetLangString"`
  - Create a shallow copy of the SetLangString.

- `discard(self, element: Union[str, LangString]) -> None`
  - Discard an element from the set of texts without raising an error if not found.

- `pop(self) -> str`
  - Remove and return an arbitrary element from the set of texts, raising a KeyError if empty.

- `remove(self, element: Union[str, LangString]) -> None`
  - Remove an element from the set of texts, raising a KeyError if not found.

- `difference(self, *others: Union[set[str], "SetLangString"]) -> "SetLangString"`
  - Return the difference of the set and another set or sets.

- `difference_update(self, *others: Union[set[str], "SetLangString"]) -> None`
  - Update the set, removing elements found in others.

- `isdisjoint(self, other: Union[set[str], "SetLangString"]) -> bool`
  - Return True if the set has no elements in common with another set.

- `issubset(self, other: Union[set[str], "SetLangString"]) -> bool`
  - Return True if the set is a subset of another set.

- `issuperset(self, other: Union[set[str], "SetLangString"]) -> bool`
  - Return True if the set is a superset of another set.

- `intersection(self, *others: Union[set[str], "SetLangString"]) -> "SetLangString"`
  - Return the intersection of the set and other sets.

- `intersection_update(self, *others: Union[set[str], "SetLangString"]) -> None`
  - Update the set, keeping only elements found in it and all others.

- `symmetric_difference(self, other: Union[set[str], "SetLangString"]) -> "SetLangString"`
  - Return the symmetric difference of the set and another set.

- `symmetric_difference_update(self, other: Union[set[str], "SetLangString"]) -> None`
  - Update the set, keeping only elements found in either set, but not in both.

- `union(self, *others: Union[set[str], "SetLangString"]) -> "SetLangString"`
  - Return the union of the set and other sets.

- `update(self, *others: Union[set[str], "SetLangString"]) -> None`
  - Update the set, adding elements from all others.

## Overwritten Set's Built-in Dunder Methods

- `__and__(self, other: Union[set[str], "SetLangString"]) -> "SetLangString"`
  - Return the intersection of the set and another set using the & operator.

- `__contains__(self, element: Union[str, LangString]) -> bool`
  - Return True if the set contains the specified element.

- `__eq__(self, other: object) -> bool`
  - Return True if the set is equal to another set.

- `__ge__(self, other: Union[set[str], "SetLangString"]) -> bool`
  - Return True if the set is a superset of another set using the >= operator.

- `__gt__(self, other: Union[set[str], "SetLangString"]) -> bool`
  - Return True if the set is a proper superset of another set using the > operator.

- `__hash__(self) -> int`
  - Generate a hash for a SetLangString object.

- `__iand__(self, other: Union[set[str], "SetLangString"]) -> "SetLangString"`
  - Update the set, keeping only elements found in it and another set using the &= operator.

- `__ior__(self, other: Union[set[str], "SetLangString"]) -> "SetLangString"`
  - Update the set, adding elements from another set using the |= operator.

- `__isub__(self, other: Union[set[str], "SetLangString"]) -> "SetLangString"`
  - Update the set, removing elements found in another set using the -= operator.

- `__iter__(self) -> Iterator[str]`
  - Return an iterator over the elements of the set.

- `__ixor__(self, other: Union[set[str], "SetLangString"]) -> "SetLangString"`
  - Update the set, keeping only elements found in either set, but not in both using the ^= operator.

- `__le__(self, other: Union[set[str], "SetLangString"]) -> bool`
  - Return True if the set is a subset of another set using the <= operator.

- `__len__(self) -> int`
  - Return the number of elements in the set.

- `__lt__(self, other: Union[set[str], "SetLangString"]) -> bool`
  - Return True if the set is a proper subset of another set using the < operator.

- `__or__(self, other: Union[set[str], "SetLangString"]) -> "SetLangString"`
  - Return the union of the set and another set using the | operator.

- `__repr__(self) -> str`
  - Return the official string representation of the SetLangString object.

- `__str__(self) -> str`
  - Return the string representation of the SetLangString object.

- `__sub__(self, other: Union[set[str], "SetLangString"]) -> "SetLangString"`
  - Return the difference of the set and another set using the - operator.

- `__xor__(self, other: Union[set[str], "SetLangString"]) -> "SetLangString"`
  - Return the symmetric difference of the set and another set using the ^ operator.

## Static Methods

- `merge_setlangstrings(setlangstrings: list["SetLangString"]) -> list["SetLangString"]`
  - Merge duplicated SetLangStrings based on their language tags using the union method.
