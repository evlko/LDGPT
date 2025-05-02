import json

from src.dataclasses.cell import Asset, Cell
from src.dataclasses.mask import Mask
from src.utils.weighted_choice import weighted_choice


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
        assets = []
        for cell in self.cells:
            if cell.mask == mask:
                assets.extend(cell.assets)
        return weighted_choice(objects=assets)


repository = Repository()
