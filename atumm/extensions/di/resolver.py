from typing import Type, TypeVar

T = TypeVar('T')


class DependencyResolver:
    """
    This is used to override the default Depends, as an injector instance will be 
    injected at runtime as a source for dependency resolution
    or Any Resolver that has Resolver.get(dependencyClass)
    """
    _resolver = None

    @classmethod
    def set_resolver(cls, resolver):
        cls._resolver = resolver

    @classmethod
    def get(cls, dependency: Type[T]) -> T:
        if cls._resolver:
            return cls._resolver.get(dependency)
        raise Exception("Dependency resolver not set")


def LocalDepends(dependency: Type[T]) -> T:
    return DependencyResolver.get(dependency)
