from dataclasses import dataclass


@dataclass(frozen=True)
class Vector2D:
    x: float
    y: float

    def __eq__(self, other):
        if not isinstance(other, Vector2D):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __add__(self, other): #versione semplice
        if not isinstance(other, Vector2D):
            return NotImplemented
        return Vector2D(self.x + other.x, self.y + other.y)

    '''
    def __add__(self, other): versione n dim
        try:
            pairs = itertools.zip_longest(self, other, fillvalue=0.0)
            return Vector2D(a+b for a,b in pairs)
        except TypeError:
            return NotImplemented
    '''

    def __radd__(self, other):
        # compatibilita per versione built-in sum
        if other == 0:
            return self
        return self + other

    def __mul__(self, other):
        if not isinstance(other, (float, int)):
            return NotImplemented
        return Vector2D(self.x * other, self.y * other)

    def __rmul__(self, other):
        return self * other

    def __neg__(self):
        return Vector2D(- self.x, -self.y)

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
