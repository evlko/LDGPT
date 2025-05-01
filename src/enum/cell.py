from enum import Enum


class CellType(str, Enum):
    GROUND = "O"
    WALL = "X"
