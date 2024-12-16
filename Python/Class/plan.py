import heapq

# 定义节点类
class Node:
    def __init__(self, x, y, cost=0, parent=None):
        self.x = x
        self.y = y
        self.cost = cost
        self.parent = parent

    def __lt__(self, other):
        return self.cost < other.cost

# 规划型智能体类
class PlanningAgent:
    def __init__(self, start, goal, world):
        self.start = start
        self.goal = goal
        self.world = world

    def heuristic(self, node):
        # 这里使用曼哈顿距离作为启发式函数（简单估计到目标的距离）
        return abs(node.x - self.goal[0]) + abs(node.y - self.goal[1])

    def plan(self):
        open_list = []
        closed_list = set()
        start_node = Node(self.start[0], self.start[1])
        heapq.heappush(open_list, (0, start_node))
        while open_list:
            _, current_node = heapq.heappop(open_list)
            if (current_node.x, current_node.y) == self.goal:
                path = []
                while current_node:
                    path.append((current_node.x, current_node.y))
                    current_node = current_node.parent
                return path[::-1]
            closed_list.add((current_node.x, current_node.y))
            for neighbor in self.get_neighbors(current_node):
                if (neighbor.x, neighbor.y) in closed_list:
                    continue
                new_cost = current_node.cost + self.world[neighbor.x][neighbor.y]
                if not any(neighbor.x == node.x and neighbor.y == node.y and new_cost >= node.cost for _, node in open_list):
                    heapq.heappush(open_list, (new_cost + self.heuristic(neighbor), neighbor))
        return None

    def get_neighbors(self, node):
        neighbors = []
        # 上下左右四个方向的移动（假设在二维网格中，可根据实际情况修改）
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            x = node.x + dx
            y = node.y + dy
            if 0 <= x < len(self.world) and 0 <= y < len(self.world[0]):
                # 创建Node对象时使用关键字参数
                neighbors.append(Node(x=x, y=y, cost=node.cost + self.world[x][y], parent=node))
        return neighbors

# 定义一个简单的二维网格世界，0表示可通行，1表示障碍物（这里只是示例，可根据实际情况构建更复杂的世界）
world = [[0, 0, 0, 0, 0],
         [0, 1, 1, 0, 0],
         [0, 0, 0, 1, 0],
         [0, 1, 0, 0, 0],
         [0, 0, 0, 0, 0]]
start = (0, 0)
goal = (4, 4)
agent = PlanningAgent(start, goal, world)
path = agent.plan()
if path:
    print("找到路径：", path)
else:
    print("未找到路径")