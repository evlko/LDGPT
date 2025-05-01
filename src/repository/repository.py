import json

from src.dataclass.pattern import Pattern


class Repository:
    def __init__(self) -> None:
        self.patterns: list[Pattern] = []

    def register_patterns(self, path: str):
        with open(path, "r") as file:
            data = json.load(file)

        aseets_path = data["assets"]
        patterns = data["patterns"]

        self.patterns = [
            Pattern(
                uid=pattern["uid"],
                asset=f"{aseets_path}{pattern['asset']}",
                is_left_ground=pattern["is_left_ground"],
                is_right_ground=pattern["is_right_ground"],
                is_up_ground=pattern["is_up_ground"],
                is_down_ground=pattern["is_down_ground"],
            )
            for pattern in patterns
        ]

    def get_pattern_by_neighbours(
        self,
        is_left_ground: bool,
        is_right_ground: bool,
        is_up_ground: bool,
        is_down_ground: bool,
    ) -> Pattern | None:
        for pattern in self.patterns:
            if (
                pattern.is_left_ground == is_left_ground
                and pattern.is_right_ground == is_right_ground
                and pattern.is_up_ground == is_up_ground
                and pattern.is_down_ground == is_down_ground
            ):
                return pattern
        return None


repository = Repository()
