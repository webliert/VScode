import heapq

# 定义带有权重的图结构（这里为了示例简单，手动指定权重，实际可根据数据来源确定权重）
graph_with_costs = {
    'A': {'B': 2, 'C': 3},
    'B': {'D': 4, 'E': 5},
    'C': {'F': 6},
    'D': {},
    'E': {'F': 1},
    'F': {}
}

# 一致代价搜索函数
def ucs(graph, start, goal):
    visited = set()
    priority_queue = [(0, start, [])]
    while priority_queue:
        cost, node, path = heapq.heappop(priority_queue)
        if node not in visited:
            visited.add(node)
            print(node)
            if node == goal:
                return path + [node]
            for neighbor, neighbor_cost in graph[node].items():
                if neighbor not in visited:
                    heapq.heappush(priority_queue, (cost + neighbor_cost, neighbor, path + [node]))
    return None

start_node = 'A'
goal_node = 'F'
path = ucs(graph_with_costs, start_node, goal_node)
if path:
    print(f"从 {start_node} 到 {goal_node} 找到路径（一致代价搜索）：{path}")
else:
    print(f"从 {start_node} 到 {goal_node} 未找到路径（一致代价搜索）")