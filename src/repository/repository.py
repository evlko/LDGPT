import json
import random

from src.dataclass.cell import Cell
from src.dataclass.mask import Mask


class Repository:
    def __init__(self) -> None:
        self.cells: list[Cell] = []

    def register_patterns(self, path: str):
        with open(path, "r") as file:
            data = json.load(file)

        aseets_path = data["assets"]
        cells = data["cells"]

        self.cells = [
            Cell(
                uid=cell["uid"],
                asset=f"{aseets_path}{cell['asset']}",
                mask=Mask(pattern=cell["mask"]),
            )
            for cell in cells
        ]

    def get_cell_by_mask(
        self,
        mask: Mask
    ) -> Cell | None:
        acceptable = []
        for cell in self.cells:
            if cell.mask == mask:
                acceptable.append(cell)
        return random.choice(acceptable)


repository = Repository()
