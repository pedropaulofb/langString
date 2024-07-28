import pytest
from langstring.utils.non_instantiable import NonInstantiable


def test_noninstantiable_prevents_instantiation():
    """Test that NonInstantiable metaclass prevents instantiation of a class."""

    class TestClass(metaclass=NonInstantiable):
        """A test class using NonInstantiable metaclass."""

    with pytest.raises(TypeError, match="TestClass class cannot be instantiated."):
        TestClass()


class AnotherTestClass:
    """Another test class not using NonInstantiable metaclass."""


def test_regular_class_allows_instantiation():
    """Test that a regular class without NonInstantiable metaclass can be instantiated."""
    instance = AnotherTestClass()
    assert isinstance(instance, AnotherTestClass), "Regular class should be instantiable."


class StaticMethodClass(metaclass=NonInstantiable):
    """A test class with static methods using NonInstantiable metaclass."""

    @staticmethod
    def static_method():
        return "Static method called"


def test_static_method_accessible():
    """Test that static methods are accessible in a class with NonInstantiable metaclass."""
    assert StaticMethodClass.static_method() == "Static method called", "Static method should be accessible."


class ClassMethodClass(metaclass=NonInstantiable):
    """A test class with class methods using NonInstantiable metaclass."""

    @classmethod
    def class_method(cls):
        return f"Class method called on {cls.__name__}"


def test_class_method_accessible():
    """Test that class methods are accessible in a class with NonInstantiable metaclass."""
    assert (
        ClassMethodClass.class_method() == "Class method called on ClassMethodClass"
    ), "Class method should be accessible."


def test_inherited_noninstantiable_prevents_instantiation():
    """Test that a subclass of a NonInstantiable class also cannot be instantiated."""

    class BaseClass(metaclass=NonInstantiable):
        """Base class using NonInstantiable metaclass."""

    class SubClass(BaseClass):
        """Subclass inheriting from a NonInstantiable base class."""

    with pytest.raises(TypeError, match="SubClass class cannot be instantiated."):
        SubClass()
