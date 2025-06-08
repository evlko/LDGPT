from dataclasses import dataclass

import numpy as np

SYSTEM_PROMT = "where X is a wall and O is a free space"


@dataclass
class DataPoint:
    label: str
    level: np.ndarray

    @property
    def text(self):
        return (
            f"<|label|> {self.label.lower()}, {SYSTEM_PROMT} <|level|>\n"
            + "\n".join("".join(row) for row in self.level)
            + "<|endoftext|>"
            + "\n"
        )
