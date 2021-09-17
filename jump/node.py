from typing import Any, Callable, List, Optional, Tuple


class Node:
    def __init__(self, name: str):
        self.name = name

        self.outputs: Optional[Tuple[Any]] = None
        self.prevs: List[Node] = []
        self.nexts: List[Node] = []
        self.processing_time: float = 0


class NodeIO:
    def __init__(self, val: Any, returner: Node):
        self.val = val
        self.returner = returner

    def __repr__(self):
        return f"NodeIO({self.val}, type={type(self.val)})"
