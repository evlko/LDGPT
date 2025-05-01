from dataclasses import dataclass


@dataclass
class Grid:
    grid: list[list[str]]

    @property
    def width(self) -> int:
        return len(self.grid[0]) if self.grid else 0

    @property
    def height(self) -> int:
        return len(self.grid)

    def cells(self):
        for x in range(self.height):
            for y in range(self.width):
                yield x, y
