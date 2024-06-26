import heapq

class Agent(object):
    def SearchSolution(self, state):
        return []

class AgentSnake_AStar(Agent):    
    def SearchSolution(self, state):
        FoodX = state.FoodPosition.X
        FoodY = state.FoodPosition.Y

        HeadX = state.snake.HeadPosition.X
        HeadY = state.snake.HeadPosition.Y
        goal=(0,0)
        goal = (FoodX, FoodY)
        start_node=(0,0)
        start_node = (HeadX, HeadY)
        path=(0,0)
        path = self.astar_search(state, start_node, goal)
        plan=(0,0)
        plan = self.convert_path_to_plan(state, path, goal)
        
        return plan

    def astar_search(self, state, start, goal):
        frontier = []
        heapq.heappush(frontier, (0, start))
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0

        while frontier:
            current_cost, current_node = heapq.heappop(frontier)

            if current_node == goal:
                break

            for next_node in self.neighbors(state, current_node):
                new_cost = cost_so_far[current_node] + 1
                if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                    cost_so_far[next_node] = new_cost
                    priority = new_cost + self.heuristic(next_node, goal, state.maze)
                    heapq.heappush(frontier, (priority, next_node))
                    came_from[next_node] = current_node

        path = []
        current = goal
        while current != start:
            path.append(current)
            current = came_from[current]
        path.reverse()
        if goal not in path:
            path.append(goal)

        return path

    def heuristic(self, node, goal, maze):
        manhattan_distance = abs(node[0] - goal[0]) + abs(node[1] - goal[1])
        combined_heuristic = manhattan_distance
        return combined_heuristic

    def neighbors(self, state, node):
        x, y = node
        neighbors = []

        def is_valid_position(x, y, state):
             return 0 <= x < state.maze.WIDTH and 0 <= y < state.maze.HEIGHT and state.maze.MAP[y][x] != -1
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_x, new_y = x + dx, y + dy
            if is_valid_position(new_x, new_y, state):
                neighbors.append((new_x, new_y))
        down_x, down_y = x, y + 1
        if is_valid_position(down_x, down_y, state):
            neighbors.append((down_x, down_y))

        return neighbors

    def convert_path_to_plan(self, state, path, goal):
        plan = []
        g_x, g_y = goal
        start_x, start_y = path[0]
        head_x, head_y = state.snake.HeadPosition.X, state.snake.HeadPosition.Y
        dx = start_x - head_x
        dy = start_y - head_y
        if dx == 1:  
            plan.append(3)
        elif dx == -1:  
            plan.append(9)
        elif dy == 1:  
            plan.append(6)
        elif dy == -1:  
            plan.append(0)
        for i in range(len(path) - 1):
            curr_x, curr_y = path[i]
            next_x, next_y = path[i + 1]
            dx = next_x - curr_x
            dy = next_y - curr_y
            if dx == 1:  
                plan.append(3)
            elif dx == -1:  
                plan.append(9)
            elif dy == 1:  
                plan.append(6)
            elif dy == -1:  
                plan.append(0)
        return plan

