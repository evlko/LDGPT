from dataclasses import dataclass

from src.dataclass.mask import Mask


@dataclass
class Cell:
    uid: int
    asset: str
    mask: Mask
