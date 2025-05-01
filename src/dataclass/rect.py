from dataclasses import dataclass


@dataclass
class Rect:
    width: int
    height: int

    @property
    def area(self) -> int:
        return self.width * self.height

    @property
    def indices(self) -> list[tuple[int, int]]:
        return [(i, j) for i in range(self.height) for j in range(self.width)]

    @property
    def center(self) -> tuple[int, int]:
        return self.width // 2, self.height // 2
