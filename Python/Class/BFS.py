from collections import deque

# 广度优先搜索函数
def bfs(graph, start, goal):
    visited = set()
    queue = deque([(start, [])])
    while queue:
        node, path = queue.popleft()
        if node not in visited:
            visited.add(node)
            print(node)
            if node == goal:
                return path + [node]
            for neighbor in graph[node]:
                queue.append((neighbor, path + [node]))
    return None

# 定义图结构
graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': ['F'],
    'F': []
}

start_node = 'A'
goal_node = 'F'
path = bfs(graph, start_node, goal_node)
if path:
    print(f"从 {start_node} 到 {goal_node} 找到路径（广度优先搜索）：{path}")
else:
    print(f"从 {start_node} 到 {goal_node} 未找到路径（广度优先搜索）")