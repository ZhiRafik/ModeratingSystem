from dataclasses import dataclass


@dataclass(frozen=True)
class TextToModerate:
    value: str

    def __post_init__(self):
        if not isinstance(self.value, str):
            raise TypeError("Text must be string")

    def is_empty(self) -> bool:
        return not self.value or not self.value.strip()

    def get_length(self) -> int:
        return len(self.value)