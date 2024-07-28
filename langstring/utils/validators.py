"""
The `validators` module provides two classes, `TypeValidator` and `FlagValidator`, for validating argument types and \
flag-based constraints, respectively.

This module defines two classes:
- `TypeValidator`: Handles type validation for arguments based on type hints. It includes methods for validating
  single arguments, iterables, and decorated functions or methods.
- `FlagValidator`: Handles validation and transformation of text and language arguments based on configuration flags
  managed by the `Controller`.

The validators ensure that arguments and values adhere to specified types and constraints, enhancing the robustness
and reliability of the application.

Key Features:
- **Type Validation**: `TypeValidator` offers methods to validate single arguments, iterables, and function/method
  arguments based on type hints.
- **Flag-based Validation**: `FlagValidator` provides methods to validate and transform text and language arguments
  according to control flags.
- **Separation of Concerns**: By separating type validation and flag-based validation into different classes, the module
  maintains a clear and organized structure.

Classes:
- **TypeValidator**: Validates argument types based on type hints.
- **FlagValidator**: Validates and transforms arguments based on control flags.

Enums Utilized:
- **GlobalFlag**: Flags affecting the behavior of all classes.
- **LangStringFlag**: Flags specific to the `LangString` class.
- **SetLangStringFlag**: Flags specific to the `SetLangString` class.
- **MultiLangStringFlag**: Flags specific to the `MultiLangString` class.

The validators in this module are designed to be non-instantiable, emphasizing their role as static utility classes.
"""

import inspect
import warnings
from functools import wraps
from typing import Any
from typing import Callable
from typing import get_args
from typing import get_origin
from typing import get_type_hints
from typing import Optional
from typing import TypeVar
from typing import Union

from ..controller import Controller
from ..flags import GlobalFlag
from ..flags import LangStringFlag
from ..flags import MultiLangStringFlag
from ..flags import SetLangStringFlag
from .non_instantiable import NonInstantiable

# Generic type variable used for type hinting in the Validator class methods
T = TypeVar("T")


