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