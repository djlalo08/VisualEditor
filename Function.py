class Function:
    def __init__(self, name="fn", input_types=["int", "int"], output_types=["int", "int"]) -> None:
        self.input_types = input_types
        self.output_types = output_types
        self.name = name
        
    def __str__(self) -> str:
        return self.name