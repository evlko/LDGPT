from dataclasses import dataclass

from src.enum.cell import CellType

IGNORE_SYMBOLS = {CellType.SELF, CellType.ANY, None}


@dataclass
class Mask:
    pattern: list[list[str]]

    def __eq__(self, other: "Mask") -> bool:
        if not isinstance(other, Mask):
            return False

        if len(self.pattern) != len(other.pattern):
            return False

        for row1, row2 in zip(self.pattern, other.pattern):
            if len(row1) != len(row2):
                return False

            for cell1, cell2 in zip(row1, row2):
                if cell1 in IGNORE_SYMBOLS or cell2 in IGNORE_SYMBOLS:
                    continue

                if cell1 != cell2:
                    return False

        return True
