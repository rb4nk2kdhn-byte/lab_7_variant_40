from __future__ import annotations

import sys
from collections import deque


class Record:

    def __init__(self, value: int) -> None:
        self.v = value

    def score(self) -> int:
        """Повернути оцінку запису."""
        return self.v


class EnhancedRecord(Record):

    def score(self) -> int:
        return 2 * self.v


def make_record(record_type: str, value: int) -> Record: # створити запис потрібного формату з позначками n або d
    if record_type == "N":
        return Record(value)
    if record_type == "D":
        return EnhancedRecord(value)
    raise ValueError(f"Невідомий тип запису: {record_type}")


class Vertex:

    def __init__(self, vertex_id: int, record: Record) -> None:
        self.id = vertex_id
        self.record = record
        self.neighbors: list[Vertex] = []

    def add_neighbor(self, neighbor: Vertex) -> None: # додає сусіда без петель і дублікатів зберігати спадний порядок номерів
        if neighbor.id == self.id:
            return

        if all(existing.id != neighbor.id for existing in self.neighbors):
            self.neighbors.append(neighbor)
            self.neighbors.sort(key=lambda vertex: vertex.id, reverse=True)


class Graph:

    def __init__(self) -> None:
        self.vertices: dict[int, Vertex] = {}

    def add_vertex(self, vertex: Vertex) -> None:# додати вершину графа якщо її ще немає інакше помилка
        if vertex.id in self.vertices:
            raise ValueError(f"Номер вершини {vertex.id} вже існує")
        self.vertices[vertex.id] = vertex

    def add_edge(self, first_id: int, second_id: int) -> None: #додає неорієнтоване ребро зберігши посилання в обох вершинах 
        if first_id not in self.vertices or second_id not in self.vertices:
            raise KeyError("Обидва кінці ребра мають належати графу")
        if first_id == second_id:
            return

        first = self.vertices[first_id]
        second = self.vertices[second_id]
        first.add_neighbor(second)
        second.add_neighbor(first)

    def bfs(self, start_id: int) -> list[Vertex]: #повернути рядок bfs від start_id. Вершина позначається відвіданою в момент першого додавання до черги тому вона не може потрапити до черги повторно. cусіди перебираються за спаданням номерів незалежно від порядку рядків ребер у вводі
        if start_id not in self.vertices:
            return []

        start = self.vertices[start_id]
        queue: deque[Vertex] = deque([start])
        visited_ids = {start_id}
        order: list[Vertex] = []

        while queue:
            current = queue.popleft()
            order.append(current)

            for neighbor in current.neighbors:
                if neighbor.id not in visited_ids:
                    visited_ids.add(neighbor.id)
                    queue.append(neighbor)

        return order

    def unvisited_ids(self, visited_ids: set[int]) -> list[int]: #повертає номери вершин яких нема у відвіданій множині за зростанням 
        return sorted(
            vertex_id
            for vertex_id in self.vertices
            if vertex_id not in visited_ids
        )


def format_numbers(numbers: list[int]) -> str: # форматування послідовності чисел 
    return " ".join(map(str, numbers)) if numbers else "-"


def solve(input_text: str) -> list[str]: #розбирає вхід виконати завдання,вернути 5 рядків результату 
    """Розібрати вхід, виконати завдання та повернути рівно п'ять рядків результату."""
    tokens = iter(input_text.split())
    try:
        n = int(next(tokens))
    except StopIteration: # захист на випадок порожнього вводу 
        return []

    m = int(next(tokens))
    start_id = int(next(tokens))

    graph = Graph()

    for _ in range(n): #записи всіх вепршин створюються до додавання ребер 
        vertex_id = int(next(tokens))
        record_type = next(tokens)
        value = int(next(tokens))
        graph.add_vertex(Vertex(vertex_id, make_record(record_type, value)))

    edges: list[tuple[int, int]] = [] # спочатку зчитуємо ребра їній порядок у вводі не визначає порядок bfs
    for _ in range(m):
        first_id = int(next(tokens))
        second_id = int(next(tokens))
        edges.append((first_id, second_id))

    threshold = int(next(tokens))

    for first_id, second_id in edges:
        graph.add_edge(first_id, second_id)

    order = graph.bfs(start_id)
    traversal_ids = [vertex.id for vertex in order]
    visited_ids = set(traversal_ids)
    unvisited_ids = graph.unvisited_ids(visited_ids)

    scored_vertices = [
        (vertex, vertex.record.score())
        for vertex in order
    ]
    selected = [
        (vertex, score)
        for vertex, score in scored_vertices
        if score >= threshold
    ]

    selected_ids = [vertex.id for vertex, _ in selected]
    selected_count = len(selected)
    selected_sum = sum(score for _, score in selected)

    return [
        f"Обхід: {format_numbers(traversal_ids)}",
        f"Відібрано: {format_numbers(selected_ids)}",
        f"Кількість: {selected_count}",
        f"Сума: {selected_sum}",
        f"Невідвідані: {format_numbers(unvisited_ids)}",
    ]


def main() -> None:

    while True:
        first_line = sys.stdin.readline()

        if not first_line:
            return

        if first_line.strip():
            break

    first_values = first_line.split()

    if len(first_values) != 3:
        print(
            "Помилка: введи три числа в першому рядку: n m s.",
            file=sys.stderr,
        )
        return

    n, m, _ = map(int, first_values)

    input_lines = [first_line]

    for _ in range(n + m + 1):
        line = sys.stdin.readline()

        if not line:
            print(
                "Помилка: введено не всі рядки даних.",
                file=sys.stderr,
            )
            return

        input_lines.append(line)

    output_lines = solve("".join(input_lines))

    if output_lines:
        sys.stdout.write("\n".join(output_lines) + "\n")


if __name__ == "__main__":
    main()