import math
from dataclasses import dataclass

import numpy as np

from src.dataclasses.point import Point
from src.dataclasses.rect import Rect


@dataclass
class Grid:
    grid: list[list[str]]

    @property
    def width(self) -> int:
        return len(self.grid[0]) if self.grid else 0

    @property
    def height(self) -> int:
        return len(self.grid)

    @classmethod
    def from_height_map(cls, hmap: str) -> "Grid":
        grid = []
        with open(hmap, "r") as f:
            for line in f:
                row = [
                    "X" if value == "0" else "O" for value in line.strip().split(",")
                ]
                grid.append(row)
        return cls(grid=grid)
    
    @classmethod
    def from_str(cls, s: str) -> "Grid":
        L = len(s)
        for i in range(int(math.isqrt(L)), 0, -1):
            if L % i == 0:
                rows = i
                cols = L // i
                break
        grid = []
        for i in range(rows):
            row = list(s[i*cols:(i+1)*cols])
            grid.append(row)
        return cls(grid=grid)
    
    def add_ground_border(self):
        width = self.width
        self.grid = [["O"] + row + ["O"] for row in self.grid]
        new_row = ["O"] * (width + 2)
        self.grid.insert(0, new_row)
        self.grid.append(new_row.copy())

    def cells(self):
        for x in range(self.height):
            for y in range(self.width):
                yield x, y

    def get_cells_around_point(
        self, p: Point, view: Rect = Rect(width=3, height=3), is_extended: bool = True
    ) -> list[list[str | None]]:
        cx, cy = view.center

        if is_extended:
            proxy_grid = np.full(
                (self.height + 2 * cy, self.width + 2 * cx),
                None,
                dtype=object,
            )
            proxy_grid[
                cy : cy + self.height,
                cx : cx + self.width,
            ] = self.grid
            x_max, y_max = p.x + view.height, p.y + view.width
            return proxy_grid[p.x : x_max, p.y : y_max]

        x_min, x_max = max(0, p.x - cy), min(self.height, p.x + cy + 1)
        y_min, y_max = max(0, p.y - cx), min(self.width, p.y + cx + 1)
        return self.grid[y_min:y_max, x_min:x_max]
