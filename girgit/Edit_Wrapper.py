from dataclasses import dataclass
from typing import Optional


@dataclass
class Line :
    number : int
    text : str

@dataclass
class Edit:
    type : str
    old_line: Optional[Line] = None
    new_line: Optional[Line] = None

    @property # like this we don't need to write .func() we ca use it directly like attribute .func
    def old_number(self) -> str:
        return str(self.old_line.number) if self.old_line else ""

    @property
    def new_number(self) -> str:
        return str(self.new_line.number) if self.new_line else ""

    @property
    def text(self):
        return (self.old_line or self.new_line).text




