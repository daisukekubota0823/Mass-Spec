from abc import ABC, abstractmethod
    from typing import Callable, Generic, TypeVar, Any

    T = TypeVar("T")
    U = TypeVar("U")


    class IBrushMapper(ABC):
        @abstractmethod
        def map(self, key: Any) -> str:  # Using `str` as a placeholder for Brush
            pass


    class IBrushMapperGeneric(IBrushMapper, Generic[T]):
        @abstractmethod
        def map(self, key: T) -> str:  # Using `str` as a placeholder for Brush
            pass


    class BrushMapper(IBrushMapperGeneric[T], ABC):
        @abstractmethod
        def map(self, key: T) -> str:
            pass

        def map_object(self, key: Any) -> str:
            if isinstance(key, T):
                return self.map(key)
            raise TypeError(f"Type {type(key)} is not supported.")


    class BrushMapperExtensions:
        @staticmethod
        def contramap(mapper: IBrushMapperGeneric[T], consumer: Callable[[U], T]) -> IBrushMapperGeneric[U]:
            class ContravariantBrushMapper(IBrushMapperGeneric[U]):
                def __init__(self, mapper: IBrushMapperGeneric[T], consumer: Callable[[U], T]):
                    self._mapper = mapper
                    self._consumer = consumer

                def map(self, key: U) -> str:
                    return self._mapper.map(self._consumer(key))

                def map_object(self, key: Any) -> str:
                    return self.map(key)

            return ContravariantBrushMapper(mapper, consumer)
    