class FlagValidator(metaclass=NonInstantiable):
    """
    A utility class for validating and transforming text and language arguments based on configuration flags.

    The `FlagValidator` class provides static methods to validate and transform `text` and `lang` arguments
    according to the specified flag type. The validation rules and transformations are controlled by flags
    managed by the `Controller` class.

    The `FlagValidator` class is non-instantiable, emphasizing its role as a static utility class.

    Methods:
    - `validate_flags_text(flag_type: type[Enum], text: Optional[str]) -> str`: Validate and transform the `text`
      argument based on the specified flag type.
    - `validate_flags_lang(flag_type: type[Enum], lang: Optional[str]) -> Optional[str]`: Validate and transform the
      `lang` argument based on the specified flag type.

    Examples:
    - Validating and transforming text:
    >>> Controller.set_flag(GlobalFlag.STRIP_TEXT, True)
    >>> Controller.set_flag(GlobalFlag.DEFINED_TEXT, True)
    >>> print(FlagValidator.validate_flags_text(GlobalFlag, "  Hello  "))  # Output: Hello
    >>> print(FlagValidator.validate_flags_text(GlobalFlag, "     "))  # Raises ValueError
    >>> print(FlagValidator.validate_flags_text(GlobalFlag, None))  # Raises ValueError

    - Validating and transforming language:
    >>> Controller.set_flag(LangStringFlag.STRIP_LANG, True)
    >>> print(FlagValidator.validate_flags_lang(LangStringFlag, "  EN  "))  # Output: 'EN'
    >>> Controller.set_flag(LangStringFlag.LOWERCASE_LANG, True)
    >>> print(FlagValidator.validate_flags_lang(LangStringFlag, "  EN  "))  # Output: 'en'
    >>> Controller.set_flag(LangStringFlag.DEFINED_LANG, True)
    >>> try:
    ...     print(FlagValidator.validate_flags_lang(LangStringFlag, "  "))
    ... except ValueError as e:
    ...     print(e)  # Output: Invalid 'lang' value received ('  '). 'LangStringFlag.DEFINED_LANG' is enabled.
                      # Expected non-empty 'str' or 'str' with non-space characters.
    """

    @staticmethod
    def validate_flags_text(
        flag_type: type[Union[GlobalFlag, LangStringFlag, SetLangStringFlag, MultiLangStringFlag]], text: Optional[str]
    ) -> str:
        """
        Validate and transform the 'text' based on the specified flag type.

        This method ensures that the 'text' argument adheres to the constraints defined by various flags such as
        `STRIP_TEXT` and `DEFINED_TEXT`. If `DEFINED_TEXT` is enabled, it ensures that 'text' is a non-empty string.
        Additionally, it can strip whitespace from the 'text' based on the `STRIP_TEXT` flag.

        :param flag_type: The type of flags to be used for validation.
        :type flag_type: type[Union[GlobalFlag, LangStringFlag, SetLangStringFlag, MultiLangStringFlag]]
        :param text: The text to be validated and transformed.
        :type text: Optional[str]
        :return: The validated and transformed text.
        :rtype: str
        :raises TypeError: If 'flag_type' is not an instance of type or 'text' is not a string or 'None'.
        :raises ValueError: If the text does not meet the criteria specified by the control flags.

        :Example:

        >>> Controller.set_flag(GlobalFlag.STRIP_TEXT, True)
        >>> Controller.set_flag(GlobalFlag.DEFINED_TEXT, True)
        >>> print(FlagValidator.validate_flags_text(GlobalFlag, "  Hello  "))  # Output: Hello
        >>> print(FlagValidator.validate_flags_text(GlobalFlag, "     "))  # Raises ValueError
        >>> print(FlagValidator.validate_flags_text(GlobalFlag, None))  # Raises ValueError
        """
        TypeValidator.validate_type_single(flag_type, type)
        TypeValidator.validate_type_single(text, str, optional=True)

        # Initial message for potential errors
        original_text = text
        msg = f"Invalid 'text' value received ('{original_text}')."

        # Transform the text string according to STRIP_TEXT flag
        if text is not None:
            text = text.strip() if Controller.get_flag(flag_type.STRIP_TEXT) else text  # Apply STRIP_TEXT if enabled
            validate_text = text.strip()  # Remove 'whitespace characters' for validation
        else:
            validate_text = None

        # Check if DEFINED_TEXT flag is enabled and if the text is empty or None
        if Controller.get_flag(flag_type.DEFINED_TEXT) and not validate_text:
            raise ValueError(
                f"{msg} '{flag_type.__name__}.DEFINED_TEXT' is enabled. "
                f"Expected non-empty 'str' or 'str' with non-space characters."
            )

        return text or ""

    @staticmethod
    def validate_flags_lang(
        flag_type: type[Union[GlobalFlag, LangStringFlag, SetLangStringFlag, MultiLangStringFlag]], lang: Optional[str]
    ) -> str:
        """
        Validate and transform the 'lang' argument based on the specified flags.

        This method ensures that the 'lang' argument adheres to the constraints defined by various flags such as
        `STRIP_LANG`, `LOWERCASE_LANG`, `DEFINED_LANG`, and `VALID_LANG`. If `DEFINED_LANG` is enabled, it ensures
        that 'lang' is a non-empty string. If `VALID_LANG` is enabled, it verifies that 'lang' is a valid language code.
        Additionally, it can strip whitespace and convert the language code to lowercase based on the corresp. flags.

        :param flag_type: The type of flags to be used for validation, which should be one of the flag enums.
        :type flag_type: type[Union[GlobalFlag, LangStringFlag, SetLangStringFlag, MultiLangStringFlag]]
        :param lang: The language string to be validated and transformed. It can be None.
        :type lang: Optional[str]
        :return: The transformed language string if valid; otherwise, it raises an appropriate error.
        :rtype: str
        :raises ValueError: If 'lang' is empty and `DEFINED_LANG` is enabled, or if 'lang' is invalid and `VALID_LANG`
                            is enabled.
        :raises TypeError: If 'flag_type' is not of type 'Enum', or if 'lang' is not of type 'str' or 'None'.
        :raises ImportError: If 'VALID_LANG' is enabled but the 'langcodes' library is not installed and
                             `ENFORCE_EXTRA_DEPEND` is enabled.

        :Example:

        >>> Controller.set_flag(LangStringFlag.STRIP_LANG, True)
        >>> print(FlagValidator.validate_flags_lang(LangStringFlag, "  EN  "))  # Output: 'EN'
        >>> Controller.set_flag(LangStringFlag.LOWERCASE_LANG, True)
        >>> print(FlagValidator.validate_flags_lang(LangStringFlag, "  EN  "))  # Output: 'en'
        >>> Controller.set_flag(LangStringFlag.DEFINED_LANG, True)
        >>> try:
        ...     print(FlagValidator.validate_flags_lang(LangStringFlag, "  "))
        ... except ValueError as e:
        ...     print(e)  # Output: Invalid 'lang' value received ('  '). 'LangStringFlag.DEFINED_LANG' is enabled.
                          # Expected non-empty 'str' or 'str' with non-space characters.
        """

        def handle_validation_error(
            original_lang: Optional[str],
            flag_type: type[Union[GlobalFlag, LangStringFlag, SetLangStringFlag, MultiLangStringFlag]],
        ) -> None:
            """
            Raise a ValueError indicating the 'lang' value is invalid according to the specified flag type.

            :param original_lang: The original language value that was validated.
            :type original_lang: Optional[str]
            :param flag_type: The type of flag that indicates the validation rule.
            :type flag_type: type[Union[GlobalFlag, LangStringFlag, SetLangStringFlag, MultiLangStringFlag]]
            :raises ValueError: If the 'lang' value is invalid.
            """
            raise ValueError(
                f"Invalid 'lang' value received ('{original_lang}'). "
                f"'{flag_type.__name__}.VALID_LANG' is enabled. Expected valid language code."
            )

        def handle_import_error(e: ImportError) -> None:
            """
            Handle ImportError for the 'langcodes' library.

            Depending on the ENFORCE_EXTRA_DEPEND flag, this function either raises an ImportError with an appropriate
            message or issues a warning about the missing 'langcodes' library.

            :param e: The original ImportError exception.
            :type e: ImportError
            :raises ImportError: If the ENFORCE_EXTRA_DEPEND flag is set.
            :raises UserWarning: If the ENFORCE_EXTRA_DEPEND flag is not set.
            """
            if Controller.get_flag(GlobalFlag.ENFORCE_EXTRA_DEPEND):
                error_message = (
                    str(e) + ". VALID_LANG functionality requires the 'langcodes' library. "
                    "Install it with 'pip install langstring[langcodes]'."
                )
                raise ImportError(error_message) from e

            warnings.warn(
                "Language validation skipped. VALID_LANG functionality requires the 'langcodes' library. "
                "Install it with 'pip install langstring[langcodes]' to enable this feature.",
                UserWarning,
            )

        TypeValidator.validate_type_single(flag_type, type)
        TypeValidator.validate_type_single(lang, str, optional=True)

        # Initial message for potential errors
        original_lang = lang
        msg = f"Invalid 'lang' value received ('{original_lang}')."

        # Transform the lang string according to STRIP_LANG and LOWERCASE_LANG flags
        if lang is not None:
            lang = lang.strip() if Controller.get_flag(flag_type.STRIP_LANG) else lang  # Apply STRIP_LANG if enabled
            transformed_lang = (
                lang.casefold() if Controller.get_flag(flag_type.LOWERCASE_LANG) else lang
            )  # Apply LOWERCASE_LANG if enabled
            validate_lang = transformed_lang.strip()  # Remove 'whitespace characters' for validation
        else:
            transformed_lang = ""
            validate_lang = ""

        # Check if DEFINED_LANG flag is enabled and lang is empty or only whitespace
        if Controller.get_flag(flag_type.DEFINED_LANG) and not validate_lang:
            raise ValueError(
                f"{msg} '{flag_type.__name__}.DEFINED_LANG' is enabled. "
                f"Expected non-empty 'str' or 'str' with non-space characters."
            )

        # Perform language validation if VALID_LANG flag is enabled
        if Controller.get_flag(flag_type.VALID_LANG):
            try:
                from langcodes import tag_is_valid  # type: ignore[import-not-found]

                if not tag_is_valid(transformed_lang):
                    handle_validation_error(original_lang or "", flag_type)
            except ImportError as e:
                handle_import_error(e)

        return transformed_lang


