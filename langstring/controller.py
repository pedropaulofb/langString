"""
The `controller` module provides the `Controller` class, a non-instantiable class designed to manage and manipulate \
configuration flags for the `LangString`, `SetLangString`, and `MultiLangString` classes.

This module defines the `Controller` class, which offers class methods to set, retrieve, print, and reset configuration
flags. These flags influence the behavior and validation rules of the multilingual text handling classes within the
application. By centralizing flag management, the `Controller` ensures consistent configuration and behavior across
the system.

Key Features:
- **Global Configuration**: The `Controller` manages flags globally, allowing uniform behavior across different
  multilingual text classes.
- **Non-Instantiable Design**: The `Controller` class uses the `NonInstantiable` metaclass to prevent instantiation,
  emphasizing its role as a static configuration manager.
- **Flexible Flag Management**: Methods are provided to set, retrieve, print, and reset individual or all flags,
  enabling dynamic configuration during runtime.

Enums Utilized:
- **GlobalFlag**: Flags affecting the behavior of all classes.
- **LangStringFlag**: Flags specific to the `LangString` class.
- **SetLangStringFlag**: Flags specific to the `SetLangString` class.
- **MultiLangStringFlag**: Flags specific to the `MultiLangString` class.

The `Controller` class ensures that the multilingual text handling classes adhere to specified rules and constraints,
enhancing the robustness and reliability of multilingual content management.
"""

from typing import Optional
from typing import Union

from .flags import GlobalFlag
from .flags import LangStringFlag
from .flags import MultiLangStringFlag
from .flags import SetLangStringFlag
from .utils.non_instantiable import NonInstantiable


