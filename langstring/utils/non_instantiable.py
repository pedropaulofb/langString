"""
The `non_instantiable` module provides the `NonInstantiable` metaclass, designed to prevent the instantiation \
of any class that uses it.

This module is useful for creating classes intended solely as namespaces or containers for static methods and
class variables, without allowing instances of such classes to be created.

Key Features:
- **Instantiation Prevention**: `NonInstantiable` ensures that any attempt to instantiate a class using this
  metaclass will raise a `TypeError`.

Classes:
- **NonInstantiable**: A metaclass that overrides the default instantiation behavior to prevent class
  instantiation.

:Example:

    >>> class MyClass(metaclass=NonInstantiable):
    ...     @staticmethod
    ...     def my_static_method():
    ...         return "This is a static method"
    ...
    >>> try:
    ...     instance = MyClass()
    ... except TypeError as e:
    ...     print(e)  #Output: 'MyClass class cannot be instantiated.'
    ...

The `NonInstantiable` metaclass is particularly useful for creating utility classes where instantiation does
not make sense and should be prevented by design.
"""


class NonInstantiable(type):
    """
    A metaclass that prevents the instantiation of any class that uses it.

    When a class is defined with `NonInstantiable` as its metaclass, any attempt to instantiate that class will
    result in a `TypeError`. This is useful for creating classes that are meant to be used as namespaces or
    containers for static methods and class variables, without the intention of creating instances.

    Key Features:
    - **Prevent Instantiation**: Ensures that any attempt to create an instance of a class using this metaclass
      will raise a `TypeError`.
    - **Namespace Utility**: Ideal for defining classes that serve as namespaces or containers for static methods
      and constants.

    :Example:

        >>> class MyClass(metaclass=NonInstantiable):
        ...     @staticmethod
        ...     def my_static_method():
        ...         return "This is a static method"
        ...
        >>> try:
        ...     instance = MyClass()
        ... except TypeError as e:
        ...     print(e)  #Output: 'MyClass class cannot be instantiated.'
        ...

    Methods:
        __call__: Overrides the default call behavior to prevent instantiation.
    """

    def __call__(cls) -> None:
        """
        Override the default call behavior to prevent instantiation of the class.

        When this method is called, it raises a `TypeError`, effectively preventing the creation of an instance of the
        class that uses `NonInstantiable` as its metaclass.

        :raises TypeError: Always, to indicate that the class cannot be instantiated.

        :Example:

            >>> class MyClass(metaclass=NonInstantiable):
            ...     @staticmethod
            ...     def my_static_method():
            ...         return "This is a static method"
            ...
            >>> try:
            ...     instance = MyClass()
            ... except TypeError as e:
            ...     print(e)  #Output: 'MyClass class cannot be instantiated.'
            ...
        """
        raise TypeError(f"{cls.__name__} class cannot be instantiated.")
