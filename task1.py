from __future__ import annotations

import sys


class Record:

    def __init__(self, value: int) -> None:
        self.v = value

    def score(self) -> int:
        """Повернути оцінку запису."""
        return self.v


class EnhancedRecord(Record):

    def score(self) -> int:
        """Перевизначена оцінка для поліморфного виклику score()."""
        return 2 * self.v


def make_record(record_type: str, value: int) -> Record:
    if record_type == "N":
        return Record(value)
    if record_type == "D":
        return EnhancedRecord(value)
    raise ValueError(f"Невідомий тип запису: {record_type}")


class TreeNode:

    def __init__(self, node_id: int, record: Record) -> None:
        self.id = node_id
        self.record = record
        self.children: list[TreeNode] = []

    def add_child(self, child: TreeNode) -> None:
        """Додати дитину, не створюючи дубліката, і впорядкувати дітей за спаданням id."""
        if child.id == self.id:
            raise ValueError("Вузол дерева не може бути власною дитиною")

        if all(existing.id != child.id for existing in self.children):
            self.children.append(child)
            self.children.sort(key=lambda node: node.id, reverse=True)


class Tree:

    def __init__(self) -> None:
        self.nodes: dict[int, TreeNode] = {}
        self.root: TreeNode | None = None

    def add_node(self, node: TreeNode) -> None: # додати вузол до дерева
        if node.id in self.nodes:
            raise ValueError(f"Номер вузла {node.id} вже існує")
        self.nodes[node.id] = node

    def set_root(self, node: TreeNode) -> None:# встановити корінб дерева
        if node.id not in self.nodes or self.nodes[node.id] is not node:
            raise ValueError("Корінь має належати цьому дереву")
        self.root = node

    def connect(self, parent_id: int, child_id: int) -> None : #з'єднує наявні вузли від батька до дитини
        if parent_id not in self.nodes or child_id not in self.nodes:
            raise KeyError("Батько та дитина мають бути додані до дерева")
        self.nodes[parent_id].add_child(self.nodes[child_id])

    def traverse_limited(self, max_depth: int) -> list[tuple[TreeNode, int]]: # повертає обхід дерева до max_depth
        if self.root is None or max_depth < 0:
            return []

        visited: list[tuple[TreeNode, int]] = []

        def visit(node: TreeNode, depth: int) -> None:
            visited.append((node, depth))
            if depth >= max_depth: # на граничній глибині не викликаємо дітей які все одно не допускаються
                return
            for child in node.children:  
                visit(child, depth + 1)

        visit(self.root, 0)
        return visited


def format_numbers(numbers: list[int]) -> str: # форматування послідовності чисел 
    return " ".join(map(str, numbers)) if numbers else "-"


def solve(input_text: str) -> list[str]: # розбирає вхід виконує завдання і виводить 5 рядків результату
    tokens = iter(input_text.split())
    try:
        n = int(next(tokens))
    except StopIteration: # захист на випадок порожнього вводу
        return []

    tree = Tree()
    parent_by_id: dict[int, int] = {}

    for _ in range(n):
        node_id = int(next(tokens))
        parent_id = int(next(tokens))
        record_type = next(tokens)
        value = int(next(tokens))

        tree.add_node(TreeNode(node_id, make_record(record_type, value)))
        parent_by_id[node_id] = parent_id

    max_depth = int(next(tokens))

    if n > 0:
        tree.set_root(tree.nodes[1])
        for node_id in range(2, n + 1):
            tree.connect(parent_by_id[node_id], node_id)

    visited = tree.traverse_limited(max_depth)
    traversal_ids = [node.id for node, _ in visited]
    deepest_level = max((depth for _, depth in visited), default=-1)

    scored_nodes = [
        (node, node.record.score())
        for node, _ in visited
    ]

    if scored_nodes:
        best_score = max(score for _, score in scored_nodes)
        selected = [
            (node, score)
            for node, score in scored_nodes
            if score == best_score
        ]
    else:
        selected = []

    selected_ids = [node.id for node, _ in selected]
    selected_count = len(selected)
    selected_sum = sum(score for _, score in selected)

    return [
        f"Обхід: {format_numbers(traversal_ids)}",
        f"Відібрано: {format_numbers(selected_ids)}",
        f"Кількість: {selected_count}",
        f"Сума: {selected_sum}",
        f"Глибина: {deepest_level}",
    ]


def main() -> None:
    first_line = sys.stdin.readline()

    if not first_line:
        return

    n = int(first_line.strip())
    input_lines = [first_line]

    for _ in range(n + 1):
        input_lines.append(sys.stdin.readline())

    output_lines = solve("".join(input_lines))

    if output_lines:
        sys.stdout.write("\n".join(output_lines) + "\n")


if __name__ == "__main__":
    main()