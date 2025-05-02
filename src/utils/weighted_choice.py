import numpy as np

from src.dataclass.w_obj import WeightedObject


def weighted_choice(objects: list[WeightedObject], seed: int = None) -> WeightedObject:
    random_gen = np.random.RandomState(seed)

    weights = np.array([obj.weight for obj in objects])
    probabilities = weights / np.sum(weights)

    return random_gen.choice(objects, p=probabilities)
