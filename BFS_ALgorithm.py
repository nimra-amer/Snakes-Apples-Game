class Agent(object):
    def SearchSolution(self, state):
        return []

class BFS_ALgorithm(Agent):    
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
        path = self.bfs_search(state, start_node, goal)
        plan=(0,0)
        plan = self.convert_path_to_plan(state, path, goal)
        
        return plan

    def bfs_search(self, state, start, goal):
        queue = []
        queue.append(start)
        came_from = {}
        came_from[start] = None

        while queue:
            current_node = queue.pop(0)

            if current_node == goal:
                break

            for next_node in self.neighbors(state, current_node):
                if next_node not in came_from:
                    queue.append(next_node)
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

    def neighbors(self, state, node):
        x, y = node
        neighbors = []

        def is_valid_position(x, y, state):
            if 0 <= x < state.maze.WIDTH and 0 <= y < state.maze.HEIGHT:
                if 0 <= y < len(state.maze.MAP) and 0 <= x < len(state.maze.MAP[y]):
                    return state.maze.MAP[y][x] != -1
            return False
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

