import copy

from src.augmentations.augmentation import (ClipAugmentation,
                                            DensityInjectionAugmentation,
                                            DiagonalShiftAugmentation,
                                            DualFlipAugmentation,
                                            FillAugmentation,
                                            HorizontalFlipAugmentation,
                                            HorizontalShiftAugmentation,
                                            ReverseDiagonalShiftAugmentation,
                                            ReverseHorizontalShiftAugmentation,
                                            ReverseVerticalShiftAugmentation,
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
        "reverse_horizontal_shift": ReverseHorizontalShiftAugmentation,
        "vertical_shift": VerticalShiftAugmentation,
        "reverse_vertical_shift": ReverseVerticalShiftAugmentation,
        "diagonal_shift": DiagonalShiftAugmentation,
        "reverse_diagonal_shift": ReverseDiagonalShiftAugmentation,
        "rotate": RotateAugmentation,
        "syn": SynonymAugmentation,
        "shuffle": ShuffleLabelAugmentation,
        "density_injection": DensityInjectionAugmentation,
    }

    def handle(augmentation: str, datap: DataPoint, param: int | None = None):
        augmentator = AugmentationHandler._registry.get(augmentation)
        datap_copy = copy.copy(datap)
        if augmentator is None:
            raise ValueError(f"Unknown augmentation: {augmentation}")

        return augmentator.augment(datap=datap_copy, param=param)
