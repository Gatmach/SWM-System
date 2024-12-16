
import heapq

def optimize_route(start, end, locations):
    """
    Use Dijkstra’s algorithm to find the shortest path from start to end.
    """
    # Simple graph for demonstration (you can replace this with real bin locations and distances)
    graph = {
        'A': {'B': 5, 'C': 10},
        'B': {'C': 2, 'D': 4},
        'C': {'D': 3},
        'D': {}
    }

    # Dijkstra’s algorithm to find the shortest path
    queue = [(0, start)]  # (distance, node)
    distances = {start: 0}
    previous_nodes = {start: None}
    while queue:
        current_distance, current_node = heapq.heappop(queue)

        if current_node == end:
            break

        for neighbor, weight in graph.get(current_node, {}).items():
            distance = current_distance + weight
            if neighbor not in distances or distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(queue, (distance, neighbor))

    # Reconstruct path from start to end
    path = []
    node = end
    while node:
        path.append(node)
        node = previous_nodes[node]
    path.reverse()

    return path, distances[end]
