import copy

import numpy as np

from src.augmentations.augmentation import (ClipAugmentation,
                                            DualFlipAugmentation,
                                            FillAugmentation,
                                            HorizontalFlipAugmentation,
                                            HorizontalShiftAugmentation,
                                            RotateAugmentation,
                                            ShuffleLabelAugmentation,
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
        "dual_flip": DualFlipAugmentation,
        "horizontal_shift": HorizontalShiftAugmentation,
        "vertical_shift": VerticalShiftAugmentation,
        "rotate": RotateAugmentation,
        "syn": SynonymAugmentation,
        "shuffle": ShuffleLabelAugmentation,
    }

    def handle(augmentation: str, datap: DataPoint, param: int | None = None):
        augmentator = AugmentationHandler._registry.get(augmentation)
        datap_copy = copy.copy(datap)
        if augmentator is None:
            raise ValueError(f"Unknown augmentation: {augmentation}")

        return augmentator.augment(datap=datap_copy, param=param)
