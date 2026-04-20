import heapq
import math

def distance(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

def astar(graph, start, end, store):
    open_set = []
    heapq.heappush(open_set, (0, start))

    came_from = {}
    g_score = {node: float("inf") for node in store}
    g_score[start] = 0

    f_score = {node: float("inf") for node in store}
    f_score[start] = distance(store[start], store[end])

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]

        for neighbor in graph.get(current, []):
            tentative_g = g_score[current] + distance(store[current], store[neighbor])

            if tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + distance(store[neighbor], store[end])
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return []

def nearest_node(point, store):
    return min([n for n in store if n.startswith("P")],
               key=lambda n: distance(store[n], point))
