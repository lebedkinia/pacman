class Node:
    def __init__(self, position, parent=None):
        self.position = position
        self.parent = parent
        self.g = 0  # cost from start to current node
        self.h = 0  # heuristic cost to goal
        self.f = 0  # total cost

    def __eq__(self, other):
        return self.position == other.position


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])  # Manhattan distance


def a_star_search(start, goal, matrix):
    open_list = []
    closed_list = []

    start_node = Node(start)
    goal_node = Node(goal)

    open_list.append(start_node)

    while open_list:
        # Находим узел с наименьшей стоимостью f
        current_node = min(open_list, key=lambda node: node.f)
        open_list.remove(current_node)
        closed_list.append(current_node)

        # Проверка, достигли ли мы цели
        if current_node == goal_node:
            path = []
            while current_node:
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1]  # Возвращаем путь в обратном порядке

        # Получаем соседей (вверх, вниз, влево, вправо)
        neighbors = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        for new_position in neighbors:
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Проверка на выход за границы
            if (0 <= node_position[0] < len(matrix)) and (0 <= node_position[1] < len(matrix[0])):
                if matrix[node_position[0]][node_position[1]] != 0:  # 0 - проходимая клетка
                    continue

                # Создаём новый узел
                neighbor_node = Node(node_position, current_node)

                # Проверка, находится ли сосед в закрытом списке
                if neighbor_node in closed_list:
                    continue

                # Вычисляем стоимости
                neighbor_node.g = current_node.g + 1
                neighbor_node.h = heuristic(neighbor_node.position, goal_node.position)
                neighbor_node.f = neighbor_node.g + neighbor_node.h

                # Проверка, находится ли сосед в открытом списке
                if any(neighbor_node == node and neighbor_node.g >= node.g for node in open_list):
                    continue

                # Добавляем соседа в открытый список
                open_list.append(neighbor_node)

    return None  # Путь не найден


def create_path_matrix(matrix, path):
    path_matrix = [[0 for _ in range(len(matrix[0]))] for _ in range(len(matrix))]
    for position in path:
        path_matrix[position[0]][position[1]] = 2  # Отмечаем путь единицами
    return path_matrix


def main(map_data, start, end):
    matrix = map_data

    start = start  # Начальная точка
    goal = end  # Конечная точка

    path = a_star_search(start, goal, matrix)
    if path:
        path_matrix = create_path_matrix(matrix, path)
        return path_matrix
    else:
        return map_data
