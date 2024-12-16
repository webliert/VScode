# 定义图结构（这里使用邻接表表示，实际应用中可根据数据来源构建图）
graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': ['F'],
    'F': []
}

# 深度优先搜索函数
def dfs(graph, start, goal, visited=None):
    if visited is None:
        visited = set()
    visited.add(start)
    print(start)
    if start == goal:
        return True
    for neighbor in graph[start]:
        if neighbor not in visited:
            if dfs(graph, neighbor, goal, visited):
                return True
    return False

# 执行深度优先搜索
start_node = 'A'
goal_node = 'F'
found = dfs(graph, start_node, goal_node)
if found:
    print(f"从 {start_node} 到 {goal_node} 找到路径（深度优先搜索）")
else:
    print(f"从 {start_node} 到 {goal_node} 未找到路径（深度优先搜索）")