from dataclasses import dataclass
from typing import Optional

from map import Position, Action


@dataclass
class Node:
    state: Position
    parent: Optional['Node']
    action: Optional[Action]
    cost: int

    def __hash__(self):
        return hash(self.state)

