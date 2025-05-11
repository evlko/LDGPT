import json
import random
import re
from abc import ABC, abstractmethod
from collections import defaultdict, deque

import numpy as np
from deep_translator import GoogleTranslator

from config import SYNONYMS
from src.dataclasses.datapoint import DataPoint


class Augmentation(ABC):
    @staticmethod
    @abstractmethod
    def augment(datap: DataPoint, param: int | None) -> np.ndarray:
        pass


class VerticalFlipAugmentation(Augmentation):
    @staticmethod
    def augment(datap: DataPoint, param: int) -> DataPoint:
        datap.level = np.flipud(datap.level)
        return datap


class HorizontalFlipAugmentation(Augmentation):
    @staticmethod
    def augment(datap: DataPoint, param: int = None) -> DataPoint:
        datap.level = np.fliplr(datap.level)
        return datap


class HorizontalShiftAugmentation(Augmentation):
    @staticmethod
    def augment(datap: DataPoint, param: int) -> DataPoint:
        datap.level = np.roll(datap.level, shift=param, axis=1)
        return datap


class ReverseHorizontalShiftAugmentation(HorizontalShiftAugmentation):
    @staticmethod
    def augment(datap: DataPoint, param: int) -> DataPoint:
        return HorizontalShiftAugmentation.augment(datap=datap, param=-param)


class VerticalShiftAugmentation(Augmentation):
    @staticmethod
    def augment(datap: DataPoint, param: int) -> DataPoint:
        datap.level = np.roll(datap.level, shift=param, axis=0)
        return datap


class ReverseVerticalShiftAugmentation(VerticalShiftAugmentation):
    @staticmethod
    def augment(datap: DataPoint, param: int) -> DataPoint:
        return VerticalShiftAugmentation.augment(datap=datap, param=-param)


class DiagonalShiftAugmentation(Augmentation):
    @staticmethod
    def augment(datap: DataPoint, param: int) -> DataPoint:
        intermediate = VerticalShiftAugmentation.augment(datap=datap, param=param)
        return HorizontalShiftAugmentation.augment(datap=intermediate, param=param)


class ReverseDiagonalShiftAugmentation(DiagonalShiftAugmentation):
    @staticmethod
    def augment(datap: DataPoint, param: int) -> DataPoint:
        return DiagonalShiftAugmentation.augment(datap=datap, param=-param)


class DualFlipAugmentation(Augmentation):
    @staticmethod
    def augment(datap: DataPoint, param: int | None = None) -> DataPoint:
        datap.level = np.flipud(np.fliplr(datap.level))
        return datap


class ClipAugmentation(Augmentation):
    @staticmethod
    def augment(datap: DataPoint, param: int) -> np.ndarray:
        """Remove c rows/columns from each border"""
        if datap.level.shape[0] <= 2 * param or datap.level.shape[1] <= 2 * param:
            return np.array([[]])
        datap.level = datap.level[param:-param, param:-param]
        return datap


class FillAugmentation(Augmentation):
    @staticmethod
    def augment(datap: DataPoint, param: int) -> np.ndarray:
        """Add c rows/columns of 'O' padding to each border"""
        level = datap.level
        for _ in range(param):
            level = np.vstack([level, np.full((1, level.shape[1]), "O", dtype=str)])
            level = np.hstack([level, np.full((level.shape[0], 1), "O", dtype=str)])
        datap.level = level
        return datap


class RotateAugmentation(Augmentation):
    @staticmethod
    def augment(datap: DataPoint, param: int) -> DataPoint:
        """
        Rotate the level clockwise by `param` * 90 degrees.
        Valid values for param: 1 (90°), 2 (180°), 3 (270°), 4 (360° ≡ 0°)
        """
        if param not in {1, 2, 3, 4}:
            raise ValueError("RotateAugmentation only supports param in {1, 2, 3, 4}")

        rotated = np.rot90(datap.level, k=-param)
        datap.level = rotated
        return datap


class ShuffleLabelAugmentation(Augmentation):
    @staticmethod
    def augment(datap: DataPoint, param: int | None = None) -> DataPoint:
        """Shuffle the words in the label"""
        words = datap.label.split()
        random.shuffle(words)
        datap.label = " ".join(words)
        return datap


class TranslationAugmentation(Augmentation):
    @staticmethod
    def augment(datap: DataPoint, param: None = None) -> DataPoint:
        """Translate label to another language and back to English to augment it."""
        lang = "ru"

        try:
            translated = GoogleTranslator(source="en", target=lang).translate(
                datap.label
            )
            roundtrip = GoogleTranslator(source=lang, target="en").translate(translated)
            datap.label = roundtrip
        except Exception as e:
            print(f"[TranslationAugmentation] Failed: {e}")
        return datap


class DensityInjectionAugmentation(Augmentation):
    @staticmethod
    def augment(datap: DataPoint, param: None = None) -> DataPoint:
        num_walls = np.sum(datap.level == "X")
        total = datap.level.size
        density = num_walls / total
        if density > 0.5:
            datap.label = "dense " + datap.label
        elif density < 0.2:
            datap.label = "sparse " + datap.label
        return datap


class SynonymAugmentation(Augmentation):
    _graph = None
    _equivalence = None

    @classmethod
    def load_config(cls) -> dict:
        with open(SYNONYMS) as f:
            return json.load(f)

    @classmethod
    def _build_graph(cls, config: dict):
        graph = defaultdict(set)
        for word, synonyms in config.items():
            for syn in synonyms:
                graph[word].add(syn)
                graph[syn].add(word)
        return graph

    @classmethod
    def _build_equivalence(cls, graph: dict):
        visited = set()
        equivalent = {}
        for word in graph:
            if word in visited:
                continue
            group = set()
            queue = deque([word])
            while queue:
                node = queue.popleft()
                if node not in visited:
                    visited.add(node)
                    group.add(node)
                    queue.extend(graph[node])
            for w in group:
                equivalent[w] = group - {w}
        return equivalent

    @classmethod
    def get_equivalence(cls):
        if cls._equivalence is None:
            config = cls.load_config()
            cls._graph = cls._build_graph(config)
            cls._equivalence = cls._build_equivalence(cls._graph)
        return cls._equivalence

    @staticmethod
    def augment(datap: DataPoint, param: int | None = None) -> DataPoint:
        equivalence = SynonymAugmentation.get_equivalence()

        words = datap.label.split()
        new_words = []

        for word in words:
            stripped = re.sub(r"\W", "", word.lower())
            if stripped in equivalence:
                candidates = list(equivalence[stripped])
                replacement = random.choice(candidates)
                new_word = re.sub(stripped, replacement, word, flags=re.IGNORECASE)
                new_words.append(new_word)
            else:
                new_words.append(word)

        datap.label = " ".join(new_words)
        return datap
