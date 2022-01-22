from dataclasses import dataclass, field

@dataclass
class Function:
    name: str = "fn"
    input_types:  list[str] = field(default_factory=lambda: ["int"])
    output_types: list[str] = field(default_factory=lambda: ["int"])
        
    def __str__(self) -> str:
        return self.name