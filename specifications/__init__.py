from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, Iterable, TypeVar

T = TypeVar("T")

__all__ = (
    "Specification",
    "And",
    "AndSpecification",
    "Or",
    "OrSpecification",
    "Invert",
    "InvertSpecification",
)


class Specification(ABC, Generic[T]):

    @abstractmethod
    def is_specified_by(self, candidate: T) -> bool:
        pass

    def and_(self, another: Specification[T]) -> Specification[T]:
        return self & another

    def and_not(self, another: Specification[T]) -> Specification[T]:
        return self & ~another

    def or_(self, another: Specification[T]) -> Specification[T]:
        return self | another

    def invert(self) -> Specification[T]:
        return ~self

    def select_specified(self, candidates: Iterable[T]) -> Iterable[T]:
        return filter(self.is_specified_by, candidates)

    def __and__(self, other: Specification[T]) -> Specification[T]:
        return And(self, other)

    def __or__(self, other: Specification[T]) -> Specification[T]:
        return Or(self, other)

    def __invert__(self) -> Specification[T]:
        return Invert(self)


class And(Specification[T]):
    __slots__ = (
        "_specifications",
    )

    def __init__(self, *specifications: Specification[T]) -> None:
        assert len(specifications) > 0, "No specifications were provided"

        self._specifications = specifications

    def is_specified_by(self, candidate: T) -> bool:
        for specification in self._specifications:
            if not specification.is_specified_by(candidate):
                return False
        return True


AndSpecification = And


class Or(Specification[T]):
    __slots__ = (
        "_specifications",
    )

    def __init__(self, *specifications: Specification[T]) -> None:
        assert len(specifications) > 0, "No specifications were provided"

        self._specifications = specifications

    def is_specified_by(self, candidate: T) -> bool:
        for specification in self._specifications:
            if specification.is_specified_by(candidate):
                return True
        return False


OrSpecification = Or


class Invert(Specification[T]):
    __slots__ = (
        "_specification",
    )

    def __init__(self, specification: Specification[T]) -> None:
        self._specification = specification

    def is_specified_by(self, candidate: T) -> bool:
        return not self._specification.is_specified_by(candidate)


InvertSpecification = Invert
