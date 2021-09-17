from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Tuple

import graphviz

from .node import Node, NodeIO


class Pipeline:
    def __init__(self, name: str = ""):
        self.name = name

        self.nodes: List[Node] = []
        self.node_dict: Dict = {}

    def node(self, func: Callable):
        """This method is meant to be used as a decorator"""

        def node_func(*args, **kwargs):
            # Unpack the value from argument if it is a NodeIO instance
            new_args = []
            input_nodes = []
            new_node = Node(name=func.__name__)

            for arg in args:
                if isinstance(arg, NodeIO):
                    new_args.append(arg.val if isinstance(arg, NodeIO) else arg)
                    if not arg.returner in input_nodes:
                        input_nodes.append(arg.returner)
                        new_node.prevs.append(arg.returner)
                        arg.returner.nexts.append(new_node)

            # TODO: keep track the linking of the nodes as the result of NodeIO passing in kwargs
            new_kwargs = {
                k: kwargs[k].val if isinstance(kwargs[k]) else kwargs[k] for k in kwargs
            }

            # The actual function execution, with its processing time calculation
            then = datetime.now()
            ret = func(*new_args, **new_kwargs)
            dt = datetime.now() - then
            new_node.processing_time = dt.total_seconds()

            # Pack the function return value as a NodeIO instance
            if isinstance(ret, tuple):
                ret = tuple(NodeIO(val=val, returner=new_node) for val in ret)
            else:
                ret = NodeIO(val=ret, returner=new_node)

            self.nodes.append(new_node)
            return ret

        return node_func

    def visualize(self, show=True):
        dot = graphviz.Digraph(comment=self.name, format="png")
        dot.graph_attr["rankdir"] = "LR"

        # artificial start and end node
        common_attr = dict(
            style="filled",
            shape="doublecircle",
            fontname="Menlo",
            height="0.2",
        )
        dot.node("start", "", color="#487794", **common_attr)
        dot.node("end", "", color="#E05C5B", **common_attr)

        for node in self.nodes:
            dot.node(
                node.name,
                f"{node.name}\n{node.processing_time:.3f}s",
                shape="rect",
                fontname="Menlo",
            )
            if node.prevs:
                for prev in node.prevs:
                    dot.edge(prev.name, node.name)
            else:
                dot.edge("start", node.name, style="dashed")

            if not node.nexts:
                dot.edge(node.name, "end", style="dashed")

        dot.render(self.name, view=show)
