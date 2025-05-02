from dataclasses import dataclass

from src.enums.cell import CellType

IGNORE_SYMBOLS = {CellType.SELF, CellType.ANY, None}


@dataclass
class Mask:
    pattern: list[list[str]]

    def cut_to_other(self, other: "Mask") -> "Mask":
        original_height = len(self.pattern)
        original_width = len(self.pattern[0]) if original_height > 0 else 0
        cell_height = len(other.pattern)
        cell_width = len(other.pattern[0]) if cell_height > 0 else 0

        if cell_height < original_height or cell_width < original_width:
            top_cut = (original_height - cell_height) // 2
            bottom_cut = original_height - top_cut - cell_height
            left_cut = (original_width - cell_width) // 2
            right_cut = original_width - left_cut - cell_width

            trimmed_mask = Mask(
                pattern=[
                    row[left_cut : original_width - right_cut]
                    for row in self.pattern[top_cut : original_height - bottom_cut]
                ]
            )
            return trimmed_mask

        return self

    def __len__(self) -> int:
        return len(self.pattern)

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
