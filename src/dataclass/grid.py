from dataclasses import dataclass

import numpy as np

from src.dataclass.point import Point
from src.dataclass.rect import Rect


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
