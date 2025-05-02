import json
from collections import defaultdict

from src.dataclasses.cell import Asset, Cell
from src.dataclasses.mask import Mask
from src.utils.weighted_choice import weighted_choice


class CellsRepository:
    def __init__(self) -> None:
        self.cells: list[Cell] = []

    def register_cells(self, path: str):
        with open(path, "r") as file:
            data = json.load(file)

        aseets_path = data["assets"]
        cells = data["cells"]

        self.cells = [
            Cell(
                uid=cell["uid"],
                mask=Mask(pattern=cell["mask"]),
                assets=[
                    Asset(
                        sprite=f"{aseets_path}{asset["sprite"]}",
                        weight=asset["weight"],
                    )
                    for asset in cell["assets"]
                ],
            )
            for cell in cells
        ]

    def get_asset_by_mask(self, mask: Mask) -> Cell | None:
        assets = defaultdict(list)
        for cell in self.cells:
            lookup_mask = mask
            if len(cell) < len(mask):
                lookup_mask = mask.cut_to_other(other=cell.mask)
            if cell.mask == lookup_mask:
                assets[len(cell)].extend(cell.assets)
        assets = assets[max(assets.keys())]
        return weighted_choice(objects=assets)


cells_repository = CellsRepository()
