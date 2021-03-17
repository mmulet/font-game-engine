from typing import Any


class NodeItem:
    def __init__(self, node: str) -> None:
        ...


class NodeCategory:
    def __init__(self, label: str,
                 label_again: str,
                 items: "list[NodeItem]") -> None:
        ...


def register_node_categories(
    id: str, categories: "list[Any]") -> None: ...


def unregister_node_categories(
    id: str) -> None: ...
