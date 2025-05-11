from dataclasses import dataclass

import numpy as np


@dataclass
class DataPoint:
    label: str
    level: np.ndarray

    @property
    def text(self):
        return (
            f"<|label|> {self.label} <|level|>\n"
            + "\n".join("".join(row) for row in self.level)
            + "\n"
        )
