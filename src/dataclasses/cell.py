from dataclasses import dataclass, field

from src.dataclasses.mask import Mask
from src.dataclasses.w_obj import WeightedObject


@dataclass(unsafe_hash=True)
class Asset(WeightedObject):
    sprite: str


@dataclass
class Cell:
    uid: int
    mask: Mask
    assets: list[Asset] = field(default_factory=list, repr=False)