class Controller(metaclass=NonInstantiable):
    """
    Control class for managing configuration flags, designed to be non-instantiable.

    This class uses class methods to set and retrieve configuration flags for the behavior of the `LangString`,
    `SetLangString`, and `MultiLangString` classes, ensuring a consistent global configuration state. It is made
    non-instantiable by using the `NonInstantiable` metaclass, emphasizing its role as a static configuration manager
    rather than an object to be instantiated.

    :cvar _DEFAULT_FLAGS: The default state of each flag.
    :vartype DEFAULT_FLAGS: dict[Union[GlobalFlag, LangStringFlag, SetLangStringFlag, MultiLangStringFlag], bool]
    :cvar flags: Stores the current state of each flag.
    :vartype flags: dict[Union[GlobalFlag, LangStringFlag, SetLangStringFlag, MultiLangStringFlag], bool]

    :Example:

    Set a flag:
    >>> Controller.set_flag(GlobalFlag.LOWERCASE_LANG, True)

    Get a flag:
    >>> print(Controller.get_flag(GlobalFlag.LOWERCASE_LANG))
    # Output: True

    Reset a flag to its default value:
    >>> Controller.reset_flag(GlobalFlag.LOWERCASE_LANG)
    >>> print(Controller.get_flag(GlobalFlag.LOWERCASE_LANG))
    # Output: False

    Print the state of a specific flag:
    >>> Controller.print_flag(GlobalFlag.LOWERCASE_LANG)
    # Output: GlobalFlag.LOWERCASE_LANG = False

    Print the states of all flags:
    >>> Controller.print_flags()
    # Output: (Output of all flags with their states)

    Reset all flags to their default values:
    >>> Controller.reset_flags()
    >>> Controller.print_flags()
    # Output: (Output of all flags reset to their default states)
    """

    # Define the default values of all flags as a class-level private constant
    _DEFAULT_FLAGS: dict[Union[GlobalFlag, LangStringFlag, SetLangStringFlag, MultiLangStringFlag], bool] = {
        # Default values for GlobalFlags
        GlobalFlag.DEFINED_LANG: False,
        GlobalFlag.DEFINED_TEXT: False,
        GlobalFlag.ENFORCE_EXTRA_DEPEND: False,
        GlobalFlag.LOWERCASE_LANG: False,
        GlobalFlag.METHODS_MATCH_TYPES: False,
        GlobalFlag.PRINT_WITH_LANG: True,
        GlobalFlag.PRINT_WITH_QUOTES: True,
        GlobalFlag.STRIP_LANG: False,
        GlobalFlag.STRIP_TEXT: False,
        GlobalFlag.VALID_LANG: False,
        # Default values for LangStringFlags
        LangStringFlag.DEFINED_LANG: False,
        LangStringFlag.DEFINED_TEXT: False,
        LangStringFlag.LOWERCASE_LANG: False,
        LangStringFlag.METHODS_MATCH_TYPES: False,
        LangStringFlag.PRINT_WITH_LANG: True,
        LangStringFlag.PRINT_WITH_QUOTES: True,
        LangStringFlag.STRIP_LANG: False,
        LangStringFlag.STRIP_TEXT: False,
        LangStringFlag.VALID_LANG: False,
        # Default values for SetLangStringFlags
        SetLangStringFlag.DEFINED_LANG: False,
        SetLangStringFlag.DEFINED_TEXT: False,
        SetLangStringFlag.LOWERCASE_LANG: False,
        SetLangStringFlag.METHODS_MATCH_TYPES: False,
        SetLangStringFlag.PRINT_WITH_LANG: True,
        SetLangStringFlag.PRINT_WITH_QUOTES: True,
        SetLangStringFlag.STRIP_LANG: False,
        SetLangStringFlag.STRIP_TEXT: False,
        SetLangStringFlag.VALID_LANG: False,
        # Default values for MultiLangStringFlags
        MultiLangStringFlag.DEFINED_LANG: False,
        MultiLangStringFlag.DEFINED_TEXT: False,
        MultiLangStringFlag.LOWERCASE_LANG: False,
        MultiLangStringFlag.PRINT_WITH_LANG: True,
        MultiLangStringFlag.PRINT_WITH_QUOTES: True,
        MultiLangStringFlag.STRIP_LANG: False,
        MultiLangStringFlag.STRIP_TEXT: False,
        MultiLangStringFlag.VALID_LANG: False,
    }

    # Mutable copy of default flag values to track the current state of flags.
    flags: dict[Union[GlobalFlag, LangStringFlag, SetLangStringFlag, MultiLangStringFlag], bool] = _DEFAULT_FLAGS.copy()

    @classmethod
    def set_flag(
        cls, flag: Union[GlobalFlag, LangStringFlag, SetLangStringFlag, MultiLangStringFlag], state: bool
    ) -> None:
        """
        Set the state of a specified configuration flag for LangString, SetLangString, or MultiLangString.

        If a GlobalFlag is set, it also sets the corresponding flags in LangStringFlag, SetLangStringFlag,
        and MultiLangStringFlag to the same state.

        :param flag: The flag to be set, either an instance of one of the flag enums.
        :type flag: Union[GlobalFlag, LangStringFlag, SetLangStringFlag, MultiLangStringFlag]
        :param state: Setting this to True or False will enable or disable the flag, respectively.
        :type state: bool
        :raises TypeError: If 'flag' is not an instance of one of the flag enums, or if 'state' is not a boolean.

        :Example:

        >>> Controller.set_flag(GlobalFlag.LOWERCASE_LANG, True)
        >>> print(Controller.get_flag(GlobalFlag.LOWERCASE_LANG))  # Output: True
        """
        if not isinstance(state, bool):
            raise TypeError("Invalid state received. State must be a boolean new_text.")

        if not isinstance(flag, (GlobalFlag, LangStringFlag, SetLangStringFlag, MultiLangStringFlag)):
            raise TypeError(
                f"Invalid flag type. Expected GlobalFlag, LangStringFlag, SetLangStringFlag, or MultiLangStringFlag, "
                f"got '{type(flag).__name__}'."
            )

        if isinstance(flag, GlobalFlag):
            # Set the state for all flags that match the name of the global flag
            for key in cls.flags:
                if key.name == flag.name:
                    cls.flags[key] = state
        else:
            # Set the state for the specific flag
            cls.flags[flag] = state

    @classmethod
    def get_flag(cls, flag: Union[GlobalFlag, LangStringFlag, SetLangStringFlag, MultiLangStringFlag]) -> bool:
        """
        Retrieve the current state of a specified configuration flag.

        Available for GlobalFlag, LangString, SetLangString, or MultiLangString.

        This class method provides a way to access the state of a flag globally for LangString, SetLangString,
        and MultiLangString classes.

        :param flag: The flag whose state is to be retrieved, either an instance of GlobalFlag, LangStringFlag,
                     SetLangStringFlag, or MultiLangStringFlag.
        :type flag: Union[GlobalFlag, LangStringFlag, SetLangStringFlag, MultiLangStringFlag]
        :return: The current state of the flag.
        :rtype: bool
        :raises TypeError: If 'flag' is not a member of GlobalFlag, LangStringFlag, SetLangStringFlag,
                           or MultiLangStringFlag.

        :Example:

        >>> Controller.set_flag(GlobalFlag.LOWERCASE_LANG, True)
        >>> print(Controller.get_flag(GlobalFlag.LOWERCASE_LANG))  # Output: True
        """
        if not isinstance(flag, (GlobalFlag, LangStringFlag, SetLangStringFlag, MultiLangStringFlag)):
            raise TypeError(
                f"Invalid flag type. Expected GlobalFlag, LangStringFlag, SetLangStringFlag, or MultiLangStringFlag, "
                f"got '{type(flag).__name__}'."
            )

        return cls.flags.get(flag, False)

    @classmethod
    def get_flags(cls) -> dict[Union[GlobalFlag, LangStringFlag, SetLangStringFlag, MultiLangStringFlag], bool]:
        """
        Retrieve the current state of all configuration flags.

        This class method provides a way to access the states of all flags globally for LangString, SetLangString,
        and MultiLangString classes.
        It returns a copy of the flags dictionary, ensuring that the original data is not modified.

        :return: A dictionary mapping each flag to its boolean state.
        :rtype: dict[Union[GlobalFlag, LangStringFlag, SetLangStringFlag, MultiLangStringFlag], bool]

        :Example:

        >>> Controller.set_flag(GlobalFlag.LOWERCASE_LANG, True)
        >>> flags = Controller.get_flags()
        >>> print(flags[GlobalFlag.LOWERCASE_LANG])  # Output: True
        """
        return cls.flags.copy()

    @classmethod
    def print_flag(cls, flag: type[Union[GlobalFlag, LangStringFlag, SetLangStringFlag, MultiLangStringFlag]]) -> None:
        """
        Print the current state of a specific configuration flag.

        This class method prints the state of the specified flag to the console. It is useful for checking the state
        of an individual flag for LangString, SetLangString, MultiLangString, or GlobalFlag.

        :param flag: The flag whose state is to be printed.
        :type flag: Union[GlobalFlag, LangStringFlag, SetLangStringFlag, MultiLangStringFlag]
        :raises TypeError: If 'flag' is not an instance of one of the flag enums.

        :Example:

        >>> Controller.set_flag(GlobalFlag.LOWERCASE_LANG, True)
        >>> Controller.print_flag(GlobalFlag.LOWERCASE_LANG)  # Output: GlobalFlag.LOWERCASE_LANG = True
        """
        if not isinstance(flag, (GlobalFlag, LangStringFlag, SetLangStringFlag, MultiLangStringFlag)):
            raise TypeError(
                f"Invalid flag type. Expected GlobalFlag, LangStringFlag, SetLangStringFlag, or MultiLangStringFlag, "
                f"got '{type(flag).__name__}'."
            )

        flag_state = cls.flags.get(flag, False)
        print(f"{flag.__class__.__name__}.{flag.name} = {flag_state}")

    @classmethod
    def print_flags(cls, flag_type: Optional[type] = None) -> None:
        """
        Print the current state of configuration flags in alphabetical order.

        If a flag type is specified, only flags of that type are printed.
        If no flag type is specified, all flags are printed.

        :param flag_type: The type of flags to print (e.g., GlobalFlag, LangStringFlag). If None, all flags are printed.
        :type flag_type: Optional[type]
        :raises TypeError: If 'flag_type' is not a valid flag type.

        :Example:

        >>> Controller.set_flag(GlobalFlag.LOWERCASE_LANG, True)
        >>> Controller.print_flags()
        # Output: Prints all flags and their current state.
        """
        if flag_type:
            if not isinstance(flag_type, type):
                raise TypeError(f"Invalid flag type. Expected a class type, got '{type(flag_type).__name__}'.")
            if not issubclass(flag_type, (GlobalFlag, LangStringFlag, SetLangStringFlag, MultiLangStringFlag)):
                raise TypeError(
                    f"Invalid flag type. "
                    f"Expected GlobalFlag, LangStringFlag, SetLangStringFlag, or MultiLangStringFlag, "
                    f"got '{flag_type.__name__}'."
                )

        sorted_flags = sorted(cls.flags.items(), key=lambda item: item[0].__class__.__name__ + "." + item[0].name)
        for flag, state in sorted_flags:
            if flag_type is None or isinstance(flag, flag_type):
                print(f"{flag.__class__.__name__}.{flag.name} = {state}")

    @classmethod
    def reset_flag(cls, flag: Union[GlobalFlag, LangStringFlag, SetLangStringFlag, MultiLangStringFlag]) -> None:
        """
        Reset a specific flag to its default value.

        If the flag is of type GlobalFlag, reset all equivalent flags of other types.
        For example, reset_flag(GlobalFlag.VALID_TEXT) will reset GlobalFlag.VALID_TEXT, LangStringFlag.VALID_TEXT,
        SetLangStringFlag.VALID_TEXT, and MultiLangStringFlag.VALID_TEXT.

        :param flag: The flag to be reset.
        :type flag: Union[GlobalFlag, LangStringFlag, SetLangStringFlag, MultiLangStringFlag]
        :raises TypeError: If 'flag' is not an instance of one of the flag enums.

        :Example:

        >>> Controller.set_flag(GlobalFlag.LOWERCASE_LANG, True)
        >>> Controller.reset_flag(GlobalFlag.LOWERCASE_LANG)
        >>> print(Controller.get_flag(GlobalFlag.LOWERCASE_LANG))  # Output: False
        """
        all_flag_types = (GlobalFlag, LangStringFlag, SetLangStringFlag, MultiLangStringFlag)

        if not isinstance(flag, all_flag_types):
            raise TypeError(
                f"Invalid flag. Expected GlobalFlag, LangStringFlag, SetLangStringFlag, "
                f"or MultiLangStringFlag, but got {type(flag).__name__}."
            )

        if isinstance(flag, GlobalFlag):
            flag_name = flag.name
            for flag_type in all_flag_types:
                # Check if the flag_type has an attribute with the name of the GlobalFlag
                if hasattr(flag_type, flag_name):
                    # Access the specific member of the flag_type using its name
                    matching_flag = getattr(flag_type, flag_name)
                    cls.flags[matching_flag] = cls._DEFAULT_FLAGS[matching_flag]
        else:
            cls.flags[flag] = cls._DEFAULT_FLAGS[flag]

    @classmethod
    def reset_flags(cls, flag_type: Optional[type] = GlobalFlag) -> None:
        """
        Reset all flags of a specific type to their default values.

        :param flag_type: The type of flags to reset (e.g., GlobalFlag, LangStringFlag). If None, all flags are reset.
        :type flag_type: Optional[type]
        :raises TypeError: If 'flag_type' is not a valid flag type.

        :Example:

        >>> Controller.set_flag(GlobalFlag.LOWERCASE_LANG, True)
        >>> Controller.reset_flags(GlobalFlag)
        >>> print(Controller.get_flag(GlobalFlag.LOWERCASE_LANG))  # Output: False
        """
        if flag_type is not None and not isinstance(flag_type, type):
            raise TypeError("Invalid flag type. Expected a class type.")

        if not flag_type or not issubclass(
            flag_type, (GlobalFlag, LangStringFlag, SetLangStringFlag, MultiLangStringFlag)
        ):
            raise TypeError(
                "Invalid flag type. Expected GlobalFlag, LangStringFlag, SetLangStringFlag, or MultiLangStringFlag."
            )

        if flag_type == GlobalFlag:
            cls.flags = cls._DEFAULT_FLAGS.copy()
        else:
            for flag, default_value in cls._DEFAULT_FLAGS.items():
                if isinstance(flag, flag_type):
                    cls.flags[flag] = default_value
