from dataclasses import dataclass


@dataclass
class Pattern:
    uid: int
    asset: str
    is_left_ground: bool
    is_right_ground: bool
    is_up_ground: bool
    is_down_ground: bool
