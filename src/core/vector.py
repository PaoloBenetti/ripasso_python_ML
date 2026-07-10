from dataclasses import dataclass


@dataclass(frozen=True)
class Vector2D:
    x: float
    y: float

    def __eq__(self, other):
        if not isinstance(other, Vector2D):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f'Vector2D({self.x!r},{self.y!r})'

    def __str__(self):
        return f'Vettore di coordinate ( {self.x}, {self.y})'

@dataclass
class Polyline:
    linea: list[Vector2D]

    def __len__(self):
        return len(self.linea)

    def __getitem__(self, item):
        if isinstance(item, slice):
            cls = type(self)
            return cls(self.linea[item])
        return self.linea[item]

    def __setitem__(self, key, value):
        if not isinstance(value, Vector2D): # in fase ottimizzazione gli assert spariscono
            raise TypeError(f"Expected Vector2D, got {type(value).__name__}")
        if isinstance(key, slice):
            cls = type(self)
            return cls(self.linea[key])
        else:
            self.linea[key] = value
