import copy

import numpy as np

from src.augmentations.augmentation import (ClipAugmentation, FillAugmentation,
                                            HorizontalFlipAugmentation,
                                            HorizontalShiftAugmentation,
                                            RotateAugmentation,
                                            SynonymAugmentation,
                                            TranslationAugmentation,
                                            VerticalFlipAugmentation,
                                            VerticalShiftAugmentation)
from src.dataclasses.datapoint import DataPoint


class AugmentationHandler:
    _registry = {
        "clip": ClipAugmentation,
        "fill": FillAugmentation,
        "translation": TranslationAugmentation,
        "vertical_flip": VerticalFlipAugmentation,
        "horizontal_flip": HorizontalFlipAugmentation,
        "horizontal_shift": HorizontalShiftAugmentation,
        "vertical_shift": VerticalShiftAugmentation,
        "rotate": RotateAugmentation,
        "syn": SynonymAugmentation,
    }

    def handle(augmentation: str, datap: DataPoint, param: int | None = None):
        augmentator = AugmentationHandler._registry.get(augmentation)
        datap_copy = copy.copy(datap)
        if augmentator is None:
            raise ValueError(f"Unknown augmentation: {augmentation}")

        return augmentator.augment(datap=datap_copy, param=param)