class TypeValidator(metaclass=NonInstantiable):
    """
    A utility class for validating the types of arguments passed to functions and methods.

    The `TypeValidator` class provides static methods to validate single arguments, iterables, and to apply type
    validation decorators to functions or methods.
    The validation ensures that the arguments match the specified type hints.

    The `TypeValidator` class is non-instantiable, emphasizing its role as a static utility class.

    Methods:
    - `_check_arg(arg: Any, hint: type[Any]) -> bool`: Check if the argument matches the type hint.
    - `validate_type_decorator(func: Callable[..., T]) -> Callable[..., T]`: Decorator to validate the types of
       arguments passed to a function or method based on their type hints.
    - `validate_type_single(arg: Any, arg_exp_type: type, optional: bool = False) -> None`: Validate that a single
       argument matches the expected type.
    - `validate_type_iterable(arg: Any, arg_exp_type: type, arg_content_exp_type: type, optional: bool = False)
                                                                                                            -> None`:
      Validate that an argument is an iterable of the expected type and that its contents match the expected
      content type.

    Examples:
    - Using the type validation decorator:
    >>> @TypeValidator.validate_type_decorator
    ... def greet(name: str, age: int) -> str:
    ...     return f"Hello, {name}. You are {age} years old."
    ...
    >>> print(greet("Alice", 30))  # Output: Hello, Alice. You are 30 years old.

    >>> @TypeValidator.validate_type_decorator
    ... def process_list(data: list[int]) -> int:
    ...     return sum(data)
    ...
    >>> print(process_list([1, 2, 3]))  # Output: 6

    >>> @TypeValidator.validate_type_decorator
    ... def union_example(value: Union[int, str]) -> str:
    ...     return f"Received: {value}"
    ...
    >>> print(union_example(42))  # Output: Received: 42
    >>> print(union_example("42"))  # Output: Received: 42

    - Validating a single argument:
    >>> TypeValidator.validate_type_single(5, int)  # Does not raise error.
    >>> TypeValidator.validate_type_single(5, str)  # Raise TypeError
    >>> TypeValidator.validate_type_single(None, str, optional=True)  # Does not raise error.

    - Validating an iterable:
    >>> TypeValidator.validate_type_iterable([1, 2, 3], list, int)  # Does not raise error.
    >>> TypeValidator.validate_type_iterable({"a", "b", "c"}, set, str)  # Does not raise error.
    >>> TypeValidator.validate_type_iterable({"a", "b", "c"}, list, str)  # Raises TypeError
    >>> TypeValidator.validate_type_iterable({"a", "b", "c"}, set, int)  # Raises TypeError
    >>> TypeValidator.validate_type_iterable(None, list, int, optional=True)  # Does not raise error.
    """

    @staticmethod
    def _check_arg(arg: Any, hint: type[Any]) -> bool:
        """
        Check if the argument matches the type hint.

        This private method validates that the provided argument matches the specified type hint.
        It supports basic types, parameterized generics like lists and dictionaries, and unions of types.
        It is intended to be used internally by the `validate_type_decorator` method for argument validation.

        This method has functionalities that the `validate_type_single` and `validate_type_iterable` methods do
        not fully cover:
        1. **Handling Union Types**:
            `_check_arg` can handle `Union` types, allowing for type hints that specify multiple possible
            types for an argument (e.g., `Union[int, str]`).
        2. **Parameterized Generics**:
            `_check_arg` supports parameterized generics such as `List[int]`, `Set[str]`, `Tuple[int, str]`,
            and `Dict[str, int]`. It checks both the container type and the types of the items within the container.
        3. **Nested Types**:
            `_check_arg` can validate more complex nested types,
            such as a list of dictionaries or a dictionary with tuple values.

        :param arg: The argument to be checked.
        :type arg: Any
        :param hint: The expected type of the argument.
        :type hint: type[Any]
        :return: True if the argument matches the type hint, otherwise raises a TypeError.
        :rtype: bool
        :raises TypeError: If the argument does not match the expected type hint.

        :Example:

        # Check a simple type
        >>> print(TypeValidator._check_arg(5, int))  # Output: True

        # Check a union type
        >>> print(TypeValidator._check_arg("test", Union[str, int]))  # Output: True

        # Check a list of integers
        >>> print(TypeValidator._check_arg([1, 2, 3], list[int]))  # Output: True

        # Check a dictionary with string keys and integer values
        >>> print(TypeValidator._check_arg({"a": 1, "b": 2}, dict[str, int]))  # Output: True

        # This will raise a TypeError because the argument does not match the expected type
        >>> print(TypeValidator._check_arg("test", int))  # Raises TypeError
        """
        origin = get_origin(hint)
        args = get_args(hint)

        # Handle Union types
        if origin is Union:
            if not any(isinstance(arg, t) for t in args):
                allowed_types = " or ".join(f"'{t.__name__}'" for t in args)
                raise TypeError(
                    f"Invalid argument with value '{arg}'. "
                    f"Expected one of {allowed_types}, but got '{type(arg).__name__}'."
                )
            return True

        # Handle parameterized generics
        if origin is not None:
            TypeValidator.validate_type_single(arg, origin)
            if args:
                # fmt: off
                if origin in (list, set, tuple):
                    for item in arg:
                        if not any(
                            isinstance(item, arg_type) or (
                                get_origin(arg_type) is Union and isinstance(item, tuple(get_args(arg_type)))
                            )
                            for arg_type in args
                        ):
                            allowed_types = " or ".join(f"'{t.__name__}'" for t in args)
                            raise TypeError(
                                f"Invalid item with value '{item}' in '{origin.__name__}'. "
                                f"Expected one of {allowed_types}, but got '{type(item).__name__}'."
                            )
                # fmt: on
                elif origin is dict:
                    key_type, value_type = args
                    # Validate the dictionary keys and values
                    for key, value in arg.items():
                        TypeValidator.validate_type_single(key, key_type)
                        TypeValidator.validate_type_single(value, value_type)
            return True

        # Handle simple types
        TypeValidator.validate_type_single(arg, hint)
        return True

    @staticmethod
    def validate_type_decorator(func: Callable[..., T]) -> Callable[..., T]:
        """
        Is a decorator to validate the types of arguments passed to a function or method based on their type hints.

        This method checks if each argument's type matches its corresponding type hint. It is intended for use with
        functions or instance methods where explicit type hints are provided for all arguments.

        Usage:
            - Apply this decorator to functions or instance methods that require type validation based on type hints.

        When to Use:
            - Use this decorator for functions or methods where argument types need to be strictly validated.
            - Suitable for validating primitive types (int, str, float, bool, etc.), Optional types, and Union types.
            - Useful for parameterized generics like List[int], Set[str], etc., to ensure both the container and its
            contents match the specified types.
            - Appropriate for instance methods, adjusting for the 'self' parameter automatically.
            - Suitable for static methods but requires manual validation for class methods and setters.

        When Not to Use:
            - Do not use this decorator for class methods with the 'cls' parameter. It doesn`t handle 'cls' explicitly.
            - Avoid using this decorator for property setters.
            - This decorator is not suitable for methods with parameters involving generic collections parameterized
              with type variables (e.g., List[T] where T is a type variable).
            - Complex nested generics (e.g., List[Dict[str, Union[int, List[str]]]]) might not be fully validated.
            - Specifically, cases like `(["test", 1], list, False)` (List with mixed types) and nested `Union` within
              parameterized generics (e.g., `list[Union[int, str]]`) are out of scope and will not be correctly
              validated by this decorator.

        :param func: The function or method to be decorated.
        :type func: Callable[..., T]
        :return: The decorated function or method with type validation applied.
        :rtype: Callable[..., T]
        :raises TypeError: If an argument's type does not match its type hint.

        :Example:

        >>> @TypeValidator.validate_type_decorator
        ... def greet(name: str, age: int) -> str:
        ...     return f"Hello, {name}. You are {age} years old."
        ...
        >>> print(greet("Alice", 30))  # Output: Hello, Alice. You are 30 years old.

        >>> @TypeValidator.validate_type_decorator
        ... def process_list(data: list[int]) -> int:
        ...     return sum(data)
        ...
        >>> print(process_list([1, 2, 3]))  # Output: 6

        # Raises TypeError because 'age' is expected to be an int, not a str
        >>> greet("Alice", "30")  # Raises TypeError

        # Raises TypeError because 'data' is expected to be a list[int], not a list[str]
        >>> process_list(["1", "2", "3"])  # Raises TypeError

        >>> @TypeValidator.validate_type_decorator
        ... def union_example(value: Union[int, str]) -> str:
        ...     return f"Received: {value}"
        ...
        >>> print(union_example(42))  # Output: Received: 42
        >>> print(union_example("42"))  # Output: Received: 42

        # Raises TypeError because 'value' is expected to be Union[int, str], not a list
        >>> union_example([42])  # Raises TypeError
        """

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Extract type hints from the function, excluding the return type
            type_hints = {k: v for k, v in get_type_hints(func).items() if k != "return"}
            # Get the parameter names from the function signature
            param_names = list(inspect.signature(func).parameters)

            # Check if the function is an instance method
            is_instance_method = "self" in param_names and len(args) > 0 and isinstance(args[0], args[0].__class__)
            if is_instance_method:
                # Remove 'self' from parameters and type hints for validation
                param_names.remove("self")
                type_hints.pop("self", None)
                # Skip 'self' when checking arguments
                args_to_check = args[1:]
            else:
                args_to_check = args

            # Validate positional arguments against their type hints
            for arg, (name, hint) in zip(args_to_check, zip(param_names, type_hints.values())):
                TypeValidator._check_arg(arg, hint)

            # Validate keyword arguments against their type hints
            for kwarg, hint in type_hints.items():
                if kwarg in kwargs:
                    TypeValidator._check_arg(kwargs[kwarg], hint)

            # Call the original function with validated arguments
            return func(*args, **kwargs)

        return wrapper

    @staticmethod
    def validate_type_single(arg: Any, arg_exp_type: type, optional: bool = False) -> None:
        """
        Validate that a single argument matches the expected type.

        This method checks if the provided argument is of the expected type. If the `optional` parameter is set to True,
        the argument can also be None. If the argument does not match the expected type, a TypeError is raised.

        :param arg: The argument to be checked.
        :type arg: Any
        :param arg_exp_type: The expected type of the argument.
        :type arg_exp_type: type
        :param optional: If True, the argument can be None.
        :type optional: bool
        :raises TypeError: If the argument does not match the expected type.

        :Example:

        >>> TypeValidator.validate_type_single(5, int)
        >>> TypeValidator.validate_type_single("test", str)
        >>> TypeValidator.validate_type_single(None, str, optional=True)

        # This will raise a TypeError because the argument is not of the expected type
        >>> TypeValidator.validate_type_single(5, str)
        # Raises TypeError: Invalid argument with value '5'. Expected 'str', but got 'int'.

        # This will also raise a TypeError because the argument is not of the expected type
        >>> TypeValidator.validate_type_single("test", int)
        # Raises TypeError: Invalid argument with value 'test'. Expected 'int', but got 'str'.
        """
        if optional and arg is None:
            return

        if not isinstance(arg, arg_exp_type):
            raise TypeError(
                f"Invalid argument with value '{arg}'. "
                f"Expected '{arg_exp_type.__name__}', but got '{type(arg).__name__}'."
            )

    @staticmethod
    def validate_type_iterable(
        arg: Any, arg_exp_type: type, arg_content_exp_type: type, optional: bool = False
    ) -> None:
        """
        Validate that an argument is an iterable of the expected type and that its contents match the expected \
        content type.

        This method checks if the provided argument is of the expected iterable type (e.g., list, set, tuple)
        and that each element within the iterable matches the expected content type.
        If the `optional` parameter is set to True, the argument can also be None.
        If the argument or its contents do not match the expected types, a TypeError is raised.

        :param arg: The iterable argument to be checked.
        :type arg: Any
        :param arg_exp_type: The expected type of the iterable argument.
        :type arg_exp_type: type
        :param arg_content_exp_type: The expected type of the elements within the iterable.
        :type arg_content_exp_type: type
        :param optional: If True, the argument can be None.
        :type optional: bool
        :raises TypeError: If the argument or its contents do not match the expected types.

        :Example:

        >>> TypeValidator.validate_type_iterable([1, 2, 3], list, int)
        >>> TypeValidator.validate_type_iterable({"a", "b", "c"}, set, str)
        >>> TypeValidator.validate_type_iterable(None, list, int, optional=True)

        # This will raise a TypeError because the argument is not of the expected iterable type
        >>> TypeValidator.validate_type_iterable([1, 2, 3], set, int)
        # Raises TypeError: Invalid argument with value '[1, 2, 3]'. Expected 'set', but got 'list'.

        # This will also raise a TypeError because the contents are not of the expected type
        >>> TypeValidator.validate_type_iterable([1, "2", 3], list, int)
        # Raises TypeError: Invalid argument with value '2'. Expected 'int', but got 'str'.
        """
        if optional and arg is None:
            return
        TypeValidator.validate_type_single(arg, arg_exp_type)
        for elem in arg:
            TypeValidator.validate_type_single(elem, arg_content_exp_type)
